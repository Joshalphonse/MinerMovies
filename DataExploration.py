# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 08:41:00 2017

@author: cglynn
"""

import json, sets, matplotlib.pyplot as plt, numpy as np
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
#Attribute array of tweet lengths.  [Positive, negative]
tweetLength = []
#Attribute array of tweet query term counts [Postivie, negative]
tweetQueryTermCount = [] 

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

def populateAttributes():
    global tweetLength
    global tweetQueryTermCount 
    
#    Populate tweetLength attributes [positive, negative]
    positiveLengthCount=[]
    negativeLengthCount = []
    for tweet in positiveTweetList:
        positiveLengthCount.append(len(tweet))
    for tweet in negativeTweetList:
        negativeLengthCount.append(len(tweet))
    tweetLength.append(positiveLengthCount)
    tweetLength.append(negativeLengthCount)
    
# Populate tweet query term count attribute [positive, negative]  
    positiveQueryCount=[] 
    negativeQueryCount=[] 
    queryTerms = []
    with open('query.data') as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    
    for tweet in positiveTweetList:
        wordList = tweet.split()
        count=0
        for word in wordList:
            for term in queryTerms:
                if word.lower() in term.lower():
                    count = count+1
        positiveQueryCount.append(count)
    tweetQueryTermCount.append(positiveQueryCount)
    
    for tweet in negativeTweetList:
        wordList = tweet.split()
        count=0
        for word in wordList:
            for term in queryTerms:
                if word.lower() in term.lower():
                    count = count+1
        negativeQueryCount.append(count)
    tweetQueryTermCount.append(negativeQueryCount)

def calculateSummaryStatistics():
#Summary of statistics: Mean, Standard Deviation (STD), Median, Median
#Absolute Deviation (MAD), Max, and Min.
    print 'Positive Tweet Length Mean: ', np.mean(tweetLength[0])
    print 'Negative Tweet Length Mean: ', np.mean(tweetLength[1])
    print 'Positive Tweet Length STD: ', np.std(tweetLength[0])
    print 'Negative Tweet Length STD: ', np.std(tweetLength[1])
    print 'Positive Tweet Length Max: ', np.max(tweetLength[0])
    print 'Negative Tweet Length Max: ', np.max(tweetLength[1])
    print 'Positive Tweet Length Min: ', np.min(tweetLength[0])
    print 'Negative Tweet Length Min: ', np.min(tweetLength[1])
    positiveMedian = np.median(tweetLength[0])
    negativeMedian = np.median(tweetLength[1])
    print 'Positive Tweet Length Median: ', positiveMedian
    print 'Negative Tweet Length Median: ', negativeMedian
    print "MAD Positive Tweet Length :", np.median([abs(x - positiveMedian) for x in tweetLength[0]])
    print "MAD Negative Tweet Length :", np.median([abs(x - negativeMedian) for x in tweetLength[1]])
    
    print 'Positive Tweet Query Count Mean: ', np.mean(tweetQueryTermCount [0])
    print 'Negative Tweet Query Count Mean: ', np.mean(tweetQueryTermCount [1])
    print 'Positive Tweet Query Count STD: ', np.std(tweetQueryTermCount [0])
    print 'Negative Tweet Query Count STD: ', np.std(tweetQueryTermCount [1])
    print 'Positive Tweet Query Count Max: ', np.max(tweetQueryTermCount [0])
    print 'Negative Tweet Query Count Max: ', np.max(tweetQueryTermCount [1])
    print 'Positive Tweet Query Count Min: ', np.min(tweetQueryTermCount [0])
    print 'Negative Tweet Query Count Min: ', np.min(tweetQueryTermCount [1])
    positiveMedian = np.median(tweetQueryTermCount [0])
    negativeMedian = np.median(tweetQueryTermCount [1])
    print 'Positive Tweet Query Count Median: ', positiveMedian
    print 'Negative Tweet Query Count Median: ', negativeMedian
    print "MAD Positive Tweet Query Count :", np.median([abs(x - positiveMedian) for x in tweetQueryTermCount[0]])
    print "MAD Negative Tweet Query Count :", np.median([abs(x - negativeMedian) for x in tweetQueryTermCount[1]])

def histogramTweetLengthCount():
    colors = ['green', 'crimson']
    labels = ['Positive Tweets', 'Negative Tweets']
    plt.figure(1)
    plt.hist(tweetLength, 30, histtype='bar', color=colors, label = labels)
    plt.title("Tweet Lengths")
    plt.xlabel("Length of Tweets")
    plt.ylabel("Number of Tweets (up to 50)")
    plt.legend()
    plt.ylim(0,50)
    plt.savefig('tweetLengthHistogram.jpg')

def histogramQueryTermCount():
    plt.figure(3)
    colors = ['green', 'crimson']
    labels = ['Positive Tweets', 'Negative Tweets']
    plt.hist(tweetQueryTermCount, 30, histtype='bar', color=colors, label=labels)
    plt.title("Number of Query Terms in Tweets")
    plt.xlabel("Number of query terms in Tweets")
    plt.ylabel("Number of Tweets (Up to 50)")
    plt.legend()
    plt.ylim(0,50)
    plt.savefig('tweetQueryTermHistogram.jpg')
    
def scatterPlotTermCountVsLength():
    plt.figure(4)
    plt.scatter(tweetQueryTermCount[0], tweetLength[0], color='green' ,s=200)
    plt.scatter(tweetQueryTermCount[1], tweetLength[1], color='red', s=50)
    plt.suptitle('Query Term Count Vs Tweet Length')
    plt.xlabel('Query Term Count')
    plt.ylabel('Tweet Length')
    plt.show()
    plt.savefig('tweetLengthQueryTermScatter.jpg')
    
def boxPlotTweetLength():
    plt.figure(5)
    plt.title("Tweet Length")
    labels = ['Positive Tweets','Negative Tweets']
    plt.boxplot(tweetLength, labels=labels, showfliers='true')
    plt.savefig('tweetLengthBoxPlot.jpg')
    
def boxPlotQueryTermCount():
    plt.figure(6)
    plt.title("Number of Query Terms")
    labels = ['Positive Tweets','Negative Tweets']
    plt.boxplot(tweetQueryTermCount, labels=labels, showfliers='true')
    plt.savefig('tweetQueryTermBoxPlot.jpg')

def heatMapPositiveTweets():
    fig = plt.figure(7, figsize=(7,3))
    x = np.asarray(tweetQueryTermCount[0])
    y = np.asarray(tweetLength[0])
    H, xedges, yedges = np.histogram2d(x , y, bins = 6)
    H = H.T
    fig.add_subplot(132, title='Positive Tweets', aspect='equal')
    plt.imshow(H, interpolation='nearest' , origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    plt.savefig('heatMapPositiveTweet.jpg')

def heatMapNegativeTweets():
    fig = plt.figure(8, figsize=(7,3))
    x = np.asarray(tweetQueryTermCount[1])
    y = np.asarray(tweetLength[1])
    H, xedges, yedges = np.histogram2d(x , y, bins = 6)
    H = H.T
    fig.add_subplot(132, title='Negative Tweets', aspect='equal')
    plt.imshow(H, interpolation='nearest' , origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
    plt.savefig('heatMapNegativeTweet.jpg')

if __name__ == '__main__':
    populateDprime()
    populateSets()
    populateAttributes()
    calculateSummaryStatistics()
    histogramTweetLengthCount()
    histogramQueryTermCount()
    scatterPlotTermCountVsLength()
    boxPlotTweetLength()
    boxPlotQueryTermCount()
    heatMapPositiveTweets()
    heatMapNegativeTweets()