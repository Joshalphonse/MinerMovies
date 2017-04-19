# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 08:08:36 2017

@author: cglynn
"""

from CollectTweets import rest_query_movieTitlesTweets as getTweets, rest_query_movieTitle as getMovieTitles 
from clustering import cluster_tweets


#Collect Tweets
getMovieTitles()
getTweets()

#Cluster Tweets
cluster_tweets()

#Compute Most Popular movie
