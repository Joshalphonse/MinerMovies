# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 10:55:38 2017

@author: cglynn

Compute Metrics from twitter search
API Recall
Quality Precision
Quality Recall

Below two files are necessary to execute
Reads from randomSampleFile for random sample.  File contains attributes/keys
query and positive and ID.  
Reads from retrievedTweetsFile, used to compute tweets received.  Required keys: 
ID  
"""
import json, sets
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
randomSampleFile = 'cleanRandomSample.data'
#retrieved tweets file
retrievedTweetsFile = 'cleanRetrieved.data'
apiRecall = 0
qualityPrecision = 0
qualityRecall = 0

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
                    aPrime.add(foundTweet['id'])
                else:
                    mPrime.add(foundTweet['id'])    

def populateSets():
    global nPrime
    global bPrime
    global cPrime
    global dPrimeSet
    
    for tweet in dPrime:
        if(tweet['query'] == 'true'):
            if (tweet['positive'] == 'true'):
                bPrime.add(tweet['id'])
            else:
                nPrime.add(tweet['id'])
        else:
            if(tweet['positive'] == 'true'):
                cPrime.add(tweet['id'])
            else:
                dPrimeSet.add(tweet['id'])
    #Remove elements of mPrime from nPrime and aPrime from bPrime.
    nPrime = nPrime.difference(mPrime)
    bPrime = bPrime.difference(aPrime)

def computeMetrics(): 
    sizeAprime = float(len(aPrime))
    sizeMprime = float(len(mPrime) + sizeAprime)
    sizeBprime = float(len(bPrime))
    sizeNprime = float(len(nPrime) + sizeBprime + sizeMprime)
    sizeCprime = float(len(cPrime))
    global apiRecall
    global qualityPrecision
    global qualityRecall 
    
    #Add one to numerator/denominators to ensure not dividing by zero.
    #Api Recall M/N
    apiRecall = (sizeMprime + 1) / (sizeNprime + 1 )
    #Quality Precision A/M
    qualityPrecision = (sizeAprime + 1) / (sizeMprime + 1 )
    #Quality Recall A/(A+B+C)
    qualityRecall = (sizeAprime + 1)/(sizeAprime + sizeBprime + sizeCprime + 1 )
    
def printMetrics():
    print 'API Recall: ', apiRecall
    print 'Quality Precision: ', qualityPrecision
    print 'Quality Recall: ', qualityRecall
    

if __name__ == '__main__':
    populateDprime()
    populateMprimeAprime()
    populateSets()
    computeMetrics()
    printMetrics()
    
