# ClaudeAstroVolpert

An onboarding package for using Claude Code in astronomy research.
Includes a guided setup script, a generalisable CLAUDE.md template, a shared
constants file, a Claude reference dictionary, and a fully worked example project.

**Created by**: Carrie Volpert (https://github.com/cvolpert)
**Created**: 2026-05-29
**For**: ISM astronomers and radio/IR/JWST observers getting started with Claude Code

---

## Contents

```
ClaudeAstroVolpert/
├── startup.py                    — Interactive setup script (run this first)
├── hooks/
│   └── pre-commit                — Git hook: auto-updates CLAUDE.md Last Edited header
├── templates/
│   ├── CLAUDE_template.md        — Starter CLAUDE.md for a new project
│   ├── constants_template.py     — Shared physical constants template
│   └── where_I_left_off_template.md  — Session handoff log template
├── docs/
│   └── claude_command_dict.md    — Claude models, tokens, commands reference
└── example_project/              — Worked example showing the full structure
    ├── CLAUDE.md                 — Example CLAUDE.md (Local Group HI project)
    ├── constants.py              — Example constants.py (partially filled)
    ├── where_I_left_off.md       — Example session log
    ├── Background/               — Example background summary
    ├── Analysis/
    │   ├── SpectralAnalysis/spectral_fitting_lib.py   — Example library
    │   ├── tests/test_moment_maps.py                  — Example unit tests
    │   └── descriptions/spectral_fitting_lib_info.md  — Example documentation
    └── ...
```

## Quick Start

1. Install Claude Code: see [Anthropic's documentation](https://docs.anthropic.com/claude-code)
2. Open a terminal in the directory where you want your new project to live
3. Start Claude Code: `claude`
4. Run the setup script:
   ```
   !python3 /path/to/ClaudeAstroVolpert/startup.py
   ```

The script will walk you through everything interactively — project naming,
directory creation, literature digest, data organisation, and CLAUDE.md customisation.

## What You Get

- A standard directory structure (Background, Data, Analysis, Visualizations,
  Publication, ProgressReports, logs) with tests/, debug/, and descriptions/ subdirs
- Five pre-configured sub-agents (Art Critic, Physics Cop, Scribe, Code Cop, Librarian)
- A session handoff log (`where_I_left_off.md`) that persists context across sessions
- A centralised constants file (`constants.py`) for project-wide physical values
- A background summary document Claude generates from your project's literature
- A Claude reference dictionary covering models, tokens, costs, and key commands
- A git pre-commit hook that automatically updates the `Last Edited` header in
  `CLAUDE.md` whenever the file is committed — so you always know when the config changed

## Reading Order for New Users

1. Read `docs/claude_command_dict.md` for Claude basics (models, tokens, commands)
2. Look through `example_project/CLAUDE.md` to see what a filled-in config looks like
3. Browse the `example_project/Analysis/` files to see the coding and documentation conventions
4. Run `startup.py` to create your own project

## Licence / Attribution

Free to use and adapt for your own research. If you build on it substantially,
a mention to Carrie Volpert (https://github.com/cvolpert) is appreciated.
