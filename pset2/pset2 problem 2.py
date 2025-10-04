#adapt the alg2 merge sort to sort based on key value relationship
#ex: dataset of patient_id corresponding to patient_data. Sort by patient_id with its respective patient_data aligned
#should accept data as list of tuples or list of dictionaries
#provide examples

#created individual data
#https://www.geeksforgeeks.org/python/python-create-a-list-of-tuples/
#Asked ChatGPT how to retain type as tuple

patient_ids = [123, 456, 798, 234, 567, 891]
patient_names = ["John Smith", "Jane Doe", "Taylor Swift", "Harry Styles", "Mallory Swanson"]

#zipped data into list of tuples
patient_data = zip(patient_ids, patient_names)

#sort by first item in tuple
tuple_patient_data = tuple(sorted(patient_data))
print(tuple_patient_data)

#alg provided
def alg_provided(data):
  if len(data) <= 1:
    return data
  else:
    split = len(data) // 2
    left = iteralg2(data[:split]))
    right = iter(alg2(data[split:]))
    result = []
    # note: this takes the top items off the left and right piles
    left_top = next(left)
    right_top = next(right)
    while True:
      if left_top < right_top:
        result.append(left_top)
        try:
          left_top = next(left)
        except StopIteration:
          # nothing remains on the left; add the right + return
          return result + [right_top] + list(right)
      else:
        result.append(right_top)
        try:
          right_top = next(right)
        except StopIteration:
          # nothing remains on the right; add the left + return
          return result + [left_top] + list(left)
        
# https://stackoverflow.com/questions/60508591/sorting-list-of-tuples-using-merge-sort
# Google how to add key to merge sort. Merged Copilot Search result with class alg2
# Used ChatGPT to clean up errors

# alg mashed
def alg_new(data, key=lambda x: x):
    tupled_data = tuple(sorted(data)) #sorts data and creates tuple
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
  
alg_new(tuple_patient_data, key=lambda x:x[0])
#Need to add so that it sorts tuple in the merge sort?
# Provide examples demonstrating that your code works. Be clear how you know that it works.

