"""Interactive context debugger REPL.

Type user messages one at a time. Each line runs one agent turn against an
accumulating conversation history with a shared ContextManager, so compression
triggers naturally as the history grows. After every turn a debug panel shows
how the context was built and compressed.

Run from this directory (sdk/ctx_debugger); ../../ is the nexent repo root:
    ../../backend/.venv/bin/python interactive.py

Slash commands:
    /help              list commands
    /context [N]       context the main LLM received last turn (post-compression)
    /history           raw accumulated session ledger (pre-compression)
    /summary           current compression summary (full text)
    /compress          last turn's compression LLM input prompt + output summary
    /tokens            per-turn token timeline
    /stats             session-wide compression stats (LLM compression call count)
    /trace [N]         raw trace events from the last N turns (default 1)
    /step N            dump every event of agent step N in the last turn
    /config            show ContextManagerConfig
    /reset [threshold] clear history + compression state (optional new threshold)
    /quit  /q          exit
"""

import asyncio
import contextlib
import io
import json
import os
import sys
from collections import Counter

try:
    import readline
except ImportError:
    readline = None

HERE = os.path.dirname(os.path.abspath(__file__))
SDK_DIR = os.path.dirname(HERE)
BENCHMARK_DIR = os.path.join(SDK_DIR, "benchmark")
for _p in (SDK_DIR, BENCHMARK_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from agent_runner import build_agent_run_info, run_agent_with_tracking

_OUT = sys.stdout

from nexent.core.agents.agent_context import ContextManager, ContextManagerConfig
from nexent.core.agents.agent_model import AgentHistory
from nexent.core.utils.token_estimation import estimate_tokens_text

from ctx_debugger import ContextDebugger, attach_debugger

TRACE_PATH = os.environ.get("NEXENT_CONTEXT_DEBUG", "/tmp/nexent_ctx_interactive.jsonl")
HISTORY_FILE = os.path.expanduser("~/.nexent_ctx_debugger_history")
_PROMPT = "\n\001\033[1;36m\002you>\001\033[0m\002 "
console = Console(file=_OUT)


def _sum(events, key):
    return sum((e["data"].get(key) or 0) for e in events)


def _strip_surrogates(s):
    if not isinstance(s, str):
        return s
    return s.encode("utf-8", errors="ignore").decode("utf-8")


def _clean_input(raw):
    cleaned = _strip_surrogates(raw)
    if cleaned != raw:
        console.print(
            "[yellow]\u00b7[/] [dim]removed invalid characters from your input "
            "(terminal line-editing artifact — retype if it looks wrong)[/]"
        )
    return cleaned


def _init_history():
    if readline is None:
        return
    try:
        readline.read_history_file(HISTORY_FILE)
    except (FileNotFoundError, OSError):
        pass
    readline.set_history_length(2000)


def _save_history():
    if readline is None:
        return
    try:
        readline.write_history_file(HISTORY_FILE)
    except OSError:
        pass


class Session:
    def __init__(self, token_threshold=3000, keep_recent_pairs=1,
                 keep_recent_steps=4, max_steps=5):
        self.max_steps = max_steps
        self.cm_config = ContextManagerConfig(
            enabled=True,
            token_threshold=token_threshold,
            keep_recent_pairs=keep_recent_pairs,
            keep_recent_steps=keep_recent_steps,
        )
        self.history = []
        self.turn = 0
        self.turn_tokens = []
        self.last_turn_events = []
        self._last_seq = 0

        self.shared_cm = ContextManager(config=self.cm_config, max_steps=max_steps)
        self.debugger = ContextDebugger(
            trace_path=TRACE_PATH, capture_full_messages=True)

        attach_debugger(self.shared_cm, existing=self.debugger, layers={"compression"})
        self._install_agent_patch()

    def _install_agent_patch(self):
        from nexent.core.agents.core_agent import CoreAgent

        dbg = self.debugger
        if getattr(CoreAgent, "_ctxdbg_orig_init", None) is None:
            CoreAgent._ctxdbg_orig_init = CoreAgent.__init__

        orig_init = CoreAgent._ctxdbg_orig_init

        def patched_init(agent_self, *args, **kwargs):
            orig_init(agent_self, *args, **kwargs)
            try:
                attach_debugger(
                    agent_self,
                    existing=dbg,
                    layers={"model", "observer", "tools", "executor"},
                )
            except Exception as exc:
                console.print(f"[yellow]layer attach failed: {exc}[/]")

        CoreAgent.__init__ = patched_init

    async def _run_turn_async(self, user_msg):
        info = build_agent_run_info(
            user_msg,
            list(self.history),
            max_steps=self.max_steps,
            context_manager_config=self.cm_config,
        )
        info.context_manager = self.shared_cm
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = await run_agent_with_tracking(info)
        return result

    def run_turn(self, user_msg):
        self.turn += 1
        user_msg = _strip_surrogates(user_msg)
        result = asyncio.run(self._run_turn_async(user_msg))
        result.final_answer = _strip_surrogates(result.final_answer or "")
        self.history.append(AgentHistory(role="user", content=user_msg))
        self.history.append(AgentHistory(role="assistant", content=result.final_answer))
        self.last_turn_events = self._drain_events()
        self._record_tokens()
        return result

    def _drain_events(self):
        events = []
        try:
            with open(TRACE_PATH, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    e = json.loads(line)
                    if e["seq"] > self._last_seq:
                        events.append(e)
        except FileNotFoundError:
            return []
        if events:
            self._last_seq = max(e["seq"] for e in events)
        return events

    def _record_tokens(self):
        evs = self.last_turn_events
        main = [e for e in evs if e["event"] == "llm_call_end"
                and e["data"].get("tag") == "main"]
        comp = [e for e in evs if e["event"] == "llm_call_end"
                and e["data"].get("tag") == "compression"]
        self.turn_tokens.append({
            "turn": self.turn,
            "main_in": _sum(main, "input_tokens"),
            "main_out": _sum(main, "output_tokens"),
            "comp_in": _sum(comp, "input_tokens"),
            "comp_out": _sum(comp, "output_tokens"),
        })


def render_turn(session, result, events):
    answer = result.final_answer or "(no answer)"
    console.print(Panel(
        answer.strip(),
        title=f"Turn {session.turn}  \u00b7  agent final answer (main LLM)",
        border_style="green",
        expand=False,
    ))

    main = [e for e in events if e["event"] == "llm_call_end"
            and e["data"].get("tag") == "main"]
    comp = [e for e in events if e["event"] == "llm_call_end"
            and e["data"].get("tag") == "compression"]
    steps = [e for e in events if e["event"] == "observer_event"
             and e["data"].get("process_type") == "step_count"]
    cbegins = [e for e in events if e["event"] == "compress_begin"]
    cends = [e for e in events if e["event"] == "compress_end"]
    tools = [e for e in events if e["event"] == "tool_call_end"]
    code = [e for e in events if e["event"] == "code_execute_end"]

    t = Table(box=box.SIMPLE, show_header=False)
    t.add_column("k", style="cyan", no_wrap=True)
    t.add_column("v")

    t.add_row("agent steps", str(len(steps)))
    if main:
        t.add_row(
            "main LLM",
            f"\u00d7{len(main)}   {_sum(main,'input_tokens')}\u2192{_sum(main,'output_tokens')} tok"
            f"   {_sum(main,'duration_ms')/1000:.1f}s   [dim](API)[/]",
        )
    if comp:
        t.add_row(
            "compression LLM",
            f"\u00d7{len(comp)}   {_sum(comp,'input_tokens')}\u2192{_sum(comp,'output_tokens')} tok"
            f"   {_sum(comp,'duration_ms')/1000:.1f}s   [dim](API)[/]",
        )
        t.add_row(
            "",
            "[dim]\u21e3 separate LLM call (not the answer above) — "
            "/compress shows its prompt + summary[/]",
        )

    if cbegins:
        for cb, ce in zip(cbegins, cends):
            pd = cb["data"].get("predicted_decision") or {}
            tc = ce["data"].get("token_counts") or {}
            unc, cmp_ = tc.get("last_uncompressed"), tc.get("last_compressed")
            ratio = f"  ({(cmp_-unc)/unc*100:+.0f}%)" if unc and cmp_ else ""
            sc = ce["data"].get("summary_changed") or {}
            changed = []
            if sc.get("previous_changed"):
                changed.append("previous")
            if sc.get("current_changed"):
                changed.append("current")
            t.add_row(
                "compression",
                f"[bold]TRIGGERED[/]  branch={pd.get('branch')}  "
                f"{unc}\u2192{cmp_} tok{ratio}  [dim](est.)[/]",
            )
            if changed:
                t.add_row("", f"summary updated: {', '.join(changed)}")
    else:
        t.add_row("compression", "[dim]not triggered[/]")

    if code:
        t.add_row("code exec", f"\u00d7{len(code)}")
    if tools:
        names = ", ".join(e["data"].get("tool", "?") for e in tools)
        t.add_row("tool calls", names)

    errors = [e for e in events if e["event"] == "debug_error"]
    if errors:
        t.add_row("debug errors", f"[red]{len(errors)}[/] (see /trace)")

    console.print(Panel(t, title="context construction", border_style="blue",
                         expand=False))


def _print_config(session):
    c = session.cm_config
    t = Table(box=box.SIMPLE, show_header=False)
    t.add_column("k", style="cyan")
    t.add_column("v")
    t.add_row("token_threshold", str(c.token_threshold))
    t.add_row("keep_recent_pairs", str(c.keep_recent_pairs))
    t.add_row("keep_recent_steps", str(c.keep_recent_steps))
    t.add_row("max_steps", str(session.max_steps))
    t.add_row("trace file", TRACE_PATH)
    console.print(Panel(t, title="ContextManagerConfig", border_style="dim",
                         expand=False))


def _cmd_history(session):
    if not session.history:
        console.print("[dim](no history yet)[/]")
        return
    t = Table(box=box.SIMPLE)
    t.add_column("#", justify="right")
    t.add_column("role", style="cyan")
    t.add_column("content")
    for i, h in enumerate(session.history):
        content = h.content if isinstance(h.content, str) else str(h.content)
        if len(content) > 200:
            content = content[:200] + f" \u2026[+{len(content)-200} chars]"
        t.add_row(str(i), h.role, content.replace("\n", " "))
    console.print(Panel(
        t,
        title=f"Session ledger — pre-compression ({len(session.history)} msgs)",
        border_style="blue", expand=False,
    ))


def _is_summary_msg(text):
    return isinstance(text, str) and text.startswith("Summary of earlier steps")


def _cmd_context(session, arg=None):
    evs = session.last_turn_events
    if not evs:
        console.print("[dim](no events from last turn — run a turn first)[/]")
        return
    pairs = []
    pending = None
    for e in evs:
        if e["event"] == "llm_call_begin" and e["data"].get("tag") == "main":
            pending = e
        elif e["event"] == "llm_call_end" and e["data"].get("tag") == "main":
            pairs.append((pending, e))
            pending = None
    if pending is not None:
        pairs.append((pending, None))
    if not pairs:
        console.print("[dim](no main LLM call in the last turn)[/]")
        return

    idx = 1
    if arg:
        try:
            idx = int(arg)
        except ValueError:
            console.print("[red]usage: /context [N]  (N = which main LLM call)[/]")
            return
    if not (1 <= idx <= len(pairs)):
        console.print(
            f"[red]turn made {len(pairs)} main LLM call(s); pick 1..{len(pairs)}[/]")
        return

    begin, end = pairs[idx - 1]
    msgs = (begin["data"].get("input_messages")) or []
    has_summary = False
    est_total = 0

    t = Table(box=box.SIMPLE)
    t.add_column("#", justify="right")
    t.add_column("role", style="cyan", no_wrap=True)
    t.add_column("tokens", justify="right")
    t.add_column("content")
    for i, m in enumerate(msgs):
        body = m.get("text") or m.get("preview") or ""
        toks = estimate_tokens_text(body)
        est_total += toks
        role = m.get("role", "?")
        is_summary = _is_summary_msg(body)
        if is_summary:
            has_summary = True
            role = "user \u00b7 summary"
        flat = body.replace("\n", " ")
        if len(flat) > 280:
            flat = flat[:280] + f" \u2026[+{len(flat)-280} chars]"
        t.add_row(
            str(i), role, str(toks),
            f"[yellow]{flat}[/]" if is_summary else flat,
        )

    title = (f"Context fed to main LLM \u2014 turn {session.turn}, "
             f"call {idx}/{len(pairs)}  ({len(msgs)} msgs"
             f"{', incl. compression summary' if has_summary else ''})")
    console.print(Panel(t, title=title, border_style="blue", expand=False))

    real_in = end["data"].get("input_tokens") if end else None
    footer = f"[dim]\u00b7 ~{est_total} tokens estimated"
    if real_in:
        footer += f"  \u00b7  {real_in} reported by the API"
    console.print(footer + "[/]")
    if has_summary:
        console.print(
            "[dim]\u00b7 the [yellow]summary[/] row replaced earlier turns \u2014 "
            "/summary for its full text, /history for the raw ledger[/]")
    else:
        console.print(
            "[dim]\u00b7 no summary yet \u2014 model still sees the full history "
            "verbatim (compression has not collapsed anything)[/]")
    out_chars = end["data"].get("output_chars") if end else None
    reply_note = f" ({out_chars} chars)" if out_chars else ""
    console.print(
        f"[dim]\u00b7 these are the INPUT to the call; the model's reply{reply_note} "
        f"is its output \u2014 see the agent answer panel above[/]")
    if len(pairs) > 1:
        console.print(
            f"[dim]\u00b7 turn made {len(pairs)} main LLM calls (one per step); "
            f"/context N for call N[/]")


def _cmd_summary(session):
    s = session.shared_cm.export_summary()
    prev = s.get("previous_summary")
    curr = s.get("current_summary")
    if not prev and not curr:
        console.print("[dim](no compression summary yet \u2014 nothing compressed)[/]")
        return
    if prev:
        console.print(Panel(prev, title="previous_summary", border_style="yellow",
                             expand=False))
    if curr:
        console.print(Panel(curr, title="current_summary", border_style="yellow",
                             expand=False))
    boundary = s.get("compression_boundary") or {}
    console.print(f"[dim]boundary: {boundary}[/]")


def _cmd_compress(session):
    evs = session.last_turn_events
    if not evs:
        console.print("[dim](no events from last turn)[/]")
        return

    pairs = []
    pending = None
    for e in evs:
        if e["event"] == "llm_call_begin" and e["data"].get("tag") == "compression":
            pending = e
        elif e["event"] == "llm_call_end" and e["data"].get("tag") == "compression":
            pairs.append((pending, e))
            pending = None

    if not pairs:
        console.print(
            "[dim](no compression LLM call last turn \u2014 compression did not "
            "run, or resolved without invoking the LLM)[/]"
        )
        return

    call_types = [
        e["data"].get("call_type")
        for e in evs
        if e["event"] == "compression_call" and not e["data"].get("cache_hit")
    ]

    for idx, (begin, end) in enumerate(pairs):
        ctype = call_types[idx] if idx < len(call_types) else None
        header = f"compression call #{idx + 1}"
        if ctype:
            header += f"  \u00b7  {ctype}"
        console.print(f"\n[bold]{header}[/]")

        in_msgs = (begin["data"].get("input_messages") if begin else None) or []
        for m in in_msgs:
            body = m.get("text") or m.get("preview") or "(empty)"
            console.print(Panel(
                body,
                title=(f"\u2192 fed to compression LLM   [{m.get('role')}]   "
                       f"{m.get('chars')} chars"),
                border_style="cyan",
                expand=False,
            ))

        d = end["data"]
        out = d.get("output_full") or d.get("output_preview") or "(empty)"
        console.print(Panel(
            out,
            title=(f"\u2190 compression LLM produced (summary)   "
                   f"{d.get('output_chars')} chars   {d.get('duration_ms')}ms"),
            border_style="yellow",
            expand=False,
        ))


def _cmd_tokens(session):
    if not session.turn_tokens:
        console.print("[dim](no turns yet)[/]")
        return
    t = Table(box=box.SIMPLE_HEAD, title="Token timeline")
    t.add_column("Turn", justify="right")
    t.add_column("Main in", justify="right")
    t.add_column("Main out", justify="right")
    t.add_column("Comp in", justify="right")
    t.add_column("Comp out", justify="right")
    for tk in session.turn_tokens:
        t.add_row(
            str(tk["turn"]),
            str(tk["main_in"]), str(tk["main_out"]),
            str(tk["comp_in"] or "-"), str(tk["comp_out"] or "-"),
        )
    console.print(t)


def _cmd_stats(session):
    cm = session.shared_cm
    try:
        stats = cm.get_all_compression_stats()
    except Exception as exc:
        console.print(f"[red]could not read compression stats: {exc}[/]")
        return

    log = list(getattr(cm, "compression_calls_log", []) or [])
    llm_by_type = Counter(r.call_type for r in log if not r.cache_hit)
    cache_by_type = Counter(r.call_type for r in log if r.cache_hit)

    t = Table(box=box.SIMPLE, show_header=False)
    t.add_column("k", style="cyan")
    t.add_column("v")
    t.add_row("turns run", str(session.turn))
    t.add_row("LLM compression calls", f"[bold]{stats.get('total_calls', 0)}[/]")
    t.add_row("cache hits (no LLM call)", str(stats.get("total_cache_hits", 0)))
    t.add_row("total compression attempts", str(stats.get("total_attempts", 0)))
    t.add_row(
        "compression tokens in\u2192out",
        f"{stats.get('total_input_tokens', 0)}\u2192"
        f"{stats.get('total_output_tokens', 0)}  [dim](API)[/]",
    )
    console.print(Panel(t, title="Compression stats \u2014 session-wide",
                        border_style="blue", expand=False))
    if llm_by_type:
        bd = "  ".join(f"{k}\u00d7{n}" for k, n in llm_by_type.items())
        console.print(f"[dim]\u00b7 LLM compression calls by type: {bd}[/]")
    if cache_by_type:
        bd = "  ".join(f"{k}\u00d7{n}" for k, n in cache_by_type.items())
        console.print(f"[dim]\u00b7 cache-hit (no-LLM) compressions by type: {bd}[/]")


def _cmd_trace(session, arg):
    events = session.last_turn_events
    if not events:
        console.print("[dim](no events from last turn)[/]")
        return
    t = Table(box=box.SIMPLE, title="Last turn \u2014 raw events")
    t.add_column("seq", justify="right")
    t.add_column("step", justify="right")
    t.add_column("event", style="cyan")
    t.add_column("detail")
    for e in events:
        d = e["data"]
        ev = e["event"]
        if ev == "llm_call_end":
            detail = (f"tag={d.get('tag')} dur={d.get('duration_ms')}ms "
                      f"in={d.get('input_tokens')} out={d.get('output_tokens')}")
        elif ev == "compress_begin":
            pd = d.get("predicted_decision") or {}
            detail = f"branch={pd.get('branch')}"
        elif ev == "compression_call":
            detail = (f"type={d.get('call_type')} cache={d.get('cache_hit')} "
                      f"in={d.get('input_tokens')} out={d.get('output_tokens')}")
        elif ev == "compress_end":
            tc = d.get("token_counts") or {}
            detail = f"{tc.get('last_uncompressed')}\u2192{tc.get('last_compressed')}"
        elif ev == "observer_event":
            detail = f"[{d.get('process_type')}]"
        elif ev == "code_execute_end":
            detail = f"dur={d.get('duration_ms')}ms final={d.get('is_final_answer')}"
        elif ev == "tool_call_end":
            detail = f"tool={d.get('tool')} dur={d.get('duration_ms')}ms"
        elif ev == "debug_error":
            detail = f"[red]{d.get('phase')}: {d.get('error')}[/]"
        else:
            detail = ""
        t.add_row(str(e["seq"]), str(e.get("agent_step") or "-"), ev, detail)
    console.print(t)


def _cmd_step(session, arg):
    try:
        step_n = int(arg)
    except (ValueError, TypeError):
        console.print("[red]usage: /step N[/]")
        return
    events = [e for e in session.last_turn_events
              if e.get("agent_step") == step_n]
    if not events:
        console.print(f"[dim](no events at step {step_n} in last turn)[/]")
        return
    for e in events:
        content = json.dumps(e["data"], ensure_ascii=False, indent=2)
        if len(content) > 3000:
            content = content[:3000] + f"\n\u2026[+{len(content)-3000} chars]"
        console.print(Panel(content, title=f"seq={e['seq']} {e['event']}",
                             border_style="cyan", expand=False))


HELP = """[bold]Commands[/]
  /help              this help
  /context [N]       context the main LLM received last turn (post-compression)
  /history           raw session ledger (every turn verbatim, pre-compression)
  /summary           current compression summary (full text)
  /compress          last turn's compression LLM input prompt + output summary
  /tokens            per-turn token timeline
  /stats             session-wide compression stats (LLM compression call count)
  /trace             raw trace events from the last turn
  /step N            dump every event of agent step N (last turn)
  /config            show ContextManagerConfig
  /reset [threshold] fresh session, optionally new token_threshold
  /quit  /q          exit

Anything not starting with / is sent to the agent as a user turn."""


def handle_command(session, line):
    parts = line.split()
    cmd = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    if cmd in ("/quit", "/q", "/exit"):
        return None, True
    if cmd == "/help":
        console.print(Panel(HELP, border_style="magenta", expand=False))
    elif cmd == "/context":
        _cmd_context(session, arg)
    elif cmd == "/history":
        _cmd_history(session)
    elif cmd == "/summary":
        _cmd_summary(session)
    elif cmd == "/compress":
        _cmd_compress(session)
    elif cmd == "/tokens":
        _cmd_tokens(session)
    elif cmd == "/stats":
        _cmd_stats(session)
    elif cmd == "/trace":
        _cmd_trace(session, arg)
    elif cmd == "/step":
        _cmd_step(session, arg)
    elif cmd == "/config":
        _print_config(session)
    elif cmd == "/reset":
        threshold = session.cm_config.token_threshold
        if arg:
            try:
                threshold = int(arg)
            except ValueError:
                console.print("[red]threshold must be an integer[/]")
                return session, False
        new = Session(token_threshold=threshold)
        console.print(f"[green]session reset[/] (token_threshold={threshold})")
        return new, False
    else:
        console.print(f"[red]unknown command: {cmd}[/]  (/help)")
    return session, False


def main():
    console.print(Panel(
        "Nexent Context Debugger \u2014 interactive REPL\n"
        "Type a message to run one agent turn. /help for commands.\n"
        "Up/down arrows recall earlier input (history kept across sessions).",
        border_style="magenta", expand=False,
    ))
    session = Session()
    _print_config(session)
    _init_history()

    while True:
        try:
            raw = input(_PROMPT)
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]bye.[/]")
            break
        _save_history()

        line = _clean_input(raw).strip()

        if not line:
            continue

        if line.startswith("/"):
            session, should_quit = handle_command(session, line)
            if should_quit:
                console.print("[dim]bye.[/]")
                break
            continue

        with console.status("[dim]running agent turn\u2026[/]"):
            try:
                result = session.run_turn(line)
            except Exception as exc:
                console.print(f"[red]turn failed: {exc}[/]")
                import traceback
                traceback.print_exc(file=_OUT)
                continue

        render_turn(session, result, session.last_turn_events)


if __name__ == "__main__":
    main()
