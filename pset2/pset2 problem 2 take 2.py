# %%
# %%
#adapt the alg2 merge sort to sort based on key value relationship
#ex: dataset of patient_id corresponding to patient_data. Sort by patient_id with its respective patient_data aligned
#should accept data as list of tuples or list of dictionaries
#provide examples

#created individual data
#https://www.geeksforgeeks.org/python/python-create-a-list-of-tuples/
#Asked ChatGPT how to retain type as tuple
import multiprocessing
from multiprocessing import Process
import time
import plotnine as p9
from plotnine import geom_bar, ggplot, aes, geom_histogram, geom_smooth, theme_bw, labs
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import statistics
from statistics import mean
import random
import string
import math
from faker import Faker
from operator import itemgetter

# %%
patient_ids = [123, 456, 798, 234, 567, 891]
patient_names = ["John Smith", "Jane Doe", "Taylor Swift", "Harry Styles", "Mallory Swanson", "Jane Goddall"]

#zipped data into list
patient_data = list(zip(patient_ids, patient_names))
print(patient_data)

# %%
    
# https://stackoverflow.com/questions/60508591/sorting-list-of-tuples-using-merge-sort
# Google how to add key to merge sort. Merged Copilot Search result with class alg2
# Used ChatGPT to clean up errors and determine how to call a key

# alg mashed
#call alg_new(dataset, position of key wanting to sort data by)
def alg_new(data, key):
    if len(data) <= 1: 
        return data
    else:
        split = len(data) // 2
        left = alg_new(data[:split], key)
        right = alg_new(data[split:], key)
        result = []
        i=j=0
    while i < len(left) and j < len(right):
        if key(left[i]) < key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j +=1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# %%
alg_new(patient_data, key=itemgetter(0))
#Need to add so that it sorts tuple in the merge sort?
# Provide examples demonstrating that your code works. Be clear how you know that it works.

# %%
# Implement a parallel version of your modified merge sort algorithm, 
# splitting the workload across multiple processing cores
# Used ChatGPT to ensure full understading of question
# Asked ChatGPT where to imput multiprocessor.pool in current function and how to choose between .ap or .async
# https://www.geeksforgeeks.org/python/parallel-processing-in-python/

def alg_parallel(data, key):
    if len(data) <= 1: 
        return data
    else:
        split = len(data) // 2
        left_half = data[:split]
        right_half = data[split:]
    with multiprocessing.Pool(processes=2) as pool: #creates two processes #cput count and multiprocessing at top level suggested by ChatGPT
       left_sorted = pool.apply_async(alg_new, (left_half, key)) #apply_async becuase recursively calling and splitting different data 
       right_sorted = pool.apply_async(alg_new, (right_half, key))
       left = left_sorted.get()
       right = right_sorted.get()
    result = []
    i = j = 0
    while i <len(left) and j < len(right):
       if key(left[i]) < key(right[j]):
          result.append(left[i])
          i += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

# %%
if __name__ == '__main__': #guards against repeat recursion
    from operator import itemgetter
    start_time = time.perf_counter()
    alg_parallel(patient_data, key=itemgetter(0))
    stop_time = time.perf_counter()
    parallel_time = []
    print(f"Calculation took {stop_time - start_time} seconds") #times paralellization 
    main()

# %%
# Measure and compare the performance of your parallel algorithm with the original serial version.
if __name__ == '__main__': #guards against repeat recursion
    start_time = time.perf_counter()
    alg_parallel(patient_data, key=itemgetter(o))
    stop_time = time.perf_counter()
    parallel_time = []
    print(f"Parallel calculation took {stop_time - start_time} seconds") #times paralellization 

start_time = time.perf_counter()
alg_new(patient_data, [0])
stop_time = time.perf_counter()
serial_time = []
print(f"Serial calculation took {stop_time - start_time} seconds")


# %%
Faker.seed(900) #seed makes them the same everytime
fake = Faker()

# Dictionary to map digit length to its corresponding function
digit_generators = {
    1: lambda: random.randint(1, 9),
    2: lambda: random.randint(10, 99),
    3: lambda: random.randint(100, 999),
    4: lambda: random.randint(1000, 9999),
    5: lambda: random.randint(10000, 99999),
    6: lambda: random.randint(100000, 999999),
    7: lambda: random.randint(1000000, 9999999),
    8: lambda: random.randint(10000000, 99999999),
    9: lambda: random.randint(100000000, 999999999)
}

def generate_patient_data(num_patients_per_group, number_of_digits, target_list): #takes in wanted number of patients, how many digits in id and what list to save to 
    if number_of_digits not in digit_generators:
        raise ValueError("number_of_digits must be between 1 and 9")
    if target_list is None:
        target_list  = []
    generate_number = digit_generators[number_of_digits] #generates number based on given digit
    for _ in range(num_patients_per_group): 
        patient_id = generate_number() #saves random number as patient id
        name = fake.name() #creates fake name
        target_list.append((patient_id, name)) #appends both to wanted list
    return target_list

# %%
#generate fake data of varying n lengths. Store in data dictionary that can be sorted into later to retrieve wanted digit length codes

digit_data = {}

for digit in range(1, 10):
    digit_data[digit] = []
    generate_patient_data(100, digit, digit_data[digit])

# %%
#make lists of each varying id length for testing
one_digit_patients = digit_data[1]
two_digit_patients = digit_data[2]
three_digit_patients = digit_data[3]
four_digit_patients = digit_data[4]
five_digit_patients = digit_data[5]
six_digit_patients = digit_data[6]
seven_digit_patients = digit_data[7]
eight_digit_patients = digit_data[8]
nine_digit_patients = digit_data[9]

# %%
def time_new(digit):
    start_time = time.perf_counter()
    alg_new(digit_data[digit], [0])
    stop_time = time.perf_counter()
    total_time = (stop_time - start_time)
    serial_time_[digit] = []
    serial_time_[digit].append(total_time)
    print(f"Serial calculation took {stop_time - start_time} seconds")


# %%

#Visualize the results: Use a log-log plot to compare the time complexity of the parallel and serial versions, 
# focusing on how the parallel implementation scales with larger datasets.
# For full credit, demonstrate that your parallel algorithm runs in no more than 70% of the time of the serial algorithm on sufficient large datasets. 

# %%
#code to time each  WRONG

#time serial and time parallel for each length of patient data
if __name__ == '__main__': #guards against repeat recursion
    start_time = time.perf_counter()
    alg_parallel(one_digit_patients, key=itemgetter(0))
    stop_time = time.perf_counter()
    one_digit_parallel_time= []
    total_time = (stop_time - start_time)
    one_digit_parallel_time.append(total_time)

def time_new(digit):
    start_time = time.perf_counter()
    alg_new(digit_data[digit], [0])
    stop_time = time.perf_counter()
    total_time = (stop_time - start_time)
    serial_time_[digit] = []
    serial_time_[digit].append(total_time)
    print(f"Serial calculation took {stop_time - start_time} seconds")


