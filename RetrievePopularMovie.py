# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 08:08:36 2017

@author: cglynn
"""

from CollectTweets import rest_query_movieTitlesTweets as getTweets, rest_query_movieTitle as getMovieTitles 
from clustering import cluster_tweets
from classification import classifyTweets

#Cluster technique 1 for kemans, 2 agglomerative
clusterType = 1

#Collect Tweets
getMovieTitles()
getTweets()

#Classify relative tweets
classifyTweets()

#Cluster Tweets
cluster_tweets(clusterType)  

#Compute Most Popular movie
