# %%
import pandas as pd
from sklearn import decomposition
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.cluster import KMeans
import numpy as np
from plotnine import *
import warnings
from matplotlib import *


# %%
warnings.filterwarnings("ignore", message="Could not find the number of physical cores")


# %%
# import Excel sheet
data = pd.read_csv(r"C:\Users\carol\compmethods-cg2288\pset4\eeg-eye-state.csv")

# %%
# drop categorical column
data = data.drop(columns=["eyeDetection"])

# %%
# visualize data 
data.head()

# %%
# define variable that will standardize a series
def standardize(series):
    return (series - series.mean()) / series.std()

# %%
# standardize data set
data_standard = data.apply(standardize)
data_standard.head() # visualize to ensure all standard

# %%
# no need to do embeddings like previous problem set because csv is already numbers
pca_raw = decomposition.PCA() # performed on all components
pca = pd.DataFrame(
    pca_raw.fit_transform(data_standard)
)
pca = pca.rename(columns={0: 'PCA0', 1: 'PCA1'})

# %%
pca.head()

# %%
print(pca.columns.tolist())


# %%
# plot PCA0 vs PCA1

fig = make_subplots(rows=1, cols=1)

fig.add_trace(
    go.Scatter(
        x=pca['PCA0'],
        y=pca['PCA1'],
        mode='markers',
        marker=dict(size=6, opacity=0.7),
        name="PCA Points"
    ),
    row=1, col=1
)

fig.update_layout(
    title="EEG Eye State - PC0 vs PC1",
    xaxis_title="PC0",
    yaxis_title="PC1",
    template="plotly_white"
)

fig.write_image('Zoom_Out_PCA.png')
fig.show()


# %%
# zoom in near origin
fig = make_subplots(rows=1, cols=1)

fig.add_trace(
    go.Scatter(
        x=pca['PCA0'],
        y=pca['PCA1'],
        mode='markers',
        marker=dict(size=6, opacity=0.7),
        name="PCA Points"
    ),
    row=1, col=1
)

fig.update_layout(
    title="EEG Eye State - PC0 vs PC1",
    xaxis_title="PC0",
    yaxis_title="PC1",
    template="plotly_white",
    xaxis_range=[-2, 4],
    yaxis_range=[-1.5,1.5],
    width=800,
    height=800
)

fig.write_image('Zoom_PCA.png')
fig.show()


# %%
# implement k-means clustering with sklearn library. 
# k=7; init=random
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html

kmeans = KMeans(n_clusters=7, init="random", random_state=1).fit(data_standard)

pca["cluster"] = kmeans.labels_
pca["cluster"] = pca["cluster"].astype(str) # makes string so can be plotted as discrete and not continuous

# %%
centers_df =  (
    pca.groupby('cluster')[['PCA0','PCA1']]
    .mean()
    .reset_index()

)

# %%
centers_df

# %%
# # Asked ChatGPT how to make scatterplot of kmeans, order the legend and add center of clusters
# add cluster to PCA dataframe
# makes string so can be plotted as discrete and not continuous

cluster_order = [str(i) for i in range(7)]  # Specifying order of clusters for legend


# %%
# adds center 
# asked ChatGPT how to make it plottable
centers_pca = pca_raw.transform(kmeans.cluster_centers_)
centers_df = pd.DataFrame(centers_pca[:, :2], columns=['PCA0', 'PCA1'])

# %%
centers_df

# %%
# testing to determine what clusters are being plotted in viewing plane
from scipy.spatial.distance import pdist, squareform
dists=squareform(pdist(centers_df[['PCA0','PCA1']]))
np.set_printoptions(precision=4, suppress=True)
print(dists)

# %%
pca.head()

# %%

# seeing if any pca centers are being dropped due to na
pca.isna().sum()

# %%
import matplotlib.pyplot as plt


# %%
# two centers outside df
plt.scatter(centers_df["PCA0"], centers_df["PCA1"])
plt.savefig('zoomed_out_centers.png')


# %%
graph = (
    ggplot(pca, aes(x='PCA0', y='PCA1', color='cluster')) 
    + geom_point(size=2, alpha=0.7) 
    + geom_point(
        data=centers_df,
        mapping=aes(x='PCA0', y='PCA1'),
        shape='x', 
        size=3,  
        color='black' 
    ) 
    + labs(
    x='PCA0',
    y='PCA1',
    title = 'K-Means Clustering on EEG Eye State - PCA0 vs PCA1'
) + theme_minimal()
+ xlim(-2, 3.5)
+ ylim(-1.5, 1.5)
)

graph.save('x_centers.png')
graph


# %%
# implement kmeans multiple times

kmeans_1 = KMeans(n_clusters=7, init="random", random_state=2).fit(data_standard)

pca["cluster_1"] = kmeans_1.labels_
pca["cluster_1"] = pca["cluster_1"].astype(str) # makes string so can be plotted as discrete and not continuous


cluster_order_1 = [str(i) for i in range(7)]  # Specifying order of clusters for legend

centers_pca_1 = pca_raw.transform(kmeans_1.cluster_centers_)
centers_df_1 = pd.DataFrame(centers_pca_1[:, :2], columns=['PCA0', 'PCA1'])

graph = (
    ggplot(pca, aes(x='PCA0', y='PCA1', color='cluster_1')) 
    + geom_point(size=2, alpha=0.7) 
    + geom_point(
        data=centers_df_1,
        mapping=aes(x='PCA0', y='PCA1'),
        shape='x', 
        size=3,  
        color='black' 
    ) 
    + labs(
    x='PCA0',
    y='PCA1',
    title = 'K-Means Clustering on EEG Eye State - PCA0 vs PCA1 - Random State 2'
) + theme_minimal()
+ xlim(-2, 3.5)
+ ylim(-1.5, 1.5)
)

graph.save('x_centers_1.png')
graph

# %%
# implement kmeans multiple times

kmeans_2 = KMeans(n_clusters=7, init="random", random_state=5).fit(data_standard)

pca["cluster_2"] = kmeans_2.labels_
pca["cluster_2"] = pca["cluster_2"].astype(str) # makes string so can be plotted as discrete and not continuous


cluster_order_2 = [str(i) for i in range(7)]  # Specifying order of clusters for legend

centers_pca_2 = pca_raw.transform(kmeans_2.cluster_centers_)
centers_df_2 = pd.DataFrame(centers_pca_2[:, :2], columns=['PCA0', 'PCA1'])

graph = (
    ggplot(pca, aes(x='PCA0', y='PCA1', color='cluster_2')) 
    + geom_point(size=2, alpha=0.7) 
    + geom_point(
        data=centers_df_2,
        mapping=aes(x='PCA0', y='PCA1'),
        shape='x', 
        size=3,  
        color='black' 
    ) 
    + labs(
    x='PCA0',
    y='PCA1',
    title = 'K-Means Clustering on EEG Eye State - PCA0 vs PCA1 - Random State 5'
) + theme_minimal()
+ xlim(-2, 3.5)
+ ylim(-1.5, 1.5)
)

graph.save('x_centers_2.png')
graph

# %%
# implement kmeans multiple times

kmeans_3 = KMeans(n_clusters=3, init="random", random_state=0).fit(data_standard)

pca["cluster_3"] = kmeans_3.labels_ #labels_
pca["cluster_3"] = pca["cluster_3"].astype(str) # makes string so can be plotted as discrete and not continuous

cluster_order_3 = [str(i) for i in range(3)]  # Specifying order of clusters for legend

centers_pca_3 = pca_raw.transform(kmeans_3.cluster_centers_)
centers_df_3 = pd.DataFrame(centers_pca_3[:, :2], columns=['PCA0', 'PCA1'])

graph = (
    ggplot(pca, aes(x='PCA0', y='PCA1', color='cluster_3')) 
    + geom_point(size=2, alpha=0.7) 
    + geom_point(
        data=centers_df_3,
        mapping=aes(x='PCA0', y='PCA1'),
        shape='x', 
        size=3,  
        color='black' 
    ) 
    + labs(
    x='PCA0',
    y='PCA1',
    title = 'K-Means Clustering on EEG Eye State - PCA0 vs PCA1 - Cluster 3'
) + theme_minimal()
+ xlim(-2, 3.5)
+ ylim(-1.5, 1.5)
)

graph.save('x_centers_3.png')
graph

# %%
# implement kmeans multiple times

kmeans_4 = KMeans(n_clusters=10, init="random", random_state=0).fit(data_standard)

pca["cluster_4"] = kmeans_4.labels_ #labels_
pca["cluster_4"] = pca["cluster_4"].astype(str) # makes string so can be plotted as discrete and not continuous

cluster_order_4 = [str(i) for i in range(3)]  # Specifying order of clusters for legend

centers_pca_4 = pca_raw.transform(kmeans_4.cluster_centers_)
centers_df_4 = pd.DataFrame(centers_pca_4[:, :2], columns=['PCA0', 'PCA1'])

graph = (
    ggplot(pca, aes(x='PCA0', y='PCA1', color='cluster_4')) 
    + geom_point(size=2, alpha=0.7) 
    + geom_point(
        data=centers_df_4,
        mapping=aes(x='PCA0', y='PCA1'),
        shape='x', 
        size=3,  
        color='black' 
    ) 
    + labs(
    x='PCA0',
    y='PCA1',
    title = 'K-Means Clustering on EEG Eye State - PCA0 vs PCA1 - Cluster 10'
) + theme_minimal()
+ xlim(-2, 3.5)
+ ylim(-1.5, 1.5)
)

graph.save('x_centers_4.png')
graph

# %%
# implement kmeans multiple times

kmeans_5 = KMeans(n_clusters=10, init="random", random_state=0).fit(data_standard)

pca["cluster_5"] = kmeans_5.labels_ #labels_
pca["cluster_5"] = pca["cluster_5"].astype(str) # makes string so can be plotted as discrete and not continuous

cluster_order_5 = [str(i) for i in range(10)]  # Specifying order of clusters for legend

centers_pca_5 = pca_raw.transform(kmeans_5.cluster_centers_)
centers_df_5 = pd.DataFrame(centers_pca_5[:, :2], columns=['PCA0', 'PCA1'])

graph = (
    ggplot(pca, aes(x='PCA0', y='PCA1', color='cluster_5')) 
    + geom_point(size=2, alpha=0.7) 
    + geom_point(
        data=centers_df_5,
        mapping=aes(x='PCA0', y='PCA1'),
        shape='x', 
        size=3,  
        color='black' 
    ) 
    + labs(
    x='PCA0',
    y='PCA1',
    title = 'K-Means Clustering on EEG Eye State - PCA0 vs PCA1 - Cluster 10'
) + theme_minimal()
#+ xlim(-2, 3.5)
#+ ylim(-1.5, 1.5)
)

graph.save('x_centers_5.png')
graph


