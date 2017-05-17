# MinerMovies
RetrievePopularMovie.py: Executes getMovieTitles() and getTweets() from CollectTweets.py.  Then executes classifyTweets from Classification.py with inputs 'retrievedTweets.data and true.  Then retrieves the largest cluster from clusert_tweets method from clustering.py file.  As input to clustering is the type of clustering to be performed, kmeans or agglomerative.  Then scans through the largest cluster to produce the movie name.  Prints the movie name.

CollectTweets.py: This file when executed generates randomSampleTweets.data, retrievedTweets.data and query.data.
  query.data contains the queries used to retreive tweets.
  retrievedTweets.data contains the retrieved tweets using the query.
  randomSampleTweets.data contains a random sample of tweets.

Classification.py: Classifies tweets based on queryTraining.data, svmParameters.data and classificationTweetsTraining.data.  Input for classification is the file that contains tweets to be classified and if the classification will be used for clustering.  Tweet file should be a list of tweets where each tweet contains text, id.
  Outputs for Clustering:
    cluster_tweets.txt: Contains all positve tweet text
  Output for Data Analysis:
    cleanRandomSampleTraining.data: File containing all tweets as well as positive attribute with values true or false.
  
clustering.py: Clusters tweets using query.data and cluster_tweets.txt.  Creates feauture vectors using count of query term for features. Able to cluster using kmeans or agglomerative clustering.  Outputs all clusters in separate files with the naming convention clusterVideo{clusterNumber}.txt.  As well as returning the largest cluster.

Data Metrics and Exploration

After executing CollectTweets.py.  Execute classifyTweets method in Classification.py with inputs randomSampleTweets.data and false.  Then execute CleanDataMetrics.py file to add to the collected data the query property and if it is true or not.

ComputeMetrics.py: Takes as input cleanRandomSample.data and cleanRetrieved.data.  As output prints
the three data metrics, API Recall, Quality Precision and Quality Recall.

DataExploaration.py: Takes as input cleanRandomSample.data and cleanRetrieved.data.  Both files have been cleaned as well as catergorized.  Ouputs Tweet Length and Tweet Query Term Count Summary Statistics.  Mean, Standard Deviation (STD), Median, Median Absolute Deviation (MAD), Max, and Min.  Produces Histograms, scatter plots, box plots and heat maps.
