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
I implemented a Smith-Waterman function that takes in two sequences and aligns them with a default of 1 for match, mismatch, and gap penalty. 
```python 
def smith_waterman(seq1, seq2, match_score=1, mismatch_penalty=1, gap_penalty=1): 
    max_score = 0
    max_pos = (0,0)
    
    rows = len(seq2) + 1 #matrix size 
    cols = len(seq1) + 1 
    matrix = [[0 for _ in range(cols)] for _ in range(rows)] # Create scoring matrix filled with zeros
       
    # Score
    for i in range(1, rows): # first row/column is 0 so starts in second
        for j in range(1, cols):
            if seq1[j-1] == seq2[i-1]:
                diag = matrix[i-1][j-1] + match_score # if two align get match point
            else:
                diag = matrix[i-1][j-1] - mismatch_penalty # if two do not align, mismatch penalty

            up = matrix[i-1][j] - gap_penalty # puts gap penalty in seq1
            left = matrix[i][j-1] - gap_penalty # puts gap penalty in seq2

            matrix[i][j] = max(0, diag, up, left) # highest score 
            if matrix[i][j] > max_score:
                max_score = matrix[i][j] # keeps track of highest score
                max_pos = (i, j) # where highest score is 
    # now the matrix is scored 
    # reconstructs which two aligned make best match
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = max_pos # start from cell with highest score 

    while matrix[i][j] != 0: # trace backwards until reach a 0 ie a stop does not match
        score_current = matrix[i][j] # score of current
        score_diag = matrix[i-1][j-1] # score of diagonal
        score_up = matrix[i-1][j] # score of above
        score_left = matrix[i][j-1] # score of left - which could have to this one

        if seq1[j-1] == seq2[i-1]:
            match = match_score
        else:
            match = -mismatch_penalty # is diagonal a match or mismatch, subtracts for mismatch 
        # how did we arrive at the cell - diagonal, left (gap in seq2), or up (gap in seq1)
        if score_current == score_diag + match:
            aligned_seq1 = seq1[j-1] + aligned_seq1
            aligned_seq2 = seq2[i-1] + aligned_seq2
            i -= 1
            j -= 1 # match was diagnoal; add to strink and move diagonally up and left 
        elif score_current == score_left - gap_penalty: # subtract for gap
            aligned_seq1 = seq1[j-1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            j -= 1 # came from left meaning seq2 has a gap, add - in a seq2 and move left 
        elif score_current == score_up - gap_penalty:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[i-1] + aligned_seq2
            i -= 1
        else: break

    # Print full matrix
    for row in matrix:
        print(row) 

    return aligned_seq1, aligned_seq2, max_score # return the aligned sequence and max score 
```
This function scores the given sequences, aligning them to the optimal local alignment and inserting a - as a gap when needed. It returns a matrix that is calculated by backtracking from biggest values and going left, up, or diagonally based on what will give the best score and alignment. 

I tested it with a small sequence that has obvious alignment at the beginning only.
```python 
smith_waterman('TACA', 'TATG')
('TA', 'TA', 2)
```
I also tested it using the sequences given in the problem set. The first being a longer sequence that has a score of 8.
```python 
smith_waterman('tgcatcgagaccctacgtgac', 'actagacctagcatcgac')

returns
('agacccta-cgt-gac', 'aga-cctagcatcgac', 8)
```

The second being the same sequence but with a gap penalty of 2 instead leading to a best score of 7 and a more aligned sequence in the middle being the best. 
```python
smith_waterman('tgcatcgagaccctacgtgac', 'actagacctagcatcgac', gap_penalty=2)

returns 
('gcatcga', 'gcatcga', 7)
```

I also tested it on totally identical sequences. 
```python 
smith_waterman('gggg', 'gggg')

returns
('gggg', 'gggg', 4)
```
and two totally difference sequences.
```python
smith_waterman('cccc', 'gggg')

returns
('', '', 0)
```
I then tested the same sequence first with a gap penalty of 0 that ended with a score of 6 and best alignment had a gap in the middle. 
```python
smith_waterman('ACGATCG', 'ACGGTCG', gap_penalty=0)

returns 
('AC-GATCG', 'ACGG-TCG', 6)
```

I tested the same sequence with a gap penalty of 2 and it ended with a score of 5 because with the higher gap penalty it perferred the mismatch in the middle instead.
```python
smith_waterman('ACGATCG', 'ACGGTCG', gap_penalty=2)

returns
('ACGATCG', 'ACGGTCG', 5)
```

Through these tests, I can see that my function works on short and long sequences, easy and difficult alighemnet choices, and differing penalties. 

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

I only say 5 crosses for 7 clusters so I printed the pca centers dataframe and saw cluser 1 has a high PCA 0 and cluster 5 has a high PCA1, so those clusers are off the screen, which can also be seen on the zoomed out version of the centers dataframe. 
['Scatterplot of zoomed out Centers PCA dataframe'](zoomed_out_centers.png)

I repeated the k-means clustering again with 7 clusters but different random states (2 and 5) and did not see any noticeable differences - there were still only 5 crosses in the zoomed in plane and a similar differential pattern. 
['Scatterplot of PCA K-Means with Random State 2'](x_centers_1.png)
['Scatterplot of PCA K-Means with Random State 5'](x_centers_2.png)

I then did clustering with only 3 clusters and thus 3 centers. With this test we saw noticebale difference in the clustering of the group and the centers all being within the frame. 
['Scatterplot of PCA K-Means with Clustering of 3'](x_centers_3.png)

I then did a clustering with 10 clusters. There is a lot more differentiation in groups on the zoomed in portion with 7 distinct colors being seen and 7 centers, meaning 3 clusters and centers were outside the zoomed in portion. In the full scatterplot, we can then see these clusters and centers. 
['Scatterplot of PCA K-Means with Clustering of 10 Zoomed in'](x_centers_4.png)
['Scatterplot of PCA K-Means with Clustering of 10 Zoomed out'](x_centers_5.png)

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

