## Problem 1 ##
**a.** I ysed the API to fetch 1000 Alzheimer's papers and 1000 cancer papers. I stored all the PubMed ids for each in their own list. 

```python
# find 1000 alz articles 
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "Alzheimers AND 2024[pdat]",
    "retmax": "1000",
    "retmode": "xml"
}

response = requests.get(base_url, params=params)
root = ElementTree.fromstring(response.text)

alz_ids = [id_elem.text for id_elem in root.findall(".//Id")]
print(f"Found {len(alz_ids)} Alzheimers articles.")
print(alz_ids[:10])  # show first 10 IDs
```

```python
# found all 1000 cancer papers
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "pubmed", # from PubMed
    "term": "cancer AND 2024[pdat]", #cancer
    "retmax": "1000", # only send 1000 articles
    "retmode": "xml" # sends in xml format
}

response = requests.get(base_url, params=params)
root = ElementTree.fromstring(response.text)

cancer_ids = [id_elem.text for id_elem in root.findall(".//Id")]
print(f"Found {len(cancer_ids)} cancer articles.")
print(cancer_ids[:10])  # show first 10 IDs
```
[1]

**b.**
I pulled the article title, the abstract text, journal title, Pubmed ID (PMID), and year of publication of each article. I made my code robust to be able to parse article titles that were in italics and bold and to pull all abstracts, even if they were structured. It runs on batches of 200 pulled PMIDs at a time with a 1 second sleep in between to respect pull rate limits. All the metadata stores in a list; any PMIDs that failed to be pulled are stored in a list; and all individual PMIDs are stored in a list for use in future problems. 
Originally, I had 1000 Alzheimer's articles being collected and only 999 cancer articles, so I included many sanity checks in case a PMID's metadata fails to be pulled. I also have a f-string at the end that prints how many articles had metadata pulled to ensure all 2000 ran or if any PMIDs that failed.

```python
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
all_alz_metadata = []
failed_pmids = []
alz_pmids =[]

for i in range(0, len(alz_ids), 200):  # batches of 200
    batch_ids = ",".join(alz_ids[i:i+200])
    fetch_params = {
        "db": "pubmed",
        "id": batch_ids,
        "retmode": "xml"
    }
    try:
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
        fetch_response.raise_for_status()
        root = ElementTree.fromstring(fetch_response.text)
    except Exception as e:
        print(f"Error fetching batch {i//200+1}: {e}")
        continue

    for article in root:
        try:
            title_elem = article.find(".//ArticleTitle")
            abstract_elems = article.findall(".//Abstract/AbstractText")
            journal_elem = article.find(".//Journal/Title")
            pmid_elem = article.find(".//PMID")
            date_elem = article.find(".//PubDate/Year")

            title_text = (
                ElementTree.tostring(title_elem, method="text", encoding="unicode").strip()
                if title_elem is not None
                else None
            )
            abstract_text = (
                " ".join(
                    ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    if elem.get("Label") else ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    for elem in abstract_elems
            )
            if abstract_elems
            else None
            )

            metadata = {
                "PMID": pmid_elem.text if pmid_elem is not None else None,
                "ArticleTitle": title_text,
                "AbstractText": abstract_text,
                "Journal": journal_elem.text if journal_elem is not None else None,
                "YearPublished": date_elem.text if date_elem is not None else None
            }
            all_alz_metadata.append(metadata)
            alz_pmids.append(metadata['PMID'])
        except Exception as e:
            pmid_text = pmid_elem.text if pmid_elem is not None else "UNKNOWN"
            print(f"Error parsing article PMID {pmid_text}: {e}")
            failed_pmids.append(pmid_text)
            continue

    time.sleep(1)

print(f"Retrieved metadata for {len(all_alz_metadata)} Alzheimers articles.")
print(f"Failed PMIDs in first pass: {len(failed_pmids)}")
```

```python
# fetch metadata for the 1000 cancer
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
all_cancer_metadata = []
failed_pmids = []
cancer_pmids =[]

for i in range(0, len(cancer_ids), 200):  # batches of 200
    batch_ids = ",".join(cancer_ids[i:i+200])
    fetch_params = {
        "db": "pubmed",
        "id": batch_ids,
        "retmode": "xml"
    }
    try:
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
        fetch_response.raise_for_status()
        root = ElementTree.fromstring(fetch_response.text)
    except Exception as e:
        print(f"Error fetching batch {i//200+1}: {e}")
        continue

    for article in root:
        try:
            title_elem = article.find(".//ArticleTitle")
            abstract_elems = article.findall(".//Abstract/AbstractText")
            journal_elem = article.find(".//Journal/Title")
            pmid_elem = article.find(".//PMID")
            date_elem = article.find(".//PubDate/Year")

            title_text = (
                ElementTree.tostring(title_elem, method="text", encoding="unicode").strip()
                if title_elem is not None
                else None
            )
            abstract_text = (
                " ".join(
                    ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    if elem.get("Label") else ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    for elem in abstract_elems
            )
            if abstract_elems
            else None
            )

            metadata = {
                "PMID": pmid_elem.text if pmid_elem is not None else None,
                "ArticleTitle": title_text,
                "AbstractText": abstract_text,
                "Journal": journal_elem.text if journal_elem is not None else None,
                "YearPublished": date_elem.text if date_elem is not None else None
            }
            all_cancer_metadata.append(metadata)
            cancer_pmids.append(metadata['PMID'])
        except Exception as e:
            pmid_text = pmid_elem.text if pmid_elem is not None else "UNKNOWN"
            print(f"Error parsing article PMID {pmid_text}: {e}")
            failed_pmids.append(pmid_text)
            continue

    time.sleep(1)

print(f"Retrieved metadata for {len(all_cancer_metadata)} Cancer articles.")
print(f"Failed PMIDs in first pass: {len(failed_pmids)}")
```
[2]

I then saved the metadata for each set of papers in their own JSON dictionary and combined them all into one JSON dictionary

```python
# make alzheimer's metadata json

json_alz_metadata = json.dumps(all_alz_metadata, indent=2)
print(json_alz_metadata[:500])

# make cancer's metadata json

json_cancer_metadata = json.dumps(all_cancer_metadata, indent=2)
print(json_cancer_metadata[:500])
print(type(json_cancer_metadata))

# one big json of both metadata

all_paper_metadata = all_alz_metadata + all_cancer_metadata

json_all_metadata = json.dumps(all_paper_metadata, indent=2)
print(json_all_metadata[:500])
```
[3] 

**c.**
To identify if there are any overlapping papers, I utilized the PMID lists made in the original pull of the metadata. I combined them into one variable then checked that variable for only unique instance. 
**Overall there were 1996 unique papers, meaning 4 overlapped.**

```python
# check for overlapping papers by combining all 

all_pmids = cancer_pmids + alz_pmids

all_pmids_unique = list(dict.fromkeys(all_pmids))

print(f"Total combined PMIDs: {len(all_pmids)}")
print(f"Unique PMIDs: {len(all_pmids_unique)}")
```
[4]

**d.**
I have in my original implementation of pulling metadata that it will pull all of the abstract, even if it is broken down into labeled sections. It will also include and keep the label included in the abstract. 
This does return none if there are papers without abstracts, which there are many. 
**Some limitations are that**

**Sources**
[1] I used ChatGPT to edit the API call given on the class slides and make it useable for this problem [2] Asked ChatGPT how to make a for loop for getting the metadata for each article gathered earlier. Also used to ensure adding in elements of time.sleep, gathering of structured abstracts, and special titles. Used it to trouble shoot when one cancer article's metadata was missing - what the article was and what could be the problem (it was a book chapter, not an article) [3] Used ChatGPT to make the json dictionaries [4] Used ChatGPT to drop the duplicate pmid in the overall list

## Problem 2 ##
**a. Load papers dictionary**
I installed Pytorch, huggingface, and the SPECTER model given. I pulled in the cancer and Alzheimer's papers just was done in 1. 

```python
# pull in 1000 alz articles
base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "pubmed",
    "term": "Alzheimers AND 2024[pdat]",
    "retmax": "1000",
    "retmode": "xml"
}

response = requests.get(base_url, params=params)
root = ElementTree.fromstring(response.text)

alz_ids = [id_elem.text for id_elem in root.findall(".//Id")]
print(f"Found {len(alz_ids)} Alzheimers articles.")

# pull in 1000 cancer paper

base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
params = {
    "db": "pubmed", # from PubMed
    "term": "cancer AND 2024[pdat]", #cancer
    "retmax": "1000", # only send 1000 articles
    "retmode": "xml" # sends in xml format
}

response = requests.get(base_url, params=params)
root = ElementTree.fromstring(response.text)

cancer_ids = [id_elem.text for id_elem in root.findall(".//Id")]
print(f"Found {len(cancer_ids)} cancer articles.")
```
Pulled in metadata again as well.
```python

# fetch metadata for the 1000 alzheimers
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
all_alz_metadata = []
failed_pmids = []
alz_pmids =[]

for i in range(0, len(alz_ids), 200):  # batches of 200
    batch_ids = ",".join(alz_ids[i:i+200])
    fetch_params = {
        "db": "pubmed",
        "id": batch_ids,
        "retmode": "xml"
    }
    try:
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
        fetch_response.raise_for_status()
        root = ElementTree.fromstring(fetch_response.text)
    except Exception as e:
        print(f"Error fetching batch {i//200+1}: {e}")
        continue

    for article in root:
        try:
            title_elem = article.find(".//ArticleTitle")
            abstract_elems = article.findall(".//Abstract/AbstractText")
            journal_elem = article.find(".//Journal/Title")
            pmid_elem = article.find(".//PMID")
            date_elem = article.find(".//PubDate/Year")

            title_text = (
                ElementTree.tostring(title_elem, method="text", encoding="unicode").strip()
                if title_elem is not None
                else None
            )
            abstract_text = (
                " ".join(
                    ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    if elem.get("Label") else ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    for elem in abstract_elems
            )
            if abstract_elems
            else None
            )

            metadata = {
                "PMID": pmid_elem.text if pmid_elem is not None else None,
                "ArticleTitle": title_text,
                "AbstractText": abstract_text,
                "Journal": journal_elem.text if journal_elem is not None else None,
                "YearPublished": date_elem.text if date_elem is not None else None
            }
            all_alz_metadata.append(metadata)
            alz_pmids.append(metadata['PMID'])
        except Exception as e:
            pmid_text = pmid_elem.text if pmid_elem is not None else "UNKNOWN"
            print(f"Error parsing article PMID {pmid_text}: {e}")
            failed_pmids.append(pmid_text)
            continue

    time.sleep(1)

print(f"Retrieved metadata for {len(all_alz_metadata)} Alzheimers articles.")
print(f"Failed PMIDs in first pass: {len(failed_pmids)}")


# fetch metadata for the 1000 cancer
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
all_cancer_metadata = []
failed_pmids = []
cancer_pmids =[]

for i in range(0, len(cancer_ids), 200):  # batches of 200
    batch_ids = ",".join(cancer_ids[i:i+200])
    fetch_params = {
        "db": "pubmed",
        "id": batch_ids,
        "retmode": "xml"
    }
    try:
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
        fetch_response.raise_for_status()
        root = ElementTree.fromstring(fetch_response.text)
    except Exception as e:
        print(f"Error fetching batch {i//200+1}: {e}")
        continue

    for article in root:
        try:
            title_elem = article.find(".//ArticleTitle")
            abstract_elems = article.findall(".//Abstract/AbstractText")
            journal_elem = article.find(".//Journal/Title")
            pmid_elem = article.find(".//PMID")
            date_elem = article.find(".//PubDate/Year")

            title_text = (
                ElementTree.tostring(title_elem, method="text", encoding="unicode").strip()
                if title_elem is not None
                else None
            )
            abstract_text = (
                " ".join(
                    ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    if elem.get("Label") else ElementTree.tostring(elem, method="text", encoding="unicode").strip()
                    for elem in abstract_elems
            )
            if abstract_elems
            else None
            )

            metadata = {
                "PMID": pmid_elem.text if pmid_elem is not None else None,
                "ArticleTitle": title_text,
                "AbstractText": abstract_text,
                "Journal": journal_elem.text if journal_elem is not None else None,
                "YearPublished": date_elem.text if date_elem is not None else None
            }
            all_cancer_metadata.append(metadata)
            cancer_pmids.append(metadata['PMID'])
        except Exception as e:
            pmid_text = pmid_elem.text if pmid_elem is not None else "UNKNOWN"
            print(f"Error parsing article PMID {pmid_text}: {e}")
            failed_pmids.append(pmid_text)
            continue

    time.sleep(1)

print(f"Retrieved metadata for {len(all_cancer_metadata)} Cancer articles.")
print(f"Failed PMIDs in first pass: {len(failed_pmids)}")
```

I added a column named 'query' to be used later in the application of PCA - all the Alzheimer's papers would be tagged with 'Alzheimer's' and all cancer papers would be tagged with 'cancer.'
```python
for paper in all_alz_metadata:
    paper["query"] = "alzheimers"

for paper in all_cancer_metadata:
    paper["query"] = "cancer"
```

I converted all elements of the metadata into a dictionary.
```python
# convert list of all papers metadata into paper dictionary

papers = {
    paper["PMID"]: {
        "ArticleTitle": paper.get("ArticleTitle", ""),
        "AbstractText": paper.get("AbstractText", ""),
        "query": paper.get('query', "")
    }
    for paper in all_paper_metadata
    if paper.get("PMID")  # only include valid PMIDs
}

print(f"Prepared {len(papers)} papers for embedding generation.") # ensure all papers were processed
``` 
1996 unique papers were processed because of the 4 duplicate papers. 

I used the process given to find the SPECTER embeddings.
```python
def get_abstract(paper):
    return paper.get("AbstractText", "") or ""

embeddings = {}
for pmid, paper in tqdm.tqdm(papers.items()):
    data = [paper["ArticleTitle"] + tokenizer.sep_token + get_abstract(paper)]
    inputs = tokenizer(
        data, padding=True, truncation=True, return_tensors="pt", max_length=512
    )
    result = model(**inputs)
    # take the first token in the batch as the embedding
    embeddings[pmid] = result.last_hidden_state[:, 0, :].detach().numpy()[0]

# turn our dictionary into a list
embeddings = [embeddings[pmid] for pmid in papers.keys()]
```
I used the sklearn module to identify the first three principal components.
```python
pca = decomposition.PCA(n_components=3)
embeddings_pca = pd.DataFrame(
    pca.fit_transform(embeddings),
    columns=['PC0', 'PC1', 'PC2']
)
embeddings_pca["query"] = [paper["query"] for paper in papers.values()]
```

**Plot 2D scatter plots for PC0 vs PC 1 vs PC2 and PC1 vs PC2; color code these by the search query used (Alzheimers vs cancer).**

**Comment on separation or lack thereof, and any takeaways from that**
We can see in the first graph, that comparing the PC0 and PC1 there is pretty clear seperation between the two papers with minimal overlap. When comparing PC0 to PC2, there is less overlap at the lower end of PC2 but there is still good seperation at the top. In the comparison between PC1 and PC2 we see the most overlap

## Problem 3 ##
I plotted on a log-log graph the difference between the calcutating the derivative numerically and analytically. I labeled the x axis as h or steps and the y axis as the difference between the numerical and analytic approach.

['Line graph showing difference between derivative approaches'](derivative.png)

Moving from right to left on the graph, you can see that as h (or the steps) decreases, the difference (or error) also decreases. This is good and expected in the calculus world. However, we begin to see how very small steps is bad in the computer world. While small steps is good for having small error, computers don't like small numbers, so we see the graph begin to look funky around 10^-8 and actually start to increase in error again. 

This is because computers don't like this super small steps and it is creating compounding error issues that are then seen on our graph. 

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