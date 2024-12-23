from sympy.utilities.lambdify import lambdify
from sympy import *
from numpy import *
from scipy.integrate import *
import math
import sympy as sp
from scipy import integrate
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import fractions as fr
import warnings
warnings.filterwarnings("ignore")

def check_domain(func, low, upp):
    # Define the domain of trigonometric and inverse trigonometric functions
    corner_limits = {
        'asin': Interval(-1, 1),
        'acos': Interval(-1, 1),
        'atan': Interval(float('-inf'), float('inf')),
        'sin': Interval(float('-inf'), float('inf')),
        'tan': Interval(float('-inf'), float('inf')),
        'cos': Interval(float('-inf'), float('inf')),
        'cosec': Interval.open(-oo, 0) + Interval.open(0, oo),
        'sec': Interval.open(-oo, -pi/2) + Interval.open(-pi/2, pi/2) + Interval.open(pi/2, oo),
        'cot': Interval.open(-pi, 0) + Interval.open(0, pi)
    }

           # # Check if the limits are within the domain
    func_name = func.func.__name__
    if func_name in corner_limits:
        domain = corner_limits[func_name]
        if domain.contains(low) and domain.contains(upp):
            if func_name == 'cosec':
                for i in range (0,111):
                 if low <= i*pi <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi at value of ",i,"pi")
                    return False
               
                 else:
                    continue
                return True
           
            elif func_name == 'sec':
                for i in range (0,52):
                 if  low <= i*(pi/2) <= upp or low <= -i*(pi/2) <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi/2 at value of ",i,"pi/2")
                    return False
                 else :
                    continue
                return True
            elif func_name == 'tan':
                for i in range (0,52):
                 if  low <= i*(pi/2) <= upp or low <= -i*(pi/2) <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi/2 at value of ",i+1,"pi/2")
                    return False
                 else :
                    continue
                return True    
            elif func_name == 'cot':
                for i in range (0,52):
                 if low <= i*pi <= upp or low <= -i*(pi) <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi at value of ",i+1,"pi")
                    return False
                 else:  
                    continue
                return True
                 
            else:
              return True
    else:
     try:
        # Substitute limits to check if they are in the domain
            func_low = func.subs('x', low)
            func_upp = func.subs('x', upp)

        # If the function is defined at both limits, return True
            if func_low.is_real and func_upp.is_real:
              return True            
            else:
              return False
     except Exception as e:
           print("An error occurred while checking the domain:", e)
           return False
       


   
def integrate_with_graph():
    import math
    abc = input("Enter function to be integrated: ")
    abc=abc.replace('pi', str(math.pi))
   #abc=abc.replace('e','math.e')
    # Parse the function using sympy
    x = symbols('x')
    func = sympify(abc)

    # Check if limits are in the domain of the function
    print("Enter the lower bound:")
    low =input()
    low=low.replace('pi', str(math.pi))
    low=float(eval(low))
    print("Enter the upper bound:")
    upp =input()
    upp=upp.replace('pi', str(math.pi))
    upp=float(eval(upp))

    if not check_domain(func, low, upp):
        print("Limits are not within the domain of the function. The integral is divergent.")
        return

    # Define the function using lambdify
    g = lambdify(x, func, modules=['numpy', {'asin': lambda x: np.arcsin(x),
                                              'acos': lambda x: np.arccos(x),
                                              'atan': lambda x: np.arctan(x),
                                              'cosec': lambda x: 1/np.sin(x),
                                              'sec': lambda x: 1/np.cos(x),
                                              'cot': lambda x: 1/np.tan(x),
                                              'sin': lambda x: sin(x) ,
                                              'cos': lambda x: cos(x),
                                              'tan': lambda x: tan(x)}])
    # Calculate x and y values
    x_vals = np.linspace(low, upp, 1000)
    y_vals = g(x_vals)

    # Set up the plot
    fig, ax = plt.subplots()
    plt.xlabel('$x$')
    plt.ylabel("$f(x)$")
    plt.grid()
    plt.plot(x_vals, y_vals, color='blue')

    # Fill the area under the curve
    ix = np.linspace(low, upp, 1000)
    iy = g(ix)
    verts = [(low, 0), *zip(ix, iy), (upp, 0)]
    poly = Polygon(verts, facecolor='0.9', edgecolor='0.5')
    ax.add_patch(poly)

    # Calculate the integral
    try:
        result, _ = quad(g, low, upp)
        frac = fr.Fraction(result)
        print(f"The calculated integral of {abc} from {low} to {upp} is: {result} = {frac}")
        plt.show()
    except Exception as e:
        print("An error occurred while calculating the integral:", e)

ch = int(input("Enter 0 for definite and 1 for indefinite integration: "))
while ch not in [0, 1]:
    ch = int(input("Invalid choice. Enter again: "))

if ch == 0:
    integrate_with_graph()
else:
# Define the symbol
    x = sp.symbols('x')
    # Get the function from the user
    f_input = input("Enter the function you want to integrate (in terms of x): ")
    f_input = sp.parse_expr(f_input)

    # Parse the user input into a SymPy expression
    try:
        f = sp.sympify(f_input)
    except sp.SympifyError:
        print("Invalid input. Please enter a valid mathematical expression.")
        exit()

    # Perform indefinite integration
    integral_f = sp.integrate(f, x)

    # Evaluate the integral
    integral_f_evaluated = integral_f.doit()

    # Print the step-by-step integration
    print("Step-by-step integration of f(x):")
    for step in integral_f_evaluated.args:
        sp.pretty_print(step)

    # Print the final result
    print("\nFinal result of the indefinite integral of f(x):")
    sp.pretty_print(integral_f_evaluated)

    #sp.parse_expr ---> Use this for parsing