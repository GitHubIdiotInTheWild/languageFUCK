# languageFUCK

`languageFUCK` is an experimental playground for learning programming by doing. Instead of building one big app, this repo collects a mix of small, fun projects and language experiments where each file shows a different idea or technique.

The goal is to make it easy to explore language features, GUI design, interpreter ideas, and tooling without having to start from scratch. You’ll find a local AI assistant UI, a Lua adventure game, language notes, and a few quirky demos that help keep the learning process playful.

This repo is designed both as a personal scratchpad and as a lightweight learning resource: use it to test ideas, try out example code, and extend the parts you like.

# languageFUCK's features

## Structure

- `Py/something.py` — dark Tkinter UI for entering an API key selecting a provider and chatting with models
- `Py/iamok.py` — math-based close condition
- ~`Py/openaitesting.py` — example request script for OpenRouter/OpenAI-style APIs~
- `lua/bob.lua` — simple text adventure game written in Lua useful for learning the language
- ~`MD/`~ `does this even count/` — markdown notes and scratch files
- `lua/yes.lua` — i honestly forgot

## Requirements

- Python 3.11 - 3.14
	- `requests` (third-party) — used by `Py/something.py` for HTTP calls
	- `tkinter` / Tcl/Tk (GUI) — usually included with standard Python on Windows/macOS; if missing, install the standard Python distribution from python.org or enable Tcl/Tk support.

- Lua runtime for `lua/bob.lua`

Install Python dependencies:

```powershell
pip install requests
pip install tkinter
pip install socket
```

## Setup

### Python

Install `requests`:

```powershell
py -m pip install requests
```

### Lua

If Lua is not available on `PATH`, run the game with the full executable path:

```powershell
C:\Users\HP\Downloads\lua\lua55.exe lua\bob.lua
```

If you have `lua.exe` on `PATH`, run:

```powershell
lua lua\bob.lua
```

## Usage

### Run the assistant UI

```powershell
py Py\something.py
```

### Run the Lua learning game

```powershell
lua55.exe lua\bob.lua
```

or if `lua` is available:

```powershell
lua lua\bob.lua
```

## Notes

- The assistant supports OpenAI, Anthropic, and OpenRouter providers.
- The Lua game is a beginner-friendly demo that shows tables, functions, and game state.
- Pull new changes after a PR is merged with `git pull`.

