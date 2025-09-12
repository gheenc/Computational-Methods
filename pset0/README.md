# compmethods-cg2288
Caroline Gheen - cg2288
BIS 634
# Problem 1
The following function takes in a given normal temperature and returns if another temperature is within 1 degree of the normal temperature. If it is, it returns True; if it is not, it returns False. 

```python
def temp_tester(normal_temp):
    def actual_temp(temp):
        if (abs(normal_temp - temp) < 1):
            return True
        return False
    return actual_temp
```
  
There can be some ambiguity in this in that the function does not tell you how far the imput temperature is from normal or in which direction. So, medically, you don't know if someone only has a slight fever or if they have an emergent fever. Similarly, you don't know if someone has a fever or if they are hypothermic - you just know that their temperate is outside the range of normal. 

Testing the function returned the following results:
 
 ```python
 human_tester = temp_tester(37)
chicken_tester = temp_tester(41.1)

chicken_tester(42) = True
human_tester(42) = False
chicken_tester(43) = False
human_tester(35) = False
human_tester(98.6) = False
```
      
# Problem 2

Data was downloaded from the New York Times Github of covid-19-data [1].

I imported pandas, plotnine, and the data.

```python
import pandas as pd
import plotnine as p9
from plotnine import geom_bar, ggplot, aes, geom_line, labs, theme, geom_point
coviddata = pd.read_csv("us-states.csv")
```
I think converted all dates in the data set to be useable timestamps in pandas. 

```python
coviddata['date']=pd.to_datetime(coviddata['date'])
```
I then created a function that would add a new column called new_case_counts to the existing COVID data frame. I had to trouble shoot the function so it would group by states and create the new case count rather than creating new case count from dataframe with the states intermixed. I then added this new column to the overall COVID dataframe. I visualized the dataset again to ensure this new column was added.

```python
def new_case_count(df):
    df["new_case_count"] = df.groupby(["state"])["cases"].diff().fillna(0)
    return df

new_case_count(coviddata)
```

Next, I created a function that loops through multiple states and graphs new case counts versus the date. The states of interst need to be listed as variable states.  

```python
states = ["Washington", "Illinois", "Virginia"]
```

```python
plot_state = pd.DataFrame()
for state in states:
    state_df = new_case_count(coviddata[coviddata['state']==state])
    plot_state = pd.concat([plot_state, state_df], ignore_index = True)
```

We can visualize plot state to ensure only the states of interest have been chosen

```python
plot_state
```
We can then plot the graph. 
```python
g = ggplot(plot_state, p9.aes(x='date', y='new_case_count', color='state'))+ p9.geom_line()+ p9.labs(title = 'New COVID Cases by State')+ p9.theme(axis_text_x=p9.element_text(angle=45))
```

The X axis progresses through the dates and the y axis shows the number of new cases. Colors are varied based on state and the axis labels are titled to increase readability for the viewer. 

![case counts of Washington, Illinois, Virginia](images/state_graphs.png)

I checked this with 3 more states to ensure functionality. 

```python
 states2 = ["Tennessee", "Rhode Island", "Georgia"]

 plot_state2 = pd.DataFrame()

 for state in states2:
    state_df = new_case_count(coviddata[coviddata['state']==state])
    plot_state2 = pd.concat([plot_state2, state_df], ignore_index = True)

 ggplot(plot_state2, p9.aes(x='date', y='new_case_count', color='state'))+ p9.geom_line()+ p9.labs(title = 'New COVID Cases by State')+ p9.theme(axis_text_x=p9.element_text(angle=45))
```
![case counts of Tennessee, Rhode Island, and Georgia](images/states2_graphs.png)

To determine when a state peaked, I created a fucntion named date_of_peak that returns the date of it's max new case count [1A]. 

```python
def date_of_peak(df, state):
    data2 = new_case_count(df)
    data3 = data2[data2["state"]==state]
    max_case_count = data3["new_case_count"].idxmax()
    max_case_row = data3.loc[max_case_count,"date"]
    return max_case_row
```
I tested this function with Tennesse and Georgia because I could visualize when their peak was from the graph and therefore check the functions return

```python
date_of_peak(coviddata, "Georgia")
returned Timestamp('2022-01-04 00:00:00')

date_of_peak(coviddata, "Tennessee")
Timestamp('2022-01-18 00:00:00')
```

I then created a function to test what state had it's peak first and how many days between. 

```python
def compare(df, state1, state2):
    peak_date1 = date_of_peak(df, state1)
    peak_date2 = date_of_peak(df, state2)
    delta = abs((peak_date1 - peak_date2).days)
    if peak_date1 > peak_date2:
        earlier_date = peak_date2
        earlier_state = state2
        later_date = peak_date1
        later_state = state1
        return(f"{state2} had its peak first and the peak was {delta} days apart")
    elif peak_date1 < peak_date2:
        earlier_date = peak_date1
        earlier_state = state1
        later_date = peak_date2
        later_state = state2
        return(f"{state1} had its peak first and the peak was {delta} days apart")
    elif peak_date1 == peak_date2:
        return(f"{state2} and {state1} had its peak on the same day")
```
I tested this with Tennessee and Georgia, Florida and Wyoming, and Tennessee and Washington to test all three options of state1 peaking first, state2 peaking first and the states peaking at the same time.

```python
compare(coviddata, "Tennessee", "Georgia")
returned 'Georgia had its peak first and the peak was 14 days apart'

compare(coviddata, "Florida", "Wyoming")
returned 'Florida had its peak first and the peak was 14 days apart'

compare(coviddata, "Tennessee", "Washington")
returned 'Washington and Tennessee had its peak on the same day'
```
I then extrapolated Florida into its own data frame to analyze the data and plotted it.

```python
florida = coviddata[coviddata['state']=='Florida']

florida.describe()

ggplot(florida, p9.aes(x='date', y='new_case_count', color='state'))+ p9.geom_line()+ p9.labs(title = 'New COVID Cases by State')+ p9.theme(axis_text_x=p9.element_text(angle=45))
```
![Florida case count graph](images/florida.png)

We can see in the middle of 2021, Flordia had a negative new case count of -40,527. Also, toward the end of 2022, rather than having reports everyday, there are sporatic bouts of reporting. It seems they have changed their reporting cadence and potentially changed reporting standards within the state.

# Problem 3
I imported the data from the SQLite Database [2]
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
returned 152361
```
We can see the following statistics for the age group: Mean = 39.51, standard deviation = 24.15, minimum = .000748, maximum = 99.99.

```python
data.describe()
print(data['age'].max())
print(data['age'].min())
print(data['age'].mean())
print(data['age'].std())

returned 99.99154733076972
0.0007476719217636152
39.51052792739697
24.152760068601445
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

returned 100.43579300336947
3.3820836824389326
60.884134159929715
18.411824265661494
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

I used this website to help with code for histogram [3] and this website to help with code for scatterplots [4]

# Problem 4

I imported date time packages and pandas in addition to the needed data sets. All data was collected from the MIMIC-III Database [5]. I visualized the data sets to make sure they imported correctly.

```python
from datetime import datetime
from dateutil.relativedelta import relativedelta, MO
import pandas as pd
patient_data = pd.read_csv("PATIENTS.csv")
diagnosis_data = pd.read_csv("D_ICD_DIAGNOSES.csv")
icd_data = pd.read_csv("DIAGNOSES_ICD.csv")
```
I had all data sets fill NaN entries with a 0 instead.

```python
icd_data
icd_data.fillna(0)

diagnosis_data
diagnosis_data.fillna(0)
```

I went ahead and converted time and date stamps timestamp objects in the patient dataset [2A].

```python
patient_data
patient_data['dob']=pd.to_datetime(patient_data['dob'], errors='coerce')
patient_data['dod']=pd.to_datetime(patient_data['dod'], errors='coerce')

patient_data.fillna(0)
```
To compare the entries I asked for the legnth of M and F in the databases.

```python
len(patient_data[patient_data['gender']=='M'])  
len(patient_data[patient_data['gender']=='F'])
```

This returned 45 for males and 55 for females. I confirmed males have less than females by placing both on either side of the <

```python
len(patient_data[patient_data['gender']=='M']) > len(patient_data[patient_data['gender']=='F']) 
returned False 

len(patient_data[patient_data['gender']=='M']) < len(patient_data[patient_data['gender']=='F'])
returned True
```

I created a function to intake disease long names and return the patients id who had that disease.
```python
 def diagnosis_pt(diagnosis_name):
    code = diagnosis_data[diagnosis_data['long_title']==diagnosis_name]['icd9_code'].item()
    test = icd_data[icd_data['icd9_code']==code]['subject_id']
    if test.empty:
      return "There are no patients with this diagnosis"
    else:
      return list(test)
```
I tested it with 'Intestinal infection due to Clostridium difficile' which had multiple patients.

```python
diagnosis_pt('Intestinal infection due to Clostridium difficile')

[10043, 10045, 10094, 10102, 40595, 41976, 44228]
```

I also tested with 'Contact with and (suspected) exposure to mold' which had no patients.

```python
diagnosis_pt('Contact with and (suspected) exposure to mold')

There are no patients with this diagnosis
```

To calculate in days the age of patients I ensured again that the date/times were in time stamps. 

```python
pd.to_datetime(patient_data["dob"])
pd.to_datetime(patient_data["dod"])
```
I then created the function. I added barriers for if the DOB or DOD were empty in the dataframe. [2A]

```python
def dod_dob(diagnosis_name):
    code = diagnosis_data[diagnosis_data['long_title']==diagnosis_name]['icd9_code'].item()
    test = icd_data[icd_data['icd9_code']==code]['subject_id']
    test2 = test.values
    dob = patient_data[patient_data['subject_id'].isin(test2)]['dob']
    dod = patient_data[patient_data['subject_id'].isin(test2)]['dod']
    valid_indices = dob.notna() & dod.notna()
    dob=dob[valid_indices]
    dod = dod[valid_indices]
    if dob.empty:
        return "DOB is empty and operation cannot be preformed"
    if dod.empty:
        return "DOD is empty and operation cannot be preformed"
    differences = [(d.to_pydatetime() - b.to_pydatetime()).days for d, b in zip(dod, dob )]
    return differences
```

I tested on Intestinal infection due to Clostridium difficile.
```python
dod_dob('Intestinal infection due to Clostridium difficile')

returned [29891, 25087, 109593, 25626, 27999, 24235, 21358]
```

The patients diagnoised with Intestinal infection due to C.diff as 29891, 25087, 109593, 25626, 27999, 24235, 21358 days old respectfully. All patients are older then 58. The third patient is 300 years old, however, so there must be a data error in their file. Besides them, the oldest patient with C.diff is 81 years old. 

This activity shows that working across multiple data sets can quickly become difficult. Even with only 3 variables to keep track of, it added an extra layer of tracking and thought to understand which data set you needed to index into to get your wanted information. While it is doable for this activity, more complex data quickly creates more opportunities for error.  

Representing the data with dictionaries starting with the subject id and containing patient info and diagnoises would create easier location of data about an individual patient themselves. It would create difficulty for anyone looking to research how diseases affect multiple patients, like if one gender has a higher incidence of C.diff. 
A dictionary keyed by diagnosis with a list of patients would have the alternative effect. It would be easy to research the presence of a diagnoisis but difficult to see how prevelant it really is amongst a population. Using a dictionary instead of a dataframe, however, you would lose the visual benefit the tabular functionalities a dataframe provides. Because dictionaries are not hierarchical, they would not provide any usefulness for adding a time aspect to these data sets. For example, if someone wanted to transform the existing data set to include what order a patient received each diagnosis, that would not be possible in a dictionary format.

Alternatively, we can see by finding the lengths of patient_data and diagnosis_data how this would produce different lenghts of dictionarys. Sorting by subject_id would create 100 dictionary entries, which is feasible, but it doesn't show the depth of infection within the population and how many diseases are present. Alternatively, sorting by a dictionary of diagnoses requires 14,567 entries which would ask a lot of the memory power and managment of the institution. 

```python
len(patient_data['subject_id'])

returns 100

len(diagnosis_data['long_title'])

returns 14567
```

Transforming the data from a dataframe into a dictionary would require all the data to be paired up in either a tuple or a list. So, we could create a dictionary entry that is a row of each dataset (eg. diagnosis data would become a dictionary group of one icd code, the matching short title, and the matching long title repeated for each icd code) [6]. 


References
[1] https://github.com/nytimes/covid-19-data
[2]pset0-population.db SQLite
[3]https://plotnine.org/reference/examples/geom_histogram-preview
[4] https://www.geeksforgeeks.org/data-visualization/data-visualization-using-plotnine-and-ggplot2-in-python/
[5]https://physionet.org/content/mimiciii-demo/1.4/
[6]

AI Use:
[1A] I was using idmax and kept getting an error. Asked AI and it said to use idxmax. 
[2A] I had trouble with the dod-dob function returning with an overflow error. I trouble shooted with AI and had to add things to ensure date/time was in a good format. Once it began working it was returning in years, so I also used AI to troubleshoot how to have it return in days. 

