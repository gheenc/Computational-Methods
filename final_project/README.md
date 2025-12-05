## About the Dataset
**Describe the dataset and why it is interesting.**
I chose to analyze the Social Determinants of Health (SDOH) dataset, which is a large collection of data collected by different federal entities conjoined together and managed by the Agency for Healthcare Research and Quality (AHRQ). The SDOH has been published from 2010-2020 and consists of almost 1,000 variable from differing federal survey for every county, zip code, and census tract in the US. I chose to analyze on a county level because it felt the most generalizable to the state level and I was using the Rural-Urban Classification Code (RUCC) that assigns a classification to every county in the United States. Additionally, even at the highest level of organization of county, there are 3,141 counties in the 50 United States so utilizing zip code or census tract for the entire US would be a large undertaking. Overall, I think the SDOH is interesting because it pulls so many variables from all the federal agencies and is a nice way to do comprehensive research. Within the SDOH, I specificlaly pulled variables from the Provider of Service (POS) dataset and the Area Health Resources Files (AHRF) dataset. 

From the POS dataset, I used the maximum, median, and mean distance to ER, med-surgical ICU, and designated trauma center. The POS data is collected by the Centers of Medicaid and Medicare quarterly. *Who fills it out* It caluclates them based on the population centroid of each census tract to ensure it is not measuring the farthest distance as a place where no one lives. 

From the AHRF dataset, I used the Rural-Urban Continuum Codes (RUCC) from 2013. These codes are originally developed and collected by the USDA every decade. The codes for each county in the USA are  

**Explain how you acquired it (e.g. via an API, file download, etc).**
I acquired my data via a file download. On the SDOH website, they offer a direct file download of a xlsx file for every year at each level that is offered making it easy to access the whole dataset. Because it is so large, it does create a big datafile for use, especially using as many variables for the whole country over many years like I did. I downloaded all the raw data from 2013-2020 and then only called in the columns I wanted to use (9 in total *not including the total number of*). When calling in the data like this to my Flask, it was extremely slow even as a pickled file, so I made the file a paraquet.

# FAIR Data
**Discuss the FAIRness of the data provider.**
**FAIR is a journey not a destination, so when considering each aspect find something that it does well and something that could be done better**
**Include: Was the data well-annotated with metadata? Was the license clear?**
F - findable
A - 
I - 
R - 

The data was pretty well annotated but because the SDOH comes from many different sources, there are annotations that were missing. 
Yes, the license is clear that these are federal agencies and thus the data is free and available. There are stipulations if one is wanting to publish, 


# Data Cleaning
**Describe any data cleaning or other preprocessing.**
**e.g. If some data was missing, how did you handle it?**
The datasets I chose within the SDOH were very comprehensive and required little cleaning or imputations. 
After pulling in the wanted columns for each year from the raw excel file, I dropped any rows that were not from the 50 states. DC is not seperated in the calculations of RUCC or in the POS survey, so I believe it's data is wrapped into Maryland and Virginia, respectively. *Puerto Rico*. For each year, I printed any rows which were missing. 

2013: trauma - Alaska Aleutians East Borough
icu and trauma - Alaska West Census Area

2014: trauma - Alaska Aleutians East Borough
icu and trauma - Alaska West Census Area

2015: trauma - Alaska Aleutians East Borough, Nome Census Area, North Slope Borough, Northwest Artcitc Borough
icu and trauma - Alaska West Census Area

2016: trauma and icu - Alaska Aleutians West Census Area
trauma - Alaska North Slope Borough 

2017: trauma and icu - Alaska West Census Area
trauma - Alaska North Slope Borough

2018: trauma and icu - Alaska West Census Area

2019:trauma and icu - Alaska West Census Area

2020: trauma and ice - Alaksa West Census Area
everything including RCC - Alaska Valdez-Cordova Census Area
RUCC - Chugach Census Area, Cooper River Census Area - have distance to hospitals but do not have RUCC codes. There are 4 hospitals in Chugach Census and 1 in Copper River. 

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
*Switch the way the API and county counts interact. have county counts pull from api rather than api use county counts*
*AJAX Query to have plot appear and actively change as requested*
*debate if use map - a lot to zooom up*

**Recommendations from video**

# Discussion
**Mention any surprising results or unexpected difficulties.**
I considered being able to analyze multiple RUCC between each other but I didn't know how to do this without making the user face appear clunky. 

## Sources 
[1]Social Determinants of Health Database. Content last reviewed June 2023. Agency for Healthcare Research and Quality, Rockville, MD.
https://www.ahrq.gov/sdoh/data-analytics/sdoh-data.html - dataset
[2]https://www.shepscenter.unc.edu/wp-content/uploads/2015/12/ruralurbancodes2013c.pdf - images in analyze