"""
Template for implementing QLearner  (c) 2015 Tucker Balch

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

Student Name: Tucker Balch (replace with your name)
GT User ID: tb34 (replace with your User ID)
GT ID: 900897987 (replace with your GT ID)
"""

import numpy as np
import random as rand

class QLearner(object):

    def __init__(self, \
        num_states=100, \
        num_actions = 4, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.5, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False):

        self.verbose = verbose
        self.num_actions = num_actions
        self.state = 0
        self.action = 0
        self.rar = rar
        self.radr = radr
        self.dyna = dyna
        self.alpha = alpha
        self.gamma = gamma
        self.num_states = num_states
        self.q_matrix = (np.random.rand(num_states, num_actions))
        self.reward_matrix = np.zeros((num_states, num_actions))
        self.transition_matrix = np.zeros((num_states, num_actions, num_states))
        self.transition_matrix_second = np.zeros((num_states, num_actions, num_states))

    def querysetstate(self, s):
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Update the state without updating the Q-table  		   	  			    		  		  		    	 		 		   		 		  
        @param s: The new state  		   	  			    		  		  		    	 		 		   		 		  
        @returns: The selected action  		   	  			    		  		  		    	 		 		   		 		  
        """
        self.state = s
        if np.random.uniform() < self.rar:
            action = rand.randint(0, self.num_actions-1)
        else:
            action = np.argmax(self.q_matrix[s, :])
        if self.verbose: print "s =", s,"a =",action
        self.action = action
        return action

    def query(self,s_prime,r):
        """
        @summary: Update the Q table and return an action
        @param s_prime: The new state
        @param r: The ne state
        @returns: The selected action
        """
        #action = rand.randint(0, self.num_actions-1)
        self.q_matrix[self.state, self.action] = (1 - self.alpha) * self.q_matrix[self.state, self.action] + self.alpha * (r + (self.gamma * np.max(self.q_matrix[s_prime, :])))

        if (self.dyna > 0):
            self.transition_matrix_second[self.state, self.action, s_prime] = self.transition_matrix_second[self.state, self.action, s_prime] + 1
            self.transition_matrix = self.transition_matrix_second/self.transition_matrix_second.sum(axis=2, keepdims=True)
            self.reward_matrix[self.state, self.action] = ((1 - self.alpha) * self.reward_matrix[self.state, self.action]) + (self.alpha * r)
            counter = 0
            while counter < self.dyna:
                state_random = rand.randint(0, self.num_states - 1)
                action_random = rand.randint(0, self.num_actions - 1)
                s_prime_random = np.random.multinomial(100, self.transition_matrix[state_random,action_random,:]).argmax()
                self.q_matrix[state_random, action_random] = (1 - self.alpha) * self.q_matrix[state_random, action_random] + self.alpha * (self.reward_matrix[state_random, action_random] + (self.gamma * np.max(self.q_matrix[s_prime_random, :])))
                counter+=1

        action = self.querysetstate(s_prime)
        self.rar *= self.radr

        if self.verbose: print "s =", s_prime,"a =",action,"r =",r
        return action

    def author(self):
        return 'prao43'

if __name__=="__main__":
    print "Remember Q from Star Trek? Well, this isn't him"
