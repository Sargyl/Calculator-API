import math
import tkinter as tk
from tkinter import messagebox

history = []

def check_integer(num):
    return isinstance(num, int) or (isinstance(num, float) and num.is_integer())

def append_char(char):
    current = display_var.get()
    display_var.set(current + str(char))

def clear_display():
    display_var.set("")
    result_var.set("Результат: ")

def calculate(op):
    try:
        expr = display_var.get()
        if not expr:
            return
        
        if op in ["+", "-", "*", "/", "^"]:
            parts = expr.split(op)
            if len(parts) == 2 and parts[0] and parts[1]:
                a = float(parts[0])
                b = float(parts[1])
            else:
                return
        else:
            a = float(expr)
            b = 0.0

        if op == "+":
            res = a + b
        elif op == "-":
            res = a - b
        elif op == "*":
            res = a * b
        elif op == "/":
            if b == 0:
                messagebox.showerror("Ошибка", "Деление на ноль")
                return
            res = a / b
        elif op == "^":
            res = a ** b
        elif op == "sqrt":
            if a < 0:
                messagebox.showerror("Ошибка", "Корень из отрицательного числа")
                return
            res = math.sqrt(a)
        elif op == "fact":
            if a < 0 or not check_integer(a):
                messagebox.showerror("Ошибка", "Факториал только для целых >= 0")
                return
            if a > 100:
                messagebox.showerror("Ошибка", "Слишком большое число")
                return
            res = math.factorial(int(a))
        else:
            return

        result_var.set(f"Результат: {res}")
        history.append(f"{expr} = {res}")
        text_history.delete("1.0", tk.END)
        text_history.insert(tk.END, "\n".join(history[-5:]))
        
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат ввода")

root = tk.Tk()
root.title("Калькулятор")
root.geometry("320x500")
root.config(bg="#8b0000")

display_var = tk.StringVar()
result_var = tk.StringVar(value="Результат: ")

display = tk.Entry(root, textvariable=display_var, font=("Arial", 16), justify="right")
display.pack(fill=tk.X, padx=15, pady=15)

res_label = tk.Label(root, textvariable=result_var, bg="#8b0000", fg="white", font=("Arial", 12, "bold"))
res_label.pack(pady=5)

btn_frame = tk.Frame(root, bg="#8b0000")
btn_frame.pack(pady=10)

buttons = [
    [("C", clear_display), ("\u221a", lambda: append_char("sqrt")), ("!", lambda: append_char("fact")), ("/", lambda: append_char("/"))],
    [("7", lambda: append_char("7")), ("8", lambda: append_char("8")), ("9", lambda: append_char("9")), ("*", lambda: append_char("*"))],
    [("4", lambda: append_char("4")), ("5", lambda: append_char("5")), ("6", lambda: append_char("6")), ("-", lambda: append_char("-"))],
    [("1", lambda: append_char("1")), ("2", lambda: append_char("2")), ("3", lambda: append_char("3")), ("+", lambda: append_char("+"))],
    [("0", lambda: append_char("0")), (".", lambda: append_char(".")), ("^", lambda: append_char("^")), ("=", lambda: calculate(display_var.get()[-1] if display_var.get() and display_var.get()[-1] in "+-*/^" else "+"))]
]

for row_idx, row in enumerate(buttons):
    for col_idx, (text, cmd) in enumerate(row):
        btn = tk.Button(btn_frame, text=text, width=6, height=2, font=("Arial", 10, "bold"), command=cmd)
        btn.grid(row=row_idx, column=col_idx, padx=3, pady=3)

tk.Label(root, text="История вычислений:", bg="#8b0000", fg="white").pack(anchor="w", padx=15)
text_history = tk.Text(root, height=5, width=35)
text_history.pack(padx=15, pady=5)

root.mainloop()