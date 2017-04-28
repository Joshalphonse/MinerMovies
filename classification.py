# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:10:39 2017

Classify based on the following features.

Number of Query Terms
Tweet Length

Saves all positive tweets, class 1, to tweetsToCluster file.

@author: cglynn
"""

import json, numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn import svm

training_File = 'labeled_tweets.txt'
query_terms_File = 'query.data'
tweetsToClassifyFile = 'retrievedTweets.data'
tweetsToClusterFile = 'cluster_tweets.txt'
num_features = 2
classVector = []
featureVector = []
queryTerms = []
svmBestParameters = []

def classifyTweets():
    #Read in tweets for training from list ['Class label, tweet text']
    trainingTweets = []   
    
    with open(training_File) as file:
        tweetsFile = file.readlines()
        trainingTweets = json.loads(tweetsFile[0])
    
    #Read in Query Terms in dictionary
    queryDictionary = dict()
    with open(query_terms_File) as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    for term in queryTerms:
        terms = term.split()
        for word in terms:
            queryDictionary[word] = 0
    
#    # Create the training list of tweets
#    trainingList = []
#    for trainingTweet in trainingTweets:
#        trainingData = trainingTweet.split(',')
#        trainingList.append(trainingData)
            
    #Generate numpy ndarrays for features and classes
    classVector = np.zeros((len(trainingTweets),), (int))
    tweetText = []
    row = 0
    for tweet in trainingTweets:
        tweetText.append(tweet['text'])
        classVector[row] = tweet['positive']
        row += 1
    featureVector = generateFeatureVector(tweetText)   
    
    #Train the SVM Model. Parameter estimation using grid search with 10 folder cross validation
    tuned_parameters = [{'kernel':['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
                        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
    scores = ['precision', 'recall']
    svr = svm.SVC(C=1)
    for score in scores:
    #        print("# Tuning hyper-parameters for %s" % score)
        clf = GridSearchCV(svr, tuned_parameters, cv=10, scoring='%s_macro' % score)
        clf.fit(featureVector, classVector)
    #        print("best parameters %s" % clf.best_params_)
    #        means = clf.cv_results_['mean_test_score']
    #        stds = clf.cv_results_['std_test_score']
    #        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    #            print("Accuracy: %0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        
    #   Save the best parameters
    global svmBestParameters
    if 'gamma' in clf.best_params_:
        svmBestParameters = [{'kernel': [clf.best_params_['kernel']] , 'C':[clf.best_params_['C']], 'gamma':[clf.best_params_['gamma']]}]
    else :
        svmBestParameters = [{'kernel': [clf.best_params_['kernel']] , 'C':[clf.best_params_['C']]}]
            
    
        
    #Read in tweets for classifing from list in form ['tweet text']
    tweetsToClassify = []
    tweetTextToClassify = []
    
    with open(tweetsToClassifyFile) as file:
        tweetsFile = file.readlines()
        tweetsToClassify = json.loads(tweetsFile[0])
    
    for tweet in tweetsToClassify:
        tweetTextToClassify.append(tweet['text'])
    
    #Generate numpy ndarrays for features
    featureVectorClassify = generateFeatureVector(tweetTextToClassify)
    
    #   Setup Support Vector with previously found parameters. 
    svr = svm.SVC(C=1)
    clf = GridSearchCV(svr, svmBestParameters, cv=10)
    clf.fit(featureVector, classVector)
    
    #   Calculae Accuracy 
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("Accuracy: %0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
    
    #   Predict 
    y = clf.predict(featureVectorClassify)
    
    # store positive predictd tweet text to array
    predictedTweets = []
    i = 0
    for prediction in y:
        if prediction == 1:
            predictedTweets.append([tweetsToClassify[i]['id'],tweetTextToClassify[i]])
        i += 1
    
    #   Save the predictions to file. 
    with open(tweetsToClusterFile, 'w') as file:
        file.write(json.dumps(predictedTweets))

#Returns feature vector given list of tweet text
def generateFeatureVector(tweetText):
    featureVector = np.zeros((len(tweetText),num_features), (int))
    row = 0
    for tweet in tweetText:
        featureVector[row, 0] = queryTermCount(tweet)
        featureVector[row, 1] = len(tweet)
        row += 1
    return featureVector
    
def queryTermCount(tweetText):
    wordList = tweetText.split()
    count=0
    for word in wordList:
        if word in queryTerms:
            count = count+1
    return count

        
if __name__ == '__main__':
    classifyTweets()