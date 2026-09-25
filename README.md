# AI Agent CLI

A small Python command-line project containing:

- an experimental AI assistant that sends prompts to an OpenRouter model; and
- a standalone calculator application that evaluates basic arithmetic expressions.

The project is still under active development. The calculator is currently the most complete local component, while the AI assistant is a minimal proof of concept.

## Requirements

- Python 3.12 or newer
- [`uv`](https://docs.astral.sh/uv/) (recommended)
- An [OpenRouter](https://openrouter.ai/) API key for the AI assistant

## Setup

Install the project dependencies with `uv`:

```bash
uv sync
```

Create a `.env` file in the project root and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your-api-key
```

The `.env` file is ignored by Git and is loaded automatically when the AI assistant starts.

## AI assistant

Run the assistant from the project root with a prompt as the positional argument:

```bash
uv run python main.py "Explain how this project works"
```

By default, the command prints the model response. Add `--verbose` to include the prompt and token usage:

```bash
uv run python main.py "Suggest a test for the calculator" --verbose
```

The assistant currently uses the `openrouter/free` model through the OpenAI-compatible OpenRouter API. An `OPENROUTER_API_KEY` is required; the command exits with an error if it is not configured.

## Calculator

The calculator accepts space-separated infix expressions and prints the result as formatted JSON:

```bash
cd calculator
python main.py "3 + 5"
```

Output:

```json
{
    "expression": "3 + 5",
    "result": 8
}
```

Supported operators are:

- `+` addition
- `-` subtraction
- `*` multiplication
- `/` division

Multiplication and division take precedence over addition and subtraction. For example:

```bash
python main.py "2 * 3 - 8 / 2 + 5"
```

Expressions must be space-separated. Invalid expressions and arithmetic errors are reported on the command line.

## Tests

Run the calculator unit tests from its directory:

```bash
cd calculator
python -m unittest tests.py
```

The tests cover the four supported operators, operator precedence, nested expressions, empty input, invalid operators, and missing operands.

## Project layout

```text
.
├── main.py                 # AI assistant CLI
├── calculator/
│   ├── main.py             # Calculator CLI
│   ├── tests.py            # Calculator tests
│   └── pkg/
│       ├── calculator.py   # Expression evaluation
│       └── render.py       # JSON output formatting
├── pyproject.toml          # Project metadata and dependencies
└── uv.lock                 # Locked dependency versions
```
