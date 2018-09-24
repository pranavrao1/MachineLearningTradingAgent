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
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lrl

class BagLearner(object):

    def __init__(self, learner,kwargs={'verbose':False},bags=20,boost=False,verbose=False):
        self.learner = learner
        self.kwags = kwargs
        self.bags = bags
        self.boost = boost
        self.verbose = verbose
        list_of_learners = []
        for i in range(bags):
            if learner == dt.DTLearner:
                verbose_assign = False
                leaf_size_assign = 1
                if 'verbose' in kwargs.keys():
                    verbose_assign = kwargs.get('verbose')
                    pass
                if 'leaf_size' in kwargs.keys():
                    leaf_size_assign = kwargs.get('leaf_size')
                    pass
                new_learner = dt.DTLearner(leaf_size_assign, verbose_assign)
                list_of_learners.append(new_learner)
            elif learner == rt.RTLearner:
                verbose_assign = False
                leaf_size_assign = 1
                if 'verbose' in kwargs.keys():
                    verbose_assign = kwargs.get('verbose')
                    pass
                if 'leaf_size' in kwargs.keys():
                    leaf_size_assign = kwargs.get('leaf_size')
                    pass
                new_learner = rt.RTLearner(leaf_size_assign, verbose_assign)
                list_of_learners.append(new_learner)
            elif learner == lrl.LinRegLearner:
                verbose_assign = False
                if 'verbose' in kwargs.keys():
                    verbose_assign = kwargs.get('verbose')
                    pass
                new_learner = lrl.LinRegLearner(verbose_assign)
                list_of_learners.append(new_learner)
            elif learner == BagLearner:
                new_learner = BagLearner(learner, kwargs, bags, boost, verbose)
                list_of_learners.append(new_learner)
            else:
                new_learner = learner(**kwargs)
                list_of_learners.append(new_learner)

        self.list_of_learners = list_of_learners



    def author(self):
        return 'prao43'  # replace tb34 with your Georgia Tech username

    def addEvidence(self, dataX, dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        number_of_rows = dataX.shape[0]
        for learner in self.list_of_learners:
            random_ids = np.random.choice(number_of_rows, number_of_rows, replace=True)
            randomized_dataX = dataX[random_ids]
            randomized_dataY = dataY[random_ids]
            learner.addEvidence(randomized_dataX, randomized_dataY)

    def query(self, points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        number_of_rows = points.shape[0]
        number_of_columns = len(self.list_of_learners)
        results = np.full((number_of_columns, number_of_rows), -1, dtype='float_')
        counter = 0
        for learner in self.list_of_learners:
            result_temp = learner.query(points)
            results[counter] = result_temp
            counter = counter + 1
        return np.mean(results, axis=0)


if __name__ == "__main__":
    print
    "the secret clue is 'zzyzx'"
