# Gemini Coding Agent 🤖

GeminiAgent is an autonomous, lightweight AI coding assistant powered by the Google Gemini API (specifically optimized for models like `gemini-3.1-flash-lite`). It operates seamlessly within your local environment, utilizing function calling to inspect directories, read source code, write or modify files, and execute Python scripts to verify its own solutions.

Instead of relying on heavy abstraction frameworks, it communicates directly with the Gemini REST API, ensuring full control over the protocol, thought signatures, and conversation history.

## ✨ Features

The agent is equipped with a specific set of tools that allow it to act autonomously:
*   **`get_files_info`**: Scans and lists files and directories to understand the project structure.
*   **`get_file_content`**: Reads the content of specified files.
*   **`write_file`**: Creates new files or safely overwrites existing ones (including creating missing parent directories).
*   **`run_python_file`**: Executes Python scripts via the `subprocess` module and captures `STDOUT`/`STDERR`. Used primarily to run tests or verify fixes.

## 🚀 Quick Start

This project uses [`uv`](https://github.com/astral-sh/uv) for fast Python package and environment management.

### 1. Prerequisites
Ensure you have `uv` installed. If not, install it via:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

### 2. Setup
Clone the repository and set up the environment:
```bash
git clone https://github.com/ZieloPL/gemini-coding-agent.git
cd gemini-coding-agent

# Create a virtual environment and install dependencies
uv venv
uv pip install requests python-dotenv
```

### 3. Configuration
The agent requires a Google Gemini API key to function. Create a `.env` file in the root directory and add your key:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Usage
Run the agent by passing your prompt as a CLI argument. You can append `--verbose` to see the internal tool-calling iterations.
```bash
uv run main.py "Your prompt here"
uv run main.py "Explain how the calculator renders the result to the console" --verbose
```

---

## 🎯 Showcase: Fixing a Bug Autonomously

The repository includes a dummy `calculator` project designed as a playground. You can use it to test the agent's reasoning and autonomous execution.

**The Scenario:**
Imagine someone maliciously changed the mathematical operator precedence in the calculator logic. They set the precedence of addition (`+`) to `3` (higher than multiplication), causing basic math to fail.

**The Prompt:**
```bash
uv run main.py "I have a calculator project in the 'calculator' directory. There is a bug where addition is calculated before multiplication in mathematical expressions. Please find the bug, fix it, and run the tests to verify."
```

**The possible Agent's Autonomous Workflow:**
1. Calls `get_files_info` to inspect the `calculator/` directory.
2. Calls `get_file_content` to read `calculator/pkg/calculator.py` and `calculator/tests.py`.
3. Analyzes the code and discovers that `self.precedence["+"]` is incorrectly set to `3`.
4. Calls `write_file` to overwrite `calculator.py` with the corrected precedence logic (`1`).
5. Calls `run_python_file` on `calculator/tests.py` to ensure all unit tests pass.
6. Returns a final text response explaining the fix and the test results.

*Note: The `calculator` is just a demo. You can point the agent to your own projects simply by placing them in the working directory and referencing them in your prompt.*

---

## ⚠️ Security Disclaimer

**Use at your own risk.** 

While basic security constraints have been implemented (e.g., forcing the agent to use strictly relative paths and preventing it from explicitly breaking out of the working directory), this is still an autonomous agent with the ability to write and overwrite files on your disk. 

*   Do **not** run this agent in sensitive directories.
*   Do **not** grant it access to production environments or repositories with uncommitted changes.
*   The agent may hallucinate and modify files you did not intend it to touch. Always use version control (like `git`) so you can easily revert any unwanted changes made by the AI.
