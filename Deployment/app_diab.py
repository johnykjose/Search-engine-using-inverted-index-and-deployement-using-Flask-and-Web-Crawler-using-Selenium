# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 19:12:03 2020

@author: johny.jose
"""
from flask import Flask, request, render_template
from math import log, sqrt
from snowballstemmer import EnglishStemmer as es
from nltk.corpus import stopwords
import re
import numpy as np
import pickle
import pandas as pd
import random,time
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
porter = PorterStemmer()
#load vectorizer
file = open("indexer.pickle",'rb')
index = pickle.load(file)
file.close()
#load vectorizer
file = open("tfidf_vectorizer.pickle",'rb')
tfidf_vectorizer = pickle.load(file)
file.close()
#load model
file = open("clf.pickle",'rb')
clf = pickle.load(file)
file.close()
app = Flask(__name__)
indexer_flag = 1
#To check for new indexer
def check_for_new_Indexer():
    global index
    settings = pd.read_csv("C://Users/Johny/Google Drive/Cov Uni/IR/settings.csv")
    if settings["flag"][0]=="Done":
        #load vectorizer
        file = open("C://Users/Johny/Google Drive/Cov Uni/IR/indexer.pickle",'rb')
        index = pickle.load(file)
        file.close()
    settings = pd.DataFrame({'time':[time.time], 'flag':["No"]})
    settings.to_csv("C://Users/Johny/Google Drive/Cov Uni/IR/settings.csv")
# function for text cleaning 
def clean_text(text):
    # remove backslash-apostrophe 
    text = re.sub("\':.", "", text) 
    # remove everything except alphabets 
    text = re.sub("[^a-zA-Z]"," ",text) 
    # remove whitespaces 
    text = ' '.join(text.split()) 
    # convert text to lowercase 
    text = text.lower() 
    return text
def clean(text):
    # remove whitespaces 
    text = ' '.join(text.split()) 
    # convert text to lowercase 
    text = text.lower() 
    return text
#method to clean the query
def cleanQuery(string):
    englishStopWords = stopwords.words('english')
    string= clean_text(string)
    words = string.split()
    
    words = [word.lower() for word in words]
    words = [es().stemWord(word) for word in words]
    
    words = [word for word in words if word not in englishStopWords]
    
    return words
#method to rank using TF-IDF metric
def rank_Documents(index, words,doc_count):
    rankings = {}
    for word in words:
        doc_freq = index[word]['document frequency']
        for document in index[word]['document(s)'].keys():
            TF = index[word]['document(s)'][document]['frequency']
            IDF = log(doc_count/doc_freq)
            if TF > 0:
                TF = 1 + log(TF)
            else:
                TF = 0
            if document not in rankings:
                rankings[document] = TF*IDF
            else:
                rankings[document] += TF*IDF
    #sorting the results
    rankings = list(reversed(sorted(rankings.items(), key=lambda x: x[1])))
    return rankings
def get_index_data(idx):
    return index[idx]
def do_Search(user_input):
    words = cleanQuery(user_input)
    unknown_words = []
    # Collect the information for each word of the query
    query_index = {}
    doc_count = []
    for word in words:
        try:
            query_index[word] = get_index_data(word)
            doc_count = doc_count + list(index[word]['document(s)'].keys())
        except:
            unknown_words.append(word)
    # Rank the documents according to the query
    for w in words:  # iterating on a copy since removing will mess things up
        if w in unknown_words:
            words.remove(word)
    results = rank_Documents(query_index, words,len(set(doc_count)))
    #print(len(set(doc_count)))
    return results

stop_words = set(stopwords.words('english'))
def stemSentence(sentence):
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)
# function for text cleaning 
def clean_model_Input(text):
    # remove backslash-apostrophe 
    text = re.sub("\'", "", text) 
    # remove everything except alphabets 
    text = re.sub("[^a-zA-Z]"," ",text) 
    # remove whitespaces 
    text = ' '.join(text.split()) 
    # convert text to lowercase 
    text = text.lower() 
    
    return text

# function to remove stopwords
def remove_stopwords(text):
    no_stopword_text = [w for w in text.split() if not w in stop_words]
    return ' '.join(no_stopword_text)

def do_prediction(q):
    q = clean_model_Input(q)
    q = remove_stopwords(q)
    q = stemSentence(q)
    q_vec = tfidf_vectorizer.transform([q])
    y_pred = clf.predict(q_vec)
    return list(target[y_pred[0]==1])

cols_target = ['Computer Science','Physics','Mathematics','Statistics','Quantitative Biology','Quantitative Finance']
target = pd.Series(np.array(cols_target))
#loading the data
data = pd.read_csv("data.csv")
data['title'] = data['title'].apply(lambda x: clean(x))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    #now = datetime.now()
    #now = now.strftime("%H:%M:%S")
    #if now=="12:00:00":
    check_for_new_Indexer()
    if request.method == 'POST':
        input_str =request.form['search']
        #initialising list for final result
        titles=[]
        auths=[]
        links=[]
        startTime = time.time()
        #Doing the query processing
        for doc, score in do_Search(input_str):
            titles.append(data.iloc[doc,0])
            auths.append(data.iloc[doc,1])
            links.append(data.iloc[doc,2])
        prediction= []
        for t in titles:
            y = ",".join(do_prediction(t))
            if len(y) == 0:
                y='to be updated soon!'
            prediction.append(y)
        df = pd.DataFrame({'title':titles, 'link':links,'auth':auths,'class':prediction})
        input_str = "Results for: "+input_str
        total = 'Found '+str(df.shape[0])+ " records in ("+ str(round(abs(startTime-time.time()),5))+") Secs"
        return render_template('index.html',col_names =df.columns.values ,result=df.to_dict(orient='records'),zip=zip,total=total,input_str=input_str)
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(debug=False)