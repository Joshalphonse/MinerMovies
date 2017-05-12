# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:10:39 2017

Classify based on the following features.

Number of Query Terms
Tweet Length

Saves all positive tweets, class 1, to tweetsToCluster file.

classifyTrain() method saves the Best Parameters to svmBestParametersFile to be 
    used when classifying.

classifyTweets(tweetsToClassifyFile, forClustering)
    tweetsToClassifyFile: File of tweets to classify. 
    forClustering: Will clustering occur next or not.  For clustering only
        positive class tweets are saved to tweetsToClusterFile.  If false, positive
        and negative tweets saved to cleanRandomSampleTraining.data for computing 
        metrics and data exploration.
        
@author: cglynn
"""

import json, numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn import svm

training_File = 'classificationTweetsTraining.data'
query_terms_File = 'query.data'
tweetsToClusterFile = 'cluster_tweets.txt'
svmBestParametersFile = 'svmParameters.data'
num_features = 3


def classifyTrain():
  
    trainingVectors = retrieveTrainingVectors()

    #Train the SVM Model. Parameter estimation using grid search with 10 folder cross validation
    tuned_parameters = [{'kernel':['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    scores = ['precision', 'recall']
    svr = svm.SVC(C=1)
    for score in scores:
        clf = GridSearchCV(svr, tuned_parameters, cv=10, scoring='%s_macro' % score)
        clf.fit(trainingVectors[0], trainingVectors[1])
        
    #   Save the best parameters
    svmBestParameters = []
    if 'gamma' in clf.best_params_:
        svmBestParameters = [{'kernel': [clf.best_params_['kernel']] , 'C':[clf.best_params_['C']], 'gamma':[clf.best_params_['gamma']]}]
    else :
        svmBestParameters = [{'kernel': [clf.best_params_['kernel']] , 'C':[clf.best_params_['C']]}]
        
#    Write best parameters to file.
    with open(svmBestParametersFile, 'w') as file:
        file.write(json.dumps(svmBestParameters))
            
#tweetsToClassifyFile = File contains tweets to classify
#forClustering = boolean, do we want to cluster or not.
def classifyTweets(tweetsToClassifyFile, forClustering):        
    #Read in tweets for classifing from list in form {"text", "created_at", "id_str", "positive", "query", "id"}
    tweetsToClassify = []
    tweetTextToClassify = []
    
    with open(tweetsToClassifyFile) as file:
        tweetsFile = file.readlines()
        tweetsToClassify = json.loads(tweetsFile[0])
    
    for tweet in tweetsToClassify:
        tweetTextToClassify.append(tweet['text'])
    
    queryTerms = populateQueryTerms();    
    
    #Generate numpy ndarrays for features
    featureVectorClassify = generateFeatureVector(tweetTextToClassify, queryTerms)
    
    #Read in SVM Best Parameters
    svmBestParameters = []
    with open(svmBestParametersFile) as file:
        svmParamFile = file.readlines()
        svmBestParameters = json.loads(svmParamFile[0] )    

    trainingVectors = retrieveTrainingVectors()    
    
    #   Setup Support Vector with previously found parameters. 
    svr = svm.SVC(C=1)
    clf = GridSearchCV(svr, svmBestParameters, cv=10)
    clf.fit(trainingVectors[0], trainingVectors[1])
    
    #   Predict 
    y = clf.predict(featureVectorClassify)
    
    if forClustering == 'true':
        
        # store positive predictd tweet text to array
        predictedTweets = []
        i = 0
        for prediction in y:
            if prediction == 1:
                predictedTweets.append(tweetTextToClassify[i])
            i += 1    
        #   Save the predictions to file. 
        with open(tweetsToClusterFile, 'w') as file:
            file.write(json.dumps(predictedTweets))
    
    else:
        j = 0
        for prediction in y:
            if prediction == 0:
                tweetsToClassify[j]['positive'] = 'false'
            else:
                tweetsToClassify[j]['positive'] = 'true'
            j += 1
        with open('cleanRandomSampleTraining.data', 'w') as file:
            file.write(json.dumps(tweetsToClassify))

#Returns feature vector given list of tweet text
def generateFeatureVector(tweetText, queryTerms):
    featureVector = np.zeros((len(tweetText),num_features), (int))
    row = 0
    matchQuery = 0
    for tweet in tweetText:
        queryCount = queryTermCount(tweet, queryTerms)
        if queryCount > 0:
            matchQuery = 1
        else:
            matchQuery = 0
        featureVector[row, 0] = queryCount
        featureVector[row, 1] = len(tweet)
        featureVector[row, 2] = matchQuery
        row += 1
    return featureVector
    
def queryTermCount(tweetText, queryTerms):
    wordList = tweetText.split()
    count=0
    for word in wordList:
        if word.lower() in queryTerms:
            count = count+1
    return count

def populateQueryTerms():
    #Read in Query Terms
    with open(query_terms_File) as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    return queryTerms
    
def retrieveTrainingVectors():
    #Read in tweets for training from list ['Class label, tweet text']
    trainingTweets = [] 
    with open(training_File) as file:
        tweetsFile = file.readlines()
        trainingTweets = json.loads(tweetsFile[0])
    
    queryTerms = populateQueryTerms();
            
    #Generate numpy ndarrays for features and classes
    classVector = np.zeros((len(trainingTweets),), (int))
    tweetText = []
    row = 0
    for tweet in trainingTweets:
        tweetText.append(tweet['text'])
        classVector[row] = tweet['positive']
        row += 1
    featureVector = generateFeatureVector(tweetText, queryTerms)  
    return [featureVector, classVector]
        
if __name__ == '__main__':
#    classifyTrain()
    classifyTweets('retrievedTweets.data', 'true')