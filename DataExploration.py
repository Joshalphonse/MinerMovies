# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 08:41:00 2017

@author: cglynn
"""

import json, sets, matplotlib.pyplot as plt
#All tweets in random sample classified manually
dPrime =[]
#Populate retrieved tweets.  All retrieved tweets
retrievedTweets = []
#List of positive tweets
positiveTweetList =[]
#List of negative tweets
negativeTweetList =[]
#random Sample file with query and positive keys populated manually
randomSampleFile = 'randomSampleTraining.data'
#retrieved tweets with query and positive keys populated manually
retrievedTweetFile = 'retrievedTrainingData.data'

def populateDprime():
    global dPrime
    global retrievedTweets
    with open(randomSampleFile) as file:
        tweetsFile = file.readlines()
        dPrime = json.loads(tweetsFile[0])
    with open(retrievedTweetFile) as file2:
        retrievedTweetsFile = file2.readlines()
        retrievedTweets = json.loads(retrievedTweetsFile[0]) 

def populateSets():
    positiveTweets = sets.Set()
    negativeTweets = sets.Set()
    global positiveTweetList
    global negativeTweetList
    
    for tweet in dPrime:
        if (tweet['positive'] == 'true'):
            positiveTweets.add(tweet['text'])
        else:
            negativeTweets.add(tweet['text'])
    for tweets in retrievedTweets:
        if (tweets['positive'] == 'true'):
            positiveTweets.add(tweets['text'])
        else:
            negativeTweets.add(tweets['text'])
    positiveTweetList = list(positiveTweets)
    negativeTweetList = list(negativeTweets)

def histogramPositiveLengthCount():
    wordCount=[] 
    for tweet in positiveTweetList:
        wordCount.append(len(tweet))
    plt.hist(wordCount)
    plt.title("Length of Positive Tweets")
    plt.xlabel("Length of Tweets")
    plt.ylabel("Number of Tweets")

def histogramNegativeLengthCount():
    wordCount=[] 
    for tweet in negativeTweetList:
        wordCount.append(len(tweet))
    plt.hist(wordCount)
    plt.title("Length of Negative Tweets")
    plt.xlabel("Length of Tweets")
    plt.ylabel("Number of Tweets")

def histogramPositiveQueryTermCount():
    queryCount=[] 
    queryTerms = []
    with open('query.data') as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    queryString = ' '.join(queryTerms)
    queryString = queryString.lower()

    for tweet in positiveTweetList:
        count = 0
        for word in tweet:
            if word.lower() in queryString:
                count = count+1
        queryCount.append(count)
    plt.hist(queryCount)
    plt.title("Number of Query Terms in Positive Tweets")
    plt.xlabel("Number of query terms in Tweets")
    plt.ylabel("Number of Tweets")
    
def histogramNegativeQueryTermCount():
    queryCount=[] 
    queryTerms = []
    with open('query.data') as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    queryString = ' '.join(queryTerms)
    queryString = queryString.lower()
    for tweet in negativeTweetList:
        count = 0
        for word in tweet:
            if word.lower() in queryString:
                count = count+1
        queryCount.append(count)
    plt.hist(queryCount)
    plt.title("Number of Query Terms in Negative Tweets")
    plt.xlabel("Number of query terms in Tweets")
    plt.ylabel("Number of Tweets")

if __name__ == '__main__':
    populateDprime()
    populateSets()
#    histogramPositiveLengthCount()
#    histogramNegativeLengthCount()
#    histogramPositiveQueryTermCount()
    histogramNegativeQueryTermCount()