import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox
import tkinter.ttk as ttk
import threading
import requests
import json

BACKGROUND = "#121212"
FOREGROUND = "#E0E0E0"
ACCENT = "#5C7AEA"
INPUT_BG = "#1E1E1E"
INPUT_FG = "#FFFFFF"


class ApiKeyPrompt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dark API Key Entry")
        self.configure(bg=BACKGROUND)
        self.state("zoomed")
        self.resizable(False, False)
        self._build_ui()

    def _choose_font(self, size, weight="normal"):
        family = next((f for f in tkfont.families() if "merriweather" in f.lower()), None)
        if family:
            return tkfont.Font(family=family, size=size, weight=weight)
        return tkfont.Font(family="Segoe UI", size=size, weight=weight)

    def _build_ui(self):
        self.columnconfigure(0, weight=1)

        self.header_font = self._choose_font(22, "bold")
        self.body_font = self._choose_font(14)
        self.small_font = self._choose_font(11)
        self.button_font = self._choose_font(13, "bold")

        self.header = tk.Label(
            self,
            text="Welcome",
            fg=FOREGROUND,
            bg=BACKGROUND,
            font=self.header_font
        )
        self.header.grid(row=0, column=0, pady=(20, 8), sticky="n")

        self.subheader = tk.Label(
            self,
            text="Enter your API key to continue",
            fg="#B0B0B0",
            bg=BACKGROUND,
            font=self.body_font
        )
        self.subheader.grid(row=1, column=0, pady=(0, 20), sticky="n")

        self.api_var = tk.StringVar()
        self.input_frame = tk.Frame(self, bg=INPUT_BG, bd=0)
        self.input_frame.grid(row=2, column=0, padx=40, pady=(0, 12), sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        self.api_entry = tk.Entry(
            self.input_frame,
            textvariable=self.api_var,
            font=self.body_font,
            fg=INPUT_FG,
            bg=INPUT_BG,
            insertbackground=INPUT_FG,
            relief="flat",
            bd=0,
            justify="center",
            show="*"
        )
        self.api_entry.grid(row=0, column=0, sticky="ew", ipady=10)
        self.api_entry.focus()

        self.hint = tk.Label(
            self,
            text="Your key is stored only in this session.",
            fg="#7A7A7A",
            bg=BACKGROUND,
            font=self.small_font
        )
        self.hint.grid(row=3, column=0, pady=(0, 16))

        self.submit_button = tk.Button(
            self,
            text="Submit API Key",
            command=self.on_submit,
            fg=FOREGROUND,
            bg=ACCENT,
            activebackground="#4A62D7",
            activeforeground=FOREGROUND,
            font=self.button_font,
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2"
        )
        self.submit_button.grid(row=4, column=0, padx=80, sticky="ew")

        self.status = tk.Label(
            self,
            text="",
            fg="#FF5F5F",
            bg=BACKGROUND,
            font=self.small_font
        )
        self.status.grid(row=5, column=0, pady=(12, 0))
        # Provider selection (OpenAI or Anthropic)
        self.provider_var = tk.StringVar(value="openai")
        prov_frame = tk.Frame(self, bg=BACKGROUND)
        prov_frame.grid(row=6, column=0, pady=(8, 8))
        tk.Radiobutton(prov_frame, text="OpenAI", variable=self.provider_var, value="openai", fg=FOREGROUND, bg=BACKGROUND, selectcolor=BACKGROUND, activebackground=BACKGROUND, font=self.small_font).pack(side="left", padx=8)
        tk.Radiobutton(prov_frame, text="Anthropic", variable=self.provider_var, value="anthropic", fg=FOREGROUND, bg=BACKGROUND, selectcolor=BACKGROUND, activebackground=BACKGROUND, font=self.small_font).pack(side="left", padx=8)

        # Next button
        self.next_button = tk.Button(
            self,
            text="Open Chat",
            command=self.on_submit,
            fg=FOREGROUND,
            bg="#3DA36F",
            activebackground="#2E8A56",
            activeforeground=FOREGROUND,
            font=self.button_font,
            relief="flat",
            bd=0,
            padx=16,
            pady=8,
            cursor="hand2"
        )
        self.next_button.grid(row=7, column=0, padx=120, sticky="ew")

    def on_submit(self):
        key = self.api_var.get().strip()
        if not key:
            self.status.config(text="Please enter a valid API key.")
            return

        provider = self.provider_var.get()
        self.status.config(text="")
        # Open chat window and pass key/provider (kept in memory only)
        ChatWindow(self, api_key=key, provider=provider)
        self.withdraw()


class ChatWindow(tk.Toplevel):
    def __init__(self, parent, api_key, provider="openai"):
        super().__init__(parent)
        self.api_key = api_key
        self.provider = provider
        self.title("AI Coding Assistant")
        self.configure(bg=BACKGROUND)
        self.geometry("900x700")

        # System instruction to always return full code
        self.system_instruction = (
            "You are a coding assistant. When asked to implement or modify code, always return the full, runnable source files or complete code blocks. "
            "Do not reply with partial patches or say 'update this part' — provide the full code and any necessary instructions. Keep answers concise but complete."
        )

        # Chat area
        self.chat_text = tk.Text(self, bg="#0F0F0F", fg=FOREGROUND, insertbackground=FOREGROUND)
        self.chat_text.pack(fill="both", expand=True, padx=12, pady=(12, 6))
        self.chat_text.configure(state="disabled")

        entry_frame = tk.Frame(self, bg=BACKGROUND)
        entry_frame.pack(fill="x", padx=12, pady=(0, 12))

        self.input_entry = tk.Entry(entry_frame, font=self.body_font)
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        buttons_frame = tk.Frame(entry_frame, bg=BACKGROUND)
        buttons_frame.pack(side="right")
        self.send_button = tk.Button(buttons_frame, text="Send", command=self.on_send, bg=ACCENT, fg=FOREGROUND, relief="flat")
        self.send_button.pack(side="left", padx=(0, 6))
        self.make_button = tk.Button(buttons_frame, text="Make", command=self.open_spec_window, bg="#FFB86C", fg=FOREGROUND, relief="flat")
        self.make_button.pack(side="left")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.history = []

    def append_chat(self, speaker, text):
        self.chat_text.configure(state="normal")
        self.chat_text.insert("end", f"{speaker}: {text}\n\n")
        self.chat_text.see("end")
        self.chat_text.configure(state="disabled")

    def on_send(self):
        user_text = self.input_entry.get().strip()
        if not user_text:
            return
        self.input_entry.delete(0, "end")
        self.append_chat("User", user_text)
        threading.Thread(target=self.call_model, args=(user_text,), daemon=True).start()

    def call_model(self, user_text):
        try:
            if self.provider == "openai":
                reply = call_openai_chat(self.api_key, self.system_instruction, user_text)
            else:
                reply = call_anthropic(self.api_key, self.system_instruction, user_text)
        except Exception as e:
            reply = f"Error calling API: {e}"

        self.append_chat("Assistant", reply)

    def on_close(self):
        # destroy and clear any in-memory keys
        self.api_key = None
        self.destroy()

    def open_spec_window(self):
        SpecWindow(self)


def call_openai_chat(api_key, system_instruction, user_text):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_text}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    # adapt to provider response structure
    if "choices" in data and len(data["choices"])>0:
        return data["choices"][0]["message"]["content"].strip()
    return json.dumps(data)


def call_anthropic(api_key, system_instruction, user_text):
    # Example for Anthropic Claude v1; adjust if your account uses a different endpoint or model
    url = "https://api.anthropic.com/v1/complete"
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    prompt = f"{system_instruction}\n\nHuman: {user_text}\n\nAssistant:"
    payload = {
        "model": "claude-2.1",
        "prompt": prompt,
        "max_tokens_to_sample": 2000,
        "temperature": 0.2
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    if "completion" in data:
        return data["completion"].strip()
    # some Anthropic responses use 'completions' array
    if "completions" in data and len(data["completions"])>0:
        return data["completions"][0].get("data", {}).get("text", "").strip()
    return json.dumps(data)


class SpecWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Make - Project Spec")
        self.configure(bg=BACKGROUND)
        self.geometry("700x460")

        lbl = tk.Label(self, text="Describe what you want (include language, files, behavior):", fg=FOREGROUND, bg=BACKGROUND, font=parent.small_font)
        lbl.pack(padx=12, pady=(12, 6), anchor="w")

        self.text = tk.Text(self, height=14, bg="#0F0F0F", fg=FOREGROUND)
        self.text.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        bottom = tk.Frame(self, bg=BACKGROUND)
        bottom.pack(fill="x", padx=12, pady=(0, 12))

        tk.Label(bottom, text="Language:", fg=FOREGROUND, bg=BACKGROUND, font=parent.small_font).pack(side="left")
        self.lang_var = tk.StringVar(value="python")
        lang_menu = ttk.OptionMenu(bottom, self.lang_var, "python", "python", "javascript", "java", "typescript", "lua")
        lang_menu.pack(side="left", padx=(6, 12))

        gen_btn = tk.Button(bottom, text="Generate", command=self.on_generate, bg=ACCENT, fg=FOREGROUND, relief="flat")
        gen_btn.pack(side="right")

    def on_generate(self):
        spec = self.text.get("1.0", "end").strip()
        lang = self.lang_var.get()
        if not spec:
            messagebox.showinfo("Empty spec", "Please write what you want.")
            return
        prompt = f"Generate a complete, runnable {lang} project. Provide full source files and any instructions. Spec:\n{spec}"
        self.parent.append_chat("User", f"[Make] {spec}")
        threading.Thread(target=self.parent.call_model, args=(prompt,), daemon=True).start()
        self.destroy()


if __name__ == "__main__":
    app = ApiKeyPrompt()
    app.mainloop()
