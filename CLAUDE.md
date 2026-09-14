# CLAUDE.md

## No side effects on import

- Module-level code may only *define* things: imports, constants, functions, classes. It must never *do* real work — network/API calls, credential or config checks, file I/O, expensive object construction — as a side effect of the module simply being imported.
- Anything with a real effect or a failure path belongs inside a function, called only when it's actually needed. Do not reach for lazy imports as a workaround — defer the *logic*, not the *import*.
- Rationale and precedent: see Opinion #1 in `docs/opinions.md` (module-level provider/client construction and an eager skills-index read broke `mosfet config` on a fresh install, since those code paths ran just from importing the module, before any command-specific logic had a chance to run).

## README.md conventions

- Keep it a brief, high-level intro — not detailed technical documentation (no step-by-step "how this feature works" sections).
- Features section: plain sentences, not a checklist. Only list things that actually work today — skip stubs/unimplemented items entirely.
- No internal file paths, command syntax, or function/tool names in feature descriptions — describe behavior in plain English.
- Project Structure tree: top-level `src/` entries only (max depth 1), except `adapters/` and `extensions/`, which expand one level deeper to list their immediate subfolders.
- Keep "How to run the project" in sync whenever a new setup/install method is added.
- The Description should accurately reflect all extension mechanisms mentioned (skills, tools, MCP servers), not just one.
