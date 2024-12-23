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
    abc = input("Enter the function you want to integrate: ")
    abc = abc.replace("^", "**")
    
    # Define the function
    def g(x):
        import math
        if np.abs(np.tan(x)) == np.inf:
            return np.nan
        else:
            return eval(abc)
      
    # Get lower bound
    low = input("Enter the lower bound: ")
    low2 = float(eval(low.replace("pi", "np.pi").replace("π", "np.pi")))
    
    # Get upper bound
    upp = input("Enter the upper bound: ")
    upp2 = float(eval(upp.replace("pi", "np.pi").replace("π", "np.pi")))
    
    # Check for vertical asymptotes within the integration bounds
    if np.isnan(g(low2)) or np.isnan(g(upp2)):
        print("The function has vertical asymptotes in the given interval. The integral may be divergent or difficult to compute.")
        return
    
    # Perform adaptive quadrature
    try:
        print("Here is the shaded area under the curve!")
        ab, bc = quad(g, low2, upp2, epsabs=1.49e-08, epsrel=1.49e-08)
        frac = fr.Fraction(ab)
        print("The calculated integral of " + abc + " from " + str(low) + " to " + str(upp) + " is: " + str(ab) + " = " + str(frac))
        
        # Set up the plot
        fig, ax = plt.subplots()
        plt.xlabel('$x$')
        plt.ylabel("$f(x)$")
        plt.grid()
        
        # Plot the function
        x = np.linspace(low2 - 0.1 * abs(low2), upp2 + 0.1 * abs(upp2), 20000)
        y = [g(a) for a in x]
        plt.plot(x, y, color='blue')
        
        # Plot the shaded area
        ix = np.linspace(low2, upp2, 200000)
        iy = [g(i) for i in ix]
        verts = list(zip(ix, iy))
        verts.insert(0, (low2, 0))
        verts.append((upp2, 0))
        poly = Polygon(verts, facecolor='green', alpha=0.5)
        ax.add_patch(poly)
        
        plt.show()
        
    except Exception as e:
        print("Integration error:", e)

integrate_with_graph()
