export function formatHuman(r) {
    const lines = [];
    lines.push('');
    lines.push(`Loop Readiness Audit — ${r.target}`);
    lines.push('═'.repeat(50));
    lines.push(`Score: ${r.score}/100  Level: ${r.level}`);
    lines.push(r.assessment);
    lines.push('');
    lines.push('Findings:');
    for (const f of r.findings) {
        const icon = f.level === 'ok' ? '✓' : f.level === 'warn' ? '!' : '✗';
        lines.push(`  ${icon} ${f.message}`);
    }
    if (r.recommendations.length) {
        lines.push('');
        lines.push('Recommendations:');
        for (const rec of r.recommendations) {
            lines.push(`  → ${rec}`);
        }
    }
    lines.push('');
    lines.push('Docs: docs/loop-design-checklist.md');
    lines.push('Tip: rerun with --suggest for ready-to-paste copy commands from templates/starters.');
    lines.push('');
    return lines.join('\n');
}
export function formatJson(r) {
    return JSON.stringify(r, null, 2);
}
export function formatMarkdown(r) {
    const lines = [];
    lines.push('# Loop Readiness Report');
    lines.push('');
    lines.push(`| Metric | Value |`);
    lines.push(`|--------|-------|`);
    lines.push(`| Target | \`${r.target}\` |`);
    lines.push(`| Score | **${r.score}/100** |`);
    lines.push(`| Level | ${r.level} |`);
    lines.push(`| Assessment | ${r.assessment} |`);
    lines.push('');
    lines.push('## Findings');
    lines.push('');
    for (const f of r.findings) {
        lines.push(`- **${f.level}**: ${f.message}`);
    }
    if (r.recommendations.length) {
        lines.push('');
        lines.push('## Recommendations');
        lines.push('');
        for (const rec of r.recommendations) {
            lines.push(`- ${rec}`);
        }
    }
    return lines.join('\n');
}
