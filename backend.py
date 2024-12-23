import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, jsonify
from flask_cors import CORS
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
import base64
import io

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Add route handler for OPTIONS requests at the "/" endpoint
@app.route('/', methods=['OPTIONS'])
def handle_options():
    return '', 200, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

# Add route handler for OPTIONS requests at the "/integrate" endpoint
@app.route('/integrate', methods=['OPTIONS'])
def handle_integrate_options():
    return '', 200, {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

def check_domain(func, low, upp):
    # Define the domain of trigonometric and inverse trigonometric functions
    corner_limits = {
        'asin': Interval(-1, 1),
        'acos': Interval(-1, 1),
        'atan': Interval(float('-inf'), float('inf')),
        'acsc': Interval.open(-oo, -1) + Interval.open(1, oo),
        'asicant': Interval.open(-oo, -1) + Interval.open(1, oo),
        'acot': Interval(float('-inf'), float('inf')),
        'sin': Interval(float('-inf'), float('inf')),
        'tan': Interval(float('-inf'), float('inf')),
        'cos': Interval(float('-inf'), float('inf')),
        'csc': Interval.open(-oo, 0) + Interval.open(0, oo),
        'sicant': Interval.open(-oo, -pi/2) + Interval.open(-pi/2, pi/2) + Interval.open(pi/2, oo),
        'cot': Interval.open(-pi, 0) + Interval.open(0, pi)
    }

           # # Check if the limits are within the domain
    func_name = func.func.__name__
    if func_name in corner_limits:
        domain = corner_limits[func_name]
        if domain.contains(low) and domain.contains(upp):
            if func_name == 'csc':
                for i in range (0,2222):
                 if low <= i*pi <= upp or low <= -i*pi <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi at value of ",i*pi)
                    return False
               
                 else:
                    continue
                return True
           
            elif func_name == 'sicant':
                for i in range (0,2222):
                 if  low <= (2*i+1)*(pi/2) <= upp or low <= -(2*i+1)*(pi/2) <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi/2 at value of ",i*pi/2)
                    return False
                 else :
                    continue
                return True
            elif func_name == 'tan':
                for i in range (1,2222):
                 if  low <= i*(pi/2) <= upp or low <= -i*(pi/2) <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi/2 at value of ",(i+1)*pi/2)
                    return False
                 else :
                    continue
                return True    
            elif func_name == 'cot':
                for i in range (0,2222):
                 if low <= i*pi <= upp :#or low <= -i*(pi) <= upp:
                    print("The integral is divergent due to presence of limit of integral multiple of pi at value of ",i*pi)
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
            # if func.is_real in (func_low,func_upp):
            #    return True
            # else:
            #    return False
        # If the function is defined at both limits, return True
            if func_low.is_real and func_upp.is_real:
              return True            
            else:
              return False
     except Exception as e:
           print("An error occurred while checking the domain:", e)
           return False
       


@app.route('/integrate', methods=['POST'])   
def integrate_with_graph():
    data = request.get_json()

    abc = data.get('function')
    if not abc:
        return jsonify({'error': "Function expression is empty."}), 400

    
    import math
    abc = abc.replace('cosec', 'csc')
    abc = abc.replace('sec', 'sicant')
    abc = abc.replace('asec', 'asicant')
    abc = abc.replace('acosec', 'acsc')
    abc = abc.replace('pi', str(math.pi))
    abc = abc.replace('e', str(math.e))

    if 'e^' in  abc:
       import math
       abc = aba.replace('pi', str(math.pi))
       abc = abc.replace('^', '**')
       abc = abc.replace('acosec(', 'arcsin(1/')
       abc = abc.replace('acot(', 'arctan(1/')
       abc = abc.replace('asec(', 'arccos(1/')
       abc = abc.replace('cosec', '1/sin')
       abc = abc.replace('sec', '1/cos')
       abc = abc.replace('cot', '1/tan')
    

    
       e = math.e
    try:
        func = sympify(abc)
    except Exception as e:
        return jsonify({'error': "Failed to parse function expression: {}".format(e)}), 400

    low = data.get('lower_bound')
    low = low.replace('pi', str(math.pi))
    low = low.replace("π", str(math.pi))
    low = float(eval(low))
    upp = data.get('upper_bound')
    upp = upp.replace('pi', str(math.pi))
    upp = upp.replace("π", str(math.pi))
    upp = upp.replace("inf", str(math.inf))
    upp = float(eval(upp))


        
    try:       
        
        g = lambdify(x, func, modules=['numpy'])
        x_vals = np.linspace(low, upp, 1000)
        y_vals = g(x_vals)

        fig, ax = plt.subplots()
        plt.xlabel('$x$')
        plt.ylabel("$f(x)$")
        plt.grid()
        plt.plot(x_vals, y_vals, color='blue')

        # Split the polygon into two parts based on the sign of y
        ix = np.linspace(low, upp, 2000)
        iy = [g(i) for i in ix]
        verts = list(zip(ix, iy))
        verts.insert(0, (low, 0))
        verts.append((upp, 0))
        
        pos_verts = [(x, y) for x, y in verts if y >= 0]
        neg_verts = [(x, 0) if y >= 0 else (x,y) for x,y in verts]
        
        # Plot positive area in green and negative area in red
        poly_pos = Polygon(pos_verts, facecolor='green', alpha=0.5)
        poly_neg = Polygon(neg_verts, facecolor='red', alpha=0.5)
        ax.add_patch(poly_pos)
        ax.add_patch(poly_neg)

    # Define the function using lambdify
        g = lambdify(x, func, modules=['numpy', {'asin': lambda x: np.arcsin(x),
                                              'acos': lambda x: np.arccos(x),
                                              'atan': lambda x: np.arctan(x),
                                              'csc': lambda x: 1 / np.sin(x),
                                              'sicant': lambda x: 1 / np.cos(x),
                                              'cot': lambda x: 1 / np.tan(x),
                                              'sin': lambda x: sin(x),
                                              'cos': lambda x: cos(x),
                                              'tan': lambda x: tan(x),
                                              'acsc': lambda x: np.arcsin(1/x),
                                               'asicant': lambda x: np.arccos(1/x)
                                            }])

        # Limit the plotting range to x = 10 if one of the limits is infinity
        if math.isinf(low) or math.isinf(upp):
            low = max(-10, low)  # Limit the lower bound
            upp = min(10, upp)    # Limit the upper bound

        # Calculate x and y values
        x_vals = np.linspace(low, upp, 1000)
        y_vals = g(x_vals)

        # Set up the plot
        fig, ax = plt.subplots()
        plt.xlabel('$x$')
        plt.ylabel("$f(x)$")
        plt.grid()
        plt.plot(x_vals, y_vals, color='blue')

        # Fill the area under the curve with positive area in green and negative area in red
        ix = np.linspace(low, upp, 1000)
        iy = g(ix)
        verts = [(low, 0)]
        positive_verts = [(low, 0)]
        negative_verts = [(low, 0)]
        prev_y = 0
        for x_val, y_val in zip(ix, iy):
            if y_val >= 0:
                verts.append((x_val, y_val))
                positive_verts.append((x_val, y_val))
            else:
                verts.append((x_val, 0))
                verts.append((x_val, y_val))
                negative_verts.append((x_val, y_val))
            prev_y = y_val
        verts.append((upp, 0))
        positive_verts.append((upp, 0))
        negative_verts.append((upp, 0))

        poly_pos = Polygon(positive_verts, facecolor='green', edgecolor='none')
        poly_neg = Polygon(negative_verts, facecolor='red', edgecolor='none')
        poly_total = Polygon(verts, facecolor='0.9', edgecolor='0.5')

        ax.add_patch(poly_total)
        ax.add_patch(poly_pos)
        ax.add_patch(poly_neg)

        result, _ = quad(g, low, upp)
        frac = fr.Fraction(result)
        abc = abc.replace('sicant', 'sec')
        abc = abc.replace('csc', 'cosec')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Encode the image as base64
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')

        plt.close(fig)

        if (result < 10 ** (-16) and result>0):
            result=0.0
        return jsonify({'result': result, 'frac': frac, 'graphData': list(y_vals), 'graph': img_base64}), 200
        
    except Exception as e:
         return jsonify({'error': "An error occurred while calculating the integral: {}".format(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)