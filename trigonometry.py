import tkinter as tk
import math

class TrigonometryMenu:
    def __init__(self, calculator_window, calculator):
        self.calculator = calculator
        self.calculator_window = calculator_window
        self.menu = tk.Menu(self.calculator_window, tearoff=0)
        self.create_menu()

    def create_menu(self):
        button_labels =  [("sin", math.sin, "radians"), ("cos", math.cos, "radians"), 
                         ("tan", math.tan, "radians"), ("asin", math.asin, "degrees"), 
                         ("acos", math.acos, "degrees"), ("atan", math.atan, "degrees"), 
                         ("sinh", math.sinh, "radians"), ("cosh", math.cosh, "radians"), 
                         ("tanh", math.tanh, "radians"), ("asinh", math.asinh, "degrees"), 
                         ("acosh", math.acosh, "degrees"), ("atanh", math.atanh, "degrees"), 
                         ("ToRAD", math.radians, "degrees"), 
                         ("ToDEG", math.degrees, "radians")]

        for label, command, unit in button_labels:
             self.menu.add_command(label=label, command=lambda cmd=command, u=unit: self.handle_trigonometry_command(cmd, u))

    def trigonometry_flyout_window(self):
        self.menu.post(self.calculator_window.winfo_x() + 150, self.calculator_window.winfo_y() + 100)

    def handle_trigonometry_command(self, command, unit):
        try:
            if callable(command):
                result = self.compute_trigonometric_function(command, unit)
                self.update_display(''.join(self.calculator.calculation), result)
            else:
                self.calculator.add_to_calculation(str(command))
        except ValueError:
            self.calculator.clear_field()
            self.calculator.update_display(''.join(self.calculator.calculation), "Μη έγκυρη είσοδος.")
        except Exception as e:
            self.calculator.clear_field()
            self.calculator.update_display("Εμφανίστηκε σφάλμα κατά τον υπολογισμό.", "")

    def compute_trigonometric_function(self, function, unit):
        expression = ''.join(self.calculator.calculation)
        if self.calculator.result or expression:
            cal = self.calculator.result if (self.calculator.result is not None and self.calculator.result != "") else expression
            num = float(eval(cal))
            
            if unit == "radians":
                angle_radians = num * math.pi / 180
            elif unit == "degrees":
                angle_radians = num
            
            result = function(angle_radians)
            self.calculator.result = str(result)
            self.calculator.calculation = [f"{function.__name__}({expression})"]
            return result
        else:
            self.calculator.clear_field()
            self.calculator.update_display("Σφάλμα: Δεν έχει γίνει εισαγωγή.", "")

    def update_display(self, expression, result):
        self.calculator.update_display(expression, str(result))
