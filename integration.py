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

def integrate_with_graph():
    print()
    print("Enter the function you want to see graphed and INTEGRATED!")
    aba = input()
    abc = aba.replace("^", "**")

    def g(x):
        func = eval(abc)
        return func

    print("Enter the lower bound: ")
    low = float(input())
    print("Enter the upper bound: ")
    upp = float(input())

    if(("1/x" in aba or aba == "x^-1") and (low <= 0 or upp <= low+1)):
        return("This integral is divergent. It cannot be computed as of now.")

    x = np.linspace(int(floor(low))-8, int(ceil(upp))+8, 20000)
    if("ln" in aba or "log" in aba):
        x = np.linspace(int(floor(low))+1, int(ceil(upp))+8, 20000)

    # Get the corresponding y values from the function
    y = [g(a) for a in x]

    # Set up the plot
    fig, ax = plt.subplots()
    plt.xlabel('$x$')
    plt.ylabel("$f(x)$")
    plt.grid()

    # Plot x against g(x)
    plt.plot(x,y, color='orange')

    # Make the shaded region
    ix = np.linspace(low, upp)
    iy = [g(i) for i in ix]
    verts = [(low, 0)] + list(zip(ix, iy)) + [(upp, 0)]
    poly = Polygon(verts, facecolor='cyan')
    ax.add_patch(poly)

    try:
        print("Here is the shaded area under the curve! Close it to see the calculated integral.")
        plt.show()
        ab, bc = quad(g, low, upp)
        int_statement = "The calculated integral of " +aba+" from "+str(low)+" to "+str(upp)+" is: " + str(ab)
        return(int_statement)
    except:
        print("This integral is divergent!")

print(integrate_with_graph())