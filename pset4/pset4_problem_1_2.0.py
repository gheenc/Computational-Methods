# %%
import math
import numpy as np
import requests

# %%
# implement 2D version of gradient descent algorithm to find optimal choices of a and b
# used ChatGPT to ensure adjustment of code from slide(8) to 2D version and understand stopping criteria

f=lambda a, b:(a-2)**2 + (b+3)**2 # both variables 
h= .01 # did not want too small of error to avoid computational errors 
fprime_a=lambda a, b:(f(a+h, b)-f(a, b))/h
fprime_b=lambda a, b:(f(a, b+h)-f(a, b))/h
gamma = .25 # gamma controls how big of step
a, b = 0, 0 # initial guess for  both

epsilon = 1e-4 # stopping criteria of stopping when updates being too small
for i in range(30):
    grad = np.array([fprime_a(a, b), fprime_b(a, b)])
    new_a = a - gamma * grad[0]
    new_b = b - gamma * grad[1]

    if np.sqrt((new_a-a) **2 + (new_b - b)**2) < epsilon:
        break

    a, b = new_a, new_b

for i in range(10):
    print(a, b) # prints values at the start of the iteration
    a=a-gamma*fprime_a(a,b)
    b=b-gamma*fprime_b(a,b)

# %%
# EXPAIN HOW ESTIMATE GRADIENT

# gamma - how much move along gradient each iteration - controls speed - too large: overshoot; too small: slow convergence
# GAMMA - best convergence at .25; far off at 1 and .5 and too small at .01 and .1

# h - error, estimating derivative numerically - controls accuracy - too large: inaccurate; too small: numerical precision errors
# ERROR - .01 got us the closest 

# epsilon - minimum change in varibales to stop iteration - too large: stops too early, too small: too many iterations 
# EPSILON - chose 25 because too small ~ 10 was not as close as 25, but there was not much difference between 25 and 50, 30 might be the best
# EPSILON - chose 1e-4 becuase no noticeable difference after (1e-5 etc)

# range - how many iterations - too many: unnecessary , too few: don't see convergence
# RANGE -  minimal differences past .000 decimal place after 8 runs, rounded up to 10

# %%
a = 0.4
b = 0.2
float(requests.get(f"http://ramcdougal.com/cgi-bin/error_function.py?a={a}&b={b}", headers={"User-Agent": "MyScript"}).text)

# %%
# call api
# asked ChatGPT how to query an API - gave def that will call the api

a = 0.4
b = 0.2
float(requests.get(f"http://ramcdougal.com/cgi-bin/error_function.py?a={a}&b={b}", headers={"User-Agent": "MyScript"}).text)

# define error function
h = 0.01

def fprime_a(a, b):
    return (f(a+h, b) - f(a, b)) /h
def fprime_b(a, b):
    return (f(a, b+h) - f(a, b))/h

# define gradient descent paraments 
gamma = 0.25
a, b = 0, 0
epsilon = 1e-6

for i in range(10):       
    grad_a = fprime_a(a, b)
    grad_b = fprime_b(a, b)
    
    new_a = a - gamma * grad_a
    new_b = b - gamma * grad_b

    if np.sqrt((new_a - a)**2 + (new_b - b)**2) < epsilon:
        break

    a, b = new_a, new_b
    print(a, b)



# %%



