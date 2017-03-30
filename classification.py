# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:10:39 2017

@author: cglynn
"""

import json, numpy as np
from operator import itemgetter
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn import datasets

training_File = 'training_tweets.txt'
query_terms_File = 'query.data'


#iris = datasets.load_iris()
#iris.data.shape, iris.target.shape
#print iris.data

#Read in tweets for training from list ['Class label, tweet text]
trainingTweets = []
with open(training_File) as file:
    tweetsFile = file.readlines()
    trainingTweets = json.loads(tweetsFile[0])

#Read in Query Terms in dictionary
queryDictionary = dict()
queryTerms = []
with open(query_terms_File) as file:
    queryFile = file.readlines()
    queryTerms = json.loads(queryFile[0])
for term in queryTerms:
    queryDictionary[term] = 0

# Compute the top 10 query terms used
queryTopTen = []
trainingList = []
for trainingTweet in trainingTweets:
    trainingData = trainingTweet.split(',')
    trainingList.append(trainingData)
    terms = trainingData[1].split()
    for term in terms:
        if queryDictionary.has_key(term):
            queryDictionary[term] += 1 
queryList = sorted(queryDictionary.items(), key=itemgetter(1))
for term in queryList[-10:]:
    queryTopTen.append(term[0])
print 'Top ten terms' ,queryTopTen
        
#Generate numpy ndarray
numFeatures = 10
numObjects = len(trainingList)
row = 0
feature = 0
featureVector = np.zeros((numObjects,numFeatures), (int))
classVector = np.zeros((numObjects,), (int))
for tweet in trainingList[:numObjects]:
    tweetTerms = tweet[1].split()
    classVector[row] = tweet[0]
    for queryTerm in queryTopTen:
        for term in tweetTerms:
            if term.lower() == queryTerm.lower():
                featureVector[row,feature] += 1
        feature +=1
    row += 1
    feature = 0

#Train the SVM Model
#clf = svm.SVC(kernel='linear', C=1).fit(featureVector, classVector)

# 10 folder cross validation to estimate the best w and b
clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, featureVector, classVector ,cv=10)
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() *2))

## predict the class labels of new tweets
#print clf.predict(X)
#tweets = []
#for line in open('testing_tweets.txt').readlines():
#    tweets.append(line)
#
## Generate X for testing tweets
#X = []
#for text in tweets:
#    x = [0] * len(vocab)
#    terms = [term for term in text.split() if len(term) > 2]
#    for term in terms:
#        if vocab.has_key(term):
#            x[vocab[term]] += 1
#    X.append(x)
#y = clf.predict(X)
#
## print 100 example tweets and their class labels
#for idx in range(1,100):
#    print 'Sentiment Class (1 means positive; 0 means negative): ', y[idx]
#    print 'TEXT: ', idx, tweets[idx]
#
#print sum(y), len(y)
