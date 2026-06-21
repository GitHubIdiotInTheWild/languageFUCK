import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox

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

        self.columnconfigure(0, weight=1)

        self.header = tk.Label(
            self,
            text="Welcome",
            fg=FOREGROUND,
            bg=BACKGROUND,
            font=("Merriweather", 22, "bold") if "Merriweather" in tkfont.families() else ("Segoe UI", 22, "bold")
        )
        self.header.grid(row=0, column=0, pady=(20, 8), sticky="n")

        self.subheader = tk.Label(
            self,
            text="Enter your API key to continue",
            fg="#B0B0B0",
            bg=BACKGROUND,
            font=("Merriweather", 14) if "Merriweather" in tkfont.families() else ("Segoe UI", 14)
        )
        self.subheader.grid(row=1, column=0, pady=(0, 20), sticky="n")

        self.api_var = tk.StringVar()
        self.input_frame = tk.Frame(self, bg=INPUT_BG, bd=0)
        self.input_frame.grid(row=2, column=0, padx=40, pady=(0, 12), sticky="ew")
        self.input_frame.columnconfigure(0, weight=1)

        self.api_entry = tk.Entry(
            self.input_frame,
            textvariable=self.api_var,
            font=("Merriweather", 14) if "Merriweather" in tk.font.families() else ("Segoe UI", 14),
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
            font=("Merriweather", 11) if "Merriweather" in tk.font.families() else ("Segoe UI", 11)
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
            font=("Merriweather", 13, "bold") if "Merriweather" in tk.font.families() else ("Segoe UI", 13, "bold"),
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
            font=("Merriweather", 11) if "Merriweather" in tk.font.families() else ("Segoe UI", 11)
        )
        self.status.grid(row=5, column=0, pady=(12, 0))

    def on_submit(self):
        key = self.api_var.get().strip()
        if not key:
            self.status.config(text="Please enter a valid API key.")
            return

        self.status.config(text="")
        messagebox.showinfo("API Key Accepted", "API key saved. You can now continue.")
        self.destroy()


if __name__ == "__main__":
    app = ApiKeyPrompt()
    app.mainloop()
