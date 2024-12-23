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
import fractions as fr

def integrate_with_graph():
    import math
    
    aba = input("Enter the function you want to integrate: ")
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