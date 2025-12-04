## About the Dataset
**Describe the dataset and why it is interesting.**
I chose to analyze the Social Determinants of Health (SDOH) dataset, which is a large collection of data collected by different federal entities conjoined together and managed by the Agency for Healthcare Research and Quality (AHRQ). The SDOH has been published from 2010-2020 and consists of almost 1,000 variable every county, zip code, and census tract in the US. *I chose to analyze on a county level because it is the highest level of the options.* 
Specifically, I pulled variables from the Provider of Service (POS) dataset and the Area Health Resources Files (AHRF) dataset. 

From the POS dataset, I used the maximum, median, and mean distance to ER, med-surgical ICU, and designated trauma center. The POS data is collected by the Centers of Medicaid and Medicare quarterly. *Who fills it out* 

From the AHRF dataset, I used the Rural-Urban Continuum Codes (RUCC) from 2013. These codes are originally developed and collected by the USDA every decade. The codes for each county in the USA are  

**Explain how you acquired it (e.g. via an API, file download, etc).**
I acquired my data via a file download. On the SDOH website, they offer a direct file download of a xlsx file for every year at each level that is offered. 


# FAIR Data
**Discuss the FAIRness of the data provider.**
**FAIR is a journey not a destination, so when considering each aspect find something that it does well and something that could be done better**
**Include: Was the data well-annotated with metadata? Was the license clear?**
F - findable
A - 
I - 
R - 


# Data Cleaning
**Describe any data cleaning or other preprocessing.**
**e.g. If some data was missing, how did you handle it?**
Data cleaning was minimal

In 2019, Alaska split some counties and thus 2 new ones were created that did not have 2013 RUCC codes. *What shall I do with this*

# Summary Statistics
**Discuss summary statistics and how they do or do not reflect the characteristics of the data. (e.g. are they skewed by outliers, is missing data a problem? are they misleading because of non-continuous variables? etc?)**

# Analysis 
**Discuss the analyses you chose to run.**
**Why these questions?**
**What were the results?**
**Any surprises?**
I was actually suprised that most of the analysis followed the expectation of rural counties being farther from healthcare. I thought I would find some exceptions to this though but I did not. 

**How did you validate your analyses?**

# Web Front and API
**Describe your server API and the web front-end.**

# Discussion
**Mention any surprising results or unexpected difficulties.**
I considered being able to analyze multiple RUCC between each other but I didn't know how to do this without making the user face appear clunky. 

## Sources 
[1]Social Determinants of Health Database. Content last reviewed June 2023. Agency for Healthcare Research and Quality, Rockville, MD.
https://www.ahrq.gov/sdoh/data-analytics/sdoh-data.html - dataset
[2]https://www.shepscenter.unc.edu/wp-content/uploads/2015/12/ruralurbancodes2013c.pdf - images in analyze