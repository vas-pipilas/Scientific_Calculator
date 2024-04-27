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
        if 'mod' in calculation_str:
            dividend, divisor = calculation_str.split('mod')
            result = str(int(dividend) % int(divisor))
            update_display(calculation_str, result)
        else:
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
    button_labels = ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
                     "ToRAD", "ToDEG"]
    button_commands = [math.sin, math.cos, math.tan, math.asin, math.acos, math.atan, math.sinh, math.cosh, math.tanh,
                       math.asinh, math.acosh, math.atanh, lambda x: x * math.pi / 180, math.degrees]

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
            # add_to_calculation(command(0))  # Pass 0 as the argument for degree/radian conversion
            result = str(command(0))
            update_display(f"{command.__name__}(0)", result)
        else:
            try:
                # Extract the last value from the calculation list and convert it to a float
                value = float(calculation[0]) if calculation else 0
                result = str(command(value))
                update_display(f"{command.__name__}({value})", result)
                # add_to_calculation(command(value))
            except ValueError:
                clear_field()
                update_display(''.join(calculation), "Invalid input. Please enter a valid number.")
    else:  # If command is not a function, it's a value or expression
        add_to_calculation(str(command))


def update_display(calculation, result):
    text_display.delete(1.0, "end")  # Clear the current content
    text_display.insert("end", f"{calculation}\n{result}")


def change_sign():
    global calculation,result
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


def absolute_value():
    global calculation, result
    try:
        # Join the calculation list to form a string expression
        expression = ''.join(calculation)

        # Evaluate the expression
        result = str(eval(expression))

        # Calculate the absolute value of the result
        result = str(abs(float(result)))

        # Update the calculation list with the absolute value action
        calculation = [f"|{expression}|"]

        # Update the display with the absolute value result
        update_display(''.join(calculation), result)
    except ValueError:
        # If the result is not a valid number, display an error message
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        # If there is any other error, clear the field and display an error message
        clear_field()
        update_display("Error occurred while calculating.", "")

def reciprocal():
    global calculation, result
    try:
        # Join the calculation list to form a string expression
        expression = ''.join(calculation)

        # Evaluate the expression
        result = float(eval(expression))

        # Check if x is not equal to zero
        if result != 0:
            # Calculate the reciprocal (1/x) of the result
            result = round(1 / result, 5)
            result = str(result)

            # Update the calculation list with the reciprocal action
            calculation = [f"1/({expression})"]

            # Update the display with the reciprocal result
            update_display(''.join(calculation), result)
        else:
            # If x is zero, display an error message
            clear_field()
            update_display("Error: Division by zero.", "")
    except ValueError:
        # If the result is not a valid number, display an error message
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        # If there is any other error, clear the field and display an error message
        clear_field()
        update_display("Error occurred while calculating.", "")

def square_x():
    global calculation, result
    try:
        # Join the calculation list to form a string expression
        expression = ''.join(calculation)

        # Evaluate the expression
        result = float(eval(expression))

        # Calculate the square of the result
        result = str(round(result ** 2, 5))

        # Update the display with the squared result
        update_display(expression, result)

        calculation.append("**2")
        update_display(''.join(calculation), result)
    except ValueError:
        # If the result is not a valid number, display an error message
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        # If there is any other error, clear the field and display an error message
        clear_field()
        update_display("Error occurred while calculating.", "")

def square_root_x():
    global calculation, result
    try:
        # Join the calculation list to form a string expression
        expression = ''.join(calculation)

        # Evaluate the expression
        result = str(eval(expression))

        # Calculate the square root of the result
        sqrt_result = math.sqrt(float(result))
        sqrt_result = round(sqrt_result, 5)  # Limit result to 5 decimal digits

        # Update the display with the square root result
        update_display(f"sqrt({expression})", str(sqrt_result))
    except ValueError:
        # If the result is not a valid number, display an error message
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        # If there is any other error, clear the field and display an error message
        clear_field()
        update_display("Error occurred while calculating.", "")

def ten_power_x():
    global calculation, result
    try:
        expression = ''.join(calculation)
        num = float(eval(expression))
        result = str(10 ** num)
        calculation = [f"10**{expression}"]
        update_display(''.join(calculation), result)
    except ValueError:
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        clear_field()
        update_display("Error occurred while calculating.", "")

def log_x():
    global calculation, result
    try:
        expression = ''.join(calculation)
        num = float(eval(expression))
        if num > 0:
            result = str(math.log(num))
            calculation = [f"log({expression})"]
            update_display(''.join(calculation), result)
        else:
            clear_field()
            update_display("Invalid input. Please enter a positive number for log.", "")
    except ValueError:
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        clear_field()
        update_display("Error occurred while calculating.", "")

def natural_logarithm_x():
    global calculation, result
    try:
        expression = ''.join(calculation)
        num = float(eval(expression))
        if num > 0:
            result = str(math.log(num))
            calculation = [f"ln({expression})"]
            update_display(''.join(calculation), result)
        else:
            clear_field()
            update_display("Invalid input. Please enter a positive number for ln.", "")
    except ValueError:
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        clear_field()
        update_display("Error occurred while calculating.", "")
def exponential_function_x():
    global calculation, result
    try:
        expression = ''.join(calculation)
        num = float(eval(expression))
        result = str(math.exp(num))
        calculation = [f"exp({expression})"]
        update_display(''.join(calculation), result)
    except ValueError:
        clear_field()
        update_display("Invalid input. Please enter a valid number.", "")
    except:
        clear_field()
        update_display("Error occurred while calculating.", "")

def factorial_x():
    global calculation, result
    try:
        expression = ''.join(calculation)
        num = int(eval(expression))
        if num >= 0:
            result = str(math.factorial(num))
            calculation = [f"!({expression})"]
            if len(result)>20:
                result=result[:20]+"E-99"
            update_display(''.join(calculation), result)
        else:
            clear_field()
            update_display("Invalid input. Please enter a non-negative integer for factorial.", "")
    except ValueError:
        clear_field()
        update_display("Invalid input. Please enter a valid integer.", "")
    except:
        clear_field()
        update_display("Error occurred while calculating.", "")

def clear_last_input():
    global calculation
    if calculation:
        calculation.pop()
        update_display(''.join(calculation), "")
    else:
        clear_field()  # Clear the entire field if calculation list is already empty


def memory_add():
    global memory,result
    try:
        calculation_str = ''.join(calculation)
        num = eval(calculation_str)
        memory += num
        update_display(''.join(calculation), memory)
    except Exception as e:
        print("Error occurred while adding to memory:", e)
def memory_recall():
    global memory, calculation, result
    try:
        calculation_str = ''.join(calculation)
        result = str(memory)  # Update result with the memory value
        update_display(calculation_str, result)
    except Exception as e:
        print("Error occurred while recalling memory:", e)
def memory_subtract():
    global memory,result
    try:
        calculation_str = ''.join(calculation)
        num = eval(calculation_str)
        memory -= num
        update_display(''.join(calculation), memory)
    except Exception as e:
        print("Error occurred while adding to memory:", e)

def memory_store():
    global memory, result
    try:
        calculation_str = ''.join(calculation)
        num = eval(calculation_str)
        memory = num
        update_display(''.join(calculation), memory)
    except Exception as e:
        print("Error occurred while storing memory:", e)

def memory_clear():
    global memory
    memory = 0

calculator = tk.Tk()
calculator.title("Scientific Calculator by PLHPRO Team :) ")
calculator.geometry("620x337")

text_display = tk.Text(calculator, height=2, width=40, font=("Arial", 24))
text_display.grid(columnspan=6)

button_data = [
    ("MC", lambda: memory_clear()), ("MR", lambda: memory_recall()), ("M+", lambda: memory_add()),
    ("M-", lambda: memory_subtract()), ("MS", lambda: memory_store()),
    ("Trigonometry", trigonometry_flyout_window), ("π", lambda: add_to_calculation(round(math.pi, 4))),
    ("e", lambda: add_to_calculation(round(math.e,4))), ("C", clear_field),
    ("<==", lambda: clear_last_input()),
    ("x^2", lambda: square_x()), ("1/x", lambda: reciprocal()),
    ("|x|", lambda: absolute_value()), ("exp", lambda: exponential_function_x()),
    ("mod", lambda: add_to_calculation("mod")),
    ("√x", lambda: square_root_x()), ("(", lambda: add_to_calculation("(")),
    (")", lambda: add_to_calculation(")")), ("!x", lambda: factorial_x()),
    ("/", lambda: add_to_calculation("/")),
    ("x^y", lambda: add_to_calculation("**")), ("7", lambda: add_to_calculation(7)),
    ("8", lambda: add_to_calculation(8)), ("9", lambda: add_to_calculation(9)), ("*", lambda: add_to_calculation("*")),
    ("10^x", lambda: ten_power_x()), ("4", lambda: add_to_calculation(4)),
    ("5", lambda: add_to_calculation(5)), ("6", lambda: add_to_calculation(6)), ("-", lambda: add_to_calculation("-")),
    ("log", lambda: log_x()), ("1", lambda: add_to_calculation(1)),
    ("2", lambda: add_to_calculation(2)), ("3", lambda: add_to_calculation(3)), ("+", lambda: add_to_calculation("+")),
    ("ln", lambda: natural_logarithm_x()), ("+/-", lambda: change_sign()), ("0", lambda: add_to_calculation(0)),
    (".", lambda: add_to_calculation(".")), ("=", evaluate_calculation)
]

for i, (text, command) in enumerate(button_data):
    row = i // 5 + 3
    column = i % 5
    if command:
        tk.Button(calculator, text=text, width=1, font=("Arial", 12), command=command).grid(row=row, column=column,
                                                                                            columnspan=1, sticky="ew")
    else:
        tk.Button(calculator, text=text, width=1, font=("Arial", 12)).grid(row=row, column=column, columnspan=1,
                                                                           sticky="ew")

calculator.mainloop()