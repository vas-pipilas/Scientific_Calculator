import tkinter as tk
import math
from memory import Memory
from trigonometry import TrigonometryMenu

class Calculator:
    def __init__(self):
        self.calculation = []
        self.result = ""
        self.memory = Memory()

        self.calculator = tk.Tk()
        self.calculator.title("Επιστημονικός Υπολογιστής από την ομάδα PLHPRO :) ")
        self.calculator.geometry("620x370")
        self.trigonometry_menu = TrigonometryMenu(self.calculator, self)

        self.text_display = tk.Text(self.calculator, height=2, width=40, font=("Arial", 24))
        self.text_display.grid(columnspan=6)
        
        button_data = [
            ("MC", lambda: self.memory_clear()), ("MR", lambda: self.memory_recall()), ("M+", lambda: self.memory_add()),
            ("M-", lambda: self.memory_subtract()), ("MS", lambda: self.memory_store()),
            ("Τριγωνομετρία", self.trigonometry_menu.trigonometry_flyout_window), ("π", lambda: self.add_to_calculation(round(math.pi, 4))),
            ("e", lambda: self.add_to_calculation(round(math.e, 4))), ("C", self.clear_field),
            ("<==", lambda: self.clear_last_input()),
            ("x^2", lambda: self.square_x()), ("1/x", lambda: self.reciprocal()),
            ("|x|", lambda: self.absolute_value()), ("exp", lambda: self.exponential_function_x()),
            ("mod", lambda: self.add_to_calculation("mod")),
            ("√x", lambda: self.square_root_x()), ("(", lambda: self.add_to_calculation("(")),
            (")", lambda: self.add_to_calculation(")")), ("n!", lambda: self.factorial_x()),
            ("/", lambda: self.add_to_calculation("/")),
            ("x^y", lambda: self.add_to_calculation("**")), ("7", lambda: self.add_to_calculation(7)),
            ("8", lambda: self.add_to_calculation(8)), ("9", lambda: self.add_to_calculation(9)), ("*", lambda: self.add_to_calculation("*")),
            ("10^x", lambda: self.ten_power_x()), ("4", lambda: self.add_to_calculation(4)),
            ("5", lambda: self.add_to_calculation(5)), ("6", lambda: self.add_to_calculation(6)), ("-", lambda: self.add_to_calculation("-")),
            ("log", lambda: self.log_x()), ("1", lambda: self.add_to_calculation(1)),
            ("2", lambda: self.add_to_calculation(2)), ("3", lambda: self.add_to_calculation(3)), ("+", lambda: self.add_to_calculation("+")),
            ("ln", lambda: self.natural_logarithm_x()), ("+/-", lambda: self.change_sign()), ("0", lambda: self.add_to_calculation(0)),
            (".", lambda: self.add_to_calculation(".")), ("=", self.evaluate_calculation) ,
            ("n√x", lambda: self.add_to_calculation("root"))
        ]

        for i, (text, command) in enumerate(button_data):
            row = i // 5 + 3
            column = i % 5
            if command:
                tk.Button(self.calculator, text=text, width=1, font=("Arial", 12), command=command).grid(row=row, column=column, columnspan=1, sticky="ew")
            else:
                tk.Button(self.calculator, text=text, width=1, font=("Arial", 12)).grid(row=row, column=column, columnspan=1, sticky="ew")

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
        if len(self.result) > 20:
            self.result = "Μέγιστο Μήκος 20 Ψηφίων Επετεύχθη";
        if len(self.calculation) < 20:
            if callable(symbol):
                self.result = str(symbol(self.calculation))
                self.update_display(''.join(self.calculation), self.result)
            else:
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

            if isinstance(result, int):
                formatted_result = "{:,}".format(result)
            else:
                formatted_result = "{:.2f}".format(result)

            self.result = result
            self.calculation = [str(result)]
            self.update_display(calculation_str, formatted_result)
        except Exception as e:
            self.clear_field()
            self.update_display(f"Σφάλμα: {e}", "")

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
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")

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
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
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
                    self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε θετικό αριθμό για το τετράγωνο.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του τετραγώνου.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
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
                    self.result = math.sqrt(num)
                    self.result = round(self.result, 5)
                    self.calculation = [f"sqrt({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε θετικό αριθμό.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό της τετραγωνικής ρίζας.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
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
                    self.update_display("Μη έγκυρη είσοδος. Το n δεν μπορεί να είναι μηδέν.", "")
            else:
                self.clear_field()
                self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έναν μη αρνητικό αριθμό.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό για τον εκθέτη της ρίζας.", "")
        except ZeroDivisionError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Το n δεν μπορεί να είναι μηδέν.", "")
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
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
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
                    self.result = str(math.log10(num))
                    self.calculation = [f"log({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε θετικό αριθμό για το λογάριθμο.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του λογαρίθμου.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
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
                    self.result = str(math.log(num))
                    self.calculation = [f"ln({expression})"]
                    self.update_display(''.join(self.calculation), self.result)
                else:
                    self.clear_field()
                    self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε θετικό αριθμό για τον φυσικό λογάριθμο.", "")
            else:
                self.clear_field()
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του φυσικού λογαρίθμου.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def exponential_function_x(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            result = math.exp(num)
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
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
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
                    result = math.factorial(num)
                    self.result = f"{result}"
                    self.calculation = [f"fact({num})"]
                    if len(str(self.result)) > 20:  # Χρησιμοποιούμε str(result) για το μήκος
                        result = f"{int(result):.2e}"  # Αναπαράσταση σε επιστημονική μορφή
                        self.result = result
                    self.update_display(''.join(self.calculation), self.result)
            else:
                self.clear_field()
                self.update_display("Μη έγκυρη είσοδος. Παρακαλούμε εισάγετε έναν μη αρνητικό ακέραιο αριθμό για το παραγοντικό.", "")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο ακέραιο αριθμό.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def memory_clear(self):
        self.memory.clear()

    def memory_recall(self):
        self.calculation.append(self.memory.recall())
        self.update_display(''.join(self.calculation), self.result)

    def memory_add(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            self.memory.add(num)
            self.update_display(expression, f"{num} added to memory")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def memory_subtract(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            self.memory.subtract(num)
            self.update_display(expression, f"{num} subtracted from memory")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

    def memory_store(self):
        try:
            expression = ''.join(self.calculation)
            num = float(eval(expression))
            self.memory.store(num)
            self.update_display(expression, f"{num} stored in memory")
        except ValueError:
            self.clear_field()
            self.update_display("Μη έγκυρη είσοδος. Παρακαλώ εισάγετε έγκυρο αριθμό.", "")
        except:
            self.clear_field()
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")

calculator = Calculator()