# %%
import math
import numpy as np
import requests

# %%
# implement 2D version of gradient descent algorithm to find optimal choices of a and b
# used ChatGPT to ensure adjustment of code from slide(8) to 2D version and understand stopping criteria and implement error as a returned value 

def f(a, b):
    a = round(a, 6) # sending shorter floats to be nicer to server 
    b = round(b, 6)
    r = (requests.get(f"http://ramcdougal.com/cgi-bin/error_function.py?a={a}&b={b}", headers={"User-Agent": "MyScript"}).text)
    return float(r)
def fprime_a(a, b):
    return (f(a+h, b) - f(a, b)) / h 
def fprime_b(a, b):
    return (f(a, b+h) - f(a, b)) / h 

h= .01 # did not want too small of error to avoid computational errors
gamma = .25 # gamma controls how big of step
epsilon = 1e-4 # stopping criteria of stopping when updates being too small
error_tolerance = 1e-4

a, b = .4, .2 # initial guess for  both
current_run = []
previous_error = None

for i in range(15):
    current_error = f(a, b)
    current_run.append({"a":a, "b":b, "error":current_error}) 

    if previous_error is not None and abs(previous_error - current_error) < error_tolerance:
        print("Error change too small")
        break
 
    new_a = a - gamma * fprime_a(a, b) # doing gradient descent and determining new a and b
    new_b = b - gamma * fprime_b(a, b) 

    if np.sqrt((new_a-a) **2 + (new_b - b)**2) < epsilon: # stopping criteria of when updates are too small 
        print("Updates too small")
        break

    a, b = new_a, new_b
    print(f"a:{a}, b:{b}, error:{current_error}")
print(f"lowest error run: {min(current_run, key=lambda x:x['error'])}") # prints run with smallest error 


# %%
# EXPAIN HOW ESTIMATE GRADIENT

# gamma - how much move along gradient each iteration - controls speed - too large: overshoot; too small: slow convergence
# GAMMA - best convergence at .25; far off at 1 and .5 and too small at .01 and .1

# h - error, estimating derivative numerically - controls accuracy - too large: inaccurate; too small: numerical precision errors
# ERROR - .01 got us the closest 

# epsilon - minimum change in varibales to stop iteration - too large: stops too early, too small: too many iterations 
# EPSILON - chose 1e-4 becuase no noticeable difference after (1e-5 etc)

# range - how many iterations - too many: unnecessary , too few: don't see convergence
# RANGE -  minimal differences past .000 decimal place after 8 runs, rounded up to 10



