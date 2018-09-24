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
import util
import matplotlib.pyplot as plt
import time

def run_learner(learner, trainX, trainY, testX, testY):
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    print learner.author()
    tree_building_start = time.time()
    learner.addEvidence(trainX, trainY)  # training step
    tree_building_end = time.time()
    time.time()
    # # evaluate in sample
    predY = learner.query(trainX)  # get the predictions
    if hasattr(learner, 'tree'):
        tree_size = learner.tree.shape[0] * learner.tree.shape[1]
    else:
        tree_size = 0

    rmse_in = math.sqrt(((trainY - predY) ** 2).sum() / trainY.shape[0])
    print
    print "In sample results"
    print "RMSE: ", rmse_in
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0, 1]

    # evaluate out of sample
    predY = learner.query(testX)  # get the predictions
    rmse_out = math.sqrt(((testY - predY) ** 2).sum() / testY.shape[0])
    print
    print "Out of sample results"
    print "RMSE: ", rmse_out
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0, 1]
    print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    return rmse_in, rmse_out, tree_size, (tree_building_end - tree_building_start)


def generate_plots(datafile = 'Istanbul.csv'):
    np.random.seed(903205913)
    print " Plotting graphs for " + str(datafile)
    with util.get_learner_data_file(datafile) as f:
        alldata = np.genfromtxt(f, delimiter=',')
        # Skip the date column and header row if we're working on Istanbul data
        if datafile == 'Istanbul.csv':
            alldata = alldata[1:, 1:]
    data = alldata
    # print data.shape[0]
    data = np.random.permutation(data)
    # compute how much of the data is training and testing
    np.random.shuffle(data)
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows
    # separate out training and testing data
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]

    rmses_in = np.empty(100)
    rmses_in.fill(-1)
    rmses_out = np.empty(100)
    rmses_out.fill(-1)

    dt_learner_tree_size = np.empty(100)
    dt_learner_tree_size.fill(-1)
    dt_learner_tree_time = np.empty(100)
    dt_learner_tree_time.fill(-1)

    leaf_size = range(100)
    for i in leaf_size:
        learner = dt.DTLearner(leaf_size=i, verbose=False)  # constructor
        rmses_in[i], rmses_out[i], dt_learner_tree_size[i], dt_learner_tree_time[i] = run_learner(learner, trainX, trainY, testX, testY)  # training step
    plt.plot(leaf_size, rmses_in, label="In Sample")
    plt.plot(leaf_size, rmses_out, label="Out Sample")
    plt.legend(loc="best")
    plt.grid(True)
    plt.title('DTLearner overfitting with increasing leaf size.', fontsize=10)
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.savefig('DTLearner overfitting with increasing leaf size.')
    plt.clf()
    plt.cla()
    plt.close()

    rmses_in_2 = np.empty(100)
    rmses_in_2.fill(-1)
    rmses_out_2 = np.empty(100)
    rmses_out_2.fill(-1)
    for i in leaf_size:
        kwargs = {'leaf_size': i}
        learner = bl.BagLearner(learner=dt.DTLearner, kwargs=kwargs, verbose=False, bags=20)  # constructor
        rmses_in_2[i], rmses_out_2[i], ignore, ignore_2 = run_learner(learner, trainX, trainY, testX, testY)  # training step
    plt.plot(leaf_size, rmses_in_2, label="In Sample")
    plt.plot(leaf_size, rmses_out_2, label="Out Sample")
    plt.legend(loc="best")
    plt.grid(True)
    plt.title('Baglearner at 20 bags overfitting with increasing leaf size.', fontsize=10)
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.savefig('Baglearner at 20 bags overfitting with increasing leaf size.')
    plt.clf()
    plt.cla()
    plt.close()

    rmses_in_3 = np.empty(100)
    rmses_in_3.fill(-1)
    rmses_out_3 = np.empty(100)
    rmses_out_3.fill(-1)

    rt_learner_tree_size = np.empty(100)
    rt_learner_tree_size.fill(-1)
    rt_learner_tree_time = np.empty(100)
    rt_learner_tree_time.fill(-1)

    for i in leaf_size:
        learner = rt.RTLearner(leaf_size=i, verbose=False)  # constructor
        rmses_in_3[i], rmses_out_3[i], rt_learner_tree_size[i], rt_learner_tree_time[i] = run_learner(learner, trainX, trainY, testX, testY)  # training step
    plt.plot(leaf_size, rmses_in_3, label="In Sample")
    plt.plot(leaf_size, rmses_out_3, label="Out Sample")
    plt.legend(loc="best")
    plt.grid(True)
    plt.title('RTLearner overfitting with increasing leaf size.', fontsize=10)
    plt.ylabel('RMSE')
    plt.xlabel('Leaf Size')
    plt.savefig('RTLearner overfitting with increasing leaf size.')
    plt.clf()
    plt.cla()
    plt.close()


    plt.plot(leaf_size, rt_learner_tree_size, label="RTLearner")
    plt.plot(leaf_size, dt_learner_tree_size, label="DTLearner")
    plt.legend(loc="best")
    plt.grid(True)
    plt.title('RTLearner vs DTLearner Tree Size.', fontsize=10)
    plt.ylabel('Tree Size')
    plt.xlabel('Leaf Size')
    plt.savefig('RTLearner vs DTLearner Tree Size.')
    plt.clf()
    plt.cla()
    plt.close()

    plt.plot(leaf_size, rt_learner_tree_time, label="RTLearner")
    plt.plot(leaf_size, dt_learner_tree_time, label="DTLearner")
    plt.legend(loc="best")
    plt.grid(True)
    plt.title('RTLearner vs DTLearner Tree Building Time.', fontsize=10)
    plt.ylabel('Tree Size')
    plt.xlabel('Leaf Size')
    plt.savefig('RTLearner vs DTLearner Tree Building Time.')
    plt.clf()
    plt.cla()
    plt.close()


def run_debuging_tests():
    inf = open(sys.argv[1])
    data = np.array([map(float, s.strip().split(',')) for s in inf.readlines()])
    # print data.shape[0]
    data = np.random.permutation(data)
    # compute how much of the data is training and testing
    np.random.shuffle(data)
    train_rows = int(0.6 * data.shape[0])
    test_rows = data.shape[0] - train_rows
    # separate out training and testing data
    trainX = data[:train_rows, 0:-1]
    trainY = data[:train_rows, -1]
    testX = data[train_rows:, 0:-1]
    testY = data[train_rows:, -1]
    # create a learner and train it
    learner = lrl.LinRegLearner(verbose=True)  # create a LinRegLearner
    run_learner(learner, trainX, trainY, testX, testY)  # training step
    learner = dt.DTLearner(leaf_size=1, verbose=False)  # constructor
    run_learner(learner, trainX, trainY, testX, testY)  # training step
    learner = rt.RTLearner(leaf_size=1, verbose=False)  # constructor
    run_learner(learner, trainX, trainY, testX, testY)
    learner = bl.BagLearner(learner=lrl.LinRegLearner, kwargs={}, bags=10, boost=False, verbose=False)
    run_learner(learner, trainX, trainY, testX, testY)
    learner = il.InsaneLearner(verbose=False)
    run_learner(learner, trainX, trainY, testX, testY)


if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: python testlearner.py <filename>"
        generate_plots()
        sys.exit(1)
    generate_plots(sys.argv[1])

    #TODO: This was use by the student to run additional developmental steps. Uncomment if you would like to run it.
    # run_debuging_tests()

