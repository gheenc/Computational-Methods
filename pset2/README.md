## Problem 1##
**a.** I implemented the bitarray library and set the size of the bitarray to be large enough to accomodate the size of the English words repository and set all bits to 0. 
```python
#asked ChatGPT how large my bitarray needs to be to hold the large dataset
#isn't this very large and will cause hash collisions?

size = 360000
bits = bitarray(size)
bits.setall(0)
#bits n should be larger than data set size
```
I then implemented the bloom filter.

```python 
class BloomFilter(object):
    #uses murmur3 hash function
    def __init__(self, items_count, fp_prob):
        #items_count number of items expected to be sotred in bloom filter
        #fp_prob false positive probability in decimal
        self.fp_prob = fp_prob #false positive in decimal; optional if size is fixed
        self.size = 3600000 #set size of bitarray
        self.hash_count = self.get_hash_count(self.size, items_count) #number of hash function
        self.bit_array = bitarray(self.size) #bit array of given size
        self.bit_array.setall(0) #initialize all bits as 0
    def add(self, item):
        #add an item in the filter
        digests = []
        for i in range(self.hash_count): #create digest for given item, i seed for mmh3.hash; with different seed digest created is different
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)
            self.bit_array[digest] = True #set the bit True in bit_array
    def check(self, item):
        #check for item in filteer
        for i in range(self.hash_count):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                #if any of bit is False, not present; else possibility it exists
                return False
        return True
    def get_hash_count(self, m, n):
        #return hash function for formula
        #m integer size of array
        #n integer number of items expected to be stored
        k = (m/n) * math.log(2)
        return int(k)


# https://www.geeksforgeeks.org/python/bloom-filters-introduction-and-python-implementation/
```
For each word in the word list, I applied all three hash functions and set the corresponding hashes 
TEST?

```python
#for each word in the list, apply all three hash functions and set the corresponding bits in the bitarray.
#All return in [0, size] where size is some integer specified elsewhere

def my_hash(s):
    return int(sha256(s.lower().encode()).hexdigest(), 16) % size
def my_hash2(s):
    return int(blake2b(s.lower().encode()).hexdigest(), 16) % size
def my_hash3(s):
    return int(sha3_256(s.lower().encode()).hexdigest(), 16) % size

for word in words: 
    index1 = my_hash(word)
    index2 = my_hash2(word)
    index3 = my_hash3(word)
    bits[index1] = 1
    bits[index2] = 1
    bits[index3] = 1
    
#Asked ChatGPT is I answered all parts of the question and modified code (define size) 
```

**b.** I first created a function that replaced single characters in a word and tested it with cat. There are 75 combinations of single-character substitutions for cat which I checked with length. 
```python
#b. Create a function that checks all possible single-character substitutions for a given word using the Bloom filter. 
# Return words flagged by the filter as potential matches. 

#I need the function to take in each word, replace a single character, compare to the rest of list and return if it is a match. Repeat for all letter combinations

#Asked ChatGPT how to make a function that replces single character in given word
def single_char_changes(word): 
    replaced_words = []
    for i in range(len(word)):
        for letter in string.ascii_lowercase:
            if word[i] != letter:
                changed = word[:i] + letter + word[i+1:]
                replaced_words.append(changed)
    return replaced_words

#Tested that the function does single character substitution for word given
print(single_char_changes('cat'))
len(single_char_changes('cat'))
```
I then added all the words to the bloom filter and checked that they were added correctly by printing a word I knew was in the set and a word I knew was not. 
```python
#BloomFilter(number of items, false positive)
#https://www.geeksforgeeks.org/python/bloom-filters-introduction-and-python-implementation/
bloomf = BloomFilter(3600000, 0.05)

#add words to BloomFilter
for word in words:
    bloomf.add(word)

#create the function to check if word against bloom filter
def test_in_filter(test):
    return test in words if bloomf.check(test) else False

#test with words known in filter and known not in filter
print(test_in_filter('abandoner'))
print(test_in_filter('carolinejk'))
```

I then combined the single character function and comparing the words produced to the words in the Bloom into a new function.
```python
#create full function
#Asked ChatGPT 
def spell_check(word):
    def single_char_changes(word): 
        replaced_words = []
        for i in range(len(word)):
            for letter in string.ascii_lowercase:
                if word[i] != letter:
                    changed = word[:i] + letter + word[i+1:]
                    replaced_words.append(changed)
        return replaced_words
    candidates = single_char_changes(word)
    for candidate in candidates:
        if candidate in words:
            print(f"{candidate} is a Match!")
```
Tested the function again with cat and got 10 words that matched. 
```python
#test function
spell_check('cat')
```


## Problem 2##
**a.** I edited the merge sort given in Problem set 1 to sort by a wanted value (key) in a tuple and retain the relationship.

```python
# Google how to add key to merge sort. Merged Copilot Search result with class alg2
# Used ChatGPT to clean up errors
def alg_new(data, key=lambda x: x):
    tupled_data = tuple(sorted(data)) #sorts data and creates tuple
  if len(tupled_data) <= 1:
    return tupled_data
  else:
    split = len(tupled_data) // 2
    left = alg_new(tupled_data[:split], key)
    right = alg_new(tupled_data[split:], key)
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
```

I created fake data to test this algorithm. 
```python 
patient_ids = [123, 456, 798, 234, 567, 891]
patient_names = ["John Smith", "Jane Doe", "Taylor Swift", "Harry Styles", "Mallory Swanson"]

#zipped data into list of tuples
patient_data = zip(patient_ids, patient_names)

#test function
alg_new(patient_data, key=lambda x:x[0])
```

## Problem 3##
I downloaded the file and called in only the first chromosome.
```python
with open(fasta_file, "rb") as f:
    print(f.read(2))

fasta_file = r"C:\Users\carol\Downloads\human_g1k_v37.fasta.gz"

with gzip.open(fasta_file, "rt") as f:
    print(f.readline())  # Read just the first line
```
**1a.** I then extracted the overlapping 15mers from chromosome 1.

```python
#Troubleshooted with ChatGPT gzip file error. Used their suggested way of only parsing out the chromosome
def extract_15mers_from_chr1(fasta_path):
    fifteen_mers = []

    with gzip.open(fasta_path, "rt") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            if record.id.strip().lower() in ["1", "chr1"]:
                sequence = str(record.seq)
                for i in range(len(sequence) - 14):  # 15-mers
                    fifteen_mers.append(sequence[i:i+15])
                return fifteen_mers

# File path
fasta_file = r"C:\Users\carol\Downloads\human_g1k_v37.fasta.gz"

# Run the extraction
kmers = extract_15mers_from_chr1(fasta_file)

# Check a few
print(kmers[:5])
```
I then used length to see how many nucelotides were in chromosome 1.
```python
len(kmers)
```
I excluded all kmers that had a count of 3 N.
```python 
#asked ChatGPT how to create a for loop that would drop any kmers that meet given criteria

filtered_kmers = []
for kmer in kmers:
    if kmer.count('N') <= 2:
        filtered_kmers.append(kmer)

len(filtered_kmers)
```
The new number of valie 15-mers for me was 225280241.

**b.**


## Problem 4 ##
**a. Discuss some of the challenges with making more and more health care resources available over the internet.**
Definitionally, the digital divide is when already present health disparities persist in spite of, and sometimes exacerbated by, new technolgies implemented to aid healthcare delivery [1]. Sometimes the disparity can be solved with more technology - like a digital divide that exists because a rural community lacks high speed internet can be solved by installing 5G capabilities. But rural areas have long faced issues with healthcare delivery. In addition to lacking services in their local community, many rural residents are also uninsured, so even introducing telehealth capabilities would not be useful for these residents [2]. Additionally, rural communities are less likely to fully and quickly trust public health interventions, as was seen during the COVID-19 pandemic [3]. So while technology can improved the devliery and availablility of medicine, attitudes and trust that manifest into the use of the tools is still a barrier to productive healthcare delivery.

-clinical burnout and vulnerabilities exploited through technology 

References: 
[1] Saeed, S. A., & Masters, R. M. (2021). Disparities in health care and the digital divide. Current Psychiatry Reports, 23(9), 61. https://doi.org/10.1007/s11920-021-01274-4
[2] U.S. Government Accountability Office. (2023, May 16). Why health care is harder to access in rural America. GAO WatchBlog. https://www.gao.gov/blog/why-health-care-harder-access-rural-america
[3] Kricorian K, Civen R, Equils O. COVID-19 vaccine hesitancy: misinformation and perceptions of vaccine safety. Hum Vaccin Immunother. 2022 Dec 31;18(1):1950504. doi: 10.1080/21645515.2021.1950504. Epub 2021 Jul 30. PMID: 34325612; PMCID: PMC8920251.
[4] 

**b. Reflect on your own experience with digital health care resources, OR the experience of someone you know.**
-clinical burnout and lack of in person symptoms
-benefits of not having to take off work

**c. Explain what part of this assignment was most challenging for you personally. For example, did you struggle with finding credible sources, connecting research to real life, or articulating your own views.**

## Problem 5##

**a. Identify data of "moderate" size (at least 100+ rows or equivalent) that you think would be interesting to explore for your final project and has a license permitting reuse and analysis (e.g., CC BY). Tell us about it:**
**What is the data about? (1 point)**
**Where did you find it? (1 point)**
**What license was specified? (1 point)**
**Why do you think it is interesting? (1 points)**
**Give an example of two questions you could explore with this data. (1 point).**

I would like to explore the relationship between rural vs metro counties and availability to healthcare services. I can use data available on the AHRQ-SDOH. Within the dataset, there is data collected by the National Center of Healthcare Statistics that denotes each county across 6 classes as rural or metro; data collected by the Centers for Medicare and Medicaid Provider of Service that tracks the amount and types of providers in a county; and data collected by Area Health Resource Files that calculates the average distance to emergency and urgent care services for counties. All data was collected by federal agencies and housed in the AHQR dataset so they are public use data files. I think the data is interesting because I learned from the last question that rural healthcare was already sparse and has been declining in recent years and I’m interested if we could see the same issue when visualizing the data. I also believe coming from a state with many rural areas, I have seen the lengths patients have had to go to to get simple healthcare. I could explore if there have been decline in healthcare availability in rural areas in recent years. I could also explore the differences in providers based on counties that are rural vs areas that are metro. 

