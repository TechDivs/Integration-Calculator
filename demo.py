import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import fractions as fr
from scipy.integrate import quad

ch = int(input("Enter 0 for definite and 1 for indefinite integration: "))
while ch < 0 or ch > 1:
    ch = int(input("Invalid choice. Enter again: "))

if ch == 0:
    def integrate_with_graph():
        aba = input("Enter function to be integrated: ")
        abc = aba.replace("^", "**")
        abc = abc.replace("pi", "math.pi")
        abc = abc.replace("π", "math.pi")
        abc = abc.replace("cot", "1/tan")
        abc = abc.replace("cosec", "1/sin")
        abc = abc.replace("sec", "1/cos")

        def g(x):
            func = eval(abc)
            return func

        low = float(input("Enter the lower bound: "))
        upp = float(input("Enter the upper bound: "))

        try:
            x = np.linspace(low - 0.1 * abs(low), upp + 0.1 * abs(upp), 20000)
            y = [g(a) for a in x]

            integration_indices = np.where((x >= low) & (x <= upp))
            y_valid = [y[i] for i in integration_indices[0] if not np.isnan(y[i]) and not np.isinf(y[i])]

            fig, ax = plt.subplots()
            plt.xlabel('$x$')
            plt.ylabel("$f(x)$")
            plt.grid()
            plt.plot(x, y, color='blue')

            ix = np.linspace(low, upp, 200000)
            iy = [g(i) for i in ix]
            verts = list(zip(ix, iy))
            verts.insert(0, (low, 0))
            verts.append((upp, 0))

            pos_verts = [(x, y) for x, y in verts if y >= 0]
            neg_verts = [(x, 0) if y >= 0 else (x,y) for x,y in verts]

            poly_pos = Polygon(pos_verts, facecolor='green', alpha=0.5)
            poly_neg = Polygon(neg_verts, facecolor='red', alpha=0.5)
            ax.add_patch(poly_pos)
            ax.add_patch(poly_neg)

            y_max_within_bounds = max(y_valid) if y_valid else 0

            if not np.isnan(y_max_within_bounds) and not np.isinf(y_max_within_bounds):
                y_margin = 0.1 * abs(y_max_within_bounds)
                if y_valid:
                    plt.ylim(min(-y_margin, min(y_valid)), max(y_valid) + y_margin)
                else:
                    plt.ylim(-1, 1)

            ax.set_aspect('auto', adjustable='datalim')

            ab, bc = quad(g, low, upp)
            frac = fr.Fraction(ab)
            print("The calculated integral of " + aba + " from " + str(low) + " to " + str(upp) + " is: " + str(ab) + " = " + str(frac))
            plt.show()

        except (ValueError, TypeError):
            print("The integral is divergent!")

    integrate_with_graph()

else:
    x = sp.symbols('x')
    f_input = input("Enter the function you want to integrate (in terms of x): ")
    f_input = sp.parse_expr(f_input)

    try:
        f = sp.sympify(f_input)
    except sp.SympifyError:
        print("Invalid input. Please enter a valid mathematical expression.")
        exit()

    integral_f = sp.integrate(f, x)
    integral_f_evaluated = integral_f.doit()

    print("Step-by-step integration of f(x):")
    for step in integral_f_evaluated.args:
        sp.pretty_print(step)

    print("\nFinal result of the indefinite integral of f(x):")
    sp.pretty_print(integral_f_evaluated)
