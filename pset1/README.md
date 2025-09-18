Problem Set #1
cg2288 - Caroline Gheen

Problem 1


Problem 2
This function is administering medicine in increments. So, if you tell the function you want to administer medicine in 6 units, it will give 6 units until it hits the amount that is tstop. Tstop is the amount that meds need to stop being administered at; delta_t is the difference between what was administered + what was just administered; and the number of doses administered is the amount needed to get to tstop in the amount of t.

When you call 0.25, 1 you get, as expected it took four rounds of administering 0.25 doses amounts to reach full dosage of 1. 

When you call 0.1, 1 you start getting wonky decimal numbers. The dose of 3 is displayed as 3.0000000000000004. This goes awry after the 0.7 dosage. The next dose, which should be 0.8 is 0.7999999999999999. Then the dosage is 0.8999999999999999 then 0.9999999999999999. These trailing decimals will compound into an issue, which is not great when delivering medicine. Insulin, for example, is delivered in units because it is so potent - too much insulin or too little insulin for a diabetic can have profound impacts.
 On this example, the med delivery technically never reaches 1 and we can see even more when imputting (0.1, 2) how this can be an issue. We can see the compounding trailing decimals in 1.4-1.9 and ultimately,  our patient never recieves their full dose of medicine. 

```python
administer_meds(0.1,2)
Administering meds at t=0
Administering meds at t=0.1
Administering meds at t=0.2
Administering meds at t=0.30000000000000004
Administering meds at t=0.4
Administering meds at t=0.5
Administering meds at t=0.6
Administering meds at t=0.7
Administering meds at t=0.7999999999999999
Administering meds at t=0.8999999999999999
Administering meds at t=0.9999999999999999
Administering meds at t=1.0999999999999999
Administering meds at t=1.2
Administering meds at t=1.3
Administering meds at t=1.4000000000000001
Administering meds at t=1.5000000000000002
Administering meds at t=1.6000000000000003
Administering meds at t=1.7000000000000004
Administering meds at t=1.8000000000000005
Administering meds at t=1.9000000000000006
```

To fix, I coded the function so that it only return 2 decimal places [1]. This will help the calculations stay aligned. I tested it with (0.1, 1), (0.1, 2), and (0.15, 3).

#Problem 3
algoritim 1 - data 1 is making little increments. for 100, only goes 20-50.
algorithm 1-data 2 runs a list easily for 100. Starts at 0 goes to 99
algorithm 1- data 3 runs a list easily for every number in 100. Starts at 1 ends at 100

Algorithm 1 is running a cycling list (?).
Algorithm 2 is running a binary search tree. 

Algorithm 1 is cycling through a list that is adding one point to the last (?). 
Algorithm 2 divides the data in half then splits it among a left branch and a right branch. It then cycles through the branches resulting in the number (THIS NEEDS TO BE CLEANED).

perf counter source [1] 
Data 1 tested on both algorithm:
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
alg1 (2.832) <> alg2 (.00927)





Sources used
[1] Asked ChatGPT how to code so that only 2 decimal places were returned  
[2] https://www.geeksforgeeks.org/python/time-perf_counter-function-in-python/