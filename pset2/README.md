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

I created fake data to test this algorithm. I made two list of 6 "patients" with 3 digit ids. The list of ids was out of order numerically.  
```python 
patient_ids = [123, 456, 798, 234, 567, 891]
patient_names = ["John Smith", "Jane Doe", "Taylor Swift", "Harry Styles", "Mallory Swanson", "Jane Goddall"]

#zipped data into list
patient_data = list(zip(patient_ids, patient_names))

print(alg_new(patient_data, key=itemgetter(0)))

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
**1a.** I then extracted the overlapping 15mers from chromosome 1 and visualized the first 5 to ensure they were correct. 

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
len(kmers)*15

returned
3738759105
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
The new number of valid 15-mers was 225280241.

**There were 3738759105
nucleotides in Chromosome 1. I excluded any 15-mers that contained more than two N. After excluding those, there are 225280241 valid 15-mers.**

**b.**
I implemented this code that utilized a rolling hash to returning the normalized minimum for each hash. I used ChatGPT to fine tune a rolling hash that did not exceed the memory load of my computer. My code also allows the varying of base a to generate multiple independent hash functions. 

```
import gzip
from Bio import SeqIO

def estimate_distinct_15mers_multihash(fasta_file, num_hashes=10, M=10**9 + 7):
    bases = [101 + i*2 for i in range(num_hashes)]  # Ensure different odd bases
    min_hashes = [None] * num_hashes
    window_size = 15

    # Updated encoding: fixed character to integer mapping
    char_to_int = {'A': 1, 'C': 2, 'G': 3, 'T': 4, 'N': 5, 'X': 6}

    with gzip.open(fasta_file, "rt") as handle:
        for record in SeqIO.parse(handle, "fasta"):
            if record.id.strip().lower() in ["1", "chr1"]:
                seq = str(record.seq).upper()
                n = len(seq)

                for h, base in enumerate(bases):
                    power = [1] * window_size
                    for i in range(1, window_size):
                        power[i] = (power[i - 1] * base) % M

                    current_hash = 0
                    for i in range(window_size):
                        c = char_to_int.get(seq[i], 0)  # fallback to 0 if unexpected char
                        current_hash = (current_hash * base + c) % M

                    min_hash = current_hash

                    for i in range(1, n - window_size + 1):
                        if 'N' in seq[i - 1:i + window_size]:  # Original behavior: skip if any 'N'
                            continue
                        left_char = char_to_int.get(seq[i - 1], 0)
                        right_char = char_to_int.get(seq[i + window_size - 1], 0)

                        current_hash = (current_hash - power[window_size - 1] * left_char) % M
                        current_hash = (current_hash * base + right_char) % M
                        if min_hash is None or current_hash < min_hash:
                            min_hash = current_hash

                    min_hashes[h] = min_hash

                break  # Only process chromosome 1

    # Normalize and estimate
    normalized_mins = [h / M for h in min_hashes if h is not None]
    mean_min = sum(normalized_mins) / len(normalized_mins)
    estimated_distinct = (1 / mean_min) - 1 if mean_min > 0 else 0

    return estimated_distinct, normalized_mins, min_hashes, mean_min
```
**c.**
I included the normalizing of minimum hash values and calculation of mean of minima in my original rolling hash as it allowed me to store them without exceeding my computer memory. I then implemented a for loop that using the rolling hash for a base 1, 2, 5, 10, and 100 and stored the estimate for each in a list.  

Portion of my rolling hash that calculated the minimum for each hash, normalized it, calculated the mean of minima, the converted the result into an estimate of distinct 15-mers.
```python

    # Normalize and estimate
    normalized_mins = [h / M for h in min_hashes if h is not None]
    mean_min = sum(normalized_mins) / len(normalized_mins)
    estimated_distinct = (1 / mean_min) - 1 if mean_min > 0 else 0

    return estimated_distinct, normalized_mins, min_hashes, mean_min
```
For loop that applied each wanted base hash.
```python
hash_counts = [1, 2, 5, 10, 100]
estimates = []

for n_hash in hash_counts:
    est, _, _, _ = estimate_distinct_15mers_multihash(fasta_file, num_hashes=n_hash)
    print(f"{n_hash} hash(es): estimated = {int(est)}")
    estimates.append(est)
```
**for each hash function, the minimum value is tracked. It is then  normalized by dividing by M. The results are then combined across all hash functions used to determine the mean of minima. This is then converted to give an estimate of the number of distinct 15-mers.**

**d.**

['Estimated Distinct Counts for Varying Hash Functions Compared to True Number of Distinct 15mers'](distinct_counts.png)

As more hash functions are combined, the closer the estimated distinct count comes to the true distinct count. We can especially see this in the move to using 1, 2, and 5 rolling hashes. 10 and 100 are slightly higher than using 2 or 5 rolling hashes and I believe this is due to noise created during the long process of creating a calculating the rolling hashes (my computer took 8 hours to compute the estimated distinct count of 100 hashes). Although this is still better than using a single hash which was the most off of the true number of distinct elements. Using only a single hash overestimates the number of distinct elements by almost 200,000,000.

**e.**
I used the example values given for a. As explained in d, it took my machine a long time to compute an estimate using 100 rolling hashes. I would be interesting to repeat the experiment using 50 rolling hashes to see if it would continue to trend down toward the true distinct without the machine's noise impedding. 

I did not make many optimizations (which is probably why it took so long). I only parsed the first chromosome out of the original data file which I think helped maintain low overhead. I orignally completed the problem using 5 string of 5 nucleotides, so when I attempted to run the code on the full data set ending with returning all the hash values, I ran into memory load issues. This is when I implemented the rolling hash returning the mean, which I could then build on to complete part c. If I were to optomize more, I think there is something with numpy that I could use when storing hashes to minimize overhead even more.  

Sources: 

## Problem 4 ##
**a. Discuss some of the challenges with making more and more health care resources available over the internet.**
 
Technology seems to be today’s society answer to every issue. But with evolving technology comes greater responsibility and can sometimes spur issues of its own. This can be seen in the healthcare sector as the creation and permeation of a ‘digital divide,’ end-user responsibilities in use of technological tools, and threats to institutions from cybercriminals. 

Definitionally, the digital divide is when already present health disparities persist in spite of, and sometimes exacerbated by, new technologies implemented to aid healthcare delivery [1]. Sometimes the disparity can be solved with more technology - like a digital divide that exists because a rural community lacks high speed internet can be solved by installing 5G capabilities. But the digital divide provides many complex examples of how technology cannot always solve an issue and how technology implementation can even create more issues. Recently, many rural communities have seen their already few local healthcare providers close [2]. Telehealth might seem like a nice solution to this issue, but many rural residents are also uninsured, so even introducing telehealth capabilities would not be useful for these residents [2]. Additionally, rural communities are less likely to fully and quickly trust public health interventions, as was seen during the COVID-19 pandemic [3]. So, while technology can improved the delivery and availability of medicine, attitudes and trust that manifest into the use of the tools is still a barrier to productive healthcare delivery. 

Many of the implementation of the advancements in technology rely on the users to adapt and learn new skills. The pressures on those creating the medical technologies and those using them to encompass all details and adapt quickly are burdensome to an already responsibility-heavy profession of health care workers. As was captured in Evolutionary Pressures on the Electronic Health Record, “there is a building resentment against the shackles of the present HER, every additional click inflicts a nick on physicians’ morale,” [4]. When physicians already have limited time to care for their patients, establish new research, and fulfill all their professional responsibilities, any additional work created by the EHR is cumbersome and counterproductive to the original purpose of technology to simplify the care process. 
Cybersecurity is a growing concern of the technology era as well. While the interoperability allowed by technology has been a great advantage to internal communication and continuous care of patients, it leaves institutions vulnerable to external threats [5]. Cybersecurity also lends itself to identifying how complex the downsides of technologizing everything because the increase in cyberthreats and phishing scams in recent years has required additional end-user training, adding tasks to an already fully physicians plate and public data breeches can dismay the already flimsy trust of a community [6]. 

Overall, while the benefits of technology have been great and will continue to improve the workflow and delivery of healthcare, caution must be exercised before implementing technology into everything. Undermining the implications and added responsibility of a technological tool could cause more headaches than the technologizing warrants. 

References: 
[1] Saeed, S. A., & Masters, R. M. (2021). Disparities in health care and the digital divide. Current Psychiatry Reports, 23(9), 61. https://doi.org/10.1007/s11920-021-01274-4
[2] U.S. Government Accountability Office. (2023, May 16). Why health care is harder to access in rural America. GAO WatchBlog. https://www.gao.gov/blog/why-health-care-harder-access-rural-america
[3] Kricorian K, Civen R, Equils O. COVID-19 vaccine hesitancy: misinformation and perceptions of vaccine safety. Hum Vaccin Immunother. 2022 Dec 31;18(1):1950504. doi: 10.1080/21645515.2021.1950504. Epub 2021 Jul 30. PMID: 34325612; PMCID: PMC8920251.
[4] Zulman, Donna M., Nigam H. Shah, and Abraham Verghese. "Evolutionary pressures on the electronic health record: caring for complexity." Jama 316, no. 9 (2016): 923-924
[5] Coventry, L., & Branley, D. (2018). Cybersecurity in healthcare: A narrative review of trends, threats and ways forward. Maturitas, 113, 48–52. https://doi.org/10.1016/j.maturitas.2018.04.008
[6] Alder, S. (2025, January 14). 2024 was another bad year for healthcare ransomware attacks. HIPAA Journal. https://www.hipaajournal.com/2024-was-another-bad-year-for-healthcare-ransomware-attacks/ 

**b. Reflect on your own experience with digital health care resources, OR the experience of someone you know (family, friend, or community member).**

I have mostly been a patient during the digital era and have reaped many benefits from the convenience of today’s healthcare resources. I am a patient who is guilty of using the electronic messaging like they are texting their doctor and waiting for an immediate answer. I have also seen the other side, as a worker in the health care field, and the strain technology can put on the health care workforce. While, in my opinion, the benefits ultimately outweigh the downsides, the added responsibility to remember passwords, stay current on trainings, answer patient messages, etc. are very real added responsibilities to today’s healthcare workforce. I also think as scientists, it can be overlooked that digitized does not equate to correctness. Just because something is in a digital format does not mean that it is correct and human error still permeates these mediums. For example, I would see a lot in the EHR a patient’s height incorrectly entered in inches rather than centimeters, as the field required. This would then lead to them having a massively inflated (and impossible) BMI. If this BMI is added to a dataset without any additional checks, it will not lend itself to good science. 

**c. Explain what part of this assignment was most challenging for you personally. For example, did you struggle with finding credible sources, connecting research to real life, or articulating your own views?**
I honestly enjoyed this assignment. I felt like it allowed me to synthesize a lot of the conversations we’ve been having in Clinical Informatics and bring my personal views into the topics of this class. I also think coming from both sides of today’s healthcare, I enjoyed looking at the benefits and downsides of technology and the central place it is taking up in our healthcare landscape today. I also think coming from a state with rural areas and a spectrum of attitudes toward technology, it made me think about how they feel about their healthcare being digitized. I struggled with the word count because I wanted to be concise in my thoughts while also expanding on all the complexities of the benefits and downsides of technology. 

## Problem 5##

**a. Identify data of "moderate" size (at least 100+ rows or equivalent) that you think would be interesting to explore for your final project and has a license permitting reuse and analysis (e.g., CC BY). Tell us about it:**

**What is the data about? (1 point)**
Using AHRQ-SDOH, I identified data concerning availability of healthcare services to rural and metro counties in the US.

**Where did you find it? (1 point)**
The data is available within the AHRQ-SDOH.
Data is collected by the National Center of Healthcare Statistics that denotes each county across 6 classes as rural or metro; by the Centers for Medicare and Medicaid Provider of Service that tracks the amount and types of providers in a county; and by Area Health Resource Files that calculates the average distance to emergency and urgent care services for counties

**What license was specified? (1 point)**
All data was collected by federal agencies and housed in the AHQR dataset so they are public use data files. 

**Why do you think it is interesting? (1 points)**
I think the data is interesting because I learned from researching the last question that rural healthcare was already sparse and has been declining in recent years and I’m interested if we could see the same issue when visualizing the data. I also believe coming from a state with many rural areas, I have seen the lengths patients have had to go to to get simple healthcare.

**Give an example of two questions you could explore with this data. (1 point).**
I could explore if there have been decline in healthcare availability in rural areas in recent years. I could also explore the differences in providers based on counties that are rural vs areas that are metro. 


