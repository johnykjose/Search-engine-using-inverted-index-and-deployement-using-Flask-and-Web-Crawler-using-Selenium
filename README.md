# Search-engine-using-inverted-index-and-deployement-using-Flask
![Search Engine home page](https://github.com/johnykjose/Search-engine-using-inverted-index-and-deployement-using-Flask-in-python/blob/main/images/se_home.png?raw=true)

A vertical search engine using inverted index to retrieve research papers based on the search strings. 
Part 1 – Search engine
The search engine has been deployed as a Flask application with a user interface for the user to interact with the search engine. This is a fully automated application and manual intervention is not needed once it started. Complete backed applications are developed in Python and front end with Flask, html and CSS.

****1.	Crawler****

The web crawler is capable of identifying all the profiles of Coventry University Faculties in Google Scholar and every papers published by them in a BFS manner. The main component of my web crawler is a Selenium driver which can go through every pages by identifying the JavaScript buttons (e.g. Next, Show more) in Google scholar and crawl through. Beautiful Soup library is used to extract relevant details from the html pages. 

1.1	Dataset created by the Crawler
Number of records fetched by the crawler is below
 
All the data extracted by the crawler is saved into a CSV file as shown below
 


1.2	Attributes fetched by the Crawler
Paper details fetched from the Google Scholar are,
Title- Title of the research paper
Authors- Author details of the paper
Link- Link to the actual source of the paper (e.g. www.Sciencedirect.com)
1.3	Pre-Processing steps before indexing
•	Combining  author details and titles to include author keywords in the search engine
•	Cleaning the data
•	Removing unnecessary characters (e.g. /,:,#) using regular expressions
•	Keeping only the alphabets after removing whitespaces using regular expressions
•	Conversion to lowercase letters
•	Converting the text to list of words
•	Removing the stop words using nltk.corpus tool stop words for English
•	Stemming to normalise the words using snowballstemmer tool for English
•	Sample data before and after cleaning
 


1.4	Crawler scheduler
Crawler is scheduled to run in every 10 days using python schedule library
 
1.5	Working
The Crawler will be fetching all the Coventry University profiles and all of their papers in BFS manner. 
Step 1:  When start_crawler() executes, the base URL of Google scholar Coventry University page is passed to the method crawler_profiles() to fetch the profile links of Coventry University staffs. This profile links are stored to avoid any data loss.
Step 1.1: For every profiles fetched in step#1, their, profiles pages will be visited and loads all of their papers.
Step 1.1.1: For every papers of each profiles, their actual source link, author details and titles are fetched and stored
Note that the web crawler and data extractions happens in BFS manner. Selenium driver is used to redirect to next pages automatically. Also, it controls the JavaScript buttons to use ‘show more’ button in the profile to load all the papers. Sample output of the crawler is given below
 
The number of papers found and completion status after fetching it will also be displayed. The final data with all the crawled data will be stored to a CSV file to be consumed by the indexer.
	       
****2.	Indexer****
2.1	Index architecture and data structure used
An index is created to be used by the query engine. Inverted index is the data structure used and it is a dictionary of nested dictionaries. The structure of Inverted index is given below
 

Fields are,
Word- word
Document frequency – number of documents where the word occurred
Term frequeny- Number of times the word occurred in all the docs
Douments- documents with the word
Doc_id- indices are used as doc identifier
Frequeny – Number of occurrences of word in the doc
Position – positions of word in the doc

The ‘document frequency’ is used while calculating the TF-IDF score and positions are for future work while doing phrase querying.

2.2	Updating the indexer
Every time the crawler fetches the data successfully, then it automatically calls the method to update the index. Index is made from the scratch every time. After updating the index, a status value of ‘Done’ will be added in the settings.csv file to inform the front end Flask application to load the new index for query processing.
2.3	Contents
Giving below a sample content of the index.
 
2.4	Working
Step 1: The main_indexer() function takes the input data.csv
Step 2: Cleaning is done on the data as in the section #1.3 and all the documents will be tokenised into words after the pre-processing.
Step 3: indexer() method is called for all pre-processed data to add it to the inverted index. Inverted index structure is already explained above.
Step 4: The inverted index is exported into a pickle files to store it permanently
Step 5: Update the settings.csv file to notify the Flask app to reload the new index into it.

****3.	Query processor****
3.1	Query type
User can input the search query in the Flask web app. And after all the pre-pre-processing steps it will be passed to application engine to process further. This search engine can accept keywords like Google does (without any need for AND, OR, NOT etc.). All the results will be displayed in the web application in the order of its relevance to the query
3.2	Ranking the results
TF-IDF is used as the scoring mechanism. Score will be calculated for every documents against the search query
 











Displaying the results to user for the query given as author name “TIMOTHY”

 
The web app will display the results in such a way that the more relevant ones (higher  TF.IDF score) will be coming at the top. Details displayed are,
•	Results sorted according to their TF.IDF score. Results have,
o	Title of the doc
o	Link to the actual paper
o	Fields using multi-label classifier trained on 19k+ data.
o	Author details
•	Total number of results found
•	Time taken to get the results
•	Query by the user

3.4	Working
Step 1: Starting the web server. While starting it will load the Inverted index, multi-label classification model and the papers details to display.
Step 2: User can input the search string in the input field and hit on search button provided by the Flask web app.
Step 3: search query being received by the application back end.
1: Cleaning and pre-processing the query as in section #1.3
2: Iterating through the index and fetches the terms (words) and values (docs) of all the words in the pre-processed user query
3: TF-IDF score is calculated for all the docs fetched in step #3.2
4: Docs are sorted based on their TF-IDF ranking score
5: Results are being sent back to the web app front end
6: Checks the setting.csv file to see if new index and data is available. If available index and data will be reloaded to the web server and update the settings.csv as reloaded.
  Step 4: Displaying the results in web page with all the details discussed before

4.	Features added
4.1	Deployment of the search engine so that user can use it directly
4.2	FULLY automated process once it started
4.3	Extra components in the web crawler
•	VPN rotating feature to change the network in case the crawler get blocked
•	Random delays before every request to deal nicely with the source website
•	Dynamic user agents to the header of request drivers to make the crawling pattern different.

Part 2 – Subject classification (text classification)

1.	Data
Here, I have used a dataset found in Kaggle website which is having 20972 records with the details such as title, abstract, field.

Link to the dataset- https://www.kaggle.com/shivanandmn/multilabel-classification-dataset

Giving below a sample of dataset
 

The dataset is having paper details of in 6 fields. Giving below plot showing the number papers in each field
 

A quick analysis on the length of characters in each paper is giving beow
 
I have also done a correlation analysis between the classes to see how each of the fields are correlated
 
We can see that most of the fields are correlated each other.

2.	Pre-processing
As part of the pre-processing step, we have done the below processes on data
1.	Cleaning
•	Removing the unnecessary characters and white spaces
•	Keeping only the alphabets
•	Conversion to lower case
2.	Stemming – Here, using the PortStemmer() tool, all the data have been normalised.
3.	Stop words removal – Stop words are removed from the titles and abstracts
4.	Using TFIDF vectoriser, all the input data (abstracts values) values are vectorised.
Giving below a quick analysis on the important or frequent words in the data
 
Words with higher occurrences are at the top.

3.	Model Development and evaluation
The final pre-processed data is divided into training and test dataset (20%). Here, we have used only the abstracts to train the data because our crawled data is having only titles as the model input. I chose to train using abstracts instead of titles of papers after observing higher performance with abstract.
Model used:  LinearSVC() with OneVsRestClassifier() –model LinearSVC() is selected after comparing the results of other algorithms DecisionTreeClassifier, LogisticRegression, XGBClassifier.
During the model development, OneVsRestClassifier() is instantiated with the LinearSVC() model. One Vs Rest classifier is used in order to equip the model to output multiple labels if match is found. 
To evaluate the model, I have used the concept of hamming score because the typical classification accuracy metric would not be the best to evaluate a multi-label problem. 
Hamming score achieved: 76.21%
Considering the difficulty of the text inputs given to model training and the high correlation between the classes, we can conclude that the score of 76.2% is fair enough. Also, for a paper classification problem, a high accuracy is not mandatory as the decision made is not of high impact.
Model and vectorizer are exported to pickle files to be used by the search engine for classifying the papers 
4.	Working
Step 1: Model and vectorizer are loaded to Flask web app which starting the web server
Step 2: Every time a new query comes, the query processor will be identifying all the documents relevant to the user query. Query processor working is already explained. 
Step 3: For all the result documents’ titles,
1.	Title is cleaned and pre-processed as explained in the pre-processing section
2.	Title is input to the model to predict the labels.
3.	If labels are not found an info string ‘to be updated soon!’ will be sent
Step 4: Corresponding classification labels will also be sent to the front end app along with the result documents.
Step 5: labels will be displayed as ‘Fields’ to the user
