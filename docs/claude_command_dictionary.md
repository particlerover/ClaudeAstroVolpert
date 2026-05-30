# Claude Code — Reference Dictionary for Astronomers

*A practical reference for using Claude Code in scientific research.*
*This document lives in your project's Background/ directory for easy access.*

---

## Table of Contents

1. [What is Claude Code?](#1-what-is-claude-code)
2. [Context Windows and Why They Matter](#2-context-windows-and-why-they-matter)
3. [Input and Output Tokens](#3-input-and-output-tokens)
4. [Claude Models — Capabilities and Costs](#4-claude-models--capabilities-and-costs)
5. [Starting and Resuming Conversations](#5-starting-and-resuming-conversations)
6. [Switching Models Mid-Conversation](#6-switching-models-mid-conversation)
7. [Checking Usage and Costs](#7-checking-usage-and-costs)
8. [Usage Plans and Limits](#8-usage-plans-and-limits)
9. [Key Slash Commands](#9-key-slash-commands)
10. [Custom Agents and Sub-Agents](#10-custom-agents-and-sub-agents)
11. [CLAUDE.md and Project Memory](#11-claudemd-and-project-memory)
12. [Practical Workflow Tips for Astronomy](#12-practical-workflow-tips-for-astronomy)

---

## 1. What is Claude Code?

Claude Code is Anthropic's command-line interface (CLI) for interacting with Claude in a software development and research context. Unlike the web chat interface (claude.ai), Claude Code:

- Runs in your terminal, where your files and code already live
- Can read, write, and edit files directly (with your permission for each action)
- Can run shell commands (grep, python, git, SLURM, etc.)
- Reads a project-specific instruction file (`CLAUDE.md`) at the start of each session
- Maintains a persistent memory system across sessions
- Supports custom sub-agents for specialised tasks

**Starting Claude Code:**
```bash
cd /path/to/your/project
claude
```

Claude will read `CLAUDE.md` and `where_I_left_off.md` automatically and start with full project context.

**Exiting:**
Type `/exit` or press `Ctrl-C` twice. Claude will prompt you to save context in `where_I_left_off.md` if you ask it to wrap up first.

---

## 2. Context Windows and Why They Matter

The **context window** is the total amount of text Claude can see at once — your messages, its replies, any files it has read, the contents of CLAUDE.md, and the conversation history. Think of it as working memory: everything within it is immediately accessible; everything outside it is not.

**Why this matters for research:**

- Long conversations with many file reads can fill the context window. When it fills, Claude either starts to "forget" earlier content (compression) or the session must be restarted.
- Large FITS headers, long Python scripts, or pasting extensive data outputs all consume context quickly.
- CLAUDE.md and `where_I_left_off.md` are read at session start and consume context — keep them concise and information-dense.

**Context window sizes by model** (as of mid-2026; check Anthropic's website for current values):

| Model | Context Window | Notes |
|-------|---------------|-------|
| Claude Opus 4 | 200K tokens | ~150,000 words |
| Claude Sonnet 4 | 200K tokens | Same window, lower cost |
| Claude Haiku 4 | 200K tokens | Fastest, cheapest |

**Managing context:**
- `/compact` — Claude compresses the conversation history, freeing space while retaining key facts
- `/clear` — Clears the entire conversation and starts fresh (use when pivoting to a completely new task)
- Start a new session for each major task if sessions are getting long

---

## 3. Input and Output Tokens

Tokens are the basic unit of text Claude processes. Roughly:
- **1 token ≈ 0.75 words** (English text)
- **1 token ≈ 3–4 characters**
- A 10-page paper (PDF text) ≈ 5,000–8,000 tokens
- A 500-line Python script ≈ 3,000–5,000 tokens
- This entire reference document ≈ 4,000 tokens

**Input tokens** are everything Claude reads in a session:
- Your messages
- Claude's previous responses (conversation history)
- Files Claude reads (`Read` tool)
- `CLAUDE.md` contents (read at session start)
- `where_I_left_off.md` (read at session start)
- Sub-agent system prompts
- Results from Bash commands

**Output tokens** are Claude's responses:
- Text responses
- Code it writes
- File edits (which are transmitted as diffs)

**Cost:** Input tokens cost less than output tokens (roughly 3–5× cheaper depending on model). Long files Claude reads are input-token heavy; long code Claude writes is output-token heavy. For most research workflows, input dominates.

**Check your usage:** `/cost` shows the token count and estimated cost for the current session.

---

## 4. Claude Models — Capabilities and Costs

Three model tiers are available. Switch with `/model` at any time.

### Claude Opus 4 — Maximum capability
**Best for:**
- Complex multi-step analysis planning
- Reasoning through novel scientific problems
- Writing/editing manuscript sections
- Debugging subtle logic errors in analysis pipelines
- Tasks where quality matters more than speed or cost

**Characteristics:**
- Most capable; best reasoning and scientific understanding
- Slowest response time (~2–5× slower than Sonnet)
- Most expensive (~5–10× Sonnet per token)
- Use for your most demanding tasks

### Claude Sonnet 4 — Best all-around (recommended default)
**Best for:**
- Day-to-day coding and analysis work
- Reviewing and editing existing scripts
- Running sub-agents (Art Critic, Physics Cop, Code Cop)
- Literature searches (Librarian sub-agent)
- Most tasks where Haiku might lack depth

**Characteristics:**
- Strong capability, much faster than Opus
- Moderate cost — the sweet spot for most research workflows
- This is Claude Code's default model

### Claude Haiku 4 — Speed and cost
**Best for:**
- Simple, well-defined tasks (format a table, rename variables, grep for a pattern)
- Documentation generation (Scribe sub-agent uses Haiku)
- Citation lookups (Librarian sub-agent uses Haiku)
- Quick summaries of output files

**Characteristics:**
- Fastest response time
- Lowest cost (~10–20× cheaper than Opus)
- Less capable on complex reasoning or novel problems

### Cost comparison (approximate, per million tokens):

| Model | Input | Output |
|-------|-------|--------|
| Haiku 4 | $0.80 | $4 |
| Sonnet 4 | $3 | $15 |
| Opus 4 | $15 | $75 |

*Actual costs: check console.anthropic.com for current pricing. These figures are approximate and change with Anthropic's pricing updates.*

**Rule of thumb for astronomy research:**
- Default to Sonnet 4 for most sessions
- Switch to Opus 4 when you need deep reasoning (planning a novel analysis method, debugging a subtle statistical issue, writing a methods section from scratch)
- Switch to Haiku 4 for repetitive or simple tasks (batch summarising, formatting, trivial edits)

---

## 5. Starting and Resuming Conversations

### Starting a new session
```bash
cd /path/to/your/project
claude
```

### Resuming a recent conversation
Claude Code keeps a conversation history on your machine. To resume:
```bash
claude --resume     # shows recent conversations to pick from
claude --resume <conversation-id>   # resumes a specific conversation
```

Or, within Claude Code, you can switch between conversations with:
- `/conversations` — list recent conversations
- Select from the list to resume

**Best practice for astronomy research:** Rather than resuming old conversations (which may have stale context), start fresh sessions and rely on `where_I_left_off.md` for continuity. Tell Claude at session start:

> "Please read where_I_left_off.md and Background/project_background_summary.md, then tell me where we are and what the immediate next step is."

### Multiple projects
Each project directory has its own `CLAUDE.md`. Claude reads the `CLAUDE.md` of whichever directory you launch `claude` from. You can have as many independent Claude projects as you like — just `cd` to the right directory before starting.

---

## 6. Switching Models Mid-Conversation

Switch the active model at any point in a session:

```
/model                  # shows available models and current selection
/model opus             # switch to Claude Opus 4
/model sonnet           # switch to Claude Sonnet 4
/model haiku            # switch to Claude Haiku 4
```

Or use the full model ID:
```
/model claude-opus-4-8
/model claude-sonnet-4-6
/model claude-haiku-4-5
```

**When to switch:**
- Start on Sonnet, switch to Opus when you hit a hard problem
- Switch to Haiku for a batch of simple formatting tasks, then back to Sonnet

---

## 7. Checking Usage and Costs

**Current session:**
```
/cost       # shows input tokens, output tokens, and estimated cost
```

**Account-level usage:**
Log in to `console.anthropic.com` → Usage dashboard. Shows:
- Monthly token consumption by model
- Cost breakdown
- Rate limit status

**Monitoring in real time:**
Claude Code shows a running token count in the status bar (if using the desktop app or IDE extension). In the CLI, use `/cost` periodically during long sessions.

---

## 8. Usage Plans and Limits

### Claude.ai plans (for web + Claude Code)

**Pro plan (~$20/month):**
- Includes Claude Code access
- Higher usage limits than free tier
- Access to Opus, Sonnet, and Haiku
- Good for individual research use

**Team plan (~$25–30/user/month):**
- Higher limits than Pro
- Shared billing for research groups
- Priority access during high-demand periods

**API / pay-as-you-go:**
- No monthly fee — pay per token
- Best if usage is sporadic or you want granular cost control
- Access through `console.anthropic.com` → API keys
- Claude Code can use API keys directly: set `ANTHROPIC_API_KEY` in your environment

**Switching between plans:**
Log in at `anthropic.com` → Account settings. Changes take effect immediately.

**Usage limits:**
- Pro/Team plans have daily and monthly usage limits that reset on a schedule
- If you hit a limit, Claude will notify you; usage resets within hours to a day
- API usage has no hard cap — you set your own spending limits in the console

**For research groups:**
Consider the Team plan or an API key with a shared project budget. This avoids one user exhausting the shared limit.

---

## 9. Key Slash Commands

These are typed directly in the Claude Code prompt.

### Conversation control
| Command | What it does |
|---------|-------------|
| `/clear` | Clear conversation history — start fresh context |
| `/compact` | Compress conversation to save context while retaining key facts |
| `/exit` | End the Claude Code session |
| `/conversations` | List and switch between recent conversations |

### Model and configuration
| Command | What it does |
|---------|-------------|
| `/model` | Show and change the active Claude model |
| `/model sonnet` / `/model opus` / `/model haiku` | Switch to that model |
| `/config` | Open configuration settings (API keys, permissions, theme) |

### Usage and monitoring
| Command | What it does |
|---------|-------------|
| `/cost` | Show token usage and estimated cost for this session |
| `/status` | Show the current model, context usage, and session info |

### Memory and context
| Command | What it does |
|---------|-------------|
| `/memory` | View Claude's persistent memory entries |
| `/memory add <text>` | Add a memory that persists across sessions |
| `/memory clear` | Remove all memory entries |

### Planning and tasks
| Command | What it does |
|---------|-------------|
| `/plan` | Enter planning mode — Claude thinks through an approach before acting |
| `/tasks` | View and manage the current task list |

### Agents and skills
| Command | What it does |
|---------|-------------|
| `@agent-<Name>` | Invoke a specific sub-agent (e.g. `@agent-Art_Critic`) |
| `/code-review` | Run a code review on changed files |
| `/code-review ultra` | Deep multi-agent cloud review of the current branch |

### Files and git
| Command | What it does |
|---------|-------------|
| `/diff` | Show the current git diff |
| `/undo` | Undo the last file change Claude made |

### Help
| Command | What it does |
|---------|-------------|
| `/help` | Show all available commands |
| `!<command>` | Run a shell command directly (e.g. `!ls Data/Raw/`) |

---

## 10. Custom Agents and Sub-Agents

Claude Code supports specialised sub-agents — separate Claude instances with defined system prompts and restricted tool access. They cannot accidentally modify files outside their allowed scope.

**Your project's default sub-agents** (defined in `CLAUDE.md` and set up by Claude in `.claude/agents/`):

| Agent | Model | Purpose |
|-------|-------|---------|
| Art Critic | Sonnet | Visual QA for plots and figures |
| Physics Cop | Sonnet | Physical sanity checks on numerical results |
| Scribe | Haiku | LaTeX documentation for finalised methods |
| Code Cop | Sonnet | Pre-run code review for Python scripts |
| Librarian | Haiku | NASA ADS / arXiv citation lookup and BibTeX |

**Invoking a sub-agent:**
Tell the main Claude agent to use one:
> "Please ask the Art Critic to review the figure at Visualizations/moment_map.png"
> "Run Code Cop on Analysis/tests/new_fitting_script.py before I run it"
> "Have Physics Cop check these column density results: [paste results]"

**Creating a new sub-agent:**
Tell Claude:
> "Please create a new sub-agent called [Name] with the following purpose: [description]. It should be able to use these tools: [list]. It should NOT be able to modify files."

Claude will create the YAML definition in `.claude/agents/` and update `CLAUDE.md`.

**Pros:**
- Specialised focus and domain knowledge per agent
- Protected by tool restrictions — cannot cause collateral damage
- Can run in parallel within one session
- Use cheaper models where depth is not needed (Haiku for Scribe, Librarian)
- Findings are logged in `where_I_left_off.md` under QA Findings

**Cons:**
- Each sub-agent starts with no conversation history — you must give it sufficient context in the invocation prompt
- Sub-agents cannot call each other; the main agent brokers all communication
- Additional token cost (sub-agents have their own context windows)
- Art Critic cannot read FITS files; always render a PNG first

---

## 11. CLAUDE.md and Project Memory

### CLAUDE.md
The single most important file in the project. Claude reads it at the start of every conversation. It tells Claude:
- Who you are and what this project is about
- The scientific context (via the background summary pointer)
- Coding conventions, file organisation rules, naming conventions
- Which sub-agents to use and when
- Physical sanity check reference values for this specific project

**Keep it updated.** When you adopt a new analysis method, determine a key physical parameter, or significantly change the project scope, update `CLAUDE.md`. It takes a few tokens at session start but saves you from re-explaining context every time.

**Edit it directly** (it is just a Markdown file) or tell Claude:
> "Please update the Project Overview section of CLAUDE.md to reflect [new information]."

### Claude's persistent memory
Separate from `CLAUDE.md`, Claude Code maintains a file-based memory system (in `~/.claude/projects/.../memory/`). This is for:
- Your preferences and workflow style
- Feedback Claude has received (what approaches work, what to avoid)
- Cross-session facts about the project that are not in `CLAUDE.md`

Claude manages this automatically. You can view it with `/memory` or ask:
> "What do you remember about my preferences for this project?"

**Rule of thumb:** `CLAUDE.md` is for project-level instructions (shared, version-controlled); Claude's memory is for personal preferences and session-to-session continuity (local, automatic).

---

## 12. Practical Workflow Tips for Astronomy

### Starting a session efficiently
```
"Read where_I_left_off.md and the background summary, then tell me the
 immediate next step and ask if I want to proceed."
```

### Managing large data files
- Never paste raw FITS data or large array contents into the conversation
- Tell Claude to read FITS headers specifically: "Read the FITS header of Data/Raw/mycube.fits"
- Use `!python3 -c "from astropy.io import fits; fits.info('file.fits')"` for quick inspection

### Running long jobs
For long RADEX grids, SLURM jobs, or overnight fits:
> "I am about to submit a long SLURM job. Please write the submission script,
>  check it with Code Cop, then update where_I_left_off.md with what the job
>  does and what output files to expect."

### Keeping sessions focused
- One major task per session works better than jumping between unrelated things
- If you need to pivot: `/compact` first to save context, then pivot
- Use `/plan` before any complex multi-file change to get Claude to lay out the approach before touching anything

### When Claude seems confused
- Clear symptoms: repeating itself, contradicting earlier statements, misremembering file locations
- Solution: `/compact` (preserves key facts, discards stale dialogue) or `/clear` + start fresh
- Then start with: "Please read CLAUDE.md and where_I_left_off.md and summarise your understanding of the current state."

### Working with plots
Always render figures before asking Art Critic:
```python
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for remote/CLI use
import matplotlib.pyplot as plt
# ... your plot ...
plt.savefig('Visualizations/debug/moment0_check.png', dpi=150, bbox_inches='tight')
```
Then: "Please ask Art Critic to review Visualizations/debug/moment0_check.png."

### Version control for code
Tell Claude to commit at logical stopping points:
> "Please commit the changes to Analysis/SpectralFitting/ with a descriptive message."

Claude will stage the files, write a commit message referencing what changed and why, and run the commit. **It will not push unless you explicitly ask.**

### Quick sanity checks without sub-agents
For quick checks that don't warrant invoking Physics Cop:
> "Before I use this result, do a quick OOM check: I got a CO column density
>  of 3×10²⁰ cm⁻² for a 10 km/s linewidth GMC at 1 kpc. Does this make sense?"

Claude will do the check inline. Use Physics Cop for formal vetting of results going into the paper.
