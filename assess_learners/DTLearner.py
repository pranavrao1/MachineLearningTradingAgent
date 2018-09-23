"""  		   	  			    		  		  		    	 		 		   		 		  
A simple wrapper for linear regression.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
class DTLearner(object):
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size=1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose
  		   	  			    		  		  		    	 		 		   		 		  
    def author(self):  		   	  			    		  		  		    	 		 		   		 		  
        return 'prao43' # replace tb34 with your Georgia Tech username
  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self,dataX,dataY):  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			    		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			    		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # slap on 1s column so linear regression finds a constant term
        combo_data = np.column_stack((dataX, dataY))
        self.tree =  self.build_tree(combo_data)
  		   	  			    		  		  		    	 		 		   		 		  
        # build and save the model

    def build_tree(self, data):
        number_of_columns = data.shape[1]
        max_correlation = -1
        best_correlation_index = -1
        for i in range(number_of_columns-1):
            correlate = np.correlate(data[:,i],data[:,-1])
            if correlate > max_correlation:
                max_correlation = correlate
                best_correlation_index = i

        if data.shape[0] == 1:
            return np.array([[-1, data[:,-1], -1, -1]])
        elif np.unique(data[:, -1]).size == 1:
            return np.array([[-1, data[0,-1], -1, -1]])
        elif data.shape[0] <= self.leaf_size:
            return self.create_new_leaf(data)
        else:
            split_value = np.median(data[:,best_correlation_index])

            less_than_split = data[data[:, best_correlation_index] <= split_value]
            greater_than_split = data[data[:, best_correlation_index] > split_value]
            # Ensure that split is not all to one side.
            min_value = np.amin(data[:, best_correlation_index])
            max_value = np.amax(data[:, best_correlation_index])
            if split_value == min_value or split_value == max_value:
                return self.create_new_leaf(data)
            left_tree = self.build_tree(less_than_split)
            right_tree = self.build_tree(greater_than_split)
            root = np.array([best_correlation_index, split_value, 1, left_tree.shape[0] + 1])
            result_1 = np.vstack((root, left_tree))
            final = np.vstack((result_1, right_tree))
            return final

    def create_new_leaf(self, data):
        mean_value = np.mean(data[:, -1])
        return np.array([[-1, mean_value, -1, -1]])

    def query(self,points):
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			    		  		  		    	 		 		   		 		  
        @param points: should be a numpy array with each row corresponding to a specific query.  		   	  			    		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			    		  		  		    	 		 		   		 		  
        """

        result = np.empty(points.shape[0])
        result.fill(-1)
        tree = self.tree
        i = 0
        for entry in points:
            value = self.result_single_node(entry,tree[0], 0)
            result[i] = value
            i = i + 1
        return result

    def result_single_node(self,row, node, index):
        factor = node[0]
        diff = node[1]
        if factor == -1:
            return diff
        elif row[int(factor)] <= diff:
            tree = self.tree
            left = node[2]
            next_index = index + left
            next_node = tree[int(next_index)]
            return self.result_single_node(row, next_node, next_index)
        else:
            tree = self.tree
            right = node[3]
            next_index = index + right
            next_node = tree[int(next_index)]
            return self.result_single_node(row, next_node, next_index)
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "the secret clue is 'zzyzx'"  		   	  			    		  		  		    	 		 		   		 		  
