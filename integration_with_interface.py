from sympy.utilities.lambdify import lambdify
from sympy import *
from numpy import *
from scipy.integrate import *
import math, scipy
from scipy import integrate
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import warnings
warnings.filterwarnings("ignore")
import tkinter as tk
import fractions as fr

# Global variable to store the function
function_string = ""

import tkinter as tk

class FunctionInput:
    def __init__(self, master, callback):
        self.master = master
        master.title("Function Input")
        master.geometry("312x100")

        self.function_text = tk.StringVar()
        self.function_text.set("∫")

        self.entry = tk.Entry(master, textvariable=self.function_text, font=("Helvetica", 14))
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.submit_button = tk.Button(master, text="Submit", command=self.submit_function)
        self.submit_button.grid(row=1, column=1, pady=5)

        self.callback = callback

    def submit_function(self):
        function = self.function_text.get()
        self.callback(function)
        self.master.destroy()

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")
        master.geometry("900x424")

        self.total = tk.StringVar()
        self.total.set("∫")

        self.function = ""

        self.entry = tk.Entry(master, textvariable=self.total, font=("Helvetica", 40))
        self.entry.grid(row=0, column=0, columnspan=5, pady=20, padx=10, sticky="ew")  # Adjusted columnspan to 5

        self.create_buttons()

    def create_buttons(self):
        button_list = [
            ['sin', 'cos', 'tan', '^', 'x'],
            ['cot', '7', '8', '9', '/'],
            ['cosec', '4', '5', '6', '*'],
            ['sec', '1', '2', '3', '-'],
            ['√','','x','+','']
        ]

        for i, row in enumerate(button_list):
            for j, button_text in enumerate(row):
                button = tk.Button(
                    self.master, text=button_text, width=3, height=3, font=("Bold", 20),
                    command=lambda text=button_text: self.click(text)
                )
                button.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
            self.master.rowconfigure(i + 1, weight=1)

        equal_button = tk.Button(self.master, text="=", width=3, height=3, font=("Helvetica", 20),
                                 command=lambda: self.click('='))
        equal_button.grid(row=5, column=4, padx=5, pady=5, sticky="nsew")

        # Adding Log and Erase Buttons
        log_button = tk.Button(self.master, text="log(x,base)", width=3, height=3, font=("Helvetica", 20),
                               command=lambda: self.click('log'))
        log_button.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

        backspace_button = tk.Button(self.master, text="Bkspace", width=3, height=3, font=("Helvetica", 20),
                                     command=lambda: self.click('backspace'))
        backspace_button.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        curly_bracket_open_button = tk.Button(self.master, text="(", width=3, height=3, font=("Helvetica", 20),
                                              command=lambda: self.click('('))
        curly_bracket_open_button.grid(row=5, column=2, padx=5, pady=5, sticky="nsew")

        curly_bracket_close_button = tk.Button(self.master, text=")", width=3, height=3, font=("Helvetica", 20),
                                               command=lambda: self.click(')'))
        curly_bracket_close_button.grid(row=5, column=3, padx=5, pady=5, sticky="nsew")

        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.columnconfigure(3, weight=1)
        self.master.columnconfigure(4, weight=1)

    def click(self, button_text):
        current_text = self.entry.get()
        if button_text == 'C':
            self.total.set("")
            self.function = ""
        elif button_text == '=':
            self.function = current_text
            global function_string
            function_string = self.function[1:len(current_text)]
            print("Function:", self.function)
        elif button_text == 'backspace':
            self.function = self.function[:-1]
            self.total.set(current_text[:-1])
        elif button_text == 'log':
            self.function += 'log('
            self.total.set(current_text + 'log(')
        elif button_text == '^':    
            self.function += '**('
            self.total.set(current_text + '^(')
        elif button_text in ['sin', 'cos', 'tan', 'cosec', 'sec', 'cot']:
            self.function += button_text + '('
            self.total.set(current_text + button_text + '(')
        elif button_text == ')':
            self.function += ')'
            self.total.set(current_text + ')')
        else:
            self.function += button_text
            self.total.set(current_text + button_text)

if __name__ == '__main__':
    root = tk.Tk()
    my_calculator = Calculator(root)
    root.mainloop()

def integrate_with_graph():
    import math
    
    global function_string
    
    aba = function_string
    abc = aba.replace("^", "**")
    abc = abc.replace("pi", "math.pi")
    abc = abc.replace("π", "math.pi")
    abc = abc.replace("cot", "1/tan")
    abc = abc.replace("cosec", "1/sin")
    abc = abc.replace("sec", "1/cos")

    # Define 'e' as a variable
    e = math.e

    def g(x):
        import math
        func = eval(abc)
        return func

    
    print("Enter the lower bound:")
    low = input()
    low1 = low.replace("pi", "math.pi")
    low1 = low1.replace("π", "math.pi")
    low1 = low1.replace("inf", "math.inf")
    low2 = float(eval(low1))
    
    print("Enter the upper bound:")
    upp = input()
    upp1 = upp.replace("pi", "math.pi")
    upp1 = upp1.replace("π", "math.pi")
    upp1 = upp1.replace("inf", "math.inf")
    upp2 = float(eval(upp1))
    
    # Calculate x and y values
    x = np.linspace(low2 - 0.1 * abs(low2), upp2 + 0.1 * abs(upp2), 20000)
    y = [g(a) for a in x]

    # Filter out NaN and Inf values from y within integration bounds
    integration_indices = np.where((x >= low2) & (x <= upp2))
    y_valid = [y[i] for i in integration_indices[0] if not np.isnan(y[i]) and not np.isinf(y[i])]
    
    # Set up the plot
    fig, ax = plt.subplots()
    plt.xlabel('$x$')
    plt.ylabel("$f(x)$")
    plt.grid()
    plt.plot(x, y, color='blue')
    
    # Split the polygon into two parts based on the sign of y
    ix = np.linspace(low2, upp2, 200000)
    iy = [g(i) for i in ix]
    verts = list(zip(ix, iy))
    verts.insert(0, (low2, 0))
    verts.append((upp2, 0))
    
    pos_verts = [(x, y) for x, y in verts if y >= 0]
    neg_verts = [(x, 0) if y >= 0 else (x,y) for x,y in verts]
    
    # Plot positive area in green and negative area in red
    poly_pos = Polygon(pos_verts, facecolor='green', alpha=0.5)
    poly_neg = Polygon(neg_verts, facecolor='red', alpha=0.5)
    ax.add_patch(poly_pos)
    ax.add_patch(poly_neg)

    # Calculate y_max within the integration bounds
    y_max_within_bounds = max(y_valid) if y_valid else 0
    
    # Set y-axis limits with a margin
    if not np.isnan(y_max_within_bounds) and not np.isinf(y_max_within_bounds):
        y_margin = 0.1 * abs(y_max_within_bounds)
        if y_valid:
            plt.ylim(min(-y_margin, min(y_valid)), max(y_valid) + y_margin)
        else:
        # Set default y-limits if y_valid is empty
            plt.ylim(-1, 1)  # You can adjust these default limits as needed

    # Set aspect ratio to magnify the plot
    ax.set_aspect('auto', adjustable='datalim')

    try:
        print("Here is the shaded area under the curve!")
        ab, bc = quad(g, low2, upp2)
        frac = fr.Fraction(ab)
        print("The calculated integral of " + aba + " from " + str(low) + " to " + str(upp) + " is: " + str(ab) + " = " + str(frac))
        plt.show()
    except:
        print("This integral is divergent!")

integrate_with_graph()
