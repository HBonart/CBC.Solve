# Use this for replacing stuff.

value1 = "-3*pi*C*sin(pi*t)**2*cos(pi*Y) + 6*pi*C*X*sin(pi*t)**2*cos(pi*Y) + 8*C**2*sin(pi*Y)**2*sin(pi*t)**4 - 16*X*C**2*sin(pi*Y)**2*sin(pi*t)**4 + X*pi**2*C**2*sin(pi*Y)**2*sin(pi*t)**4 - 6*pi**2*C**2*X**3*cos(pi*Y)**2*sin(pi*t)**4 - 3*X*pi**2*C**2*cos(pi*Y)**2*sin(pi*t)**4 - 3*pi**2*C**2*X**2*sin(pi*Y)**2*sin(pi*t)**4 + 2*pi**2*C**2*X**3*sin(pi*Y)**2*sin(pi*t)**4 + 9*pi**2*C**2*X**2*cos(pi*Y)**2*sin(pi*t)**4"


value2 = "2*C*sin(pi*t)**2*sin(pi*Y) - 200*C*pi**2*X**2*cos(pi*t)**2*sin(pi*Y) - 196*C*X*pi**2*sin(pi*t)**2*sin(pi*Y) - 8*pi*C**2*sin(pi*t)**4*cos(pi*Y)*sin(pi*Y) + 196*C*pi**2*X**2*sin(pi*t)**2*sin(pi*Y) + 200*C*X*pi**2*cos(pi*t)**2*sin(pi*Y) - 72*pi**2*C**3*X**3*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) - 40*pi*C**2*X**2*sin(pi*t)**4*cos(pi*Y)*sin(pi*Y) - 24*pi**3*C**2*X**3*sin(pi*t)**4*cos(pi*Y)*sin(pi*Y) - 18*pi**4*C**3*X**4*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) - 8*X*pi**2*C**3*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) - 6*pi**4*C**3*X**6*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) + 6*pi**4*C**3*X**3*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) + 12*pi**3*C**2*X**2*sin(pi*t)**4*cos(pi*Y)*sin(pi*Y) + 12*pi**3*C**2*X**4*sin(pi*t)**4*cos(pi*Y)*sin(pi*Y) + 18*pi**4*C**3*X**5*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) + 36*pi**2*C**3*X**4*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) + 40*pi*X*C**2*sin(pi*t)**4*cos(pi*Y)*sin(pi*Y) + 44*pi**2*C**3*X**2*cos(pi*Y)**2*sin(pi*t)**6*sin(pi*Y) + 12*C**3*sin(pi*Y)**3*sin(pi*t)**6 - 48*X*C**3*sin(pi*Y)**3*sin(pi*t)**6 + 48*C**3*X**2*sin(pi*Y)**3*sin(pi*t)**6 - 10*pi**2*C**3*X**2*sin(pi*Y)**3*sin(pi*t)**6 - 8*pi**2*C**3*X**4*sin(pi*Y)**3*sin(pi*t)**6 + 2*X*pi**2*C**3*sin(pi*Y)**3*sin(pi*t)**6 + 16*pi**2*C**3*X**3*sin(pi*Y)**3*sin(pi*t)**6"

values = [value1, value2]
replacements = {"sin(pi*t)**2": "pow(sin(pi*t), 2)",
                "sin(pi*t)**4": "pow(sin(pi*t), 4)",
                "sin(pi*t)**6": "pow(sin(pi*t), 6)",
                "sin(pi*Y)**2": "pow(sin(pi*Y), 2)",
                "sin(pi*Y)**3": "pow(sin(pi*Y), 3)",
                "sin(pi*Y)**4": "pow(sin(pi*Y), 4)",
                "sin(pi*Y)**6": "pow(sin(pi*Y), 6)",
                "cos(pi*Y)**2": "pow(cos(pi*Y), 2)",
                "cos(pi*t)**2": "pow(cos(pi*t), 2)",
                "cos(pi*t)**4": "pow(cos(pi*t), 4)",
                "cos(pi*t)**6": "pow(cos(pi*t), 6)",
                "pi**2": "pow(pi, 2)",
                "pi**3": "pow(pi, 3)",
                "pi**4": "pow(pi, 4)",
                "C**2": "pow(C, 2)",
                "C**3": "pow(C, 3)",
                "X**2": "pow(X, 2)",
                "X**3": "pow(X, 3)",
                "X**4": "pow(X, 4)",
                "X**5": "pow(X, 5)",
                "X**6": "pow(X, 6)",
                }
for (i, value) in enumerate(values):
    for (key, repl) in replacements.iteritems():
        value = value.replace(key, repl)
    print "values[%d] = %s;" % (i, value)


