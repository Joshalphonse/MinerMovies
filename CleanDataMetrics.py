# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:25:55 2017

@author: cglynn

Cleans collected data to compute three metric including API recall, 
quality recall, and quality precision.

Necessary Files
retrieved tweets from file retrievedTweets.data
Tweets from random sample from file: cleanRandomSampleTraining.data created from 
    classification.
"""
import json

dPrimeFile = 'cleanRandomSampleTraining.data'
mFile = 'retrievedTweets.data'
query_terms_File = 'query.data'

def populateDprimeMprime():
    dPrime = []
    mPrime = []
    
#    Load Random Sample to dPrime
    with open(dPrimeFile) as file:
        tweetsFile = file.readlines()
        dPrime = json.loads(tweetsFile[0])

#   Load in retrieved tweets
    tweetsFound = []
    with open(mFile) as file:
        tweetsFile = file.readlines()
        tweetsFound = json.loads(tweetsFile[0])
        
#Add labels for query.  Label found tweets as matching the query.
    for allTweets in dPrime:
        allTweets['query'] = 'false'
        for foundTweet in tweetsFound:
            if(allTweets['id'] == foundTweet['id']):
                mPrime.append(foundTweet)
                allTweets['query'] = 'true'

        #Read in Query Terms in dictionary
    queryDictionary = dict()
    with open(query_terms_File) as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    for term in queryTerms:
        terms = term.split()
        for word in terms:
            queryDictionary[word] = 0
            
#    If tweet contains a query term, matches query.
    for tweet in dPrime:
        if tweet['query'] == 'false':
            for words in tweet['text'].split():
                if queryDictionary.has_key(words.lower()):
                    tweet['query'] = 'true'
            
    with open("cleanRetrieved.data", 'w') as file:
        file.write(json.dumps(mPrime))
    with open("cleanRandomSample.data", 'w') as file:
        file.write(json.dumps(dPrime))
 
if __name__ == '__main__':
    populateDprimeMprime()