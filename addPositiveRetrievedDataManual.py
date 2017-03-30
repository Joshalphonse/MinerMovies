# -*- coding: utf-8 -*-
"""
Created on Fri Mar 03 16:16:09 2017

@author: cglynn
"""

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

def populateMprime():

    tweetsFound = []
    with open('retrievedTrainingData.data') as file:
        tweetsFile = file.readlines()
        tweetsFound = json.loads(tweetsFile[0])
    with open('randomSampleTraining.dat') as file3:
        tweetsFile2 = file3.readlines()
        dPrime = json.loads(tweetsFile2[0])
    for allTweets in tweetsFound:
        for tweets in dPrime:
            if tweets['id'] == allTweets['id']:
                allTweets['positive'] = tweets['positive']
    with open("retrievedTrainingData.data", 'w') as file2:
        file2.write(json.dumps(tweetsFound))
 
if __name__ == '__main__':
    populateMprime()