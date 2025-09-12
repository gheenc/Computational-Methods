# compmethods-cg2288
Caroline Gheen - cg2288
BIS 634
# Problem 1
The following function takes in a given normal temperature and returns if another temperature is within 1 degree of the normal temperature. If it is, it returns True; if it is not, it returns False. 

      def temp_tester(normal_temp):
        def actual_temp(temp):
            if (abs(normal_temp - temp) < 1):
                return True
            return False
        return actual_temp
  
  ##Do you mean of the true/false answer, my code, or the question?

Testing the temp_tester function using human_tester = temp_tester(37) and    chicken_tester = temp_tester(41.1) returned the following results
 
      chicken_tester(42) = True
      human_tester(42) = False
      chicken_tester(43) = False
      human_tester(35) = False
      human_tester(98.6) = False
      
# Problem 2
First, to create a function that takes in a list of state names and plots new COVID cases in a line graph, new case counts needed to be obtained. I did this by frist extrapolating the states of interest from the full data set. You can see an example of this being done with Florida as a state of interest. This then creates a variable that easily pulls a smaller databasee of that interest.

      state_df = coviddata[coviddata['state']=='state of interest']
      florida = coviddata[coviddata['state'] == 'Florida']
##CAN I ENTER THE DATAFRAME

New case counts were then obtained for the state of interest. I created a function that would add a column of 'new case count' to the state of interest data frame by looping through the state cases and subtracting from the day before, thereby obtaining a new case count. This new case count was then added in the 'new case count' column in the state of interest data frame. 

      def new_case_count(state_df):
          state_cases = list(state_df['cases'])
          new_case_list = list(range(len(state_cases)))
          new_case_list[0]=0
          for i in range(1, len(state_cases)):
              new_case_list[i] = state_cases[i] - state_cases[i-1]
          state_df['new case count']=new_case_list
          return state_df

Then, when multiple states are wanted to cycle through, for example Washington, Illinois, and Virginia...

      states = ['Washington", "illinois", "Virginia"]

a new dataframe of all interested states can be created whos new cases will be plotted.

      plot_state = pd.DataFrame()

Then, a for loop can be written to cycle through all states in the states list and create a state dataframe, as we saw with Florida, with new case counts already obtained. This state dataframe is then added to the dataframe of all interested states. This is done for all interested states. 

    for state in states:
      state_df = new_case_count(coviddata[coviddata['state']==state])
      plot_state = pd.concat([plot_state, state_df], ignore_index = True)   

We are then able to plot the total interested states dataframe using ggplot. You can see an graph here following our example of Washington, Illinois, and Virginia, but any state could be plotted by inserting the name (exactly as written in the original database) into the states list. 

      ggplot(plot_state, p9.aes(x='date', y='new case count', color='state'))+ p9.geom_line()+ p9.labs(title = 'New COVID Cases by State')+ p9.theme(axis_text_x=p9.element_text(angle=45))

The X axis is progresses through the dates and the y axis shows the number of new cases. Colors are varied based on state and the axis labels are titled to increase readability for the viewer. 

![case counts of multiple states](images/state_graphs.png)

To determine when a state peaked, I created a variable named peak that returned the max new cases counted. This relied on the previously created state dataframe. 

```python
peak=state_df['new case count'].max()
```
We can once again see an example with Florida

      peak=florida['new case count'].max()

I checked this worked by describing Florida and ensuring the peak number given matched the max in the cases column given in the describe output

      florida.describe()

To better approach this problem and allow 

      def date_of_peak(state_df):
          max_case_count = state_df['new case count'].idxmax()
          max_case_row = state_df.loc[max_case_count]
          return max_case_row['date']

to test what state had it's peak first and how many days between I created this function

       def compare(df, state1, state2):
          peak_date1 = date_of_peak(df, state1)
          peak_date2 = date_of_peak(df, state2)
          delta = abs((peak_date1 - peak_date2).days)
          if peak_date1 > peak_date2:
              earlier_date = peak_date2
              earlier_state = state2
              later_date = peak_date1
              later_state = state1
              return(f"{state2} had its peak first and the peak was                         {delta} days apart")
          elif peak_date1 < peak_date2:
                earlier_date = peak_date1
                earlier_state = state1
                later_date = peak_date2
              later_state = state2
              return(f"{state1} had its peak first and the peak was                         {delta} days apart")
          elif peak_date1 == peak_date2:
              return(f"{state2} and {state1} had its peak on the same day")
##ANALYZE FLORIDA

![Florida case count graph](images/florida.png)

##ADD SOURCES

# Problem 3
I imported the data from the SQLite Database [3]
```python 
import pandas as pd
import sqlite3
with sqlite3.connect("pset0-population.db") as db:
data = pd.read_sql_query("SELECT * FROM population", db)
```

I also imported plotnnine for later use during graphing.

```python
import plotnine as p9
from plotnine import geom_bar, ggplot, aes, geom_histogram, geom_smooth, theme_bw
```
Visualizing the data, we can see the column names are: name, age, weight, eyecolor and there are 152361 rows or individuals in the data set.

```python
data
len(data)
```
We can see the following statistics for the age group: Mean = 39.51, standard deviation = 24.15, minimum = .000748, maximum = 99.99.

```python
data.describe()
print(data['age'].max())
print(data['age'].min())
print(data['age'].mean())
print(data['age'].std())
```
The age distributions were graphed in a histogram.

```python
h = ggplot(data, aes(x ='age'))+ geom_histogram(bins=10, color = 'black')
``` 

![graph of age distributions](images/age_counts.png)
For the histogram of age, I chose to use bin size of 10. With a smaller bin width, you could loose some of the true distribution of the data because it becomes very minute but a larger bin width, some of the distribution gets lost. With too many bins (like bins=100), the graph can become seem to focus in on individual data points rather than visualizing the data as groups. With too few bins (like bins = 3), you lose the trends you are able to visualize through creating a graph. I also changed the color to black to be easier to visualize.
There is a potential outlier in the 90-100 bucket. 
The majority of data points are pretty uniformly distributed in the 10-60 age range. 

For the weight group we can see the following statistics: mean = 60.88, standard deviation = 18.41, minimum = 3.382, maximum = 100.44

```python
print(data['weight'].max())
print(data['weight'].min())
print(data['weight'].mean())
print(data['weight'].std())
```
```python
g = ggplot(data, aes(x ='weight'))+ geom_histogram(bins=10, color = 'black')
```

![graph of weight distribution](images/weight_counts.png)

I chose 10 bins again for the same reason stated in the age histogram. I also liked 10 because it evenly and logically slpit 100 into 10 even group.  

```python
f = p9.ggplot(data, p9.aes(x='age', y='weight'))+p9.geom_point()
```
![scatterplot of age vs weight](images/age_vs_weight.png)

From the scatterplot, we can tell there is a relationship between age and weight in that, typically, weight has a small range until about 20 years of age. After 20, the data suggests that there is more varaibility in the weight. 
There is an outlier at around 35 years of age and 20 weight. Their data does not follow the general relationship observed. 
I confirmed my identification of this outlier by adding a linear regression line to the plot to understand better how intense the relationship level was between data. I also re analyzed the describe outlook to better understand the standard deviations of the data and confirmed that this data point would lie outside the standard deviation. It would be ideal to add the standard deviation as a visualization to the plot because then you can see if the data point lands in or out of the catchment of the standard deviation. 

```python
fg = p9.ggplot(data, p9.aes(x='age', y='weight'))+p9.geom_point()+p9.geom_smooth(method='lm', se=True, color='blue')
```

![age vs weight with a linear regression line](images/age_vs_weight_with_line.png)

# Problem 4
To compare the entries I asked for the legnth of M and F in the databases.

      len(patient_data[patient_data['gender']=='M'])  
      len(patient_data[patient_data['gender']=='F'])

This returned 45 for males and 55 for females. I confirmed males have less than females by placing both on either side of the <

      len(patient_data[patient_data['gender']=='M']) > len(patient_data[patient_data['gender']=='F']) 
returned False 

      len(patient_data[patient_data['gender']=='M']) < len(patient_data[patient_data['gender']=='F'])
returned True

    def diagnosis_pt(diagnosis_name):
          code =                               diagnosis_data[diagnosis_data['long_title']==diagnosis_name]["icd9_code"].item()
          test = icd_data[icd_data["icd9_code"]==code]['subject_id']
          return list(test)

    diagnosis_pt('Intestinal infection due to Clostridium difficile')
    
##diagnosis -> subject id
##function testing
##age calculation
##reflection

References
[3]pset0-population.db SQLite