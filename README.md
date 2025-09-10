# compmethods-cg2288
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
First, to create a function that takes in a list of state names and plots new COVID cases in a line graph, new case counts needed to be obtained. I did this by frist extrapolating the states of interest from the full data set. You can see an example of this being done with Florida as a state of interest

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

##CAN I INSERT THE GRAPH
To determine when a state peaked, I created a variable named peak that returned the max new cases counted. This relied on the previously created state dataframe. 

      peak=state_df['new case count'].max()

We can once again see an example with Florida

      peak=florida['new case count'].max()

I checked this worked by describing Florida and ensuring the peak number given matched the max in the cases column given in the describe output

      florida.describe()
##FINISH RETURN DATE. WITH EXAMPLES

##CREATE FUNCTION OEAKBETWEEN TWO STATES AND WHICH HAD PEAK FIRST WITH HOW MANY DAYS IN BETWEEN. WITH EXAMPLES

##ANALYZE FLORIDA

##ADD SOURCES

# Problem 3
We can see by importing the data the column headers of 'name', 'age', 'weight', and 'eyecolor.' 

      data
      #ADD PHOTO OF DATABASE?

We can also confirm the number of items in the list to be 152361 by getting the length of the data base.

      len(data)
I examined the statistics of the data set by using describe

      data.describe()
Then we could see that, for age, the mean was 39.51, standard deviation was 24.15, minimum was 0.00075 and the maxiumum was 99.99.

I then plotted a histogram using ggplot with the bins=10 as I thought this provided a good overview  of the data in realtion to the scale (0-100). With a smaller bin width, you could loose some of the true distribution of the data because it becomes very minute but a larger bin width, some of the distribution gets lost. Ten is also a good number because it divides 100 evenly. With too many bins (like bins=100), the graph can become seem to focus in on individual data points rather than visualizing the data as groups. With too few bins (like bins = 3), you lose the trends you are able to visualize through creating a graph. I also set the color to be black so the individual bins could be seen better. 
You can see the data is largest around 10-60 ages and is similarly distributed there as well. There are fewer data points in the final bin, the 90-100 group that may be considered outliers. 

I again examined the statistics of the data set by using describe

      data.describe()
Then we could see that, for weight, the mean was 39.51, standard deviation was 24.15, minimum was 0.00075 and the maxiumum was 99.99.

I then plotted a histogram using ggplot with the bins=10 as I thought this provided a good overview  of the data in realtion to the scale (0-100). With a smaller bin width, you could loose some of the true distribution of the data because it becomes very minute but a larger bin width, some of the distribution gets lost. Ten is also a good number because it divides 100 evenly. With too many bins (like bins=100), the graph can become seem to focus in on individual data points rather than visualizing the data as groups. With too few bins (like bins = 3), you lose the trends you are able to visualize through creating a graph. I also set the color to be black so the individual bins could be seen better. 
You can see the data is largest around 10-60 ages and is similarly distributed there as well. There are fewer data points in the final bin, the 90-100 group that may be considered outliers. 
