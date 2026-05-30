# ClaudeAstroVolpert

A Claude Code onboarding package tuned specifically for observational ISM astronomy
research, using the Volpert code and project architecture framework. Includes a
guided interactive setup script, a generalisable `CLAUDE.md` project configuration
template, a shared physical constants file, a Claude reference dictionary, and a
fully worked example project showing the complete directory structure and workflow.

**Created by**: Carrie Volpert (https://github.com/cvolpert)
**Created**: 2026-05-29
**For**: Observational ISM astronomers working with radio, IR, and JWST data —
radio continuum and spectral line observers, multi-phase ISM analysts, and anyone
studying the MW, Local Group, or low-redshift universe who wants a rigorous,
well-structured Claude Code workflow out of the box.

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

## Installation

Everything can be done from the command line — no GitHub UI needed.

**Step 1 — Install Claude Code** (if you haven't already):
```bash
npm install -g @anthropic-ai/claude-code
```
Or see [Anthropic's installation docs](https://docs.anthropic.com/claude-code) for
alternative install methods (pip, brew, etc.).

**Step 2 — Clone this repository** to wherever you want to keep it
(e.g. `~/software/` or `~/`). This is the *package* location, not your project:
```bash
git clone https://github.com/particlerover/ClaudeAstroVolpert.git
```

That's it. No build step, no dependencies beyond Python 3 (which you already have).

---

## Quick Start

Run the setup script as a plain Python script from any terminal — you do **not**
need to be inside a Claude Code session to run it:

```bash
python3 ~/ClaudeAstroVolpert/startup.py
```

The script handles all the mechanical setup (directory structure, template files,
git initialisation) on its own. At steps that require Claude's intelligence
(digesting your literature, organising data files, customising CLAUDE.md), it
pauses and prints a highlighted **TELL CLAUDE** box containing the exact prompt
to use. You copy that prompt, open Claude Code in your new project directory,
paste it, let Claude do its work, then come back and press Enter to continue.

After the script finishes, start your first Claude session:
```bash
cd ~/path/to/YourNewProject
claude
```
Claude will read `CLAUDE.md` and `where_I_left_off.md` automatically and pick
up right where the setup left off.

> **Note for Windows users**: use `python` instead of `python3` if that is how
> Python 3 is registered on your system. The script is fully cross-platform.

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
