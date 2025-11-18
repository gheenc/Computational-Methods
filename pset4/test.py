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

