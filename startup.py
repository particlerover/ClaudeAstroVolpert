#!/usr/bin/env python3
# Created: 2026-05-29 00:00:00
# Last Modified: 2026-05-29 14:00:00
# Description: Startup script for ClaudeAstroVolpert. Creates the project directory
#   structure, copies templates, initialises git, writes an .onboarding_pending
#   marker, then launches a normal Claude Code session. Claude reads CLAUDE.md,
#   detects the marker, and walks the user through the rest interactively with
#   full normal permissions — no special flags required.
# Last Edit: Rearchitect: startup.py is purely mechanical setup; all onboarding
#   logic moved into CLAUDE.md First Run Protocol / Onboarding Mode.

"""
ClaudeAstroVolpert — Interactive Project Setup
================================================
Created by Carrie Volpert (https://github.com/cvolpert)

Run this script from within a Claude Code terminal session (or a regular terminal).
It will walk you through setting up a new Claude-assisted research project.

Usage:
    python3 startup.py
"""

import os
import sys
import shutil
import json
import textwrap
import subprocess
from pathlib import Path
from datetime import datetime

# ─── Terminal width ────────────────────────────────────────────────────────────
try:
    COLS = os.get_terminal_size().columns
except OSError:
    COLS = 80
COLS = min(max(COLS, 40), 100)  # clamp to [40, 100] to avoid edge cases


# ─── ANSI colour codes ────────────────────────────────────────────────────────

def _enable_color():
    """Return True if ANSI colour codes will render in the current terminal."""
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        # Windows: try to enable VT100 virtual terminal processing.
        # Works on Windows 10+ (build 1511+) and Windows Terminal.
        # Silently falls back to no colour on older consoles.
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT |
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 0x0007)
            return True
        except Exception:
            return False
    return True

_USE_COLOR = _enable_color()


def _enable_unicode():
    """Return True if the terminal encoding can render Unicode box characters."""
    enc = getattr(sys.stdout, "encoding", "") or ""
    return enc.lower().replace("-", "").startswith("utf")

_USE_UNICODE = _enable_unicode()


# Printable character set — Unicode where supported, ASCII fallback elsewhere.
_CH = {
    "hrule":  "─" if _USE_UNICODE else "-",
    "tick":   "✓" if _USE_UNICODE else "OK",
    "cross":  "✗" if _USE_UNICODE else "X",
    "arrow":  "▶" if _USE_UNICODE else ">",
    "tri":    "►" if _USE_UNICODE else ">",
    "tee":    "├──" if _USE_UNICODE else "+--",
    "bend":   "└──" if _USE_UNICODE else "+--",
    "pipe":   "│"   if _USE_UNICODE else "|",
}


def _c(*codes):
    return "\033[" + ";".join(str(c) for c in codes) + "m" if _USE_COLOR else ""

RESET   = _c(0)
BOLD    = _c(1)
DIM     = _c(2)
CYAN    = _c(36)
YELLOW  = _c(33)
GREEN   = _c(32)
RED     = _c(31)
MAGENTA = _c(35)
BCYAN   = _c(96)   # bright cyan
BYELLOW = _c(93)   # bright yellow
BGREEN  = _c(92)   # bright green
BWHITE  = _c(97)   # bright white


# ─── Display helpers ──────────────────────────────────────────────────────────

def _wrap_line(line, width, indent=0):
    """Wrap a single plain-text line, preserving its leading indentation."""
    stripped = line.lstrip()
    lead = len(line) - len(stripped)
    prefix = " " * (indent + lead)
    if not stripped:
        return ""
    return textwrap.fill(
        stripped, max(width - indent - lead, 10),
        initial_indent=prefix, subsequent_indent=prefix,
    )


def hr(char="-", color=CYAN):
    """Print a full-width horizontal rule."""
    print(f"{color}{char * COLS}{RESET}")


def banner(lines):
    """
    Print a bordered banner.  lines is either a list of strings or a single
    newline-delimited string.  Line 0 = title (bold white), line 1 = subtitle
    (cyan), remainder = body text (dim).  Empty lines print as blank rows.
    """
    if isinstance(lines, str):
        lines = lines.split("\n")

    print(f"{BCYAN}{BOLD}{'=' * COLS}{RESET}")
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            print()
            continue
        if i == 0:
            color = BOLD + BWHITE
        elif i == 1:
            color = CYAN
        else:
            color = DIM
        # Wrap the plain line first, then apply colour per wrapped line.
        width = COLS - 4
        for wline in textwrap.wrap(line, width) or [""]:
            print(f"  {color}{wline}{RESET}")
    print(f"{BCYAN}{BOLD}{'=' * COLS}{RESET}")


def section(num, title):
    """Print a numbered step header."""
    print()
    hr("-", color=CYAN)
    print(f"  {BOLD}{YELLOW}STEP {num}:{RESET} {BOLD}{BWHITE}{title}{RESET}")
    hr("-", color=CYAN)
    print()


def info(text, indent=2):
    """
    Print body text preserving line structure within paragraphs.
    Splits on double-newlines for paragraphs, single newlines for lines —
    so numbered lists and indented blocks render correctly.
    Uses textwrap.dedent to strip Python source indentation first.
    """
    text = textwrap.dedent(text).strip()
    for para in text.split("\n\n"):
        for line in para.split("\n"):
            wrapped = _wrap_line(line, COLS, indent)
            if wrapped:
                print(wrapped)
            else:
                print()
        print()


def claude_prompt_box(label, prompt_text):
    """Print a highlighted box containing the prompt to give Claude."""
    width = COLS - 6
    rule = _CH["hrule"] * (COLS - 4)
    print()
    print(f"{BYELLOW}{BOLD}  {rule}{RESET}")
    print(f"  {BOLD}{BYELLOW}{_CH['tri']} TELL CLAUDE:{RESET}")
    print(f"{BYELLOW}{BOLD}  {rule}{RESET}")
    for line in prompt_text.strip().split("\n"):
        for wline in textwrap.wrap(line.strip(), width) or [""]:
            print(f"  {BWHITE}{wline}{RESET}")
    print(f"{BYELLOW}{BOLD}  {rule}{RESET}")
    print()


def pause(msg="Press Enter when ready to continue..."):
    print(f"\n  {BGREEN}{_CH['arrow']}{RESET}  {msg}")
    try:
        input("     ")
    except KeyboardInterrupt:
        print("\n\nSetup interrupted. Re-run startup.py to resume.")
        sys.exit(0)


def ask(prompt, default=None):
    if default:
        full_prompt = f"  {GREEN}{_CH['arrow']}{RESET}  {prompt} [{default}]: "
    else:
        full_prompt = f"  {GREEN}{_CH['arrow']}{RESET}  {prompt}: "
    try:
        val = input(full_prompt).strip()
    except KeyboardInterrupt:
        print("\n\nSetup interrupted.")
        sys.exit(0)
    return val if val else default


# ─── State tracking ───────────────────────────────────────────────────────────

PACKAGE_DIR = Path(__file__).resolve().parent
STATE_FILENAME = ".claude_setup_state.json"


def load_state(project_dir):
    path = Path(project_dir) / STATE_FILENAME
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return {"completed_steps": [], "project_dir": str(project_dir)}


def save_state(project_dir, state):
    path = Path(project_dir) / STATE_FILENAME
    with open(path, "w") as f:
        json.dump(state, f, indent=2)


# ─── Claude launcher ─────────────────────────────────────────────────────────

def _claude_available():
    """Return True if the claude CLI is on PATH."""
    return shutil.which("claude") is not None


def launch_claude(project_dir):
    """
    Launch a normal interactive Claude session in project_dir.

    Claude reads CLAUDE.md on startup, detects the .onboarding_pending marker,
    and walks the user through the rest of setup conversationally with full
    normal permissions — no special flags needed.
    """
    if not _claude_available():
        print()
        info(f"""\
    Claude Code does not appear to be installed (the 'claude' command was not
    found on your PATH).

    To complete project setup, install Claude Code:
        npm install -g @anthropic-ai/claude-code
    (or see https://docs.anthropic.com/claude-code for other install methods)

    Then open Claude in your new project directory:
        cd {project_dir}
        claude

    Claude will read CLAUDE.md, see the onboarding instructions, and walk you
    through the remaining setup steps automatically.
        """)
        return

    info(f"""\
    Mechanical setup is complete. Launching Claude in your new project...

    If this is your first time using Claude Code, it will prompt you to
    sign in before anything else. Follow the sign-in steps (it will open
    a browser or give you a URL). Once signed in, type:

        Read claude.md

    and onboarding will begin. You only need to sign in once.

    When you are done with onboarding, type /exit to close Claude.
    You can start a new session any time with:
        cd {project_dir}
        claude
    """)

    pause("Press Enter to launch Claude...")
    subprocess.run(["claude"], cwd=str(project_dir))


# ─── Directory layout ─────────────────────────────────────────────────────────

TOP_LEVEL_DIRS = [
    ("Background",      "Literature, papers, and Claude's project background summary."),
    ("Data",            "Observational data — raw, reduced, auxiliary. NOT committed to git."),
    ("Analysis",        "Processing and analysis pipelines (Python scripts, notebooks)."),
    ("Visualizations",  "Plots, figures, and diagnostic outputs."),
    ("Publication",     "Manuscript drafts, figures, and .bib bibliography."),
    ("ProgressReports", "PDF summaries for advisor/collaborator meetings."),
    ("logs",            "Run logs, SLURM outputs, debugging output files."),
]

METADATA_SUBDIRS = ["tests", "debug", "descriptions"]
METADATA_PARENTS = ["Analysis", "Visualizations", "Data"]

GITIGNORE_TEMPLATE = """\
# Data directories — never commit observational data
Data/

# Python
*.pyc
__pycache__/
*.egg-info/
.eggs/
dist/
build/
.tox/
.pytest_cache/

# Editor & OS
.DS_Store
*.swp
*~
.idea/
.vscode/

# Claude setup state (auto-generated, not needed in git)
.claude_setup_state.json

# Large output files
*.fits
*.h5
*.hdf5
*.nc
"""


def create_project_structure(project_dir):
    """Create the full standard directory structure and populate template files."""
    project_dir = Path(project_dir)
    project_dir.mkdir(parents=True, exist_ok=True)

    # Top-level dirs
    for name, _ in TOP_LEVEL_DIRS:
        (project_dir / name).mkdir(exist_ok=True)

    # Metadata subdirs
    for parent in METADATA_PARENTS:
        for sub in METADATA_SUBDIRS:
            (project_dir / parent / sub).mkdir(parents=True, exist_ok=True)

    # .gitkeep placeholders in empty dirs
    for dirpath, dirnames, filenames in os.walk(project_dir):
        d = Path(dirpath)
        if not any(d.iterdir()):
            (d / ".gitkeep").touch()

    # .gitignore
    gi = project_dir / ".gitignore"
    if not gi.exists():
        gi.write_text(GITIGNORE_TEMPLATE)

    # Copy templates
    templates_src = PACKAGE_DIR / "templates"
    copies = [
        ("CLAUDE_template.md",              "CLAUDE.md"),
        ("constants_template.py",           "constants.py"),
        ("where_I_left_off_template.md",    "where_I_left_off.md"),
    ]
    for src_name, dst_name in copies:
        src = templates_src / src_name
        dst = project_dir / dst_name
        if src.exists() and not dst.exists():
            shutil.copy(src, dst)

    # Copy command dictionary
    docs_src = PACKAGE_DIR / "docs" / "claude_command_dictionary.md"
    docs_dst = project_dir / "Background" / "claude_command_dictionary.md"
    if docs_src.exists() and not docs_dst.exists():
        shutil.copy(docs_src, docs_dst)

    # Initialise git repo and install the CLAUDE.md auto-update hook
    import subprocess
    git_dir = project_dir / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init", str(project_dir)],
                       capture_output=True, check=False)
    hook_src = PACKAGE_DIR / "hooks" / "pre-commit"
    hook_dst = project_dir / ".git" / "hooks" / "pre-commit"
    if hook_src.exists():
        shutil.copy(hook_src, hook_dst)
        hook_dst.chmod(0o755)  # make executable

    print(f"  {BGREEN}{_CH['tick']}{RESET}  {BOLD}Project directory created:{RESET} {MAGENTA}{project_dir}{RESET}")
    print()
    print(f"  {DIM}Structure:{RESET}")
    for name, desc in TOP_LEVEL_DIRS:
        print(f"    {CYAN}{name}/{RESET}  {DIM}— {desc}{RESET}")
    for parent in METADATA_PARENTS:
        for sub in METADATA_SUBDIRS:
            print(f"    {DIM}{parent}/{sub}/{RESET}")
    print(f"    {BOLD}CLAUDE.md{RESET}")
    print(f"    {BOLD}constants.py{RESET}")
    print(f"    {BOLD}where_I_left_off.md{RESET}")
    print(f"    {DIM}.gitignore{RESET}")
    print(f"    {DIM}.git/hooks/pre-commit{RESET}  {DIM}— auto-updates CLAUDE.md header on each commit{RESET}")


# ─── Individual steps ─────────────────────────────────────────────────────────

def step_1_project_name(cwd):
    section(1, "PROJECT NAME & DIRECTORY SETUP")

    info(f"""\
    This script will create a new project directory with a standardised structure
    for Claude-assisted astronomical research.

    Enter the full path where you want the project to live, including the project
    directory name itself. Use ~ for your home directory. Examples:

      ~/Research/GalacticFilaments_2026
      ~/projects/JWST_M33_ISM
      /data/projects/HI_LocalGroup_Survey

    (Your current working directory is: {cwd})
    """)

    while True:
        raw = ask("Full path for the new project directory\n"
                  "     (e.g. ~/Research/GalacticFilaments_2026)")
        if not raw:
            print(f"  {RED}{_CH['cross']}{RESET}  Please enter a path.")
            continue

        # Expand ~ and any env vars, then resolve to absolute
        project_dir = Path(os.path.expandvars(raw)).expanduser().resolve()
        name = project_dir.name.replace(" ", "_")
        project_dir = project_dir.parent / name  # sanitised name

        if project_dir.exists():
            print(f"  {RED}{_CH['cross']}{RESET}  '{project_dir}' already exists. Choose a different path.")
            continue

        print(f"\n  Resolved path: {MAGENTA}{project_dir}{RESET}")
        confirm = ask("Create project here? [Y/n]")
        if confirm.lower() in ("", "y", "yes"):
            break
        print("  Re-enter path.")

    create_project_structure(project_dir)
    state = load_state(project_dir)
    state["project_name"] = name
    state["project_dir"] = str(project_dir)
    state["created"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_state(project_dir, state)
    return name, project_dir



# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    cwd = os.getcwd()

    banner([
        "ClaudeAstroVolpert — Astronomy Research Starter",
        "by Carrie Volpert  |  github.com/cvolpert",
        "",
        "Sets up your project directory, then hands off to Claude for",
        "an interactive onboarding session.",
    ])

    # Check for claude CLI before doing any work
    if not _claude_available():
        print(f"  {BYELLOW}{BOLD}Claude Code is not installed (the 'claude' command was not found).{RESET}")
        print()
        info("""\
    Claude Code is required to complete project onboarding. Install it first:

      npm install -g @anthropic-ai/claude-code

    Or see the full installation options at:
      https://docs.anthropic.com/claude-code

    Once installed, re-run this script.
    """)
        sys.exit(1)

    info("""\
    This script will:
      1. Ask where you want your new project directory
      2. Create the full directory structure, copy template files,
         and initialise a git repository
      3. Launch Claude Code in the new project directory

    Claude will then walk you through the rest interactively:
      - Digesting your background literature
      - Organising any existing data or analysis code
      - Customising CLAUDE.md for your specific project
      - Writing your first session log

    You can interrupt with Ctrl-C at any time — the project directory
    will persist and you can open Claude in it manually.
    """)

    pause("Press Enter to begin.")

    project_name, project_dir = step_1_project_name(cwd)

    # Write the onboarding marker that tells Claude to run the setup flow
    marker = Path(project_dir) / ".onboarding_pending"
    marker.write_text(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # Show what was created
    section(_CH["tick"], "PROJECT STRUCTURE CREATED")
    print(f"  {BOLD}{BWHITE}{project_dir.name}/{RESET}")
    for name, desc in TOP_LEVEL_DIRS:
        print(f"  {DIM}{_CH['tee']}{RESET} {CYAN}{name}/{RESET}  {DIM}{desc}{RESET}")
    print(f"  {DIM}{_CH['tee']}{RESET} {BOLD}CLAUDE.md{RESET}            {DIM}— project instructions{RESET}")
    print(f"  {DIM}{_CH['tee']}{RESET} {BOLD}constants.py{RESET}         {DIM}— shared physical constants{RESET}")
    print(f"  {DIM}{_CH['tee']}{RESET} {BOLD}where_I_left_off.md{RESET}  {DIM}— session handoff log{RESET}")
    print(f"  {DIM}{_CH['bend']} .git/ + pre-commit hook  — auto-dates CLAUDE.md on each commit{RESET}")
    print()

    # Last thing before the launch prompt
    print("  Generating project structure, then launching Claude to")
    print("  complete project setup.")
    print()
    print("  After Claude launches, type this in the Claude input line:")
    print()
    print(f"      {BOLD}Read claude.md{RESET}")
    print()
    print("  Claude will then guide you through the rest of setup.")
    print()

    launch_claude(project_dir)


if __name__ == "__main__":
    main()
