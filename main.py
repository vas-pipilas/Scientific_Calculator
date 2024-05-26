import tkinter as tk
import multiprocessing
from math import *

def worker(expr, queue):
    try:
        # Ορισμός των επιτρεπόμενων συναρτήσεων και σταθερών για το eval
        allowed_functions = {
            "log10": log10, "log": log, "exp": exp, "sqrt": sqrt, "factorial": factorial
        }
        # Αξιολόγηση της έκφρασης
        result = eval(expr, {"__builtins__": None}, allowed_functions)
        # Έλεγχος εάν το αποτέλεσμα είναι αριθμός και το μήκος του είναι μεγαλύτερο από το όριο
        if isinstance(result, (int, float)) and len(str(result)) > 4300:
            # Εκτίμηση σφάλματος σε επιστημονική μορφή
            raise OverflowError("3.129E-99")                                                                                                                            
        # Τοποθέτηση του αποτελέσματος στην ουρά
        queue.put(result)
    except Exception as e:
        # Τοποθέτηση μηνύματος σφάλματος στην ουρά
        queue.put(f"Error: {e}")

class Calculator:
    def __init__(self):
        self.calculation = [] # Λίστα για την αποθήκευση των εισόδων του χρήστη
        self.result = "" # Μεταβλητή για την αποθήκευση του αποτελέσματος
        self.memory = Memory()  # Δημιουργία αντικειμένου της κλάσης Memory για τη διαχείριση της μνήμης

        # Δημιουργία του κύριου παραθύρου της εφαρμογής
        self.calculator = tk.Tk()
        self.calculator.title("Επιστημονικός Υπολογιστής από την ομάδα PLHPRO :) ")
        self.calculator.configure(background="gray26")  # Ορισμός του φόντου του παραθύρου

        # Δημιουργία του μενού της τριγωνομετρίας
        self.trigonometry_menu = TrigonometryMenu(self.calculator, self) 

        # Δημιουργία πεδίου εμφάνισης κειμένου για την εισαγωγή των αριθμών και των αποτελεσμάτων
        self.text_display = tk.Text(self.calculator, height=2, width=40, font=("Arial", 24), bg="gray26", fg="white") 
        self.text_display.grid(row=0, column=0, columnspan=5)
        self.calculator.resizable(False, False)
        
        button_padx = 5
        button_pady = 5
        button_width = self.text_display.winfo_width() // 5  # Υπολογισμός πλάτους των κουμπιών ανάλογα με το πλάτος του πεδίου εμφάνισης
        button_height = self.text_display.winfo_height()

        # Ορισμός των δεδομένων για τα κουμπιά της εφαρμογής
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

        # Δημιουργία κουμπιών στο παράθυρο της εφαρμογής, ταξινομημένων σε γραμμές και στήλες
        for i, (text, command) in enumerate(button_data):
            row = i // 5 + 3  # Υπολογισμός της γραμμής
            column = i % 5  # Υπολογισμός της στήλης
            button_bg_color = "gray56" if str(text).isdigit() else "gray36"  # Χρώματα κουμπιών ανάλογα με το κείμενο
            button_relief = "raised" if command else "flat"  # Εφέ των κουμπιών
            # Δημιουργία κουμπιών με τις αντίστοιχες παραμέτρους
            if command:
                tk.Button(self.calculator, text=text, width=button_width, height=button_height, font=("Arial", 12), 
                        command=command, bg=button_bg_color, fg="white", bd=0, borderwidth=1, relief=button_relief, padx=button_padx, pady=button_pady).grid(row=row, column=column, columnspan=1, padx=1, pady=1, sticky="nsew")
            else:
                tk.Button(self.calculator, text=text, width=button_width, height=button_height, font=("Arial", 12),
                        bg=button_bg_color, fg="white", bd=0, borderwidth=1, relief=button_relief, padx=button_padx, pady=button_pady).grid(row=row, column=column, columnspan=1, padx=1, pady=1, sticky="nsew")

        # Υπολογισμός του συνολικού ύψους των κουμπιών και του περιθωρίου
        total_button_height = button_height * (len(button_data) - 1) 
        total_padding_height = button_pady * ((len(button_data) - 1)) // 5
        # Υπολογισμός του ύψους του παραθύρου
        window_height = total_button_height * ((len(button_data) - 1) // 5 + 2) + total_padding_height

        # Ορισμός των διαστάσεων του παραθύρου
        self.calculator.geometry(f"{self.text_display.winfo_reqwidth()}x{window_height}")

        # Αντιστοίχιση του πλήκτρου Key με τη συνάρτηση handle_key_input
        self.calculator.bind("<Key>", self.handle_key_input)
        # Εκκίνηση της κύριας λούπας γραφικού περιβάλλοντος
        self.calculator.mainloop()

    def handle_key_input(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/().":  # Έλεγχος αν ο χαρακτήρας είναι ψηφίο ή σύμβολο τελεστών
            self.add_to_calculation(key)  # Προσθήκη του χαρακτήρα στον υπολογισμό
        elif key == "\r" or key == "\n":  # Έλεγχος αν ο χαρακτήρας είναι είσοδος (Enter)
            self.evaluate_calculation()  # Αξιολόγηση του υπολογισμού
        elif key == "\x08":  # Έλεγχος αν ο χαρακτήρας είναι η πίσω διαγραφή (Backspace)
            self.clear_last_input()  # Διαγραφή της τελευταίας εισόδου

    def add_to_calculation(self, symbol):
        if isinstance(self.result, str):  # Έλεγχος αν το self.result είναι συμβολοσειρά
            if len(self.result) > 20:
                self.update_display("Επετεύχθη Μέγιστο Μήκος 20 Ψηφίων", "")
        else:  # Αν το self.result δεν είναι συμβολοσειρά, υποθέτουμε ότι είναι αριθμός
            if self.result > 20:
                self.update_display("Επετεύχθη Μέγιστο Μήκος 20 Ψηφίων", "")
        if len(self.calculation) < 20:
            if callable(symbol):  # Έλεγχος αν το σύμβολο είναι κλήσιμο συνάρτησης
                self.result = str(symbol(self.calculation))  # Εκτέλεση της συνάρτησης και αποθήκευση του αποτελέσματος
                self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
            else:
                if symbol == 2.7183 or symbol == 3.1416:
                    self.clear_field()  # Καθαρισμός του πεδίου εμφάνισης για τις σταθερές e και π
                self.calculation.append(str(symbol))  # Προσθήκη του συμβόλου στη λίστα υπολογισμού
                self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
        else:
            self.update_display("3.129E-99", "Επετεύχθη Μέγιστο Μήκος 20 Ψηφίων")  # Εμφάνιση μηνύματος σφάλματος
            self.calculation = []  # Επαναφορά της λίστας υπολογισμού σε κενή κατάσταση

    def handle_missing_number(self):
        """
        Αντιμετωπίζει την περίπτωση όπου λείπει ένας αριθμός στην εξίσωση.
        Αν δεν υπάρχει κανένας αριθμός στην εξίσωση, παίρνει τον αριθμό από τη μνήμη αν είναι διαθέσιμος, αλλιώς θέτει τον αριθμό σε 0.
        Στη συνέχεια προσθέτει τον αριθμό στο τέλος της εξίσωσης και ενημερώνει την οθόνη εμφάνισης.
        Εάν υπάρχουν αριθμοί στην εξίσωση, ελέγχει εάν η εξίσωση ξεκινά με έναν τελεστή (+, -, *, /).
        Σε αυτήν την περίπτωση, προσθέτει τον αριθμό από τη μνήμη αν είναι διαθέσιμος, αλλιώς θέτει τον αριθμό σε 0, στο τέλος της εξίσωσης.
        Εάν η εξίσωση ξεκινά με έναν τελεστή, προσθέτει τον αριθμό από τη μνήμη αν είναι διαθέσιμος, αλλιώς θέτει τον αριθμό σε 0, στην αρχή της εξίσωσης.
        """
        if not any(char.isdigit() for element in self.calculation for char in element):
            num_from_memory = self.memory.recall()
            if num_from_memory is not None:
                self.result = num_from_memory
            else:
                self.result = 0
            self.calculation.append(str(self.result))
            self.update_display("", str(self.result))
        else:
            calculation_str = ''.join(self.calculation)  # Σχηματισμός του υπολογισμού από τη λίστα
            if calculation_str.endswith('+') or calculation_str.endswith('-') or calculation_str.endswith('*') or calculation_str.endswith('/'):
                num_from_memory = self.memory.recall()
                if num_from_memory is not None:
                    self.calculation.append(str(num_from_memory))
                else:
                    self.calculation.append('0')
                calculation_str = ''.join(self.calculation)
            if calculation_str.startswith('+') or calculation_str.startswith('-') or calculation_str.startswith('*') or calculation_str.startswith('/'):
                num_from_memory = self.memory.recall()
                if num_from_memory is not None:
                    self.calculation.insert(0, str(num_from_memory))
                else:
                    self.calculation.insert(0, '0')        
                calculation_str = ''.join(self.calculation)

    def evaluate_expression(self, expression, timeout=2):
        # Δημιουργία ουράς για επικοινωνία με τη διεργασία
        queue = multiprocessing.Queue()
        # Δημιουργία νέας διεργασίας για την εκτέλεση του υπολογισμού
        process = multiprocessing.Process(target=worker, args=(expression, queue))
        process.start()
        # Αναμονή για την ολοκλήρωση της διεργασίας με timeout
        process.join(timeout)

        # Αν η διεργασία είναι εξακολουθεί ενεργή (δεν ολοκληρώθηκε μέσα στο timeout)
        if process.is_alive():
            # Τερματισμός της διεργασίας
            process.terminate()
            # Επιστροφή ενός σφάλματος σε επιστημονική μορφή
            return "3.129E-99"

        # Λήψη του αποτελέσματος από την ουρά
        result = queue.get()
        # Έλεγχος εάν το αποτέλεσμα είναι αριθμός και η μήκος του είναι μεγαλύτερο από το όριο
        if isinstance(result, (int, float)) and len(str(result)) > 20:
            # Επιστροφή σφάλματος σε επιστημονική μορφή
            return "3.129E-99"
        # Επιστροφή του αποτελέσματος
        return result

    def evaluate_calculation(self):
        try:
            calculation_str = ''.join(self.calculation)  # Σχηματισμός του υπολογισμού από τη λίστα
            if 'mod' in calculation_str:  # Έλεγχος αν υπάρχει το σύμβολο mod στον υπολογισμό
                dividend, divisor = calculation_str.split('mod')  # Διαχωρισμός αριθμητή και παρανομαστή
                dividend = int(dividend) if dividend else 0  # Μετατροπή σε ακέραιο του αριθμητή
                divisor = int(divisor) if divisor else dividend  # Μετατροπή σε ακέραιο του παρανομαστή
                result = self.calculate_mod(dividend, divisor)  # Υπολογισμός του mod
            elif 'root' in calculation_str:  # Έλεγχος αν υπάρχει το σύμβολο root στον υπολογισμό
                n, x = calculation_str.split('root')  # Διαχωρισμός του n και του x
                n = int(n) if n else 0  # Μετατροπή σε ακέραιο του n
                x = int(x) if x else n  # Μετατροπή σε ακέραιο του x
                result = self.nth_root_x(n, x)  # Υπολογισμός της n-οστής ρίζας
            else:
                self.handle_missing_number()
                calculation_str = ''.join(self.calculation)
                result = eval(calculation_str)  # Υπολογισμός του αποτελέσματος
            self.evaluate_expression(calculation_str)
            if isinstance(result, str) and result.startswith("Error"):
                self.clear_field()
                self.update_display(f"{result}", "")
            elif isinstance(result, (int, float)) and len(str(result)) > 20:
                 self.update_display(calculation_str, "3.129E-99")     
            else:
                self.result = result  # Αποθήκευση του αποτελέσματος
                formatted_result = self.format_result()  # Μορφοποίηση του αποτελέσματος
                self.calculation = [str(result)]  # Ενημέρωση της λίστας υπολογισμού με το αποτέλεσμα
                self.update_display(calculation_str, formatted_result)  # Ενημέρωση της εμφάνισης
        except ZeroDivisionError:  # Εάν η διαίρεση γίνει με το μηδέν
            self.clear_field()  # Καθαρισμός του πεδίου εμφάνισης
            self.update_display(f"Σφάλμα: Διαίρεση με το μηδέν", "")  # Εμφάνιση μηνύματος σφάλματος
        except Exception as e:  # Εάν υπάρξει σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός του πεδίου εμφάνισης
            self.update_display(f"Σφάλμα: {e}", "")  # Εμφάνιση μηνύματος σφάλματος

    def format_result(self):
        if isinstance(self.result, int):  # Έλεγχος αν το αποτέλεσμα είναι ακέραιος
            return "{:,}".format(self.result)  # Μορφοποίηση ως ακέραιος με διαχωριστικά χιλιάδων
        elif isinstance(self.result, float):  # Έλεγχος αν το αποτέλεσμα είναι δεκαδικός
            result_str = "{:,.2f}".format(self.result)  # Μορφοποίηση με δύο δεκαδικά ψηφία
            if '.' in result_str:  # Έλεγχος αν υπάρχουν δεκαδικά
                integer_part, decimal_part = result_str.split('.')  # Διαχωρισμός ακέραιου και δεκαδικού μέρους
                integer_part = "{:,}".format(int(integer_part))  # Μορφοποίηση του ακεραίου με διαχωριστικά χιλιάδων
                return f"{integer_part}.{decimal_part}"  # Επιστροφή του μορφοποιημένου ακεραίου και δεκαδικού μέρους
            else:
                return "{:,}".format(int(self.result))  # Μορφοποίηση ως ακέραιος αν δεν υπάρχουν δεκαδικά
        else:
            return str(self.result)  # Για άλλους τύπους δεδομένων, επιστροφή ως συμβολοσειρά

    def calculate_mod(self, dividend, divisor):
        try:
            result = dividend % divisor  # Υπολογισμός του υπολοίπου της διαίρεσης
            return result  # Επιστροφή του αποτελέσματος
        except ZeroDivisionError:  # Εάν η διαίρεση γίνει με το μηδέν
            return "Σφάλμα: Διαίρεση με το μηδέν"  # Επιστροφή μηνύματος σφάλματος
        except Exception as e:  # Εάν υπάρξει άλλο σφάλμα
            return f"Σφάλμα: {e}"  # Επιστροφή λεπτομερούς μηνύματος σφάλματος

    def clear_field(self):
        self.calculation = []  # Εκκαθάριση της λίστας υπολογισμού
        self.result = ""  # Εκκαθάριση του αποτελέσματος
        self.update_display("", "")  # Ενημέρωση της εμφάνισης με κενά

    def update_display(self, calculation, result):
        self.text_display.delete(1.0, "end")  # Διαγραφή του περιεχομένου της εμφάνισης
        self.text_display.insert("end", f"{calculation}\n{result}")  # Εισαγωγή του υπολογισμού και του αποτελέσματος στην εμφάνιση


    def clear_last_input(self):
        if self.calculation:  # Έλεγχος αν η λίστα υπολογισμού δεν είναι κενή
            self.calculation.pop()  # Αφαίρεση του τελευταίου στοιχείου από τη λίστα υπολογισμού
            self.update_display(''.join(self.calculation), "")  # Ενημέρωση της εμφάνισης με τον υπολογισμό χωρίς το τελευταίο στοιχείο
        else:  # Αν η λίστα υπολογισμού είναι κενή
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης

    def clear_last_input_and_memory(self):
            self.clear_last_input()  # Καθαρισμός της τελευταίας εισόδου
            self.memory_clear()  # Καθαρισμός της μνήμης

    def change_sign(self):
        try:
            self.handle_missing_number()
            num_str = ''.join(self.calculation)  # Σχηματισμός του αριθμού από τη λίστα υπολογισμού
            num = float(num_str)  # Μετατροπή του αριθμού σε δεκαδικό
            is_integer = num.is_integer()  # Έλεγχος αν ο αριθμός είναι ακέραιος
            num = -num if num >= 0 else abs(num)  # Αλλαγή του προσήμου του αριθμού
            if is_integer:  # Αν ο αριθμός ήταν ακέραιος πριν την αλλαγή προσήμου
                num = int(num)  # Μετατροπή του αριθμού πίσω σε ακέραιο
            self.calculation = [str(num)]  # Ενημέρωση της λίστας υπολογισμού με τον νέο αριθμό
            self.update_display(''.join(self.calculation), "")  # Ενημέρωση της εμφάνισης
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος


    def absolute_value(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος αν υπάρχει ήδη αποτέλεσμα ή έκφραση
                cal = self.result if (self.result is not None and self.result != "") else expression  # Χρήση του αποτελέσματος αν υπάρχει, αλλιώς της έκφρασης
                if isinstance(cal, (int, float)) and float(cal).is_integer():
                    # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    cal =  str(int(cal))
                num = float(eval(cal))  # Υπολογισμός του αριθμού
                self.result = str(abs(float(num)))  # Υπολογισμός της απόλυτης τιμής του αριθμού και αποθήκευση στο αποτέλεσμα
                self.calculation = [f"abs({expression})"]  # Ενημέρωση της λίστας υπολογισμού με την απόλυτη τιμή της έκφρασης
                self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
            else:
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Σφάλμα: Δεν δόθηκε είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def reciprocal(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος αν υπάρχει ήδη αποτέλεσμα ή έκφραση
                cal = self.result if (self.result is not None and self.result != "") else expression  # Χρήση του αποτελέσματος αν υπάρχει, αλλιώς της έκφρασης
                if isinstance(cal, (int, float)) and float(cal).is_integer():
                    # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    cal =  str(int(cal))
                num = float(eval(cal))  # Υπολογισμός του αριθμού
                if num != 0:  # Έλεγχος αν ο αριθμός είναι διάφορος του μηδέν
                    self.result = round(1 / num, 5)  # Υπολογισμός του αντίστροφου και κατακερματισμός σε πέντε δεκαδικά ψηφία
                    self.result = str(self.result)  # Μετατροπή του αποτελέσματος σε συμβολοσειρά
                    self.calculation = [f"1/({expression})"]  # Ενημέρωση της λίστας υπολογισμού με τον αντίστροφο της έκφρασης
                    self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
                else:  # Αν ο αριθμός είναι μηδέν
                    self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                    self.update_display("Σφάλμα: Διαίρεση με το μηδέν.", "")  # Εμφάνιση μηνύματος σφάλματος
            else:
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Σφάλμα: Δεν δόθηκε είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except Exception as e:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display(f"Σφάλμα: {e}", "")  # Εμφάνιση λεπτομερούς μηνύματος σφάλματος

    def square_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος αν υπάρχει ήδη αποτέλεσμα ή έκφραση
                cal = self.result if (self.result is not None and self.result != "") else expression  # Χρήση του αποτελέσματος αν υπάρχει, αλλιώς της έκφρασης
                num = float(cal)  # Μετατροπή της έκφρασης σε δεκαδικό αριθμό
                if num > 0:  # Έλεγχος αν ο αριθμός είναι θετικός
                    self.result = str(round(num ** 2, 5))  # Υπολογισμός του τετραγώνου και κατακερματισμός σε πέντε δεκαδικά ψηφία
                    self.calculation.append("**2")  # Προσθήκη της έκφρασης για τον τετραγωνισμό στη λίστα υπολογισμού
                    self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
                else:  # Αν ο αριθμός είναι μη θετικός
                    self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό για το τετράγωνο.", "")  # Εμφάνιση μηνύματος σφάλματος
            else:  # Αν δεν υπάρχει προηγούμενο αποτέλεσμα ή έκφραση
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του τετραγώνου.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def square_root_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος αν υπάρχει ήδη αποτέλεσμα ή έκφραση
                cal = self.result if (self.result is not None and self.result != "") else expression  # Χρήση του αποτελέσματος αν υπάρχει, αλλιώς της έκφρασης
                if isinstance(cal, (int, float)) and float(cal).is_integer():
                    # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    cal =  str(int(cal))
                num = float(cal)  # Μετατροπή της έκφρασης σε δεκαδικό αριθμό
                if(num >= 0):  # Έλεγχος αν ο αριθμός είναι μη αρνητικός
                    self.result = sqrt(num)  # Υπολογισμός της τετραγωνικής ρίζας
                    self.result = round(self.result, 5)  # Κατακερματισμός σε πέντε δεκαδικά ψηφία
                    self.calculation = [f"sqrt({expression})"]  # Ενημέρωση της λίστας υπολογισμού με την τετραγωνική ρίζα της έκφρασης
                    self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
                else:  # Αν ο αριθμός είναι αρνητικός
                    self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό.", "")  # Εμφάνιση μηνύματος σφάλματος
            else:  # Αν δεν υπάρχει προηγούμενο αποτέλεσμα ή έκφραση
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό της τετραγωνικής ρίζας.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def nth_root_x(self, n, x):
        try:
            num = x  # Αποθήκευση του αριθμού x
            if num >= 0:  # Έλεγχος αν ο αριθμός είναι μη αρνητικός
                n = n  # Αποθήκευση του εκθέτη n
                if n != 0:  # Έλεγχος αν ο εκθέτης είναι διάφορος του μηδενός
                    result = num ** (1 / n)  # Υπολογισμός της ρίζας
                    return result  # Επιστροφή του αποτελέσματος
                else:  # Αν ο εκθέτης είναι μηδέν
                    self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                    self.update_display("Το n δεν μπορεί να είναι μηδέν.", "")  # Εμφάνιση μηνύματος σφάλματος
            else:  # Αν ο αριθμός δεν είναι μη αρνητικός
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Παρακαλώ εισάγετε έναν μη αρνητικό αριθμό.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν είναι έγκυρη
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Παρακαλώ εισάγετε έγκυρο αριθμό για τον εκθέτη της ρίζας.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ZeroDivisionError:  # Εάν ο εκθέτης είναι μηδέν
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Το n δεν μπορεί να είναι μηδέν.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def ten_power_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if isinstance(expression, (int, float)) and float(expression).is_integer():
                # Αν το expression είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                expression =  str(int(expression))
            num = float(eval(expression))  # Μετατροπή της έκφρασης σε δεκαδικό αριθμό
            self.result = str(10 ** num)  # Υπολογισμός του 10 στην δύναμη της έκφρασης
            self.calculation = [f"10**{expression}"]  # Ενημέρωση της λίστας υπολογισμού με τη δύναμη του 10
            self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def log_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος αν υπάρχει αποτέλεσμα ή έκφραση
                cal = self.result if (self.result is not None and self.result != "") else expression  # Επιλογή της αριθμητικής τιμής για τον υπολογισμό του λογαρίθμου
                if isinstance(cal, (int, float)) and float(cal).is_integer():
                # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    cal =  str(int(cal))
                num = float(eval(cal))  # Μετατροπή της αριθμητικής τιμής σε δεκαδικό αριθμό
                if num > 0:  # Έλεγχος αν ο αριθμός είναι θετικός
                    self.result = str(log10(num))  # Υπολογισμός του δεκαδικού λογαρίθμου
                    self.calculation = [f"log10({expression})"]  # Ενημέρωση της λίστας υπολογισμού με την έκφραση του λογαρίθμου
                    self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
                else:  # Αν ο αριθμός δεν είναι θετικός
                    self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό, μεγαλύτερο από το μηδέν, για το λογάριθμο.", "")  # Εμφάνιση μηνύματος σφάλματος
            else:  # Αν δεν υπάρχει προηγούμενο αποτέλεσμα ή έκφραση
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του λογαρίθμου.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def natural_logarithm_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος αν υπάρχει αποτέλεσμα ή έκφραση
                cal = self.result if (self.result is not None and self.result != "") else expression  # Επιλογή της αριθμητικής τιμής για τον υπολογισμό του φυσικού λογαρίθμου
                if isinstance(cal, (int, float)) and float(cal).is_integer():
                    # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    cal =  str(int(cal))
                num = float(eval(cal))  # Μετατροπή της αριθμητικής τιμής σε δεκαδικό αριθμό
                if num > 0:  # Έλεγχος αν ο αριθμός είναι θετικός
                    self.result = str(log(num))  # Υπολογισμός του φυσικού λογαρίθμου
                    self.calculation = [f"log({expression})"]  # Ενημέρωση της λίστας υπολογισμού με την έκφραση του φυσικού λογαρίθμου
                    self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
                else:  # Αν ο αριθμός δεν είναι θετικός
                    self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                    self.update_display("Παρακαλώ εισάγετε θετικό αριθμό για τον φυσικό λογάριθμο.", "")  # Εμφάνιση μηνύματος σφάλματος
            else:  # Αν δεν υπάρχει προηγούμενο αποτέλεσμα ή έκφραση
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Δεν υπάρχει προηγούμενο αποτέλεσμα για τον υπολογισμό του φυσικού λογαρίθμου.", "")  # Εμφάνιση μηνύματος σφάλματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def exponential_function_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation ) # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if isinstance(expression, (int, float)) and float(expression).is_integer():
                # Αν το expression είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    expression =  str(int(expression))
            num = float(eval(expression))  # Μετατροπή της αριθμητικής τιμής σε δεκαδικό αριθμό
            result = exp(num)  # Υπολογισμός της εκθετικής συνάρτησης
            self.result = f"{result}"  # Καθορισμός του αποτελέσματος ως αλφαριθμητική τιμή
            if num.is_integer():  # Έλεγχος αν ο αριθμός είναι ακέραιος
                self.calculation = [f"{int(num)}.e"]  # Καθορισμός της έκφρασης στη λίστα υπολογισμού
            else:  # Αν ο αριθμός δεν είναι ακέραιος
                num_str = str(num)  # Μετατροπή του αριθμού σε αλφαριθμητική τιμή
                if '.' in num_str:  # Έλεγχος αν υπάρχει δεκαδικό μέρος στον αριθμό
                    self.calculation = [f"{num_str}e"]  # Καθορισμός της έκφρασης στη λίστα υπολογισμού
            self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν μπορεί να μετατραπεί σε αριθμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος

    def factorial_x(self):
        try:
            self.handle_missing_number()
            expression = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            if self.result or expression:  # Έλεγχος για την ύπαρξη αποτελέσματος ή έκφρασης
                cal = self.result if (self.result is not None and self.result != "") else expression  # Επιλογή της έκφρασης από το αποτέλεσμα ή την έκφραση
                if isinstance(cal, (int, float)) and float(cal).is_integer():
                # Αν το cal είναι αριθμός και είναι ακέραιος, το μετατρέπει σε string ακέραιου αριθμού
                    cal =  str(int(cal))
                num = int(eval(cal))  # Μετατροπή του αριθμού σε ακέραιο
                if num >= 0:  # Έλεγχος για θετικό αριθμό
                    result = factorial(num)  # Υπολογισμός του παραγοντικού
                    self.result = f"{result}"  # Καθορισμός του αποτελέσματος
                    self.calculation = [f"factorial({num})"]  # Καθορισμός της έκφρασης
                    if len(str(self.result)) > 20:  # Έλεγχος για το μήκος του αποτελέσματος
                        result = f"{int(result):.2e}"  # Μορφοποίηση σε επιστημονική μορφή
                        self.result = result
                self.update_display(''.join(self.calculation), self.result)  # Ενημέρωση της εμφάνισης
            else:
                self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
                self.update_display("Παρακαλούμε εισάγετε έναν μη αρνητικό ακέραιο αριθμό για το παραγοντικό.", "")  # Εμφάνιση μηνύματος
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν είναι έγκυρη
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά τον υπολογισμό
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Σφάλμα κατά τον υπολογισμό.", "")  # Εμφάνιση μηνύματος σφάλματος


    def memory_clear(self):
        self.memory.clear()  # Καθαρισμός της μνήμης
        self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης

    def memory_recall(self):
        calculation_str = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
        num = str(self.memory.recall())  # Επαναφορά της τιμής από τη μνήμη
        self.update_display(calculation_str, num)  # Ενημέρωση της εμφάνισης

    def memory_add(self):
        try:
            calculation_str = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            num = eval(calculation_str)  # Υπολογισμός του αποτελέσματος της έκφρασης
            self.memory.add(num)  # Προσθήκη του αποτελέσματος στη μνήμη
            self.update_display(''.join(self.calculation), self.memory.recall())  # Ενημέρωση της εμφάνισης
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν είναι έγκυρη
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά την εκτέλεση
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Δεν υπάρχει αριθμός αποθηκευμένος στη μνήμη", "")  # Εμφάνιση μηνύματος σφάλματος

    def memory_subtract(self):
        try:
            calculation_str = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            num = eval(calculation_str)  # Υπολογισμός του αποτελέσματος της έκφρασης
            self.memory.subtract(num)  # Αφαίρεση του αποτελέσματος από τη μνήμη
            self.update_display(''.join(self.calculation), self.memory.recall())  # Ενημέρωση της εμφάνισης
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν είναι έγκυρη
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά την εκτέλεση
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Δεν υπάρχει αριθμός αποθηκευμένος στη μνήμη", "")  # Εμφάνιση μηνύματος σφάλματος

    def memory_store(self):
        try:
            calculation_str = ''.join(self.calculation)  # Σχηματισμός της έκφρασης από τη λίστα υπολογισμού
            num = eval(calculation_str)  # Υπολογισμός του αποτελέσματος της έκφρασης
            self.memory.store(num)  # Αποθήκευση του αποτελέσματος στη μνήμη
            self.update_display(''.join(self.calculation), self.memory.recall())  # Ενημέρωση της εμφάνισης
        except ValueError:  # Εάν η τρέχουσα είσοδος δεν είναι έγκυρη
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Μη έγκυρη είσοδος.", "")  # Εμφάνιση μηνύματος σφάλματος
        except:  # Εάν υπάρξει άλλο σφάλμα κατά την εκτέλεση
            self.clear_field()  # Καθαρισμός ολόκληρου του πεδίου εμφάνισης
            self.update_display("Δεν υπάρχει αριθμός αποθηκευμένος στη μνήμη", "")  # Εμφάνιση μηνύματος σφάλματος


class TrigonometryMenu:
    def __init__(self, calculator_window, calculator):
        self.calculator = calculator  # Αρχικοποίηση του αντικειμένου υπολογιστή
        self.calculator_window = calculator_window  # Αρχικοποίηση του παραθύρου υπολογιστή
        self.menu = tk.Menu(self.calculator_window, tearoff=0)  # Δημιουργία μενού χρησιμοποιώντας το tkinter
        self.create_menu()  # Κλήση της μεθόδου για δημιουργία του μενού

    def create_menu(self):
       # Ορισμός ετικετών, συναρτήσεων και μονάδων μέτρησης των τριγωνομετρικών συναρτήσεων
        button_labels =  [("sin", sin, "radians"), ("cos", cos, "radians"), 
                         ("tan", tan, "radians"), ("asin", asin, "degrees"), 
                         ("acos", acos, "degrees"), ("atan", atan, "degrees"), 
                         ("sinh", sinh, "radians"), ("cosh", cosh, "radians"), 
                         ("tanh", tanh, "radians"), ("asinh", asinh, "degrees"), 
                         ("acosh", acosh, "degrees"), ("atanh", atanh, "degrees"), 
                         ("ToRAD", radians, "degrees"), 
                         ("ToDEG", degrees, "radians")]

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
                angle_radians = num * pi / 180
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

class Memory:
    def __init__(self):
        self.memory_value = 0  # Αρχικοποίηση της μεταβλητής μνήμης σε 0

    def store(self, value):
        self.memory_value = value  # Αποθήκευση της τιμής στη μνήμη

    def recall(self):
        return self.memory_value  # Επαναφορά της αποθηκευμένης τιμής

    def add(self, value):
        self.memory_value += value  # Προσθήκη της τιμής στη μνήμη

    def subtract(self, value):
        self.memory_value -= value  # Αφαίρεση της τιμής από τη μνήμη

    def clear(self):
        self.memory_value = 0  # Εκκαθάριση της μνήμης (επαναφορά στο 0)


# Κύριο σημείο εκκίνησης
if __name__ == "__main__":
    # Δημιουργία μιας νέας περίπτωσης της κλάσης Calculator
    calc = Calculator()