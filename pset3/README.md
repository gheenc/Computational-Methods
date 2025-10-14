## Problem 1 ##
**Fetch PubMed IDs: Use Entrez API to retrieve PubMed IDs for 1_000 Alzheimer's papers and 1_000 cancer papers for 2024.**

**Pull Metadata for Papers: Use Entrez API to pull metadata for each of the PubMed IDs retrieved. Save results in JSON file**

**Identify if any PubMed IDs present in both Alzheimer's and cancer paper sets**

**Ensure all sections (methods, backgrounds, results) in abstract are in metadata by concatenating them with spaces or using a list structure. Identify any limitations**


## Problem 2 ##
**Load papers dictionary**

**process dictionary of papers to find SPECTER embeddings. embeddings[i] is 768-dim vector for the ith paper**

**Apply principal component analysis to identify first three principal components**

**Plot 2D scatter plots for PC0 vs PC 1 vs PC2 and PC1 vs PC2; color code these by the search query used (Alzheimers vs cancer).**

**Comment on separation or lack thereof, and any takeaways from that**


## Problem 3 ##
**Plot on a log-log graph the difference between... varying between 10^-10 and 1**

**Describe what happens are h gets smaller and smaller**

**Offer hypothesis as to why you see the results you see**

## Problem 4 ##
**Write a python function that uses Explicit Euler method to plot I(t) given S(0), I(0), R(0), Beta, Gamma, and Tmax(last time point to compute)**

**Plot the time course of the number of infected invdividuals until that number drops below 1**

**When does number of infected people peak**

**How many people are infected at the peak**

**Vary Beta and Gamma over nearby values and plot on heat map how the time of the peak of the infection depends on two variables**

**Do same for number of individuals infected at peak**

## Problem 5 ##
**Do data exploration on data set**

**Present representative set of figures that gives insight into data. Comment on insights gained**

**Identify any data cleaning needs (including checking missing data) and write code to perform them.**

## Code Appendix ##