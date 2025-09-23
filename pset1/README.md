Problem Set #1
cg2288 - Caroline Gheen

Problem 1

Sources: [1] https://pythonguides.com/read-xml-files-in-python/
loading xml data

[2] https://www.geeksforgeeks.org/python/reading-and-writing-xml-files-in-python/
visualizing data and finding attributable tags

#Problem 2

a. This function is administering medicine in increments. So, if you tell the function you want to administer medicine in 6 units, it will give 6 units until it hits the amount that is tstop. Tstop is the amount of full medicine needed to be given; delta_t is the difference between what has already been administered + what was just administered; and the number of doses administered is the amount needed to get to tstop in the incremental amounts that is t.

b. When you call 0.25, 1 you get, as expected it took four rounds of administering 0.25 doses amounts to reach full dosage of 1. 
```python
administer_meds(0.25,1)
Administering meds at t=0
Administering meds at t=0.25
Administering meds at t=0.5
Administering meds at t=0.75
```

c. When you call 0.1, 1 you start getting wonky decimal numbers. The dose of 3 is displayed as 3.0000000000000004. This goes awry after the 0.7 dosage. The next dose, which should be 0.8 is 0.7999999999999999. Then the dosage is 0.8999999999999999 then 0.9999999999999999. 

d. The dosage is not as expected and this could lead to a compounding effect of delivering too much medicine. The times are also not as expected because with the trailing decimals, the function is not realizing it has hit t-stop.  

e. These trailing decimals will compound into an issue, which is not great when delivering medicine. Insulin, for example, is delivered in units because it is so potent - too much insulin or too little insulin for a diabetic can have profound impacts.

f. To fix, I coded the function so that it only return 2 decimal places [1]. This will help the calculations stay aligned. I tested it with (0.1, 1), (0.1, 2), and (0.15, 3).

Sources used:

[1] Asked ChatGPT how to code so that only 2 decimal places were returned  

#Problem 3

a. algorithm 1 and 2 - data 1 is making little increments between range. for 100, only goes 20-50.
algorithm 1 and 2 -data 2 runs a list easily for 100. Starts at 0 goes to 99
algorithm 1 and 2- data 3 runs a list easily for every number in 100. Starts at 1 ends at 100.

I hypothesize that Algorithm 1 is running a bubble sort. Algorithm 2 is running a merge sort.
```python
 alg1(data1(100))
 [20.204472832048545,
 20.213040136936243,
 20.27775999095576,
 20.295935618820344,
 20.44001633033436,
 20.445173959305194,
 20.65234381358303,
 20.698073859463396,
 20.908711658169402,
 21.05868316994932,
 21.20538012061718,
 21.52876758765491,
 21.53348028121465,
 21.884376174024972,
 22.115699414903467,
 22.249861191779097,
 22.622329751533943,
 22.827555082811326,
 22.994912567212936,
 23.361569287372784,
 23.67329118682685,
 23.717137289248004,
 24.057339507317266,
 24.378757031841133,
 24.662764470091197,
...
 50.10966699477457,
 50.70001159917119,
 50.8852397709095,
 51.13969178536924,
 51.21913659552547]

 alg1(data2(100))
[0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
...
 95,
 96,
 97,
 98,
 99]

 alg1(data3(100))
[1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
 25,
...
 96,
 97,
 98,
 99,
 100]
 *Outputs are truncated
 ```

```python
alg2(data1(100))
[20.204472832048545,
 20.213040136936243,
 20.27775999095576,
 20.295935618820344,
 20.44001633033436,
 20.445173959305194,
 20.65234381358303,
 20.698073859463396,
 20.908711658169402,
 21.05868316994932,
 21.20538012061718,
 21.52876758765491,
 21.53348028121465,
 21.884376174024972,
 22.115699414903467,
 22.249861191779097,
 22.622329751533943,
 22.827555082811326,
 22.994912567212936,
 23.361569287372784,
 23.67329118682685,
 23.717137289248004,
 24.057339507317266,
 24.378757031841133,
 24.662764470091197,
...
 50.10966699477457,
 50.70001159917119,
 50.8852397709095,
 51.13969178536924,
 51.21913659552547]

alg2(data2(100))
[0,
 1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
...
 95,
 96,
 97,
 98,
 99]

 alg2(data3(100))
 [1,
 2,
 3,
 4,
 5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13,
 14,
 15,
 16,
 17,
 18,
 19,
 20,
 21,
 22,
 23,
 24,
 25,
...
 96,
 97,
 98,
 99,
 100]
 *Outputs are truncated
 ```

b. Algorithm 1 is cycling through a list that if the index + 1 is less than the index it places it places it before in the list, otherwise it returns the value. 
Algorithm 2 divides the data in half then splits it among a left branch and a right branch. It then proceeds down each branch and if the left branch is less than the right branch it adds the number to the left branch and moves to the next value until nothing remains. 

c. Data 1 tested on both algorithms [1]:

The Big O of algorithm 1 is...
The Big O of algorithm 2 is...

![time elapsed using alg1 and alg2 on data 1](data1_algs.png)

Data 2 tested on both algorithms:

The Big O of algorithm 1 is...
The Big O of algorithm 2 is...

![time elapsed using alg1 and alg2 on data 2](data2_algs.png)

Data 3 tested on both algorithms:

The Big O of algorithm 1 is...
The Big O of algorithm 2 is...
 
![time elapsed using alg1 and alg2 on data 3](data3_algs.png) [2]

d. At all numbers using data 1, algorithm 1 is slower than algorithm 2. Both slow down at data bigger than 100.

For data 2, algorithm 1 preforms better at all n values. Algorithm 1 is very fast until 100 then begins slowing down.

Using data 3, the algorithms perform similarly at small numbers but eventually algorithm 2 preforms faster. Both increase at similar increments as data increases. 

Algorthim 1 is perferable for .
Algorithm 2 is perferable for  

Sources Used: 
[1] https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/
[2]Asked Yale Clarity how to plot so axises are log-log and how to save photo of graph generated in matplot. 