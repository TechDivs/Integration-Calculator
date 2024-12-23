import sympy as sp

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