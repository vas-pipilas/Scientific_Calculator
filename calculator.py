import tkinter as tk
from math import *
from memory import Memory
from trigonometry import TrigonometryMenu

class Calculator:
    def __init__(self):
        self.calculation = []
        self.result = ""
        self.memory = Memory()

        self.calculator = tk.Tk()
        self.calculator.title("Επιστημονικός Υπολογιστής από την ομάδα PLHPRO :) ")
        self.calculator.configure(background="gray26") 
        self.trigonometry_menu = TrigonometryMenu(self.calculator, self)

        self.text_display = tk.Text(self.calculator, height=2, width=40, font=("Arial", 24), bg="gray26", fg="white") 
        self.text_display.grid(row=0, column=0, columnspan=5)
        self.calculator.resizable(False, False)

        button_padx = 5
        button_pady = 5
        button_width = self.text_display.winfo_width() // 5  # Adjust according to the number of columns
        button_height = self.text_display.winfo_height()


        button_data = [
            ("MC", lambda: self.memory_clear()), ("MR", lambda: self.memory_recall()), ("M+", lambda: self.memory_add()),
            ("M-", lambda: self.memory_subtract()), ("MS", lambda: self.memory_store()),
            ("Τριγωνομετρία", self.trigonometry_menu.trigonometry_flyout_window), ("π", lambda: self.add_to_calculation(round(pi, 4))),
            ("e", lambda: self.add_to_calculation(round(e, 4))), ("C", self.clear_field),
            ("AC", lambda: self.clear_last_input_and_memory()),
            ("1⁄x", lambda: self.reciprocal()),
            ("|x|", lambda: self.absolute_value()), ("exp", lambda: self.exponential_function_x()),
            ("mod", lambda: self.add_to_calculation("mod")),("<==", lambda: self.clear_last_input()),
            ("x²", lambda: self.square_x()), ("(", lambda: self.add_to_calculation("(")),
            (")", lambda: self.add_to_calculation(")")), ("n!", lambda: self.factorial_x()),
            ("/", lambda: self.add_to_calculation("/")),
            ("x^y", lambda: self.add_to_calculation("**")), ("7", lambda: self.add_to_calculation(7)),
            ("8", lambda: self.add_to_calculation(8)), ("9", lambda: self.add_to_calculation(9)), ("*", lambda: self.add_to_calculation("*")),
            ("10ⁿ", lambda: self.ten_power_x()), ("4", lambda: self.add_to_calculation(4)),
            ("5", lambda: self.add_to_calculation(5)), ("6", lambda: self.add_to_calculation(6)), ("-", lambda: self.add_to_calculation("-")),
            ("log", lambda: self.log_x()), ("1", lambda: self.add_to_calculation(1)),
            ("2", lambda: self.add_to_calculation(2)), ("3", lambda: self.add_to_calculation(3)), ("+", lambda: self.add_to_calculation("+")),
            ("ln", lambda: self.natural_logarithm_x()), ("+/-", lambda: self.change_sign()), ("0", lambda: self.add_to_calculation(0)),
            (".", lambda: self.add_to_calculation(".")), ("=", self.evaluate_calculation) ,
            ("√x", lambda: self.square_root_x()),("n√x", lambda: self.add_to_calculation("root"))
        ]

        for i, (text, command) in enumerate(button_data):
            row = i // 5 + 3
            column = i % 5
            button_bg_color = "gray56" if str(text).isdigit() else "gray36"
            button_relief = "raised" if command else "flat"
            if command:
                tk.Button(self.calculator, text=text, width=button_width, height=button_height, font=("Arial", 12), 
                        command=command, bg=button_bg_color, fg="white", bd=0, borderwidth=1, relief=button_relief, padx=button_padx, pady=button_pady).grid(row=row, column=column, columnspan=1, padx=1, pady=1, sticky="nsew")
            else:
                tk.Button(self.calculator, text=text, width=button_width, height=button_height, font=("Arial", 12),
                        bg=button_bg_color, fg="white", bd=0, borderwidth=1, relief=button_relief, padx=button_padx, pady=button_pady).grid(row=row, column=column, columnspan=1, padx=1, pady=1, sticky="nsew")

        
        total_button_height = button_height * (len(button_data) - 1) 
        total_padding_height = button_pady * ((len(button_data) - 1)) // 5
        window_height = total_button_height * ((len(button_data) - 1) // 5 + 2) + total_padding_height

        self.calculator.geometry(f"{self.text_display.winfo_reqwidth()}x{window_height}")

        self.calculator.bind("<Key>", self.handle_key_input)
        self.calculator.mainloop()

    def handle_key_input(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/().":
            self.add_to_calculation(key)
        elif key == "\r" or key == "\n":
            self.evaluate_calculation()
        elif key == "\x08":
            self.clear_last_input()

    def add_to_calculation(self, symbol):
        if isinstance(self.result, str):  # Έλεγχος αν το self.result είναι συμβολοσειρά
            if len(self.result) > 20:
                self.update_display("Επετεύχθη Μέγιστο Μήκος 20 Ψηφίων", "")
        else:  # Αν το self.result δεν είναι συμβολοσειρά, υποθέτουμε ότι είναι αριθμός
            if self.result > 20:
                self.update_display("Επετεύχθη Μέγιστο Μήκος 20 Ψηφίων", "")
        if len(self.calculation) < 20:
            if callable(symbol):
                self.result = str(symbol(self.calculation))
                self.update_display(''.join(self.calculation), self.result)
            else:
                if symbol == 2.7183 or symbol == 3.1416:
                    self.clear_field()
                self.calculation.append(str(symbol))
                self.update_display(''.join(self.calculation), self.result)
        else:
            self.update_display("3.129E-99", "Επετεύχθη Μέγιστο Μήκος 20 Ψηφίων")
            self.calculation = []

    def evaluate_calculation(self):
        try:
            calculation_str = ''.join(self.calculation)
            if 'mod' in calculation_str:
                dividend, divisor = calculation_str.split('mod')
                dividend = int(dividend) if dividend else 0
                divisor = int(divisor) if divisor else dividend
                result = self.calculate_mod(dividend, divisor)
            elif 'root' in calculation_str:
                n, x = calculation_str.split('root')
                n = int(n) if n else 0
                x = int(x) if x else n
                result = self.nth_root_x(n, x)
            else:
                result = eval(calculation_str)
            self.result = result
            formatted_result = self.format_result()
            self.calculation = [str(result)]
            self.update_display(calculation_str, formatted_result)
        except Exception as e:
            self.clear_field()
            self.update_display(f"Σφάλμα: {e}", "")

    def format_result(self):
        if isinstance(self.result, int):
            return "{:,}".format(self.result)
        elif isinstance(self.result, float):
            result_str = "{:,.2f}".format(self.result)  # Format with two decimal places
            if '.' in result_str:  # Check if there are decimals
                integer_part, decimal_part = result_str.split('.')
                integer_part = "{:,}".format(int(integer_part))  # Format integer part with commas
                return f"{integer_part}.{decimal_part}"  # Concatenate formatted integer and decimal parts
            else:
                return "{:,}".format(int(self.result))  # Format as integer if no decimal part
        else:
            return str(self.result)  # For other types, return as string

    def calculate_mod(self, dividend, divisor):
        try:
            result = dividend % divisor
            return result
        except ZeroDivisionError:
            return "Σφάλμα: Διαίρεση με το μηδέν"
        except Exception as e:
            return f"Σφάλμα: {e}"

    def clear_field(self):
        self.calculation = []
        self.result = ""
        self.update_display("", "")

    def update_display(self, calculation, result):
        self.text_display.delete(1.0, "end")
        self.text_display.insert("end", f"{calculation}\n{result}")

    def clear_last_input(self):
        if self.calculation:
            self.calculation.pop()
            self.update_display(''.join(self.calculation), "")
        else:
            self.clear_field()

    def clear_last_input_and_memory(self):
            self.clear_last_input()
            self.memory_clear()

    def change_sign(self):
        try:
            num_str = ''.join(self.calculation)
            num = float(num_str)
            is_integer = num.is_integer()
            num = -num if num >= 0 else abs(num)
            if is_integer:
                num = int(num)
            self.calculation = [str(num)]
            self.update_display(''.join(self.calculation), "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")

    def absolute_value(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = float(eval(cal))
                self.result = str(abs(float(num)))
                self.calculation = [f"abs({expression})"]
                self.update_display(''.join(self.calculation), self.result)
            else:
                self.clear_field()
                self.update_display("Σφάλμα: Δεν δόθηκε είσοδος.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def reciprocal(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = float(eval(cal))
                if num != 0:
                    self.result = round(1 / num, 5)
                    self.result = str(self.result)
                    self.calculation = [f"1/({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Σφάλμα: Διαίρεση με το μηδέν.", "")
            else:
                self.clear_field()
                self.update_display("Σφάλμα: Δεν δόθηκε είσοδος.", "")
        except Exception as e:
            self.clear_field()
            self.update_display(f"Σφάλμα: {e}", "")

    def square_x(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = float(cal)
                if num > 0:
                    self.result = str(round(num ** 2, 5))
                    self.calculation.append("**2")
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό για το τετράγωνο.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του τετραγώνου.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def square_root_x(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = float(cal)
                if(num >= 0):
                    self.result = sqrt(num)
                    self.result = round(self.result, 5)
                    self.calculation = [f"sqrt({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό της τετραγωνικής ρίζας.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def nth_root_x(self, n, x):
        try:
            num = x
            if num >= 0:
                n = n 
                if n != 0:
                    result = num ** (1 / n)
                    return result
                else:
                    self.clear_field()
                    self.update_display("Το n δεν μπορεί να είναι μηδέν.", "")
            else:
                self.clear_field()
                self.update_display("Παρακαλώ εισάγετε έναν μη αρνητικό αριθμό.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Παρακαλώ εισάγετε έγκυρο αριθμό για τον εκθέτη της ρίζας.", "")
        except ZeroDivisionError:
            self.clear_field()
            self.update_display("Το n δεν μπορεί να είναι μηδέν.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def ten_power_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            self.result = str(10 ** num)
            self.calculation = [f"10**{expression}"]
            self.update_display(''.join(self.calculation), self.result)
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def log_x(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = float(eval(cal))
                if num > 0:
                    self.result = str(log10(num))
                    self.calculation = [f"log10({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό για το λογάριθμο.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του λογαρίθμου.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def natural_logarithm_x(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = float(eval(cal))
                if num > 0:
                    self.result = str(log(num))
                    self.calculation = [f"log({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό για τον φυσικό λογάριθμο.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του φυσικού λογαρίθμου.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def exponential_function_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            result = exp(num)
            self.result = f"{result}"
            if num.is_integer():
                self.calculation = [f"{int(num)}.e"]
            else:
                num_str = str(num)
                if '.' in num_str:
                    self.calculation = [f"{num_str}e"]
            self.update_display(''.join(self.calculation), self.result)
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def factorial_x(self):
        try:
            expression = ''.join(self.calculation)
            if self.result or expression:
                cal = self.result if (self.result is not None and self.result != "") else expression
                num = int(eval(cal))  # Χρησιμοποιούμε int αντί για float
                if num >= 0:
                    result = factorial(num)
                    self.result = f"{result}"
                    self.calculation = [f"factorial({num})"]
                    if len(str(self.result)) > 20:  # Χρησιμοποιούμε str(result) για το μήκος
                        result = f"{int(result):.2e}"  # Αναπαράσταση σε επιστημονική μορφή
                        self.result = result
                self.update_display(''.join(self.calculation), self.result)
            else:
                self.clear_field()
                self.update_display("Παρακαλούμε εισάγετε έναν μη αρνητικό ακέραιο αριθμό για το παραγοντικό.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def memory_clear(self):
        self.memory.clear()
        self.clear_field()

    def memory_recall(self):
        calculation_str = ''.join(self.calculation)
        num = str(self.memory.recall())
        self.update_display(calculation_str, num)

    def memory_add(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = eval(calculation_str)
            self.memory.add(num)
            self.update_display(''.join(self.calculation), self.memory.recall())
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Δεν υπάρχει αριθμός αποθηκευμένος στη μνήμη", "")

    def memory_subtract(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = eval(calculation_str)
            self.memory.subtract(num)
            self.update_display(''.join(self.calculation), self.memory.recall())
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Δεν υπάρχει αριθμός αποθηκευμένος στη μνήμη", "")

    def memory_store(self):
        try:
            calculation_str = ''.join(self.calculation)
            num = eval(calculation_str)
            self.memory.store(num)
            self.update_display(''.join(self.calculation), self.memory.recall())
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος.", "")
        except:
            self.clear_field()
            self.update_display("Δεν υπάρχει αριθμός αποθηκευμένος στη μνήμη", "")