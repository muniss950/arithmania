
import sympy
expr1 = sympy.sympify("x^2 + 2*x + 1")
expr2 = sympy.sympify("(x+1)^2")
print(sympy.simplify(expr1 - expr2) == 0)  # True if equivalent
