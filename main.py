##############################
####Scientific Calculator#####
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
        calculation_str = ''.join(calculation)
        calculation=str(eval(calculation_str))
        text_result.delete(1.0, "end")
        text_result.insert(1.0, calculation)
    except:
        clear_field()
        text_calculation.insert(1.0, "ERROR!!")
        pass


###Edw tha exoume to katharismo ths metavlhths
def clear_field():
    global calculation
    calculation= []
    text_calculation.delete(1.0, "end")


calculator = tk.Tk()
calculator.title("Scientific Calculator by PLHPRO Team :) ")
calculator.geometry("640x480")

###parathyro pou mas deixnei thn praksh oso proxwrame
text_calculation=tk.Text(calculator, height=1 , width=40,font=("Arial", 24))
text_calculation.pack(fill="both", expand=True)
text_calculation.grid(columnspan=6)

##parathyro mono gia to apotelesma
text_result=tk.Text(calculator, height=1 , width=40,font=("Arial", 24))
text_result.grid(columnspan=6)

#####Buttons#########

####PH in button means PlaceHolders. We will decide what we do with them ###

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
button_eraser.grid(row=5,column=3,columnspan=1,sticky="ew")
button_x2 = tk.Button(calculator,text="x2",width=1,font=("Arial", 12))
button_x2.grid(row=6,column=0,columnspan=1,sticky="ew")
button_1divx = tk.Button(calculator,text="1/x",width=1,font=("Arial", 12))
button_1divx.grid(row=6,column=1,columnspan=1,sticky="ew")
button_absolutex = tk.Button(calculator,text="|x|",width=1,font=("Arial", 12))
button_absolutex.grid(row=6,column=2,columnspan=1,sticky="ew")
button_placeholder = tk.Button(calculator,text="PH",width=1,font=("Arial", 12))
button_placeholder.grid(row=6,column=3,columnspan=1,sticky="ew")
button_mod = tk.Button(calculator,text="mod",width=1,font=("Arial", 12))
button_mod.grid(row=6,column=4,columnspan=1,sticky="ew")
button_mod = tk.Button(calculator,text="mod",width=1,font=("Arial", 12))
button_mod.grid(row=6,column=4,columnspan=1,sticky="ew")
button_root = tk.Button(calculator,text="√x",width=1,font=("Arial", 12))
button_root.grid(row=7,column=0,columnspan=1,sticky="ew")
button_leftparenthesis = tk.Button(calculator,text="(",width=1,font=("Arial", 12),command=lambda: add_to_calculation("("))
button_leftparenthesis.grid(row=7,column=1,columnspan=1,sticky="ew")
button_rightparenthesis = tk.Button(calculator,text=")",width=1,font=("Arial", 12),command=lambda: add_to_calculation(")"))
button_rightparenthesis.grid(row=7,column=2,columnspan=1,sticky="ew")
button_paragontiko = tk.Button(calculator,text="!x",width=1,font=("Arial", 12))
button_paragontiko.grid(row=7,column=3,columnspan=1,sticky="ew")
button_div = tk.Button(calculator,text="/",width=1,font=("Arial", 12),command=lambda: add_to_calculation("/"))
button_div.grid(row=7,column=4,columnspan=1,sticky="ew")
button_xpowery = tk.Button(calculator,text="x^y",width=1,font=("Arial", 12))
button_xpowery.grid(row=8,column=0,columnspan=1,sticky="ew")
button_7 = tk.Button(calculator,text="7",width=1,font=("Arial", 12),command=lambda: add_to_calculation("7"))
button_7.grid(row=8,column=1,columnspan=1,sticky="ew")
button_8 = tk.Button(calculator,text="8",width=1,font=("Arial", 12),command=lambda: add_to_calculation("8"))
button_8.grid(row=8,column=2,columnspan=1,sticky="ew")
button_9 = tk.Button(calculator,text="9",width=1,font=("Arial", 12),command=lambda: add_to_calculation("9"))
button_9.grid(row=8,column=3,columnspan=1,sticky="ew")
button_multiply = tk.Button(calculator,text="*",width=1,font=("Arial", 12),command=lambda: add_to_calculation("*"))
button_multiply.grid(row=8,column=4,columnspan=1,sticky="ew")
button_placeholder = tk.Button(calculator,text="PH",width=1,font=("Arial", 12))
button_placeholder.grid(row=9,column=0,columnspan=1,sticky="ew")
button_4 = tk.Button(calculator,text="4",width=1,font=("Arial", 12),command=lambda: add_to_calculation("4"))
button_4.grid(row=9,column=1,columnspan=1,sticky="ew")
button_5 = tk.Button(calculator,text="5",width=1,font=("Arial", 12),command=lambda: add_to_calculation("5"))
button_5.grid(row=9,column=2,columnspan=1,sticky="ew")
button_6 = tk.Button(calculator,text="6",width=1,font=("Arial", 12),command=lambda: add_to_calculation("6"))
button_6.grid(row=9,column=3,columnspan=1,sticky="ew")
button_minus = tk.Button(calculator,text="-",width=1,font=("Arial", 12),command=lambda: add_to_calculation("-"))
button_minus.grid(row=9,column=4,columnspan=1,sticky="ew")
button_log = tk.Button(calculator,text="log",width=1,font=("Arial", 12))
button_log.grid(row=10,column=0,columnspan=1,sticky="ew")
button_1 = tk.Button(calculator,text="1",width=1,font=("Arial", 12),command=lambda: add_to_calculation("1"))
button_1.grid(row=10,column=1,columnspan=1,sticky="ew")
button_2 = tk.Button(calculator,text="2",width=1,font=("Arial", 12),command=lambda: add_to_calculation("2"))
button_2.grid(row=10,column=2,columnspan=1,sticky="ew")
button_3 = tk.Button(calculator,text="3",width=1,font=("Arial", 12),command=lambda: add_to_calculation("3"))
button_3.grid(row=10,column=3,columnspan=1,sticky="ew")
button_plus = tk.Button(calculator,text="+",width=1,font=("Arial", 12),command=lambda: add_to_calculation("+"))
button_plus.grid(row=10,column=4,columnspan=1,sticky="ew")
button_ln = tk.Button(calculator,text="ln",width=1,font=("Arial", 12))
button_ln.grid(row=11,column=0,columnspan=1,sticky="ew")
button_changesign = tk.Button(calculator,text="+/-",width=1,font=("Arial", 12))
button_changesign.grid(row=11,column=1,columnspan=1,sticky="ew")
button_0 = tk.Button(calculator,text="0",width=1,font=("Arial", 12),command=lambda: add_to_calculation("0"))
button_0.grid(row=11,column=2,columnspan=1,sticky="ew")
button_separator = tk.Button(calculator,text=".",width=1,font=("Arial", 12),command=lambda: add_to_calculation("."))
button_separator.grid(row=11,column=3,columnspan=1,sticky="ew")
button_calculation = tk.Button(calculator,text="=",width=1,font=("Arial", 12),command=evaluate_calculation)
button_calculation.grid(row=11,column=4,columnspan=1,sticky="ew")

calculator.mainloop()

