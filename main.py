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
    calculation= []
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
button_trigonometry = tk.Button(calculator,text="Trigonometry",width=1,font=("Arial", 12))
button_trigonometry.grid(row=4,column=0,columnspan=3,sticky="ew")
button_pi = tk.Button(calculator,text="π",width=1,font=("Arial", 12))
button_pi.grid(row=5,column=0,columnspan=1,sticky="ew")
button_e = tk.Button(calculator,text="e",width=1,font=("Arial", 12))
button_e.grid(row=5,column=1,columnspan=1,sticky="ew")
button_clear = tk.Button(calculator,text="C",width=1,font=("Arial", 12))
button_clear.grid(row=5,column=2,columnspan=1,sticky="ew")
button_eraser = tk.Button(calculator,text="<==",width=1,font=("Arial", 12)) ###Eraser Button. It should remove only the last entry##
button_eraser.grid(row=5,column=2,columnspan=1,sticky="ew")
button_x2 = tk.Button(calculator,text="x2",width=1,font=("Arial", 12))
button_x2.grid(row=6,column=0,columnspan=1,sticky="ew")
button_1divx = tk.Button(calculator,text="1/x",width=1,font=("Arial", 12))
button_1divx.grid(row=6,column=1,columnspan=1,sticky="ew")
button_absolutex = tk.Button(calculator,text="|x|",width=1,font=("Arial", 12))
button_absolutex.grid(row=6,column=1,columnspan=1,sticky="ew")


calculator.mainloop()

