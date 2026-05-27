# Setup Notes

## Official Sources

- CodeGraph: https://github.com/colbymchenry/codegraph
- Understand-Anything: https://github.com/Lum1104/Understand-Anything

Both are external dependencies. Check the official README before running install or upgrade commands.

## Expected Local Artifacts

```text
.codegraph/
.understand-anything/knowledge-graph.json
```

Do not commit these artifacts unless the repository intentionally tracks them.

## Suggested Ignore Policy

Exclude:

- `.git/`
- `.codegraph/`
- `.understand-anything/`
- `.idea/`, `.vscode/`
- `vendor/`, `node_modules/`
- build outputs, caches, logs, coverage
- large binaries, dumps, private snapshots
- conversation histories unless task memory is explicitly needed

## Project Cache Placement

Prefer one compact summary file:

- `.codex/memories/project-knowledge-graph-map.md`
- `.specstory/history/<task>.md`
- project-documented agent notes

Include:

- generation time
- tool path used
- graph artifact status
- exclusions and blind spots
- entry points and risk areas
- validation commands
- refresh rule

Avoid:

- full graph dumps in prompts
- raw secret/config values
- stale summaries without dates
