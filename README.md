# compmethods-cg2288
BIS 634
# Problem 1
    def temp_tester(normal_temp):
    def actual_temp(temp):
        if (abs(normal_temp - temp) < 1):
            return True
        return False
    return actual_temp
  
  ##Do you mean of the true/false answer, my code, or the question?

Testing the temp_tester function using human_tester = temp_tester(37) and    chicken_tester = temp_tester(41.1) returned the following results
 
      *chicken_tester(42) = True
      *human_tester(42) = False
      *chicken_tester(43) = False
      *human_tester(35) = False
      *human_tester(98.6) = False
