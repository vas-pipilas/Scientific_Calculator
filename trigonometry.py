import tkinter as tk
import math

class TrigonometryMenu:
    def __init__(self, calculator_window, calculator):
        self.calculator = calculator
        self.calculator_window = calculator_window
        self.menu = tk.Menu(self.calculator_window, tearoff=0)
        self.create_menu()

    def create_menu(self):
        # Define the labels and corresponding commands for each button
        button_labels = ["sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh",
                         "ToRAD", "ToDEG"]
        button_commands = [math.sin, math.cos, math.tan, math.asin, math.acos, math.atan, math.sinh, math.cosh, math.tanh,
                           math.asinh, math.acosh, math.atanh, lambda x: x * math.pi / 180, math.degrees]

        # Add buttons to the menu in a grid layout
        for label, command in zip(button_labels, button_commands):
            self.menu.add_command(label=label, command=lambda cmd=command: self.handle_trigonometry_command(cmd))

    def trigonometry_flyout_window(self):
        self.menu.post(self.calculator_window.winfo_x() + 150, self.calculator_window.winfo_y() + 100)

    def handle_trigonometry_command(self, command):
        try:
            # Extract the last value from the calculation list and convert it to a float
            value = float(self.calculator.calculation[0]) if self.calculator.calculation else 0
            result = ""
            if callable(command):  # If command is a function, call it directly
                if command.__name__ == "ToRAD" or command.__name__ == "ToDEG":
                    result = str(command(0))
                    self.calculator.result = result
                    self.calculator.update_display(f"{command.__name__}(0)", result)
                else:
                    result = str(command(value))
                    self.calculator.update_display(f"{command.__name__}({value})", result)
            else:  # If command is not a function, it's a value or expression
                self.calculator.add_to_calculation(str(command))
        except ValueError:
            self.calculator.clear_field()
            self.calculator.update_display(''.join(self.calculator.calculation), "Invalid input. Please enter a valid number.")
