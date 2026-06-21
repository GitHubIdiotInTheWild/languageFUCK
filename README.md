# languageFUCK

small experimental repo containing a LOT of random code so i can learn every language (in a basic manner)

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

