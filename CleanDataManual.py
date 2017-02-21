# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 14:25:55 2017

@author: cglynn

Cleans collected data to compute three metric including API recall, 
quality recall, and quality precision.

Necessary Files
retrieved tweets from file retrievedTweets.data
Tweets from random sample from file: randomSampleTweets.data
"""
import json

#d prime.  List of tweets from random sample
dPrime = []
dPrimeFile = 'randomSampleTweets.data'
#mprime list of tweets retrieved from search
mPrime = []
mFile = 'retrievedTweets.data'

def populateDprime():
    global dPrime
    with open(dPrimeFile) as file:
        tweetsFile = file.readlines()
        dPrime = json.loads(tweetsFile[0])

def populateMprime():
    global mPrime
    global dPrime
    tweetsFound = []
    with open(mFile) as file:
        tweetsFile = file.readlines()
        tweetsFound = json.loads(tweetsFile[0])
    for allTweets in dPrime:
        allTweets['query'] = 'false'
        allTweets['positive'] = 'false'
        for foundTweet in tweetsFound:
            if(allTweets['id'] == foundTweet['id']):
                mPrime.append(foundTweet)
                allTweets['query'] = 'true'
#    print 'MPrime length: ' , len(mPrime)
#    print 'DPrime length: ' , len(dPrime)
            
def removeEntriesForManual():
    global dPrime
    global mPrime
    dPrime = updateKeys(dPrime)
    mPrime = updateKeys(mPrime)

#remove extraneous keys and add keys for manual classification
def updateKeys(dictionaryList):
    temporaryList = []
    keysToRemove=("favorited", "contributors", "truncated", "source_url", "geo", "created_at", "retweeted", "coordinates", "source", "id_str", "retweet_count")
    for dictionary in dictionaryList:    
        for key in keysToRemove:
            if key in dictionary:
                del dictionary[key]
        temporaryList.append(dictionary)
    return temporaryList
    
def saveToFile():
    with open("cleanRetrieved.data", 'w') as file:
        file.write(json.dumps(mPrime))
    with open("cleanRandomSample.data", 'w') as file:
        file.write(json.dumps(dPrime))
 
if __name__ == '__main__':
    populateDprime()
    populateMprime()
    removeEntriesForManual()
    saveToFile()