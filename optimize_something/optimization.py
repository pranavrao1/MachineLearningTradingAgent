"""MC1-P2: Optimize a portfolio.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Pranav Pradeep Rao (replace with your name)
GT User ID: prao43 (replace with your User ID)
GT ID: 903205913 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt
import scipy.optimize as spo
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
# This is the function that will be tested by the autograder  		   	  			    		  		  		    	 		 		   		 		  
# The student must update this code to properly implement the functionality  		   	  			    		  		  		    	 		 		   		 		  
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Read in adjusted closing prices for given symbols, date range  		   	  			    		  		  		    	 		 		   		 		  
    dates = pd.date_range(sd, ed)  		   	  			    		  		  		    	 		 		   		 		  
    prices_all = get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
    prices = prices_all[syms]  # only portfolio symbols  		   	  			    		  		  		    	 		 		   		 		  
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # find the allocations for the optimal portfolio  		   	  			    		  		  		    	 		 		   		 		  
    # note that the values here ARE NOT meant to be correct for a test case

    number_of_stocks = len(syms)
    allocs = np.full(number_of_stocks, 1/float(number_of_stocks), dtype=np.float_)
    prices.fillna(method="ffill", inplace=True)
    prices.fillna(method="bfill", inplace=True)
    prices_SPY.fillna(method="ffill", inplace=True)
    prices_SPY.fillna(method="bfill", inplace=True)

    def optimization_method(allocs):
        cr_inner, adr_inner, sddr_inner, sr_inner = compute_assesment(prices, allocs, syms)
        return -1 * sr_inner

    bounds = [(0, 1)]*number_of_stocks
    max_results = spo.minimize(optimization_method, allocs, method='SLSQP', options={'disp':True}, bounds=bounds,
                               constraints=({'type': 'eq', 'fun': lambda x: 1 - np.sum(x)}))
    allocs = max_results.x
    cr, adr, sddr, sr = compute_assesment(prices, allocs, syms)
    # Get daily portfolio value  		   	  			    		  		  		    	 		 		   		 		  
    port_val = compute_portfolio_value_daily(allocs, prices, syms)/1000000
  		   	  			    		  		  		    	 		 		   		 		  
    # Compare daily portfolio value with SPY using a normalized plot  		   	  			    		  		  		    	 		 		   		 		  
    if gen_plot:  		   	  			    		  		  		    	 		 		   		 		  
        # add code to plot here
        port_val_spy = compute_portfolio_spy_daily(prices_SPY)
        df_temp = pd.concat([port_val, port_val_spy], keys=['Portfolio', 'SPY'], axis=1)
        plt.figure()
        df_temp.plot()
        plt.legend(loc="best")
        plt.grid(True)
        plt.title('Daily Portfolio Value and SPY', fontsize=12)
        plt.ylabel('Price')
        plt.xlabel('Date')
        plt.savefig('Daily Portfolio Value')
        plt.clf()
        plt.cla()
        plt.close()
  		   	  			    		  		  		    	 		 		   		 		  
    return allocs, cr, adr, sddr, sr

def compute_assesment(prices, allocs_initial, syms):
    portfolio_value_daily = compute_portfolio_value_daily(allocs_initial, prices, syms)
    daily_returns = (portfolio_value_daily[1:]/portfolio_value_daily[:-1].values) - 1
    cr = (portfolio_value_daily[-1] / portfolio_value_daily[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    delta_returns_diff = np.subtract(daily_returns, 0)
    sr = np.multiply(np.sqrt(252),np.divide(delta_returns_diff.mean(),sddr))
    return cr, adr, sddr, sr


def compute_portfolio_value_daily(allocs_initial, prices, syms):
    normalized_prices = prices / prices.iloc[0]
    ## Multiply allocation
    allocated_prices = normalized_prices.copy(deep=True)
    portfolio_prices = normalized_prices.copy(deep=True)
    for i in range(allocs_initial.size):
        allocated_prices[syms[i]] = normalized_prices[syms[i]] * allocs_initial[i]
        portfolio_prices[syms[i]] = allocated_prices[syms[i]] * 1000000
    portfolio_value_daily = portfolio_prices.sum(axis=1)
    return portfolio_value_daily

def compute_portfolio_spy_daily(prices_SPY):
    ### Calculate values
    normalized_prices_spy = prices_SPY / prices_SPY.iloc[0]
    return normalized_prices_spy


def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # This function WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that any variables defined here are available to your function/code  		   	  			    		  		  		    	 		 		   		 		  
    # It is only here to help you set up and test your code  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
    # Note that ALL of these values will be set to different values by  		   	  			    		  		  		    	 		 		   		 		  
    # the autograder!  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']
  		   	  			    		  		  		    	 		 		   		 		  
    # Assess the portfolio  		   	  			    		  		  		    	 		 		   		 		  
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)
  		   	  			    		  		  		    	 		 		   		 		  
    # Print statistics  		   	  			    		  		  		    	 		 		   		 		  
    print "Start Date:", start_date  		   	  			    		  		  		    	 		 		   		 		  
    print "End Date:", end_date  		   	  			    		  		  		    	 		 		   		 		  
    print "Symbols:", symbols  		   	  			    		  		  		    	 		 		   		 		  
    print "Allocations:", allocations  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio:", sr  		   	  			    		  		  		    	 		 		   		 		  
    print "Volatility (stdev of daily returns):", sddr  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return:", adr  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return:", cr  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    # This code WILL NOT be called by the auto grader  		   	  			    		  		  		    	 		 		   		 		  
    # Do not assume that it will be called  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
