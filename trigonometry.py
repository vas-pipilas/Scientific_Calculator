import tkinter as tk
import math

class TrigonometryMenu:
    def __init__(self, calculator_window, calculator):
        self.calculator = calculator  # Αρχικοποίηση του αντικειμένου υπολογιστή
        self.calculator_window = calculator_window  # Αρχικοποίηση του παραθύρου υπολογιστή
        self.menu = tk.Menu(self.calculator_window, tearoff=0)  # Δημιουργία μενού χρησιμοποιώντας το tkinter
        self.create_menu()  # Κλήση της μεθόδου για δημιουργία του μενού

    def create_menu(self):
       # Ορισμός ετικετών, συναρτήσεων και μονάδων μέτρησης των τριγωνομετρικών συναρτήσεων
        button_labels =  [("sin", math.sin, "radians"), ("cos", math.cos, "radians"), 
                         ("tan", math.tan, "radians"), ("asin", math.asin, "degrees"), 
                         ("acos", math.acos, "degrees"), ("atan", math.atan, "degrees"), 
                         ("sinh", math.sinh, "radians"), ("cosh", math.cosh, "radians"), 
                         ("tanh", math.tanh, "radians"), ("asinh", math.asinh, "degrees"), 
                         ("acosh", math.acosh, "degrees"), ("atanh", math.atanh, "degrees"), 
                         ("ToRAD", math.radians, "degrees"), 
                         ("ToDEG", math.degrees, "radians")]

        # Προσθήκη κάθε επιλογής του μενού ως εντολή στο μενού
        for label, command, unit in button_labels:
             self.menu.add_command(label=label, command=lambda cmd=command, u=unit: self.handle_trigonometry_command(cmd, u))

    def trigonometry_flyout_window(self):
        # Εμφάνιση του μενού στην οθόνη σε συγκεκριμένες συντεταγμένες
        self.menu.post(self.calculator_window.winfo_x() + 150, self.calculator_window.winfo_y() + 100)

    def handle_trigonometry_command(self, command, unit):
        try:
            if callable(command):
                result = self.compute_trigonometric_function(command, unit)
                self.update_display(''.join(self.calculator.calculation), result)
            else:
                self.calculator.add_to_calculation(str(command))
        except ValueError:
            # Εκτύπωση μηνύματος λάθους για μη έγκυρη είσοδο
            self.calculator.clear_field()
            self.calculator.update_display(''.join(self.calculator.calculation), "Μη έγκυρη είσοδος.")
        except Exception as e:
            # Εκτύπωση γενικού μηνύματος λάθους
            self.calculator.clear_field()
            self.calculator.update_display("Εμφανίστηκε σφάλμα κατά τον υπολογισμό.", "")

    def compute_trigonometric_function(self, function, unit):
        self.calculator.handle_missing_number()
        expression = ''.join(self.calculator.calculation)
        if self.calculator.result or expression:
            cal = self.calculator.result if (self.calculator.result is not None and self.calculator.result != "") else expression
            if isinstance(cal, (int, float)) and float(cal).is_integer():
                # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                cal =  str(int(cal))
            num = float(eval(cal))
            
            if unit == "radians":
                angle_radians = num * math.pi / 180
            elif unit == "degrees":
                angle_radians = num

            # Υπολογισμός της τριγωνομετρικής συνάρτησης
            result = function(angle_radians)
            self.calculator.result = str(result)
            self.calculator.calculation = [f"{function.__name__}({expression})"]
            return result
        else:
            # Εκτύπωση μηνύματος λάθους για έλλειψη εισόδου
            self.calculator.clear_field()
            self.calculator.update_display("Σφάλμα: Δεν έχει γίνει εισαγωγή.", "")

    def update_display(self, expression, result):
        # Ενημέρωση της οθόνης του υπολογιστή με τα αποτελέσματα
        self.calculator.update_display(expression, str(result))
