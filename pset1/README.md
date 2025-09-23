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

Sources used
[1] Asked ChatGPT how to code so that only 2 decimal places were returned  

#Problem 3
a. algoritim 1 and 2 - data 1 is making little increments. for 100, only goes 20-50.
algorithm 1 and 2 -data 2 runs a list easily for 100. Starts at 0 goes to 99
algorithm 1 and 2- data 3 runs a list easily for every number in 100. Starts at 1 ends at 100.
Algorithm 1 is creating a list that compares the index values to count up. 
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

b. Algorithm 1 is cycling through a list that is adding one point to the last (?). 
Algorithm 2 divides the data in half then splits it among a left branch and a right branch. It then cycles through the branches resulting in the number (THIS NEEDS TO BE CLEANED).

perf counter source [1] 
c. Data 1 tested on both algorithm:
For 1:
alg1 (.0001846)< alg2 (.0001995)

For 100: 
alg1 (.001192) < alg2 (.001157)

For 1000:
alg1 (0.0834) > alg2 (0.00550)

For 5000:
alg1 (2.2507) > alg2 (0.0258)

At larger numbers, algorithm 1 is slower than algorithm 2

Data 2 tested on both algorithm:
For 1:
alg1 (.000114)< alg2 (6.72 e-5)

For 100: 
alg1 (7.33 e-5) > alg2 (.000306)

For 1000:
alg1 (.000199) > alg2 (.00145)

For 5000:
alg1 (.000908) > alg2 (.014)

Data 3 tested on both algorithm:
For 1:
alg1 (8.580 e-5) > alg2 (8.690 e-5)

For 100: 
alg1 (.000995) < alg2 (.000284)

For 1000:
alg1 (0.1039) < alg2 (0.00194)

For 5000:
alg1 (2.832) < alg2 (.00927)

d. Using data 1, algorithm 2 preforms faster at all n values. Algorithm 1 performs faster on the data 

![time elapsed using alg1 and alg2 on data 1](data1_algs.png)

Using data 2, algorithm 2 preforms better at all n values.
![time elapsed using alg1 and alg2 on data 2](data2_algs.png) 

Using data 3, the algorithms perform similarly at small numbers but eventually algorithm 1 preforms better. 
![time elapsed using alg1 and alg2 on data 3](data3_algs.png) [2]

Algorthim 1 is preferred for more mathematical data that is being sorted. Algorithm 2 is preferred for Both algorithms worked well on 3 which is a small dataset. 

Sources Used: 
[1] https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/
[2]Asked Yale Clarity how to plot so axises are log-log and how to save photo of graph generated in matplot. 