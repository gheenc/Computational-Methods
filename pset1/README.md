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

To fix, I coded the function so that it only return 2 decimal places. This will help the calculations stay aligned. I tested it with (0.1, 1), (0.1, 2), and (0.15, 3).