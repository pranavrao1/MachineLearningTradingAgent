"""Assess a betting strategy.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
import matplotlib.pyplot as plt

def author():
    return 'prao43'


def gtid():
    return 903205913  # replace with your GT ID number


def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob:
        result = True
    return result

def run_figure4(win_prob):
    # Figure 4
    array_figure = np.zeros((1000,1000), dtype=np.int_)
    for i in range(1, 1000):
        simulation_results = run_simulation_with_limit(1000, win_prob)
        array_figure[i-1] = simulation_results
    mean_value = array_figure.mean(axis=0)
    std_value = array_figure.std(axis=0)
    plt.plot(mean_value, label="Mean value of winning for each spin")
    plt.plot(mean_value + std_value, label="Mean value + standard Deviation")
    plt.plot(mean_value - std_value, label="Mean value - standard Deviation")
    plt.axis([0, 300, -256, 100])
    plt.title('Figure 4: Mean values for 1000 separate simulations with 1000 bets each with 256 initial amount.')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Winnings in $')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.savefig('Figure 4')
    plt.clf()
    plt.cla()
    plt.close()

def run_figure5(win_prob):
    # Figure 5
    array_figure = np.zeros((1000,1000), dtype=np.int_)
    for i in range(1, 1000):
        simulation_results = run_simulation_with_limit(1000, win_prob)
        array_figure[i-1] = simulation_results
    median_value = np.median(array_figure, axis=0)
    std_value = array_figure.std(axis=0)
    plt.plot(median_value, label="Median value of winning for each spin")
    plt.plot(median_value + std_value, label="Median value + standard Deviation")
    plt.plot(median_value - std_value, label="Median value - standard Deviation")
    plt.axis([0,300,-256,100])
    plt.title('Figure 5: Median values for 1000 separate simulations with 1000 bets each with 256 initial amount.')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Winnings in $')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.savefig('Figure 5')
    plt.clf()
    plt.cla()
    plt.close()


def test_code():
    win_prob = 0.47  # set appropriately to the probability of a win
    np.random.seed(gtid())  # do this only once
    print
    get_spin_result(win_prob)  # test the roulette spin

    # add your code here to implement the experiments
    # Figure 1
    for i in range(1,10):
        figure_one = run_simulation(1000, win_prob)
        label = "Run " + str(i)
        plt.plot(figure_one, label=label)
    plt.axis([0,300,-256,100])
    plt.title('Figure 1: 10 separate simulations with 1000 bets')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Winnings in $')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.savefig('Figure 1')
    plt.clf()
    plt.cla()
    plt.close()

    # Figure 2
    array = np.zeros((1000,1000), dtype=np.int_)
    for i in range(1, 1000):
        simulation_results = run_simulation(1000, win_prob)
        array[i-1] = simulation_results
    mean_value = array.mean(axis=0)
    std_value = array.std(axis=0)
    plt.plot(mean_value, label="Mean value of winning for each spin")
    plt.plot(mean_value + std_value, label="Mean value + standard Deviation")
    plt.plot(mean_value - std_value, label="Mean value - standard Deviation")
    plt.axis([0,300,-256,100])
    plt.title('Figure 2: Mean values for 1000 separate simulations with 1000 bets each')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Winnings in $')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.savefig('Figure 2')
    plt.clf()
    plt.cla()
    plt.close()

    # Figure 3
    array_figure3 = np.zeros((1000,1000), dtype=np.int_)
    for i in range(1, 1000):
        simulation_results = run_simulation(1000, win_prob)
        array_figure3[i-1] = simulation_results
    median_value = np.median(array_figure3, axis=0)
    std_value_3 = array_figure3.std(axis=0)
    plt.plot(median_value, label="Median value of winning for each spin")
    plt.plot(median_value + std_value_3, label="Median value + standard Deviation")
    plt.plot(median_value - std_value_3, label="Median value - standard Deviation")
    plt.axis([0,300,-256,100])
    plt.title('Figure 3: Median values for 1000 separate simulations with 1000 bets each')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Winnings in $')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.savefig('Figure 3')
    plt.clf()
    plt.cla()
    plt.close()
    run_figure4(win_prob)
    run_figure5(win_prob)


def run_simulation(number_of_bets, win_prob):
    winnings = np.zeros(number_of_bets, dtype=np.int_)
    max_winnings = 80
    counter = 1
    while (counter < number_of_bets):
        if winnings[counter - 1] < max_winnings:
            bet_amount = 1
            spin = False
            while not spin and counter < number_of_bets:
                spin = get_spin_result(win_prob)
                if spin:
                    winnings[counter] = winnings[counter - 1] + bet_amount
                else:
                    winnings[counter] = winnings[counter - 1] - bet_amount
                    bet_amount = bet_amount * 2
                counter = counter + 1
        else:
            winnings[counter] = winnings[counter - 1]
            counter = counter + 1
    return winnings

def run_simulation_with_limit(number_of_bets, win_prob):
    winnings = np.zeros(number_of_bets, dtype=np.int_)
    max_winnings = 80

    counter = 1
    while (counter < number_of_bets):
        if winnings[counter - 1] < max_winnings and winnings[counter-1] > -256:
            bet_amount = 1
            spin = False
            while not spin and counter < number_of_bets and winnings[counter-1] > -256:
                spin = get_spin_result(win_prob)
                if spin:
                    winnings[counter] = winnings[counter - 1] + bet_amount
                else:
                    winnings[counter] = winnings[counter - 1] - bet_amount
                    bet_amount = bet_amount * 2
                    ## If the current winning is less than 0, it means you have gone below the 256 initial amount
                    ## and the bet amount is larger than loss amount you can only use the loss amount.
                    if winnings[counter] < 0 and bet_amount > (256 + winnings[counter]):
                        bet_amount = 256 + winnings[counter]
                counter = counter + 1
        else:
            winnings[counter] = winnings[counter - 1]
            counter = counter + 1
    return winnings


if __name__ == "__main__":
    test_code()
