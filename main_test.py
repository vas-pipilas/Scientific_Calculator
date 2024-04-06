import tkinter as tk
import math

calculation = []
trigonometry_menu = None

def add_to_calculation(symbol):
    global calculation
    if text_result.get(1.0, "end").strip() == "Maximum Length of 20 Digits Reached":
        text_result.delete(1.0, "end")
    if len(calculation) < 20:
        if callable(symbol):
            # If the symbol is a function, call it with the current text input as its argument
            result = symbol(calculation)
            text_result.delete(1.0, "end")
            text_result.insert(1.0, result)
        else:
            # If the symbol is not a function, append it to the calculation
            calculation += str(symbol)
            text_calculation.delete(1.0, "end")
            text_calculation.insert(1.0, calculation)
    else:
        text_calculation.insert(1.0, "3.129E-99")
        text_result.insert(1.0, "Maximum Length of 20 Digits Reached")
        calculation = []

def evaluate_calculation():
    global calculation
    try:
        calculation_str = ''.join(calculation)
        calculation = str(eval(calculation_str))
        text_result.delete(1.0, "end")
        text_result.insert(1.0, calculation)
    except:
        clear_field()
        text_calculation.insert(1.0, "ERROR!!")

def clear_field():
    global calculation
    calculation = []
    text_calculation.delete(1.0, "end")


def trigonometry_popup_window():
    global trigonometry_menu
    trigonometry_menu = tk.Menu(calculator, tearoff=0)

    # Define the labels and corresponding commands for each button
    button_labels = ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh", "ToRAD", "ToDEG"]
    button_commands = [math.sin, math.cos, math.tan, math.asin, math.acos, math.atan, math.sinh, math.cosh, math.tanh, math.asinh, math.acosh, math.atanh, lambda x: x * math.pi / 180, math.degrees]

    # Add buttons to the menu in a grid layout
    row = 0
    col = 0
    for label, command in zip(button_labels, button_commands):
        trigonometry_menu.add_command(label=label, command=lambda cmd=command: handle_trigonometry_command(cmd))

    # Add the menu to the calculator window at a fixed position
    trigonometry_menu.post(calculator.winfo_x() + 150, calculator.winfo_y() + 100)

def handle_trigonometry_command(command):
    if callable(command):  # If command is a function, call it directly
        if command.__name__ == "ToRAD" or command.__name__ == "ToDEG":
            add_to_calculation(command(0))  # Pass 0 as the argument for degree/radian conversion
        else:
            try:
                # Extract the last value from the calculation list and convert it to a float
                value = float(calculation[0]) if calculation else 0
                add_to_calculation(command(value))
            except ValueError:
                print("Invalid input. Please enter a valid number.")
    else:  # If command is not a function, it's a value or expression
        add_to_calculation(str(command))

calculator = tk.Tk()
calculator.title("Scientific Calculator by PLHPRO Team :) ")
calculator.geometry("735x400")

text_calculation = tk.Text(calculator, height=1, width=40, font=("Arial", 24))
text_calculation.pack(fill="both", expand=True)
text_calculation.grid(columnspan=6)

text_result = tk.Text(calculator, height=1, width=40, font=("Arial", 24))
text_result.grid(columnspan=6)

button_data = [
    ("MC", lambda: clear_field()), ("MR", lambda: clear_field()),
    ("M+", lambda: clear_field()), ("M-", lambda: clear_field()),
    ("MS", lambda: clear_field()), ("Trigonometry", trigonometry_popup_window),
    ("π", lambda: add_to_calculation(math.pi)), ("e", lambda: add_to_calculation("e")),
    ("C", clear_field), ("<==", lambda: calculation.pop() if calculation else None),
    ("x2", lambda: add_to_calculation("x2")), ("1/x", lambda: add_to_calculation("1/x")),
    ("|x|", lambda: add_to_calculation("|x|")), ("mod", lambda: add_to_calculation("mod")),
    ("√x", lambda: add_to_calculation("√x")), ("(", lambda: add_to_calculation("(")),
    (")", lambda: add_to_calculation(")")), ("!x", lambda: add_to_calculation("!x")),
    ("/", lambda: add_to_calculation("/")), ("x^y", lambda: add_to_calculation("^")),
    ("7", lambda: add_to_calculation("7")), ("8", lambda: add_to_calculation("8")),
    ("9", lambda: add_to_calculation("9")), ("*", lambda: add_to_calculation("*")),
    ("4", lambda: add_to_calculation("4")), ("5", lambda: add_to_calculation("5")),
    ("6", lambda: add_to_calculation("6")), ("-", lambda: add_to_calculation("-")),
    ("log", lambda: add_to_calculation("log")), ("1", lambda: add_to_calculation("1")),
    ("2", lambda: add_to_calculation("2")), ("3", lambda: add_to_calculation("3")),
    ("+", lambda: add_to_calculation("+")), ("ln", lambda: add_to_calculation("ln")),
    ("+/-", None), ("0", lambda: add_to_calculation("0")), (".", lambda: add_to_calculation(".")),
    ("=", evaluate_calculation)
]

for i, (text, command) in enumerate(button_data):
    row = i // 5 + 3
    column = i % 5
    if command:
        tk.Button(calculator, text=text, width=1, font=("Arial", 12), command=command).grid(row=row, column=column, columnspan=1, sticky="ew")
    else:
        tk.Button(calculator, text=text, width=1, font=("Arial", 12)).grid(row=row, column=column, columnspan=1, sticky="ew")

calculator.mainloop()
