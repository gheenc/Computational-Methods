# %%
import time
import matplotlib.pyplot as plt
import random
import math
from faker import Faker
from operator import itemgetter
from concurrent.futures import ProcessPoolExecutor
import heapq
import multiprocessing

# %% -----------------------------
# SERIAL MERGE SORT
def alg_new(data, key):
    if len(data) <= 1:
        return data
    else:
        split = len(data) // 2
        left = alg_new(data[:split], key)
        right = alg_new(data[split:], key)
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
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
patient_ids = [123, 456, 798, 234, 567, 891]
patient_names = ["John Smith", "Jane Doe", "Taylor Swift", "Harry Styles", "Mallory Swanson", "Jane Goddall"]

#zipped data into list
patient_data = list(zip(patient_ids, patient_names))
# print(patient_data)

#%%
# print(alg_new(patient_data, key=itemgetter(0)))
#%%
# %%

# %% -----------------------------
# CHUNKIFY HELPER
def chunkify(data, num_chunks):
    avg = math.ceil(len(data) / num_chunks)
    return [data[i:i + avg] for i in range(0, len(data), avg)]

# %% -----------------------------
# SORT CHUNK FUNCTION (safe for multiprocessing)
def sort_chunk_with_key(args):
    chunk, key = args
    return alg_new(chunk, key)

# %% -----------------------------
# PARALLEL MERGE SORT (safe for Windows)
def parallel_merge_sort(data, key, num_workers=None):
    if len(data) <= 1:
        return data
    
    if len(data) < 500_00:
        alg_new(data, key)
    
    num_workers = num_workers or min(4, multiprocessing.cpu_count())
    chunks = chunkify(data, num_workers)

    # Bundle each chunk with key for processing
    chunk_args = [(chunk, key) for chunk in chunks]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        sorted_chunks = list(executor.map(sort_chunk_with_key, chunk_args))

    return list(heapq.merge(*sorted_chunks, key=key))

# %% -----------------------------
# TIMING FUNCTION
def time_algorithms_on_patients(dataset):
    start_time = time.perf_counter()
    parallel_merge_sort(dataset, key=itemgetter(0))
    stop_time = time.perf_counter()
    total_time_p = stop_time - start_time
    print(f"Parallel calculation took {total_time_p:.4f} seconds")

    start_time = time.perf_counter()
    alg_new(dataset, key=itemgetter(0))
    stop_time = time.perf_counter()
    total_time_s = stop_time - start_time
    print(f"Serial calculation took {total_time_s:.4f} seconds")

    return total_time_p, total_time_s

# %% -----------------------------
# PLOTTING FUNCTION
def plot_timings(n_values, all_parallel_times, all_serial_times):
    plt.figure()
    plt.loglog(n_values, all_parallel_times, label='Parallel merge sort', marker='o', linestyle='-', color='blue')
    plt.loglog(n_values, all_serial_times, label='Serial merge sort', marker='o', linestyle='-', color='red')

    plt.xlabel('Dataset Size')
    plt.ylabel('Time (seconds)')
    plt.title('Serial vs Parallel Merge Sort')
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.savefig('parallelization_better2.png')
    plt.show()

# %% -----------------------------
# MAIN PROGRAM
if __name__ == '__main__':
    Faker.seed(900)
    fake = Faker()

    dataset_sizes = [100000, 250000, 500000, 1000000, 2000000, 5000000]
    length_based_data = []

    def generate_patient_data(size):
        generate_number = lambda: random.randint(100000, 999999)
        return [(generate_number(), fake.name()) for _ in range(size)]

    for size in dataset_sizes:
        length_based_data.append(generate_patient_data(size))

    all_parallel_times = []
    all_serial_times = []

    for dataset in length_based_data:
        print(f"\nRunning sort on dataset with {len(dataset)} patients")
        p_time, s_time = time_algorithms_on_patients(dataset)
        all_parallel_times.append(p_time)
        all_serial_times.append(s_time)

    plot_timings(dataset_sizes, all_parallel_times, all_serial_times)
