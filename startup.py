#!/usr/bin/env python3
# Created: 2026-05-29 00:00:00
# Last Modified: 2026-05-29 12:00:00
# Description: Interactive setup script for a new Claude-assisted astronomy research
#   project. Walks the user through project creation, directory structure setup,
#   and onboarding to Claude Code. For AI-assisted steps (literature digest, data
#   sorting, code sorting), the script prints exact prompts to paste into Claude.
# Last Edit: Fix banner/info wrapping bugs; add ANSI color coding throughout.

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
from pathlib import Path
from datetime import datetime

# ─── Terminal width ────────────────────────────────────────────────────────────
try:
    COLS = os.get_terminal_size().columns
except OSError:
    COLS = 80
COLS = min(max(COLS, 40), 100)  # clamp to [40, 100] to avoid edge cases


# ─── ANSI colour codes ────────────────────────────────────────────────────────
# Used to enable/disable colour if stdout is not a tty (e.g. piped to a file).
_USE_COLOR = sys.stdout.isatty()

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
    print()
    print(f"{BYELLOW}{BOLD}  {'─' * (COLS - 4)}{RESET}")
    print(f"  {BOLD}{BYELLOW}► TELL CLAUDE:{RESET}")
    print(f"{BYELLOW}{BOLD}  {'─' * (COLS - 4)}{RESET}")
    for line in prompt_text.strip().split("\n"):
        for wline in textwrap.wrap(line.strip(), width) or [""]:
            print(f"  {BWHITE}{wline}{RESET}")
    print(f"{BYELLOW}{BOLD}  {'─' * (COLS - 4)}{RESET}")
    print()


def pause(msg="Press Enter when ready to continue..."):
    print(f"\n  {BGREEN}▶{RESET}  {msg}")
    try:
        input("     ")
    except KeyboardInterrupt:
        print("\n\nSetup interrupted. Re-run startup.py to resume.")
        sys.exit(0)


def ask(prompt, default=None):
    if default:
        full_prompt = f"  {GREEN}▶{RESET}  {prompt} [{default}]: "
    else:
        full_prompt = f"  {GREEN}▶{RESET}  {prompt}: "
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
    docs_src = PACKAGE_DIR / "docs" / "claude_command_dict.md"
    docs_dst = project_dir / "Background" / "claude_command_dict.md"
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

    print(f"  {BGREEN}✓{RESET}  {BOLD}Project directory created:{RESET} {MAGENTA}{project_dir}{RESET}")
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
            print(f"  {RED}✗{RESET}  Please enter a path.")
            continue

        # Expand ~ and any env vars, then resolve to absolute
        project_dir = Path(os.path.expandvars(raw)).expanduser().resolve()
        name = project_dir.name.replace(" ", "_")
        project_dir = project_dir.parent / name  # sanitised name

        if project_dir.exists():
            print(f"  {RED}✗{RESET}  '{project_dir}' already exists. Choose a different path.")
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


def step_2_background_literature(project_dir, project_name):
    section(2, "BACKGROUND LITERATURE")

    info("""\
    Claude works best when it understands your scientific context. The Background/
    directory is where you store papers, review articles, and any reference material
    relevant to this project.

    After you add files there, Claude will read them and create a compressed summary
    document (Background/project_background_summary.md). It will consult this
    document at the start of every future session — so it always has your project's
    scientific context fresh in memory.

    Accepted formats: PDF, plain text, Markdown, or simply paste abstracts/key
    passages into .txt files. You can also add a file called 'my_notes.txt' with
    your own context about the project goals.
    """)

    pause(f"Add relevant papers and notes to  {project_dir}/Background/\n"
          "     Then press Enter when you are ready for Claude to digest them.")

    # Check if any files were actually added
    bg_dir = Path(project_dir) / "Background"
    bg_files = [f for f in bg_dir.rglob("*")
                if f.is_file() and f.name not in (".gitkeep", "claude_command_dict.md")]

    if not bg_files:
        info("""\
    No files found in Background/ yet. That is okay — you can skip this step now
    and run it later by telling Claude:

        "Please read everything in Background/ and create a project background
         summary document at Background/project_background_summary.md. Update
         CLAUDE.md to point to it."
    """)
        pause("Press Enter to continue to the next step.")
        return

    info(f"  Found {len(bg_files)} file(s) in Background/. Now tell Claude:")

    claude_prompt_box("LITERATURE DIGEST",
        f"Please read all files in the Background/ directory of this project "
        f"({project_name}). Create a structured summary document at "
        f"Background/project_background_summary.md that captures: (1) the key "
        f"scientific context and motivation for this project, (2) the most "
        f"important observational and theoretical results from the literature, "
        f"(3) key physical reference values (distances, typical parameter ranges, "
        f"etc.) I should remember as sanity-check anchors, and (4) the open "
        f"questions this project aims to address. Then update CLAUDE.md to "
        f"include a pointer to this file so you review it at the start of each "
        f"session. Finally, show me the summary and ask if I want to add, edit, "
        f"or remove anything.")

    pause("After Claude has created the background summary, press Enter to continue.")


def step_3_command_dictionary(project_dir):
    section(3, "CLAUDE REFERENCE: MODELS, TOKENS, AND COMMANDS")

    info("""\
    A reference document called 'claude_command_dict.md' has been placed in your
    Background/ directory. It covers:

      • Context windows — what they are and why they matter
      • Input and output tokens — how they are counted and what they cost
      • Claude models (Opus, Sonnet, Haiku) — capabilities, speeds, and costs
      • Key slash commands — /model, /clear, /compact, /cost, /plan, /memory
      • Resuming and switching between conversations
      • Checking usage and switching between plans
      • Custom agents and sub-agents

    Take a few minutes to read through it. It will save you a lot of confusion
    later. You can always find it at:
    """)
    print(f"    {MAGENTA}{project_dir}/Background/claude_command_dict.md{RESET}")
    print()

    pause("Press Enter when you are ready to continue.")


def step_4_data(project_dir, project_name):
    section(4, "DATA INVENTORY")

    info("""\
    The Data/ directory is for your observational data: raw cubes, reduced images,
    catalogues, ancillary maps, model grids, calibration files, etc.

    IMPORTANT: Data/ is listed in .gitignore and should NEVER be committed to git.
    Observational data is large, sometimes proprietary, and belongs in local storage
    or a dedicated archive — not in your code repository.

    After you add your data files, Claude will review what is there, create
    subdirectories organised by data type, move the files into the right places,
    and print a summary of what is where and why.
    """)

    pause(f"Add your data files to  {project_dir}/Data/\n"
          "     (or any subdirectory within Data/). Press Enter when done.")

    data_files = [f for f in (Path(project_dir) / "Data").rglob("*")
                  if f.is_file() and f.name != ".gitkeep"]

    if not data_files:
        info("""\
    No data files found in Data/ yet. You can do this step later by telling Claude:

        "Please review everything in Data/, organise it into subdirectories by
         data type (raw, reduced, auxiliary, models, etc.), and summarise what
         is where and what each dataset is."
    """)
        pause("Press Enter to continue.")
        return

    info(f"  Found {len(data_files)} file(s) in Data/. Now tell Claude:")

    claude_prompt_box("DATA ORGANISATION",
        f"Please review all files currently in the Data/ directory of the "
        f"{project_name} project. Organise them into logical subdirectories "
        f"by data type (e.g. Raw/, Reduced/, Auxiliary/, Models/, Catalogues/). "
        f"Create those subdirectories and move the files. Then write a brief "
        f"summary at Data/descriptions/data_inventory.md listing what each "
        f"dataset is, what format it is in, what instrument or pipeline produced "
        f"it, and where I can find it. Print the summary for me.")

    pause("After Claude organises the data, press Enter to continue.")


def step_5_existing_code(project_dir, project_name):
    section(5, "EXISTING ANALYSIS CODE")

    info("""\
    If you have existing analysis scripts or notebooks you want to bring into this
    project, add them to Analysis/ now. Claude will review them, group them by
    function, create appropriate subdirectories, move the files, and summarise the
    analysis pipeline you already have.

    If you are starting fresh with no existing code, just press Enter to skip.
    """)

    pause(f"Add any existing scripts to  {project_dir}/Analysis/\n"
          "     Press Enter when done (or just Enter to skip).")

    ana_files = [f for f in (Path(project_dir) / "Analysis").rglob("*")
                 if f.is_file() and f.name not in (".gitkeep",)
                 and ".git" not in f.parts]

    if not ana_files:
        info("  No code files added — skipping automatic organisation.")
        pause("Press Enter to continue.")
        return

    info(f"  Found {len(ana_files)} file(s) in Analysis/. Now tell Claude:")

    claude_prompt_box("CODE ORGANISATION",
        f"Please review all files in Analysis/ for the {project_name} project. "
        f"Group them by function (e.g. data reduction, cube preparation, spectral "
        f"fitting, structure finding, visualisation utilities) and create "
        f"appropriate subdirectories. Move the files into the right places. "
        f"For each file, add or update the four-line file header (Created, "
        f"Last Modified, Description, Last Edit) following the format in CLAUDE.md. "
        f"Then print a summary of what the analysis pipeline looks like now and "
        f"what each script does.")

    pause("After Claude organises the code, press Enter to continue.")


def step_6_directory_summary(project_dir):
    section(6, "YOUR PROJECT DIRECTORY STRUCTURE")

    info("""\
    Here is the full structure you now have. Each top-level directory has a specific
    role — Claude understands and respects this layout by default.
    """)

    print(f"  {BOLD}{BWHITE}{Path(project_dir).name}/{RESET}")
    for name, desc in TOP_LEVEL_DIRS:
        print(f"  {DIM}├──{RESET} {CYAN}{name}/{RESET}")
        print(f"  {DIM}│     {desc}{RESET}")
    print(f"  {DIM}├──{RESET} {BOLD}CLAUDE.md{RESET}           {DIM}— Claude's project instructions (edit this){RESET}")
    print(f"  {DIM}├──{RESET} {BOLD}constants.py{RESET}        {DIM}— Shared physical constants (import everywhere){RESET}")
    print(f"  {DIM}├──{RESET} {BOLD}where_I_left_off.md{RESET} {DIM}— Session handoff log (auto-updated by Claude){RESET}")
    print(f"  {DIM}└── .gitignore          — Data/ and scratch files excluded from git{RESET}")
    print()

    info("""\
    Within Analysis/, Visualizations/, and Data/, there are three special
    subdirectories — described in the next step.
    """)
    pause("Press Enter to continue.")


def step_7_metadata_subdirs(project_dir):
    section(7, "THE tests/, debug/, AND descriptions/ SYSTEM")

    info("""\
    Three special subdirectories appear inside Analysis/, Visualizations/, and
    Data/. They keep the pipeline clean and make it easy to find things later.

    tests/
      ALL new Python scripts start here. Claude will never put an untested script
      directly in a pipeline subdirectory. Once you are satisfied a script works,
      you tell Claude to move it to the appropriate subdirectory (e.g.
      Analysis/SpectralFitting/). This prevents accidental execution of unvetted
      code and keeps the main pipeline directories clean.

    debug/
      Debugging scripts, intermediate diagnostic outputs, temporary result files,
      and anything that helps you investigate a problem but is not part of the
      final pipeline. Claude deposits scratch work here automatically.

    descriptions/
      All documentation for code files lives here — NOT next to the code itself.
      This means .md, .tex, .pdf files describing what a script does, its inputs
      and outputs, key assumptions, and motivation. Named like:
      'spectral_fitting_method_info.md'. Claude generates these automatically for
      finalised analysis steps.

    What you need to do:
      • When Claude writes new code, it lands in tests/ — you review and test it.
      • When you are happy with a script, tell Claude: "Move X from tests/ to the
        appropriate subdirectory."
      • When you finalise an analysis step, tell Claude: "Document this in
        descriptions/." Claude's Scribe agent will create a LaTeX/PDF summary.
    """)
    pause("Press Enter to continue.")


def step_8_session_files(project_dir):
    section(8, "CLAUDE.md AND where_I_left_off.md")

    info("""\
    CLAUDE.md — The project instruction file
      This is the most important file in the project. Claude reads it at the start
      of EVERY conversation. It tells Claude:
        • Who you are and what this project is about
        • The project's scientific context (via a pointer to the background summary)
        • Your coding conventions and file organisation rules
        • Which sub-agents to use and when
        • Physical sanity check anchors for this specific project

      Open CLAUDE.md now and read through it. In Step 10 you will customise it.
      Whenever the project evolves significantly — new data, new methods, major
      results — update CLAUDE.md so Claude always has current context.

    where_I_left_off.md — The session handoff log
      Claude updates this at the end of every working session (or when you ask
      it to wrap up). It records:
        • What was completed in the session
        • Which files were edited and what changed
        • QA findings (sub-agent results that led to changes)
        • The ordered list of next steps

      When you start a new Claude session, Claude reads this file and picks up
      exactly where you left off — no re-explaining needed. You can also read
      it yourself to quickly remember where things stand.

      The template at where_I_left_off.md shows the expected format.
    """)
    pause("Press Enter to continue.")


def step_9_agents(project_dir):
    section(9, "CUSTOM AGENTS AND SUB-AGENTS")

    info("""\
    Claude Code supports specialised sub-agents — separate Claude instances
    optimised for specific tasks, with restricted tool access so they cannot
    accidentally modify files outside their scope.

    Your CLAUDE.md describes five pre-configured sub-agents:

      Art Critic     — Reviews plots and figures for formatting quality and
                       physical plausibility. Cannot modify files.

      Physics Cop    — Sanity-checks numerical results: units, order-of-magnitude
                       estimates, physical parameter ranges. Cannot modify files.

      Scribe         — Writes LaTeX documentation for finalised analysis steps.
                       Only touches descriptions/ subdirectories.

      Code Cop       — Reviews new Python scripts before you run them: checks
                       headers, PEP 8, FITS pitfalls, memory issues. Run this
                       before any major fitting job.

      Librarian      — Searches NASA ADS / arXiv for references, returns BibTeX,
                       and verifies that a specific value actually appears in a
                       cited paper. Manages your Publication/ms.bib file.

    To use a sub-agent, tell Claude (the main agent):
      "Run Art Critic on the figure at Visualizations/moment0_HI.png"
      "Ask Physics Cop to check these column density results."
      "Have Scribe document the spectral fitting method."

    Pros of sub-agents:
      • Specialised focus — they know exactly what to check for their domain
      • Protected — they cannot accidentally delete or overwrite important files
      • Parallelisable — Claude can run multiple sub-agents in one session
      • Transparent — their findings are logged in where_I_left_off.md

    Cons / caveats:
      • Each sub-agent starts with a fresh context window — it does not have
        the full conversation history. You must give it enough context in the
        invocation prompt.
      • Sub-agents cannot call each other. The main agent is the broker.
      • They incur additional token cost (though sub-agents use cheaper models
        where possible — Haiku for Scribe and Librarian).
      • Art Critic cannot read FITS files — always render a PNG first.

    You can add or modify sub-agents by editing the YAML files in .claude/agents/
    (created automatically by Claude when you set up a new agent). The CLAUDE.md
    template explains the structure.
    """)
    pause("Press Enter to continue.")


def step_10_claude_md_review(project_dir, project_name):
    section(10, "REVIEW AND CUSTOMISE CLAUDE.md")

    info("""\
    The final step is to read through CLAUDE.md and customise it for your project.
    Claude will guide you through this interactively — asking about your project
    goals, computational environment, preferred workflows, and whether you want to
    add any custom sub-agents.

    After this session, CLAUDE.md will be tailored to you. Every future Claude
    session in this directory will start with Claude reading it and knowing your
    project's specifics.

    Tell Claude:
    """)

    claude_prompt_box("CLAUDE.md CUSTOMISATION",
        f"Please guide me through customising the CLAUDE.md file for my new "
        f"project '{project_name}'. Walk through it section by section and ask "
        f"me the relevant questions: (1) my name and research role, (2) the "
        f"specific scientific goals of this project, (3) my operating system and "
        f"shell (run 'uname -a' and 'echo $SHELL' to find these), (4) any compute "
        f"cluster or HPC resources I use regularly, (5) the primary data types "
        f"and instruments for this project, (6) any specific physical parameter "
        f"ranges, distances, or reference values I want the Physics Cop to use "
        f"as sanity-check anchors, and (7) whether I want to add or modify any "
        f"sub-agents beyond the five defaults. Then update CLAUDE.md with my "
        f"answers and show me the revised version.")

    pause("After Claude finishes the CLAUDE.md review, press Enter for a final summary.")


def final_summary(project_dir, project_name):
    section("✓", "SETUP COMPLETE")

    info(f"""\
    Your project '{project_name}' is ready. Here is a quick reference:

    Starting a new Claude session:
      cd {project_dir}
      claude

    Claude will read CLAUDE.md and where_I_left_off.md automatically.

    Ending a session:
      Tell Claude: "Please wrap up and update where_I_left_off.md."

    Key files to keep updated:
      CLAUDE.md          — update when project scope or methods evolve significantly
      constants.py       — add project-specific constants as you determine them
      where_I_left_off.md — Claude updates this; you can also edit it manually

    Next steps (in rough order of priority):
      1. Add your literature to Background/ and run the literature digest (Step 2)
         if you skipped it.
      2. Add your data to Data/ and run the data organisation step (Step 4).
      3. Start your first real Claude session and tell it about your science goals.
      4. Read claude_command_dict.md (in Background/) for a full reference on
         Claude models, token costs, and key commands.

    Good luck with the research!
    """)
    print(f"{BCYAN}{BOLD}{'=' * COLS}{RESET}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    cwd = os.getcwd()

    banner([
        "ClaudeAstroVolpert — Astronomy Research Starter",
        "by Carrie Volpert  |  github.com/cvolpert",
        "",
        "Interactive project setup for Claude Code users.",
        "This script will walk you through setting up a new Claude-assisted",
        "research project with a standard directory structure, configuration",
        "files, and onboarding to Claude Code best practices.",
    ])

    info("""\
    You will be asked to:
      1.  Choose a project name and create the directory structure
      2.  Add background literature for Claude to digest
      3.  Learn about Claude models, tokens, and key commands
      4.  Add your data files for automatic organisation
      5.  Add any existing code for automatic organisation
      6–9. Receive walkthroughs of the directory structure, workflow conventions,
           and sub-agents
      10. Customise CLAUDE.md for your specific project

    Steps that require Claude's assistance (2, 4, 5, 10) will give you an
    exact prompt to paste into your Claude Code session.

    You can interrupt with Ctrl-C at any time — the project directory will
    persist and you can continue later.
    """)

    pause("Press Enter to begin.")

    # Step 1: project name and structure
    project_name, project_dir = step_1_project_name(cwd)

    # Steps 2–10
    step_2_background_literature(project_dir, project_name)
    step_3_command_dictionary(project_dir)
    step_4_data(project_dir, project_name)
    step_5_existing_code(project_dir, project_name)
    step_6_directory_summary(project_dir)
    step_7_metadata_subdirs(project_dir)
    step_8_session_files(project_dir)
    step_9_agents(project_dir)
    step_10_claude_md_review(project_dir, project_name)
    final_summary(project_dir, project_name)


if __name__ == "__main__":
    main()
