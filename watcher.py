import time, pathlib, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
pathlib.Path("wATCHER.log").write_text("", encoding='utf-8')
state = pathlib.Path("STATE.md")
last = {"mtime": 0, "size": 0}
log = pathlib.Path("wATCHER.log")
while True:
    try:
        if state.exists():
            st = state.stat()
            if st.st_mtime > last["mtime"] or st.st_size != last["size"]:
                last["mtime"] = st.st_mtime
                last["size"] = st.st_size
                log.write_text(log.read_text(encoding='utf-8', errors='replace') + f"{time.ctime()} STATE.md changed → {st.st_size} bytes\n", encoding='utf-8')
        log.write_text(log.read_text(encoding='utf-8', errors='replace') + f"{time.ctime()} heartbeat\n", encoding='utf-8')
    except Exception as e:
        log.write_text(log.read_text(encoding='utf-8', errors='replace') + f"{time.ctime()} ERROR: {e}\n", encoding='utf-8')
    time.sleep(30)
