## Problem Set 4 ##
## Problem 1 - Gradient Descent
**Is this a clean URL and why** No, this is not a Clean URL because it is querying and it is passing parameters into it to function e.g. searching for a=0.4 rather than stating a file path like a Clean URL would. 

**Implement 2-D version of gradient descent to find optimal choices of a and b**

**Explain how you estimate the gradient given that you cannot directly compute the derivate**

**Identify any numerical choices -- including stopping criteria -- and justify why this was reasonable**

**Find a and b value/location of local minimum and global minimum by querying API**

**Identify which corresponds to which**

**Discuss how to test for local vs global minima if you had not known how many minima there were**

## Problem 2
**Implement function that takes 2 strings and returns optimal local alignment** 

**and score using Smith-Waterman**

**insert - as needed to indicate gap**

**To identify the local alignment after the matrix has been calculated, your program should backtrack from the biggest value, repeatedly moving to one of the three possible places that it could have come from (left, up, or diagonally both), whichever makes the math work out - do not store location of each match's parent**

**function shoudl take in 3 keyword arguemnts: match=1, gap_penalty=1, mismatch+penalty=1**

**test and explain how test shows funcation is working. Test other values of match, gap_penalty, and mismatch-penalty**

**paralellize for extra credit**

## Problem 3
**implement k-nearest numbers. store in quad-tree**

**Given new point and value, identify most common class within those k nearest neighbors**

**Normalize seven quantitative columns to mean of 0 and standard deviation 1**

**Reduce data to two dimensions using PCA**

**Scatterplot, color-coding by type of rice**

**What does the graph suggest about effectiveness of using k-neraest neighbors on 2-D reduction of data to predict type of rice**

**train-test split with k-nearest neighbors implementation, give confusion matrix for predicting type of rice with k=1**

**interpret what confusion matrix means**

## Problem 4 
I loaded all the data from the csv file and droped the eyeDetection column full of categorical data. I visualized the rest of the data to better understand the file. 

I then created a standardize variable I could apply to the data and stored this values in a new variable named data_standard.I visualized this dataframe. 
```python
def standardize(series):
    return (series - series.mean()) / series.std()
data_standard = data.apply(standardize)
data_standard.head()
```
I then did a PCA on the standardized data and plotted the comparison between PCA0 and PCA1.
```python
pca_raw = decomposition.PCA() # performed on all components
pca = pd.DataFrame(
    pca_raw.fit_transform(data_standard))
```
!['Scatterplot of PCA1 vs PCA0 of standardized EEG-Eye data'](Original_PCA.png)

I then zoomed in on this data at the origin to better visualize the main components.
!['Zoomed in scatterplot of PCA1 vs PCA0 of standardized EEG eye data'](Zoom_PCA.png)

I performed K-means clustering using the sklearn's kmeans on the data to cluster into 7 clusters with a random init.
```python
kmeans = KMeans(n_clusters=7, init="random", random_state=0).fit(data_standard)
```

In order to plot I added a column named 'cluster' to the data frame of the kmeans labels. I also created the centers of the PCA and added them to their own data frame for plotting of the center points. 

I plotted the zoomed in standardized data, color-coding by cluster and included X's on the center of the clusters.
```python
pca["cluster"] = kmeans.labels_
pca["cluster"] = pca["cluster"].astype(str) 
cluster_order = [str(i) for i in range(7)] 
centers_pca = pca_raw.transform(kmeans.cluster_centers_)
centers_df = pd.DataFrame(centers_pca[:, :2], columns=['PCA0', 'PCA1'])
```
['Color Coded Scatterplot of K-Means Clustering with X on the Center of the Clusters'](x_centers.png)

**We only see 6 clusters instead of 7 because we have reduced it to 2 dimensions so some of the clusters are behind the others**
**They are behind each other**
**This is not a representative view of the clusters because we are representing data in only 2 dimensions. If the points were smaller, we might see some of the ones that are behind but we still wouldn't fully appreciate the relationships of the data because it has been reduced to 2 dimensions**


Repeat k means clusting several times.
When we repeat K-means are we changing number of clusters etc??


## Problem 5
I have watched the entire video and asked the TAs any of my questions.

**Who presented the lecture?** Robert McDougal presented the lecture. 

**What framework was demonstrated for building web servers?** Flask was demonstrated for building web servers. 

**How does the approach of the framework differ from "classical" servers that simply provide static web content?** This differs from the classic servers in that it is dynamic. The static servers would would require you to load the data everytime. This now allows you to load the data once and the computer will keep it. 

**Briefly explain how you might use the "Developer tools" to debug JavaScript issues in your web pages.** You can go back to the Developer Tools to see the elements and determine if things need to be edited. You can do this to simple edits without having to make large commits. 

**Explain briefly how the app.route decorator is used to implement a RESTful API.** As exhibited in the server.py script, decorators are used to implement RESTful APIs because they listen for calls and implement what they are told but they use the HTTP status codes. 


## Problem 6
**What does each file do?** Analyze is a html file that creates a body of test that takes in what the user entered and outputs the scripts analysis. Index is a html file that creates the webpage seen and offers a place to enter something to be analyzed. The server.py is a file that uses Flask and decorators. Tells Flask should trigger the function. 

**How are they interconnected?** In the server.py, you call the index and analyze that is in the template folder and return their code. Within index, you call the action of analyze. Flask allows you to input one and call the other. Decorator says when user clicks a button to move you to that page (defines routes). 

**Are there any key parts of the files for making the server do something?** Yes, the analyze and index help in displaying. The name Flask function so Flask knows to use the templates we have. 

Using my data, I want to be able answer the question of how counties in a state are classified according to the rural-metro code. So for example, if someone entered Alabama, it would return 1-x, 2-x, 3-x...

