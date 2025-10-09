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
# print(patient_data)

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
# print(alg_new(patient_data, key=itemgetter(0)))

#Need to add so that it sorts tuple in the merge sort?
# Provide examples demonstrating that your code works. Be clear how you know that it works.

# %%
# Implement a parallel version of your modified merge sort algorithm, 
# splitting the workload across multiple processing cores
# Used ChatGPT to ensure full understading of question
# Asked ChatGPT where to imput multiprocessor.pool in current function and how to choose between .ap or .async
# https://www.geeksforgeeks.org/python/parallel-processing-in-python/

def alg_parallel(data, key, cutoff=1000):
    if len(data) <= 1: 
        return data

    split = len(data) // 2
    left_half = data[:split]
    right_half = data[split:]

    if len(data) >= cutoff:
        with multiprocessing.Pool(processes=6) as pool:
            left_sorted = pool.apply_async(alg_new, (left_half, key))
            right_sorted = pool.apply_async(alg_new, (right_half, key))
            left = left_sorted.get()
            right = right_sorted.get()
    else:
        left = alg_new(left_half, key)
        right = alg_new(right_half, key)

    result = []
    i = j = 0
    while i <len(left) and j < len(right):
        if key(left[i]) < key(right[j]):
          result.append(left[i])
          i += 1
        else:
            result.append(right[j])
            j += 1    
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# %%
#generate fake data of varying n lengths. Store in data dictionary that can be sorted into later to retrieve wanted digit length codes

#%%
def time_algorithms_on_patients(dataset):
    start_time = time.perf_counter()
    alg_parallel(dataset, key=itemgetter(0), cutoff=10000)
    stop_time = time.perf_counter()
    total_time_p = stop_time - start_time
    print(f"Parallel calculation took {total_time_p} seconds") #times paralellization

    start_time = time.perf_counter()
    alg_new(dataset, key=itemgetter(0))
    stop_time = time.perf_counter()
    total_time_s = stop_time - start_time
    print(f"Serial calculation took {total_time_s} seconds")

    return total_time_p, total_time_s

# %%
def plot_timings(n_values, all_parallel_times, all_serial_times):
    plt.figure()
    plt.loglog(n_values, all_parallel_times, label='Parallelized merge', marker='o', linestyle='-', color='blue')
    plt.loglog(n_values, all_serial_times, label='Serial merge', marker='o', linestyle='-', color ='red')

    plt.xlabel('Values')
    plt.ylabel('Time Elapsed (seconds)')
    plt.title('Time Elapsed Using Parallel and Serial Merge Sorts')
    plt.legend()

    plt.grid(True, which="both", ls="--")
    h = plt.savefig('parallelization.png')
    plt.show()
# %%
if __name__ == '__main__': #guards against repeat recursion
    import matplotlib.pyplot as plt
    Faker.seed(900) #seed makes them the same everytime
    fake = Faker()

    dataset_sizes = [100, 1000, 10000, 25000, 50000, 75000, 100000, 250000]
    length_based_data = []

    def generate_patient_data(size, number_of_digits=6):
        generate_number = lambda: random.randint(100000, 999999)  #generates number based on given digit
        data = []
        for _ in range(size): 
            patient_id = generate_number() #saves random number as patient id
            name = fake.name() #creates fake name
            data.append((patient_id, name)) #appends both to wanted list
        return data

    for size in dataset_sizes:
        length_based_data.append(generate_patient_data(size, 6))
        
    all_parallel_times = []
    all_serial_times = []

    for i, dataset in enumerate(length_based_data):
        print(f"Running sort on dataset with {len(dataset)} patients")
        p_time, s_time = time_algorithms_on_patients(dataset)
        all_parallel_times.append(p_time)
        all_serial_times.append(s_time)

    plot_timings(dataset_sizes, all_parallel_times, all_serial_times)
# %%
#Visualize the results: Use a log-log plot to compare the time complexity of the parallel and serial versions, 
# focusing on how the parallel implementation scales with larger datasets.
# For full credit, demonstrate that your parallel algorithm runs in no more than 70% of the time of the serial algorithm on sufficient large datasets. 

# %%
#code to time each  WRONG

#time serial and time parallel for each length of patient data



