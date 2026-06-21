import math
import re
import tkinter as tk

root = tk.Tk()
root.title("iamok")
root.geometry("320x180")
root.resizable(False, False)

label = tk.Label(root, text="i am ok", font=("Arial", 18), pady=20)
label.pack()

entry = tk.Entry(root, justify="center")
entry.pack(pady=10)

status = tk.Label(root, text="type a math equation with pi", fg="gray")
status.pack()


def is_pi_equation(text):
    text = text.strip().lower()
    if "pi" not in text or "=" not in text:
        return False

    parts = text.split("=")
    if len(parts) != 2:
        return False

    left, right = parts[0].strip(), parts[1].strip()
    if not left or not right:
        return False

    if "pi" in right:
        return False

    left = left.replace("^", "**")
    right = right.replace("^", "**")
    allowed_left = {"pi": math.pi}

    try:
        left_value = eval(left, {"__builtins__": None}, allowed_left)
        right_value = eval(right, {"__builtins__": None}, {})
    except Exception:
        return False

    if not isinstance(left_value, (int, float)) or not isinstance(right_value, (int, float)):
        return False

    # Accept approximate values like 3.14 for pi, or 4.14 for pi + 1
    return abs(left_value - right_value) < 0.01


def on_type(event=None):
    text = entry.get().strip().lower()
    if text == "":
        status.config(text="type a math equation with pi")
    elif is_pi_equation(text):
        label.config(text="that's smart enough")
        status.config(text="closing...")
        root.after(1000, root.destroy)
    else:
        status.config(text="wrong answer")

entry.bind("<KeyRelease>", on_type)
root.mainloop()
