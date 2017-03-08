# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 08:52:26 2017

@author: cglynn
Collect Tweets including current Video names store to file retrievedTweets.data
Collect Random Sample of Tweets and store to file randomSampleTweets.data
Query terms saved to query.data
"""

# -*- coding: utf-8 -*-

import tweepy, sys, json, time, urllib2, sets, string, stop_words

#==============================================================================
# Setup tweepy API and Global variables
#==============================================================================
reload(sys)
sys.setdefaultencoding("utf-8")

consumer_key='Okf8rnmarIctPnfjwfqMj9Fpf' 
consumer_secret='HakszG0KyyjYJxA0TraalLXY6bxBTEQBst5ZgHBw5IyoZg4WAM' 
access_token_key='832742214849531905-MwZ6NMLvO0zNf0XYewBS1VwAgBxj8aC'
access_token_secret='omcKXM1kOJOIMDclejLqdY8xwCwdmwgGPjnTpCAc90OW6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
myApi = tweepy.API(auth)
numberOfResults = 1000
tweetList = []
queryFile = 'query.data'
retrievedFile = 'retrievedTweets.data'
randomSampleFile = 'randomSampleTweets.data'
###############################################################################

#==============================================================================
# Setup Gracenot API for current movie titles
#Allows up to 50 calls per day; 2 calls per second.
#==============================================================================
#consumer_key = 'cuscgszmmfg3cwenss7bj273'
consumer_key = 'wxsswsn7m4zhy823g957jbp4'
baseUrl = "http://data.tmsapi.com/v1.1"
showtimesUrl = baseUrl + '/movies/showings?'
zipCode = "12222"
date = time.strftime("%Y-%m-%d")
parameters = 'startDate=' + date + '&zip=' + zipCode + '&api_key=' + consumer_key
movieUrl = showtimesUrl + parameters
###############################################################################

#Retrieve Tweets based on current movie titles         
def rest_query_movieTitlesTweets():
    numMovies = 1
    with open(queryFile) as file:
        movieWordsFile = file.readlines()
        movieWords = json.loads(movieWordsFile[0])
    if(len(movieWords) > 1):
        numMovies = len(movieWords)
    resultCount = numberOfResults / numMovies
    numRepititions = resultCount / 100    
    if(numRepititions < 1):
        numRepititions = 1
    for movieTitle in movieWords:
        addTweets(movieTitle, numRepititions)
    with open(retrievedFile, 'w') as file:
        file.write(json.dumps(tweetList))
            
#Add tweets to list
def addTweets(queryString, numRepititions):
    geo = "42.6525,-73.7572,9mi" # City of Albany
    MAX_ID = None
    global tweetList
    tweets = myApi.search(q=queryString, geocode=geo, count=100, max_id = MAX_ID)
    for it in range(numRepititions):
        tweets = myApi.search(q=queryString, geocode=geo, count=100, max_id = MAX_ID)
        if tweets:
            MAX_ID = tweets[-1].id
            for tweet in tweets:
                tweetList.append(convertTweepyObjToDict(tweet))
    

#Retrieve movie Titles
def rest_query_movieTitle():
    request = urllib2.Request(movieUrl)
    movieSet = sets.Set()
    movieDictionary = dict()
    global queryList
    try:
        response = urllib2.urlopen(request)
        movies = response.read()
        movieDictionary = json.loads(movies)
    except urllib2.URLError, e:
        print 'Error connecting to Movie API: ' , e
    for movie in movieDictionary:
        title = removeStopWords(removePunctuation(movie['title'].lower()))
        for words in title:
            movieSet.add(words) 
    movieList = list(movieSet)
    with open(queryFile, 'w') as file:
        file.write(json.dumps(movieList))  
    

#Remove punctuation
def removePunctuation(text):
#    Replace 's and n't    
    text = text.replace("'s",'')
    text = text.replace("n't", '')
    for p in string.punctuation:
        text = text.replace(p,'')
    return text

#Remove Stopwords
def removeStopWords(textInput):
    import datetime
    tempText = textInput.split()
    now = datetime.datetime.now()
    stopWords = stop_words.get_stop_words('english')
    addStopWordsList = [str(now.year), '3d', '2']
    addStopWords(stopWords, addStopWordsList)
    wordsList = textInput.split()
    for word in wordsList:
        try:
            stopWords.index(word)
            tempText.remove(word)
        except Exception:
            pass
    clean_stopWords(stopWords, addStopWordsList)
    return tempText
    

#Retrieve Random Sample
def rest_query_randomSample():
    numResults = 100
    geo = "42.6525,-73.7572,9mi" # City of Albany
    MAX_ID = None
    tweetList = []
    tweets = myApi.search(geocode=geo,count=numResults, max_id = MAX_ID)
    for it in range(20): # Retrieve up to 2000 tweets
        tweets = myApi.search(geocode=geo,count=numResults, max_id = MAX_ID)
        if tweets:
            MAX_ID = tweets[-1].id
            for tweet in tweets:
                tweetList.append(convertTweepyObjToDict(tweet))
    with open(randomSampleFile, 'w') as file:
        file.write(json.dumps(tweetList))       

def convertTweepyObjToDict(tweepyObject):
    return {
         'contributors': tweepyObject.contributors, 
         'truncated': tweepyObject.truncated, 
         'text': tweepyObject.text,
#         'in_reply_to_status_id': tweepyObject.in_reply_to_status_id,
         'id': tweepyObject.id,
         'retweeted': tweepyObject.retweeted,
         'coordinates': tweepyObject.coordinates,
         'source': tweepyObject.source,
#         'in_reply_to_screen_name': tweepyObject.in_reply_to_screen_name,
         'id_str': tweepyObject.id_str,
         'retweet_count': tweepyObject.retweet_count,
#         'in_reply_to_user_id': tweepyObject.in_reply_to_user_id,
         'favorited': tweepyObject.favorited,
         'source_url': tweepyObject.source_url, 
         'geo': tweepyObject.geo, 
#         'in_reply_to_user_id_str': tweepyObject.in_reply_to_user_id_str, 
         'created_at': str(tweepyObject.created_at), 
#         'in_reply_to_status_id_str': tweepyObject.in_reply_to_status_id_str
#         ,'place': tweepyObject.place
    }
    
def clean_stopWords(stopWords, removeStopWordsList):
    for word in removeStopWordsList:
        stopWords.remove(word)

def addStopWords(stopWords, addStopWordsList):
    for word in addStopWordsList:
        stopWords.append(word)

if __name__ == '__main__':
#    rest_query_randomSample()
    rest_query_movieTitle()
#    rest_query_movieTitlesTweets()