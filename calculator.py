import tkinter as tk
import math
from memory import Memory
from trigonometry import TrigonometryMenu


class Calculator:
    def __init__(self):
        self.calculation = []
        self.result = ""
        self.memory = Memory()
                # Create the main Tkinter window
        self.calculator = tk.Tk()
        self.calculator.title("Scientific Calculator by PLHPRO Team :) ")
        self.calculator.geometry("620x337")
        self.trigonometry_menu = TrigonometryMenu(self.calculator, self)

        # Create and configure the text display widget
        self.text_display = tk.Text(self.calculator, height=2, width=40, font=("Arial", 24))
        self.text_display.grid(columnspan=6)
        
            # Create buttons for various functionalities and configure their commands
        button_data = [
            ("MC", lambda: self.memory_clear()), ("MR", lambda: self.memory_recall()), ("M+", lambda: self.memory_add()),
            ("M-", lambda: self.memory_subtract()), ("MS", lambda: self.memory_store()),
            ("Trigonometry", self.trigonometry_menu.trigonometry_flyout_window), ("π", lambda: self.add_to_calculation(round(math.pi, 4))),
            ("e", lambda: self.add_to_calculation(round(math.e,4))), ("C", self.clear_field),
            ("<==", lambda: self.clear_last_input()),
            ("x^2", lambda: self.square_x()), ("1/x", lambda: self.reciprocal()),
            ("|x|", lambda: self.absolute_value()), ("exp", lambda: self.exponential_function_x()),
            ("mod", lambda: self.add_to_calculation("mod")),
            ("√x", lambda: self.square_root_x()), ("(", lambda: self.add_to_calculation("(")),
            (")", lambda: self.add_to_calculation(")")), ("!x", lambda: self.factorial_x()),
            ("/", lambda: self.add_to_calculation("/")),
            ("x^y", lambda: self.add_to_calculation("**")), ("7", lambda: self.add_to_calculation(7)),
            ("8", lambda: self.add_to_calculation(8)), ("9", lambda: self.add_to_calculation(9)), ("*", lambda: self.add_to_calculation("*")),
            ("10^x", lambda: self.ten_power_x()), ("4", lambda: self.add_to_calculation(4)),
            ("5", lambda: self.add_to_calculation(5)), ("6", lambda: self.add_to_calculation(6)), ("-", lambda: self.add_to_calculation("-")),
            ("log", lambda: self.log_x()), ("1", lambda: self.add_to_calculation(1)),
            ("2", lambda: self.add_to_calculation(2)), ("3", lambda: self.add_to_calculation(3)), ("+", lambda: self.add_to_calculation("+")),
            ("ln", lambda: self.natural_logarithm_x()), ("+/-", lambda: self.change_sign()), ("0", lambda: self.add_to_calculation(0)),
            (".", lambda: self.add_to_calculation(".")), ("=", self.evaluate_calculation)
        ]

        for i, (text, command) in enumerate(button_data):
                row = i // 5 + 3
                column = i % 5
                if command:
                    tk.Button(self.calculator, text=text, width=1, font=("Arial", 12), command=command).grid(row=row, column=column, columnspan=1, sticky="ew")
                else:
                    tk.Button(self.calculator, text=text, width=1, font=("Arial", 12)).grid(row=row, column=column, columnspan=1, sticky="ew")

            # Start the main event loop
            
        # Bind keys for numbers and symbols
        self.calculator.bind("<Key>", self.handle_key_input)
        self.calculator.mainloop()

    def handle_key_input(self, event):
        key = event.char  # Get the character corresponding to the key pressed

        # Check if the key is a digit, a symbol, or special keys
        if key.isdigit() or key in "+-*/().":
            self.add_to_calculation(key)  # Call the method to add the key to the calculation
        elif key == "\r" or key == "\n":  # Enter key
            self.evaluate_calculation()
        elif key == "\x08":  # Backspace key
            self.clear_last_input()
    def add_to_calculation(self, symbol):
        if len(self.result) > 20:
            self.result = "Maximum Length of 20 Digits Reached";
        if len(self.calculation) < 20:
            if callable(symbol):
                # If the symbol is a function, call it with the current text input as its argument
                self.result = str(symbol(self.calculation))
                self.update_display(''.join(self.calculation), self.result)
            else:
                # If the symbol is not a function, append it to the calculation
                self.calculation.append(str(symbol))
                self.update_display(''.join(self.calculation), self.result)
        else:
            self.update_display("3.129E-99", "Maximum Length of 20 Digits Reached")
            self.calculation = []

    def evaluate_calculation(self):
        try:
            calculation_str = ''.join(self.calculation)
            if 'mod' in calculation_str:
                dividend, divisor = calculation_str.split('mod')
                # Convert dividend and divisor to integers
                dividend = int(dividend)
                divisor = int(divisor)
                result = self.calculate_mod(dividend, divisor)
                self.update_display(calculation_str, result)
            else:
                self.result = str(eval(calculation_str))
                # Format the result with commas for better readability
                formatted_result = "{:,}".format(int(self.result))
                self.update_display(calculation_str, formatted_result)
        except:
            self.clear_field()
            self.update_display("ERROR!!", "")


    def calculate_mod(self, dividend, divisor):
        try:
            # Calculate the remainder using the modulo operator (%)
            result = dividend % divisor
            return result
        except ZeroDivisionError:
            # Handle division by zero error
            return "Error: Division by zero"
        except Exception as e:
            # Handle other exceptions
            return f"Error: {e}"
        
    def clear_field(self):
        self.calculation = []
        self.result = ""
        self.update_display("", "")

    def update_display(self, calculation, result):
        self.text_display.delete(1.0, "end")  # Clear the current content
        self.text_display.insert("end", f"{calculation}\n{result}")

    def clear_last_input(self):
        if self.calculation:
            self.calculation.pop()
            self.update_display(''.join(self.calculation), "")
        else:
            self.clear_field()  # Clear the entire field if calculation list is already empty


    def change_sign(self):
        try:
            # Extract the current number from the calculation string
            num_str = ''.join(self.calculation)

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
            self.calculation = [str(num)]

            # Update the display with the modified number
            self.update_display(''.join(self.calculation), "")
        except ValueError:
            # If the input is not a valid number, clear the field and display an error message
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")


    def absolute_value(self):
        try:
            # Join the calculation list to form a string expression
            expression = ''.join(self.calculation)

            # Evaluate the expression
            self.result = str(eval(expression))

            # Calculate the absolute value of the result
            self.result = str(abs(float(self.result)))

            # Update the calculation list with the absolute value action
            self.calculation = [f"|{expression}|"]

            # Update the display with the absolute value result
            self.update_display(''.join(self.calculation), self.result)
        except ValueError:
            # If the result is not a valid number, display an error message
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            # If there is any other error, clear the field and display an error message
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def reciprocal(self):
        try:
            # Join the calculation list to form a string expression
            expression = ''.join(self.calculation)

            # Evaluate the expression
            self.result = float(eval(expression))

            # Check if x is not equal to zero
            if self.result != 0:
                # Calculate the reciprocal (1/x) of the result
                self.result = round(1 / self.result, 5)
                self.result = str(self.result)

                # Update the calculation list with the reciprocal action
                self.calculation = [f"1/({expression})"]

                # Update the display with the reciprocal result
                self.update_display(''.join(self.calculation), self.result)
            else:
                # If x is zero, display an error message
                self.clear_field()
                self.update_display("Error: Division by zero.", "")
        except ValueError:
            # If the result is not a valid number, display an error message
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            # If there is any other error, clear the field and display an error message
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def square_x(self):
        try:
            # Join the calculation list to form a string expression
            expression = ''.join(self.calculation)

            # Evaluate the expression
            self.result = float(eval(expression))

            # Calculate the square of the result
            self.result = str(round(self.result ** 2, 5))

            # Update the display with the squared result
            self.update_display(expression, self.result)

            self.calculation.append("**2")
            self.update_display(''.join(self.calculation), self.result)
        except ValueError:
            # If the result is not a valid number, display an error message
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            # If there is any other error, clear the field and display an error message
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def square_root_x(self):
        try:
            # Join the calculation list to form a string expression
            expression = ''.join(self.calculation)

            # Evaluate the expression
            self.result = str(eval(expression))

            # Calculate the square root of the result
            sqrt_result = math.sqrt(float(self.result))
            sqrt_result = round(sqrt_result, 5)  # Limit result to 5 decimal digits

            # Update the display with the square root result
            self.update_display(f"sqrt({expression})", str(sqrt_result))
        except ValueError:
            # If the result is not a valid number, display an error message
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            # If there is any other error, clear the field and display an error message
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def ten_power_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            self.result = str(10 ** num)
            calculation = [f"10**{expression}"]
            self.update_display(''.join(self.calculation), self.result)
        except ValueError:
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def log_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            if num > 0:
                self.result = str(math.log(num))
                self.calculation = [f"log({expression})"]
                self.update_display(''.join(self.calculation), self.result)
            else:
                self.clear_field()
                self.update_display("Invalid input. Please enter a positive number for log.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def natural_logarithm_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            if num > 0:
                self.result = str(math.log(num))
                self.calculation = [f"ln({expression})"]
                self.update_display(''.join(self.calculation), self.result)
            else:
                self.clear_field()
                self.update_display("Invalid input. Please enter a positive number for ln.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def exponential_function_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            self.result = str(math.exp(num))
            self.calculation = [f"exp({expression})"]
            self.update_display(''.join(self.calculation), self.result)
        except ValueError:
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid number.", "")
        except:
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")

    def factorial_x(self):
        try:
            expression = ''.join(self.calculation)
            num = int(eval(expression))
            if num >= 0:
                self.result = str(math.factorial(num))
                self.calculation = [f"!({expression})"]
                if len(result)>20:
                    result=result[:20]+"E-99"
                self.update_display(''.join(self.calculation), self.result)
            else:
                self.clear_field()
                self.update_display("Invalid input. Please enter a non-negative integer for factorial.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Invalid input. Please enter a valid integer.", "")
        except:
            self.clear_field()
            self.update_display("Error occurred while calculating.", "")


    def memory_add(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = eval(calculation_str)
            self.memory.add(num)
            self.update_display(''.join(self.calculation), self.memory.recall())
        except Exception as e:
            print("Error occurred while adding to memory:", e)

    def memory_recall(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = str(self.memory.recall())
            self.update_display(calculation_str, num)
        except Exception as e:
            print("Error occurred while recalling memory:", e)

    def memory_subtract(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = eval(calculation_str)
            self.memory.subtract(num)
            self.update_display(''.join(self.calculation), self.memory.recall())
        except Exception as e:
            print("Error occurred while subtracting from memory:", e)

    def memory_store(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = eval(calculation_str)
            self.memory.store(num)
            self.update_display(''.join(self.calculation), self.memory.recall())
        except Exception as e:
            print("Error occurred while storing memory:", e)

    def memory_clear(self):
        self.memory.clear()
        self.clear_field()