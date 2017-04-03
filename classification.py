# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:10:39 2017

@author: cglynn
"""

import json, numpy as np
from operator import itemgetter
from sklearn.model_selection import GridSearchCV
from sklearn import svm

training_File = 'labeled_tweets.txt'
query_terms_File = 'query.data'
tweetsToClassifyFile = 'unlabeled_tweets.txt'
features = []
numOfFeatures = 10
classVector = []
featureVector = []
svmBestParameters = []

def classificationTrain():
    #Read in tweets for training from list ['Class label, tweet text']
    trainingTweets = []
        
    global classVector
    global featureVector 
    
    with open(training_File) as file:
        tweetsFile = file.readlines()
        trainingTweets = json.loads(tweetsFile[0])
    
    #Read in Query Terms in dictionary
    queryDictionary = dict()
    queryTerms = []
    with open(query_terms_File) as file:
        queryFile = file.readlines()
        queryTerms = json.loads(queryFile[0])
    for term in queryTerms:
        terms = term.split()
        for word in terms:
            queryDictionary[word] = 0
    
    # Compute the top num of query terms used, top features
    queryTop = []
    trainingList = []
    for trainingTweet in trainingTweets:
        trainingData = trainingTweet.split(',')
        trainingList.append(trainingData)
        terms = trainingData[1].split()
        for term in terms:
            if queryDictionary.has_key(term):
                queryDictionary[term] += 1 
    queryList = sorted(queryDictionary.items(), key=itemgetter(1))
    for term in queryList[-numOfFeatures:]:
        queryTop.append(term[0])
    global features 
    features = queryTop
    print 'Top ten features' ,queryTop
            
    #Generate numpy ndarrays for features and classes
    classVector = np.zeros((len(trainingList),), (int))
    tweetText = []
    row = 0
    for tweet in trainingList:
        tweetText.append(tweet[1])
        classVector[row] = tweet[0]
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
        
def classifyTweets():
    #Read in tweets for classifing from list in form ['tweet text']
    tweetsToClassify = []

    with open(tweetsToClassifyFile) as file:
        tweetsFile = file.readlines()
        tweetsToClassify = json.loads(tweetsFile[0])

    #Generate numpy ndarrays for features
    featureVectorClassify = generateFeatureVector(tweetsToClassify)
    
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
    
    # store predictions along with text in an array
    predictedTweets = []
    i = 0
    for prediction in y:
        predictedTweets.append([prediction, tweetsToClassify[i]])
        i += 1
    
#   Save the predictions to file. 
    with open("predicted_tweets.txt", 'w') as file:
        file.write(json.dumps(predictedTweets))

#Returns feature vector given list of tweet text
def generateFeatureVector(tweetText):
    featureVector = np.zeros((len(tweetText),len(features)), (int))
    row = 0
    feature = 0
    for tweet in tweetText:
        tweetTerms = tweet.split()
        for queryTerm in features:
            for term in tweetTerms:
                if term.lower() == queryTerm.lower():
                    featureVector[row,feature] += 1
            feature +=1
        row += 1
        feature = 0
    return featureVector
        
if __name__ == '__main__':
    classificationTrain()
    classifyTweets()