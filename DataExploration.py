# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 08:41:00 2017

@author: cglynn
"""

import json, sets, matplotlib.pyplot as plt
#retrieved tweets
m = []
#retrieved tweets in dPrime
mPrime = sets.Set()
#retrieved positive tweets
aPrime = sets.Set()
#tweets in random sample match query
nPrime = sets.Set()
#tweets in random sample match query and are positive
bPrime = sets.Set()
#random sample that doesn't mathch query
dPrime = []
dPrimeSet = sets.Set()
#random sample that doesn't match query and is positive
cPrime = sets.Set()
#random Sample file with query and positive keys
randomSampleFile = 'cleanRandomSampleTraining.data'
#retrieved tweets file
retrievedTweetsFile = 'cleanRetrievedTraining.data'

def populateDprime():
    global dPrime
    with open(randomSampleFile) as file:
        tweetsFile = file.readlines()
        dPrime = json.loads(tweetsFile[0])

def populateMprimeAprime():
    global mPrime
    global aPrime
    tweetsFound = []
    with open(retrievedTweetsFile) as file:
        tweetsFile = file.readlines()
        tweetsFound = json.loads(tweetsFile[0])
    for allTweets in dPrime:
        for foundTweet in tweetsFound:
            if(allTweets['id'] == foundTweet['id']):
                if(allTweets['positive'] == 'true'):
                    aPrime.add(foundTweet['text'])
                else:
                    mPrime.add(foundTweet['text'])    

def populateSets():
    global nPrime
    global bPrime
    global cPrime
    global dPrimeSet
    
    for tweet in dPrime:
        if(tweet['query'] == 'true'):
            if (tweet['positive'] == 'true'):
                bPrime.add(tweet['text'])
            else:
                nPrime.add(tweet['text'])
        else:
            if(tweet['positive'] == 'true'):
                cPrime.add(tweet['text'])
            else:
                dPrimeSet.add(tweet['text'])
    #Remove elements of mPrime from nPrime and aPrime from bPrime.
    nPrime = nPrime.difference(mPrime)
    bPrime = bPrime.difference(aPrime)

def histogramPositiveLengthCount():
    wordCount=[] 
    tweets = sets.Set()
    tweets.update(aPrime)
    tweets.update(bPrime)
    tweets.update(cPrime)
    iterableTweets = list(tweets)
    for tweet in iterableTweets:
        wordCount.append(len(tweet))
    plt.hist(wordCount)
    plt.title("Length of Positive Tweets")
    plt.xlabel("Length of Tweets")
    plt.ylabel("Number of Tweets")

def histogramNegativeLengthCount():
    wordCount=[] 
    tweets = sets.Set()
    tweets.update(nPrime)
    tweets.update(mPrime)
    tweets.update(dPrimeSet)
    iterabletTweets = list(tweets)
    for tweet in iterabletTweets:
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
    tweets = sets.Set()
    tweets.update(aPrime)
    tweets.update(bPrime)
    tweets.update(cPrime)
    iterableTweets = list(tweets)
    for tweet in iterableTweets:
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
    tweets = sets.Set()
    tweets.update(nPrime)
    tweets.update(mPrime)
    tweets.update(dPrimeSet)
    iterableTweets = list(tweets)
    for tweet in iterableTweets:
        count = 0
        for word in tweet:
            if word.lower() in queryString:
                count = count+1
        queryCount.append(count)
    print queryCount
    plt.hist(queryCount)
    plt.title("Number of Query Terms in Negative Tweets")
    plt.xlabel("Number of query terms in Tweets")
    plt.ylabel("Number of Tweets")

if __name__ == '__main__':
    populateDprime()
    populateMprimeAprime()
    populateSets()
#    histogramPositiveLengthCount()
#    histogramNegativeLengthCount()
#    histogramPositiveQueryTermCount()
    histogramNegativeQueryTermCount()