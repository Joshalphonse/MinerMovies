# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 08:52:26 2017

@author: cglynn
Collect Tweets including current Video names store to file
Collect Random Sample of Tweets
"""

# -*- coding: utf-8 -*-

import tweepy, sys, json, hashlib, time, urllib

#==============================================================================
# Setup tweepy API
#==============================================================================
reload(sys)
sys.setdefaultencoding("utf-8")

consumer_key='PeH7lROp4ihy4QyK87FZg' 
consumer_secret='1BdUkBd9cQK6JcJPll7CkDPbfWEiOyBqqL2KKwT3Og' 
access_token_key='1683902912-j3558MXwXJ3uHIuZw8eRfolbEGrzN1zQO6UThc7'
access_token_secret='e286LQQTtkPhzmsEMnq679m7seqH4ofTDqeArDEgtXw'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
myApi = tweepy.API(auth)
###############################################################################

#==============================================================================
# Setup Fandango API
# API Code from: https://developer.fandango.com/page/API__Sample_Code_Python
#==============================================================================
class FandangoApiManager(object):

    def __init__(self):
        
        self.FandangoApiManager = [ ]

    def Sha256Encode(self, stringToEncode):

        s = hashlib.sha256();
        s.update(stringToEncode)
        result = s.hexdigest()

        return result

    def BuildAuthorizationParameters(self, apiKey, sharedSecret):

        paramsToEncode = "{0}{1}{2}".format(apiKey, sharedSecret, int(time.time()))
        encodedParams = self.Sha256Encode(paramsToEncode)
        result = "apikey={0}&sig={1}".format(apiKey, encodedParams)
        
        return result

    def GetResponse(self, parameters):

        baseUri = "http://api.fandango.com"
        apiVersion = "1"

        apiKey = "sg2jbzbj2sb6ftyyk3pzrn76"
        sharedSecret = "cfTBKsZB7n"

        authorizationParameters = self.BuildAuthorizationParameters(apiKey, sharedSecret)
        requestUri = "{0}/v{1}/?{2}&{3}".format(baseUri, apiVersion, parameters, authorizationParameters)

        response = urllib.urlopen(requestUri)
        
        result = response.read()
        
        return result

###############################################################################

#Retrieve Tweets based on current movie titles         
def rest_query_movieTitlesTweets():
    query = "FIFTY SHADES DARKER "
    geo = "42.6525,-73.7572,9mi" # City of Albany
    MAX_ID = None
    tweets = myApi.search(q=query, geocode=geo, count=100, max_id = MAX_ID)
    for it in range(2): # Retrieve up to 200 tweets
        tweets = myApi.search(q=query, geocode=geo, count=100, max_id = MAX_ID)
        if tweets:
            MAX_ID = tweets[-1].id
            print MAX_ID, len(tweets)
            print tweets[-1].text

#Retrieve movie Titles
def rest_query_movieTitle():
    
    api = FandangoApiManager()
    
    zipCode = "12222";
    parameters = "op=moviesbypostalcodesearch&postalcode={0}".format(zipCode)

    responseFromServer = api.GetResponse(parameters)

    print responseFromServer

    # process responseFromServer...

#Retrieve Random Sample
def rest_query_randomSample():
    numResults = 100
    geo = "42.6525,-73.7572,9mi" # City of Albany
    MAX_ID = None
    tweets = myApi.search(geocode=geo, count=numResults, max_id = MAX_ID)
    for it in range(2): # Retrieve up to 200 tweets
        tweets = myApi.search(geocode=geo, count=numResults, max_id = MAX_ID)
        if tweets:
            MAX_ID = tweets[-1].id
            print MAX_ID, len(tweets)
            print tweets[-1].text

if __name__ == '__main__':
#    rest_query_randomSample()
    rest_query_movieTitle()
    rest_query_movieTitlesTweets()
