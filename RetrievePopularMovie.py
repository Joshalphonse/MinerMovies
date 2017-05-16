# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 08:08:36 2017

@author: cglynn
"""

from CollectTweets import rest_query_movieTitlesTweets as getTweets, rest_query_movieTitle as getMovieTitles 
from clustering import cluster_tweets
from classification import classifyTweets
import json

#Cluster technique 1 for kemans, 2 agglomerative
clusterType = 1
query_terms_File = 'query.data'

def getPopularMovie():
    #Collect Tweets
    #getMovieTitles()
    #getTweets()
    
    #Classify relative tweets
    #classifyTweets('retrievedTweets.data', 'true')
    
    #Cluster Tweets
    #largestCluster = cluster_tweets(clusterType)  
    
    #Compute Most Popular movie
    movieName = getPopularMovieName(1)
    print movieName

def getPopularMovieName(cluster):
    #Read Tweet text in
    tweets = []
    queryTerms = []

    with open('clusterVideo-{0}.txt'.format(cluster)) as file:
        tweets = file.readlines()
    for word in tweets:
        word = word.lower()
    
    with open(query_terms_File) as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
        
    i = 0
    for term in queryTerms:
        terms = term.split()
        for word in terms:
            if word.lower() in tweets:
                return queryTerms[i]
        i += 1


    
if __name__ == '__main__':
    getPopularMovie()