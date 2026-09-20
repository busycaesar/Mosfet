# CLAUDE.md

## No side effects on import

- Module-level code may only *define* things: imports, constants, functions, classes. It must never *do* real work — network/API calls, credential or config checks, file I/O, expensive object construction — as a side effect of the module simply being imported.
- Anything with a real effect or a failure path belongs inside a function, called only when it's actually needed. Do not reach for lazy imports as a workaround — defer the *logic*, not the *import*.
- Exception: plain object construction that touches no network/credentials/files and cannot fail (e.g. `discord.Client(intents=...)`, a `Console()`) can stay as a top-level module assignment instead of being wrapped in a function. This is a narrow, deliberate exception for genuinely risk-free construction, not a loophole for anything that does real work.
- Never defer an *import statement* itself to work around this rule, even for a legitimate goal like avoiding an unrelated command from loading a subsystem it doesn't need. Fix it at the source module instead — wrap the risky logic in a function there, or use the exception above if the code truly has no failure path.
- When something is correctly deferred into a function, don't default to caching it with a module-level `global`. Caching only pays for itself if the function would otherwise run on every import or inside a hot loop — most config/env getters do neither, they're called a handful of times per process at most. In that case, redoing the cheap work each call (e.g. re-reading a small local file) is simpler and cheaper than adding global mutable state to avoid it. If caching genuinely is worth it, prefer `functools.lru_cache` over a hand-written `global` + `None`-check.
- Rationale and precedent: see Opinion #1 in `docs/opinions.md` (module-level provider/client construction and an eager skills-index read broke `mosfet config` on a fresh install, since those code paths ran just from importing the module, before any command-specific logic had a chance to run).

## README.md conventions

- Keep it a brief, high-level intro — not detailed technical documentation (no step-by-step "how this feature works" sections).
- Features section: plain sentences, not a checklist. Only list things that actually work today — skip stubs/unimplemented items entirely.
- No internal file paths, command syntax, or function/tool names in feature descriptions — describe behavior in plain English.
- Project Structure tree: top-level `src/` entries only (max depth 1), except `adapters/` and `extensions/`, which expand one level deeper to list their immediate subfolders.
- Keep "How to run the project" in sync whenever a new setup/install method is added.
- The Description should accurately reflect all extension mechanisms mentioned (skills, tools, MCP servers), not just one.
