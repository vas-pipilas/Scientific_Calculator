import tkinter as tk
import math

calculation = []
result = ""  # Define result globally
memory = 0  # Initialize memory
trigonometry_menu = None

def add_to_calculation(symbol):
    global calculation, result
    if len(result) > 20:
        result = "Maximum Length of 20 Digits Reached";
    if len(calculation) < 20:
        if callable(symbol):
            # If the symbol is a function, call it with the current text input as its argument
            result = str(symbol(calculation))
            update_display(''.join(calculation), result)
        else:
            # If the symbol is not a function, append it to the calculation
            calculation.append(str(symbol))
            update_display(''.join(calculation), result)
    else:
        update_display("3.129E-99", "Maximum Length of 20 Digits Reached")
        calculation = []

def evaluate_calculation():
    global calculation, result
    try:
        calculation_str = ''.join(calculation)
        result = str(eval(calculation_str))
        update_display(calculation_str, result)
    except:
        clear_field()
        update_display("ERROR!!", "")

def clear_field():
    global calculation, result
    calculation = []
    result = ""
    update_display("", "")


def trigonometry_flyout_window():
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
    global calculation, result
    if callable(command):  # If command is a function, call it directly
        if command.__name__ == "ToRAD" or command.__name__ == "ToDEG":
            #add_to_calculation(command(0))  # Pass 0 as the argument for degree/radian conversion
            result = str(command(0))  
            update_display(f"{command.__name__}(0)", result)
        else:
            try:
                # Extract the last value from the calculation list and convert it to a float
                value = float(calculation[0]) if calculation else 0
                result = str(command(value))
                update_display(f"{command.__name__}({value})", result)
                #add_to_calculation(command(value))
            except ValueError:
                 clear_field()
                 update_display(''.join(calculation), "Invalid input. Please enter a valid number.")
    else:  # If command is not a function, it's a value or expression
        add_to_calculation(str(command))


def update_display(calculation, result):
    text_display.delete(1.0, "end")  # Clear the current content
    text_display.insert("end", f"{calculation}\n{result}") 

def change_sign():
    global calculation
    try:
        # Extract the current number from the calculation string
        num_str = ''.join(calculation)
        
        # Convert the current number to a float
        num = float(num_str)
        
        # Check if the number is an integer
        is_integer = num.is_integer()
        
        # Change the sign of the number
        num = -num if num >= 0 else abs(num)
        
        # Convert the number back to an integer if it was originally an integer
        if is_integer:
            num = int(num)
        
        # Update the calculation list with the new number
        calculation = [str(num)]
        
        # Update the display with the modified number
        update_display(''.join(calculation), "")
    except ValueError:
        # If the input is not a valid number, clear the field and display an error message
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")

def memory_add():
    global memory
    memory += float(result) if result else 0

def memory_subtract():
    global memory
    memory -= float(result) if result else 0

calculator = tk.Tk()
calculator.title("Scientific Calculator by PLHPRO Team :) ")
calculator.geometry("620x337")

text_display = tk.Text(calculator, height=2, width=40, font=("Arial", 24))
text_display.grid(columnspan=6)

button_data = [
    ("MC", lambda: clear_field()), ("MR", lambda: clear_field()), ("M+", lambda: memory_add()), 
    ("M-", lambda: memory_subtract()), ("MS", lambda: clear_field()), 
    ("Trigonometry", trigonometry_flyout_window), ("π", lambda: add_to_calculation(math.pi)), 
    ("e", lambda: add_to_calculation("e")), ("C", clear_field), ("<==", lambda: calculation.pop() if calculation else None),
    ("x2", lambda: add_to_calculation("x2")), ("1/x", lambda: add_to_calculation("1/x")),
    ("|x|", lambda: add_to_calculation("|x|")), ("exp", lambda: add_to_calculation("exp")), ("mod", lambda: add_to_calculation("mod")),
    ("√x", lambda: add_to_calculation("√x")), ("(", lambda: add_to_calculation("(")), 
    (")", lambda: add_to_calculation(")")), ("!x", lambda: add_to_calculation("!x")), ("/", lambda: add_to_calculation("/")),
    ("x^y", lambda: add_to_calculation("^")), ("7", lambda: add_to_calculation(7)), 
    ("8", lambda: add_to_calculation(8)),("9", lambda: add_to_calculation(9)), ("*", lambda: add_to_calculation("*")),
    ("10^x", lambda: add_to_calculation("10^x")), ("4", lambda: add_to_calculation(4)), 
    ("5", lambda: add_to_calculation(5)), ("6", lambda: add_to_calculation(6)), ("-", lambda: add_to_calculation("-")),
    ("log", lambda: add_to_calculation("log")),("1", lambda: add_to_calculation(1)),
    ("2", lambda: add_to_calculation(2)), ("3", lambda: add_to_calculation(3)), ("+", lambda: add_to_calculation("+")),
    ("ln", lambda: add_to_calculation("ln")), ("+/-", lambda: change_sign()), ("0", lambda: add_to_calculation(0)), 
    (".", lambda: add_to_calculation(".")), ("=", evaluate_calculation)
]

for i, (text, command) in enumerate(button_data):
    row = i // 5 + 3
    column = i % 5
    if command:
        tk.Button(calculator, text=text, width=1, font=("Arial", 12), command=command).grid(row=row, column=column, columnspan=1, sticky="ew")
    else:
        tk.Button(calculator, text=text, width=1, font=("Arial", 12)).grid(row=row, column=column, columnspan=1, sticky="ew")

calculator.mainloop()
