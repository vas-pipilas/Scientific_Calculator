####Scientific Calculator####
###############################

import tkinter as tk
import math as math

calculation = []

###edw tha prosthetoume tis times sthn metavlhth mesw sthn function
def add_to_calculation(symbol):
    global calculation
    calculation += str(symbol)
    text_calculation.delete(1.0, "end")
    text_calculation.insert(1.0, calculation)

###edw tha ypologizoyme to apotelesma me thn parakatw function
def evaluate_calculation():
    global calculation
    try:
        calculation=str(eval(calculation))
        text_result.delete(1.0, "end")
        text_result.insert(1.0, calculation)
    except:
        clear_field()
        text_calculation.insert(1.0, "ERROR!!")
        pass


###Edw tha exoume to katharismo ths metavlhths
def clear_field(Mx):
    global calculation
    calculation= ""
    text_calculation.delete(1.0, "end")


calculator = tk.Tk()
calculator.title("Scientific Calculator by PLHPRO Team :) ")
calculator.geometry("640x480")

###parathyro pou mas deixnei thn praksh oso proxwrame
text_calculation=tk.Text(calculator, height=1 , width=20,font=("Arial", 24))
text_calculation.grid(columnspan=6)

##parathyro mono gia to apotelesma
text_result=tk.Text(calculator, height=1 , width=20,font=("Arial", 24))
text_result.grid(columnspan=6)

#####Buttons#########

button_mc = tk.Button(calculator,text="MC", command=lambda: clear_field(mc),width=1,font=("Arial", 12))
button_mc.grid(row=3,column=0,columnspan=1,sticky="ew")
button_mr = tk.Button(calculator,text="MR", command=lambda: clear_field(mr),width=1,font=("Arial", 12))
button_mr.grid(row=3,column=1,columnspan=1,sticky="ew")
button_mplus = tk.Button(calculator,text="M+", command=lambda: clear_field(mplus),width=1,font=("Arial", 12))
button_mplus.grid(row=3,column=2,columnspan=1,sticky="ew")
button_mminus = tk.Button(calculator,text="M-", command=lambda: clear_field(mminus),width=1,font=("Arial", 12))
button_mminus.grid(row=3,column=3,columnspan=1,sticky="ew")
button_ms = tk.Button(calculator,text="MS", command=lambda: clear_field(ms),width=1,font=("Arial", 12))
button_ms.grid(row=3,column=4,columnspan=1,sticky="ew")

calculator.mainloop()

