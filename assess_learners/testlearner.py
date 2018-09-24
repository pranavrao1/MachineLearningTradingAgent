"""  		   	  			    		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import math  		   	  			    		  		  		    	 		 		   		 		  
import LinRegLearner as lrl
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import InsaneLearner as il
import sys


def run_learner(learner, trainX, trainY, testX, testY):
    print learner.author()
    learner.addEvidence(trainX, trainY)  # training step
    # # evaluate in sample
    predY = learner.query(trainX)  # get the predictions
    rmse = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0, 1]

    # evaluate out of sample
    predY = learner.query(testX)  # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0, 1]


if __name__=="__main__":
    if len(sys.argv) != 2:  		   	  			    		  		  		    	 		 		   		 		  
        print "Usage: python testlearner.py <filename>"  		   	  			    		  		  		    	 		 		   		 		  
        sys.exit(1)  		   	  			    		  		  		    	 		 		   		 		  
    inf = open(sys.argv[1])  		   	  			    		  		  		    	 		 		   		 		  
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    print "Istanbul"
    datafile = 'Istanbul.csv'
    with util.get_learner_data_file(datafile) as f:
        alldata = np.genfromtxt(f, delimiter=',')
        # Skip the date column and header row if we're working on Istanbul data
        if datafile == 'Istanbul.csv':
            alldata = alldata[1:, 1:]
    data = alldata[1:, 1:]
    # print data.shape[0]
    data = np.random.permutation(data)

    # compute how much of the data is training and testing
    np.random.shuffle(data)
    train_rows = int(0.6* data.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # separate out training and testing data  		   	  			    		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    trainY = data[:train_rows,-1]  		   	  			    		  		  		    	 		 		   		 		  
    testX = data[train_rows:,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    testY = data[train_rows:,-1]
  		   	  			    		  		  		    	 		 		   		 		  
    # create a learner and train it  		   	  			    		  		  		    	 		 		   		 		  
    #learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    #run_learner(learner, trainX, trainY, testX, testY) # training step
    #
    #learner = dt.DTLearner(leaf_size=1, verbose=False)  # constructor
    #run_learner(learner, trainX, trainY, testX, testY)  # training step
    #
    # learner = rt.RTLearner(leaf_size=1, verbose=False)  # constructor
    # run_learner(learner, trainX, trainY, testX, testY)

    # learner = bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=10, boost=False, verbose=False)
    # run_learner(learner, trainX, trainY, testX, testY)

    learner = il.InsaneLearner(verbose=False)
    run_learner(learner, trainX, trainY, testX, testY)

