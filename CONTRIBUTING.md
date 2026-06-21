# Contributing to languageFUCK

Thanks for helping improve `languageFUCK`! This repo is a lightweight playground for learning and experimenting, so keep contributions small, clear, and easy to understand.

## Getting started

1. Fork the repo on GitHub.
2. Clone your fork locally:

```powershell
git clone https://github.com/<your-username>/languageFUCK.git
cd languageFUCK
```

3. Create a new branch for your work:

```powershell
git checkout -b feature/my-feature-name
```

4. Keep your branch focused on one change at a time.

## Installing dependencies

### Python

Install Python dependencies from README.md

If `tkinter` is missing, install the standard Python distribution from python.org and enable Tcl/Tk support. The GUI requires `tkinter`, and the project also depends on `requests`.

### Lua

To run the Lua demo, install a Lua runtime. If `lua` is not on your PATH, use the full executable path like:

```powershell
C:\Users\HP\Downloads\lua\lua55.exe lua\bob.lua
```

## Running the project

### Assistant UI

```powershell
py Py\something.py
```

### Lua game

```powershell
lua55.exe lua\bob.lua
```

or if `lua` is available on PATH:

```powershell
lua lua\bob.lua
```

## Testing

This project should have unit and integration tests under a `tests/` folder. When adding tests:

- keep them focused and repeatable
- prefer pure Python unit tests for interpreter core behavior
- add integration tests for example programs and expected output
- include edge cases such as pointer bounds, invalid instructions, and I/O behavior

If no test runner is installed yet, use a simple Python framework like `pytest`.

## Code style

- Use consistent indentation and formatting.
- Keep changes readable and avoid needless complexity.
- If you add formatting tooling, document it in `README.md`.

## Submitting a PR

1. Push your branch to your fork:

```powershell
git push origin feature/my-feature-name
```

2. Open a pull request against the main repository.
3. Write a clear PR title and description.
4. Explain what changed, why it changed, and how to verify it.
5. Mention any manual testing performed.

## What to include

- code changes in small, logical chunks
- tests for any new or changed behavior
- README updates for new features or dependencies
- updates to `requirements.txt` if you add Python packages

## Notes

- Keep PRs small and reviewable.
- If you add new files, explain their purpose.
- If you fix bugs, include a short reproduction case in the PR description.
- If you add new dependencies, prefer minimal installations and document them clearly.
