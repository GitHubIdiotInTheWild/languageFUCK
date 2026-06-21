# Contributing to languageFUCK

thanks for helping improve `languageFUCK`! the project is intended to stay small and experimental, but contributions are welcome.

## Getting started

1. fork the repo on GitHub.
2. clone your fork:

```powershell
git clone https://github.com/<your-username>/languageFUCK.git
cd languageFUCK
```

3. Create a branch for your work:

```powershell
git checkout -b my-feature
```

## Install dependencies

### Python

This repo currently uses a Python GUI and a Lua demo.

Install the Python dependencies, which are found in README.md

If `tkinter` is missing, install the standard Python distribution from python.org and enable Tcl/Tk support.

### Lua

To run the Lua demo, you need a working Lua runtime. If `lua` is not on your PATH, use the full executable path.

## Run the project

### Assistant UI

```powershell
py Py\something.py
```

### Lua game

```powershell
lua55.exe lua\bob.lua
```

or if `lua` is available:

```powershell
lua lua\bob.lua
```

## Tests

add tests in a new `tests/` folder and keep them focused on the interpreter core and example execution.

run tests with your chosen test runner once they exist.

## Submitting a PR

1. push your branch to your fork:

```powershell
git push origin my-feature
```

2. Open a pull request against the main repo.
3. Include a short description of what changed and why.
4. If your PR adds a feature or changes behavior, include a short testing summary.

## Notes

- keep changes small and easy to review.
- document any new features or new files in `README.md`.
- if you add new dependencies, update `requirements.txt`.
