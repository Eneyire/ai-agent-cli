# AI Agent CLI

A Python command-line AI agent that can inspect and modify files within a configured project workspace, run Python programs, and return a user-facing response. The repository also includes a calculator application used to demonstrate local code execution and agent-driven debugging.

The project highlights practical agent engineering patterns: model-driven tool selection, structured tool schemas, iterative tool execution, conversation history management, bounded agent turns, and focused automated tests.

## Capabilities

- **Tool-calling agent:** Sends a user request and available tool definitions to an OpenRouter model.
- **Workspace tools:** Lists directories, reads file contents, writes files, and runs Python scripts with optional arguments.
- **Iterative execution:** Adds assistant and tool results to the conversation and continues until the model returns a final response, with a 20-iteration limit.
- **Operational visibility:** `--verbose` displays token usage, tool calls, and tool results.
- **Calculator application:** Evaluates arithmetic expressions with operator precedence and nested parentheses, and renders results as JSON.
- **Automated tests:** Pytest coverage exercises calculator behavior and the filesystem and subprocess tools using temporary workspaces.

## Requirements

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/)
- An [OpenRouter](https://openrouter.ai/) API key to run the agent

## Setup

Install the project and development dependencies:

```bash
uv sync
```

Create a `.env` file in the project root and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your-api-key
```

The CLI loads this variable from `.env` at startup. Keep API keys private and do not commit them.

## Run the agent

Pass a request as the positional prompt:

```bash
uv run main.py "Explain how the calculator renders its result"
```

Enable verbose output to inspect token usage and tool activity:

```bash
uv run main.py "List the calculator files and explain the parser" --verbose
```

The agent uses the OpenAI-compatible OpenRouter API with the `openrouter/free` model. Model availability and tool-calling behavior depend on the selected provider and model. The agent stops after 20 model turns if it has not produced a final response.

## Available tools

| Tool               | Purpose                                                                  |
| ------------------ | ------------------------------------------------------------------------ |
| `get_files_info`   | List entries in a directory and report their sizes and directory status. |
| `get_file_content` | Read a file, with a configurable maximum content length.                 |
| `write_file`       | Create or overwrite a file.                                              |
| `run_python_file`  | Run a Python file and capture its output and exit status.                |

The agent supplies `calculator/` as the tools' working directory. Path validation limits the requested target paths to that workspace. **This is not an operating-system sandbox:** Python scripts run as subprocesses with the permissions of the current user, and code inside a script may access resources beyond the selected working directory. Only run the agent in a trusted environment and review code before executing it.

## Calculator

Run the calculator from the project root:

```bash
uv run calculator/main.py "( 3 + 5 ) * 2"
```

Example output:

```json
{
    "expression": "( 3 + 5 ) * 2",
    "result": 16
}
```

The calculator supports addition, subtraction, multiplication, division, operator precedence, and nested parentheses. Invalid expressions and arithmetic errors are reported on the command line.

## Tests

Run the complete test suite from the project root:

```bash
uv run pytest
```

The tests are in `tests/`. Filesystem-related tests use pytest's `tmp_path` fixture to avoid modifying project files.

## Project layout

```text
.
├── calculator/
│   ├── main.py              # Calculator CLI
│   └── pkg/
│       ├── calculator.py    # Expression parsing and evaluation
│       └── render.py        # JSON result formatting
├── functions/               # Agent-callable tools and dispatcher
├── tests/                   # Automated pytest suite
├── config.py                # Tool configuration
├── main.py                  # AI agent CLI and model/tool loop
├── prompts.py               # Agent system prompt
├── pyproject.toml           # Project and dependency configuration
└── uv.lock                  # Locked dependencies
```
