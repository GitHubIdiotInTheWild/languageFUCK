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
    if "pi" not in text:
        return False
    if not re.search(r"[0-9pi]\s*[-+*/^]\s*[0-9pi]", text):
        return False

    expression = text.replace("^", "**")
    allowed = {"pi": math.pi}
    try:
        result = eval(expression, {"__builtins__": None}, allowed)
    except Exception:
        return False

    return isinstance(result, (int, float))


def on_type(event=None):
    text = entry.get().strip().lower()
    if is_pi_equation(text):
        label.config(text="that's smart enough")
        status.config(text="closing...")
        root.after(1000, root.destroy)
    elif text == "":
        status.config(text="type a math equation with pi")
    else:
        status.config(text="not smart enough yet")

entry.bind("<KeyRelease>", on_type)
root.mainloop()
