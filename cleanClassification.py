# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:11:57 2017

@author: cglynn

Cleans collected data for classification
puts tweet text into file labeled_tweets.txt as list
0, tweet_text 

Necessary Files
retrieved tweets from file retrievedTweets.data
"""

import json,  sets

tweetList = []
tweetSet = sets.Set()

retrievedFile = 'retrievedTweets.data'

def populateTweetList():
    global tweetList
    with open(retrievedFile) as file:
        tweetsFile = file.readlines()
        tweetList = json.loads(tweetsFile[0])

def populateTweetSet():
    global tweetSet
    global tweetList
    for tweet in tweetList:
            tempText = '0,' + tweet['text']
            tweetSet.add(tempText)
    tweetList = []
    tweetList = list(tweetSet)
            
 
def saveToFile():
    with open("training_tweets.txt", 'w') as file:
        file.write(json.dumps(tweetList))
 
if __name__ == '__main__':
    populateTweetList()
    populateTweetSet()
    saveToFile()