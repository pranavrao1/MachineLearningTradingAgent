"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import util as ut
import QLearner as ql
from util import get_data, plot_data
  		   	  			    		  		  		    	 		 		   		 		  
class StrategyLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # constructor  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False, impact=0.0):  		   	  			    		  		  		    	 		 		   		 		  
        self.verbose = verbose  		   	  			    		  		  		    	 		 		   		 		  
        self.impact = impact
        self.ql = ql.QLearner(num_states=200,
                              num_actions=3,
                              alpha=0.2,
                              gamma=0.9,
                              rar=0.5,
                              radr=0.99,
                              dyna=0,
                              verbose=verbose)
  		   	  			    		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
        # add your code to do learning here
        window = 20  # days of window
  		   	  			    		  		  		    	 		 		   		 		  
        # example usage of the old backward compatible util function  		   	  			    		  		  		    	 		 		   		 		  
        syms=[symbol]  		   	  			    		  		  		    	 		 		   		 		  
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		   	  			    		  		  		    	 		 		   		 		  
        prices = prices_all[syms]  # only portfolio symbols
        if self.verbose: print prices


        # this is so there are not na's before the window starts
        start_date_adj = sd - dt.timedelta(window + 50)
        normed_prices = self.normalize_df(prices)
        momentum = self.compute_momentum(syms, start_date_adj, ed, window)
        sma = self.compute_sma(syms, start_date_adj, ed, window)
        bb = self.compute_bollinger(syms, start_date_adj, ed)
        bb_percent = self.compute_bb_percentage(bb,normed_prices, symbol)
        indicators = pd.concat([sma, momentum, bb_percent, bb], axis=1)
        indicators = indicators.loc[sd:]
        normed_prices = normed_prices[sd:]
        daily_returns = self.compute_daily_returns(normed_prices)

        state = self.discretize(indicators)
        initial_state = state.iloc[0]['State']
        self.ql.querysetstate(initial_state)

        shares_df = pd.DataFrame(0, index=normed_prices.index, columns=['Shares'])
        orders_df = pd.DataFrame('HOLD', index=normed_prices.index, columns=['Order'])
        symbols_df = pd.DataFrame(symbol, index=normed_prices.index, columns=['Symbol'])
        holdings_df = pd.DataFrame(0, index=normed_prices.index, columns=['Holdings'])

        count = 50
        rewards = []
        current_reward = 0
        for i in range(0, count):
            if len(rewards) > 10:
                rewards.pop(0)
            if i > 25:
                rewards.append(current_reward)
                # Policy has converged
                if (len(rewards) > 10) and all(rewards[0] == r for r in rewards):
                    break
            sum_holdings = 0
            current_reward = 0
            # Do some action
            for index, row in normed_prices.iterrows():
                current_reward = float(sum_holdings * daily_returns.loc[index]) * (1 - self.impact)
                a = self.ql.query(state.loc[index]['State'], current_reward)
                if (a == 1) and (sum_holdings < 1000):
                    orders_df.loc[index]['Order'] = 'BUY'
                    if sum_holdings == 0:
                        shares_df.loc[index]['Shares'] = 1000
                        sum_holdings += 1000
                        holdings_df.loc[index]['Holdings'] = sum_holdings
                    else:
                        shares_df.loc[index]['Shares'] = 2000
                        sum_holdings += 2000
                        holdings_df.loc[index]['Holdings'] = sum_holdings
                elif (a == 2) and (sum_holdings > -1000):
                    orders_df.loc[index]['Order'] = 'SELL'
                    if sum_holdings == 0:
                        shares_df.loc[index]['Shares'] = -1000
                        sum_holdings -= 1000
                        holdings_df.loc[index]['Holdings'] = sum_holdings
                    else:
                        shares_df.loc[index]['Shares'] = -2000
                        sum_holdings -= 2000
                        holdings_df.loc[index]['Holdings'] = sum_holdings
                holdings_df.loc[index]['Holdings'] = sum_holdings
            df_trades = pd.concat([symbols_df, orders_df, shares_df, holdings_df], axis=1)
            df_trades.columns = ['Symbol', 'Order', 'Shares', 'Holdings']
            df_trades = df_trades[df_trades.Shares != 0]

        # example use with new colname
        if self.verbose: print df_trades
        return df_trades
  		   	  			    		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		   	  			    		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        # add your code to do learning here
        window = 20  # days of window

        # example usage of the old backward compatible util function
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        if self.verbose: print
        prices

        # this is so there are not na's before the window starts
        start_date_adj = sd - dt.timedelta(window + 50)
        normed_prices = self.normalize_df(prices)
        momentum = self.compute_momentum(syms, start_date_adj, ed, window)
        sma = self.compute_sma(syms, start_date_adj, ed, window)
        bb = self.compute_bollinger(syms, start_date_adj, ed)
        bb_percent = self.compute_bb_percentage(bb, normed_prices, symbol)
        indicators = pd.concat([sma, momentum, bb_percent, bb], axis=1)
        indicators = indicators.loc[sd:]
        normed_prices = normed_prices[sd:]

        state = self.discretize(indicators)
        initial_state = state.iloc[0]['State']
        shares_df = pd.DataFrame(0, index=normed_prices.index, columns=['Shares'])
        orders_df = pd.DataFrame('HOLD', index=normed_prices.index, columns=['Order'])
        total_holdings = 0
        self.ql.querysetstate(initial_state)

        for index, row in normed_prices.iterrows():
            a = self.ql.querysetstate(state.loc[index]['State'])
            if (a == 1) and (total_holdings < 1000):
                orders_df.loc[index]['Order'] = 'BUY'
                if total_holdings == 0:
                    shares_df.loc[index]['Shares'] = 1000
                    total_holdings += 1000
                else:
                    shares_df.loc[index]['Shares'] = 2000
                    total_holdings += 2000
            elif (a == 2) and (total_holdings > -1000):
                orders_df.loc[index]['Order'] = 'SELL'
                if total_holdings == 0:
                    shares_df.loc[index]['Shares'] = -1000
                    total_holdings -= 1000
                else:
                    shares_df.loc[index]['Shares'] = -2000
                    total_holdings -= 2000

        shares_df = shares_df[shares_df.Shares != 0]
        return shares_df

    def testPolicyWithAdditionalStats(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):
        # add your code to do learning here
        window = 20  # days of window

        # example usage of the old backward compatible util function
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        if self.verbose: print
        prices

        # this is so there are not na's before the window starts
        start_date_adj = sd - dt.timedelta(window + 50)
        normed_prices = self.normalize_df(prices)
        momentum = self.compute_momentum(syms, start_date_adj, ed, window)
        sma = self.compute_sma(syms, start_date_adj, ed, window)
        bb = self.compute_bollinger(syms, start_date_adj, ed)
        bb_percent = self.compute_bb_percentage(bb, normed_prices, symbol)
        indicators = pd.concat([sma, momentum, bb_percent, bb], axis=1)
        indicators = indicators.loc[sd:]
        normed_prices = normed_prices[sd:]

        state = self.discretize(indicators)
        initial_state = state.iloc[0]['State']
        shares_df = pd.DataFrame(0, index=normed_prices.index, columns=['Shares'])
        orders_df = pd.DataFrame('HOLD', index=normed_prices.index, columns=['Order'])
        symbols_df = pd.DataFrame(symbol, index=normed_prices.index, columns=['Symbol'])
        holdings_df = pd.DataFrame(0, index=normed_prices.index, columns=['Holdings'])
        total_holdings = 0
        self.ql.querysetstate(initial_state)

        for index, row in normed_prices.iterrows():
            a = self.ql.querysetstate(state.loc[index]['State'])
            if (a == 1) and (total_holdings < 1000):
                orders_df.loc[index]['Order'] = 'BUY'
                if total_holdings == 0:
                    shares_df.loc[index]['Shares'] = 1000
                    total_holdings += 1000
                else:
                    shares_df.loc[index]['Shares'] = 2000
                    total_holdings += 2000
            elif (a == 2) and (total_holdings > -1000):
                orders_df.loc[index]['Order'] = 'SELL'
                if total_holdings == 0:
                    shares_df.loc[index]['Shares'] = -1000
                    total_holdings -= 1000
                else:
                    shares_df.loc[index]['Shares'] = -2000
                    total_holdings -= 2000

        df_trades = pd.concat([symbols_df, orders_df, shares_df, holdings_df], axis=1)
        df_trades.columns = ['Symbol', 'Order', 'Shares', 'Holdings']
        df_trades = df_trades[df_trades.Shares != 0]
        df_trades['Shares'] = df_trades['Shares'].abs()
        return df_trades


    def discretize(self, df):
        bins = ['0', '1', '2', '3', '4', '5']
        columns = ['SMA', 'Price/SMA', 'Momentum',
                   'BBP', 'lower', 'upper',
                   'band']
        temporary_df = pd.DataFrame(0, index=df.index, columns=columns)
        # states
        for c in columns:
            temporary_df[c] = pd.cut(df[c], bins=6, labels=bins)

        state = pd.DataFrame(0, index=df.index, columns=['State'])
        state['State'] = temporary_df['Momentum'].astype(str) + temporary_df['BBP'].astype(str)
        state['State'] = state['State'].astype(int)
        return state

    def author(self):
        return 'prao43'

    def normalize_df(self, df):
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)
        return df / df.ix[0, :]

    def compute_bollinger(self, symbols=['JPM'],
                          start_date='2008-01-01',
                          end_date='2009-12-31',
                          window=20):
        dates = pd.date_range(start_date, end_date)
        prices_all = get_data(symbols, dates)
        normed_prices = self.normalize_df(prices_all)
        columns = ['lower', 'upper', 'band']
        bb = pd.DataFrame(0, index=normed_prices.index, columns=columns)
        bb['band'] = normed_prices.rolling(window=window, min_periods=window).std()
        sma = self.compute_sma(symbols, start_date, end_date, window)
        bb['upper'] = sma['SMA'] + (bb['band'] * 2)
        bb['lower'] = sma['SMA'] - (bb['band'] * 2)
        return bb

    def compute_sma(self, symbols=['JPM'],
                    start_date='2008-01-01',
                    end_date='2009-12-31',
                    window=20):
        """
        Simple Moving Average
        window size default of 20
        """
        dates = pd.date_range(start_date, end_date)
        prices_all = get_data(symbols, dates)
        normed_prices = self.normalize_df(prices_all)
        columns = ['SMA', 'Price/SMA']
        sma = pd.DataFrame(0, index=normed_prices.index, columns=columns)
        sma['SMA'] = normed_prices[symbols[0]].rolling(window=window, center=False).mean()
        sma['Price/SMA'] = normed_prices[symbols[0]] / sma['SMA']
        return sma

    def compute_bb_percentage(self, bb, normed_syms, symbol):
        bb_percent = pd.DataFrame(0, index=normed_syms.index, columns=['BBP'])
        bb_percent['BBP'] = (normed_syms[symbol] - bb['lower']) / (bb['upper'] - bb['lower'])
        return bb_percent

    def compute_momentum(self, symbols=['JPM'],
                         start_date='2008-01-01',
                         end_date='2009-12-31',
                         window=20):
        dates = pd.date_range(start_date, end_date)
        prices_all = get_data(symbols, dates)
        normed_prices = self.normalize_df(prices_all)
        columns = ['Momentum']
        momentum = pd.DataFrame(0, index=normed_prices[symbols[0]].index, columns=columns)
        momentum['Momentum'] = normed_prices[symbols[0]].diff(window) / normed_prices[symbols[0]].shift(window)
        return momentum

    def compute_daily_returns(self, df):
        daily_returns = df.copy()
        daily_returns[1:] = (df[1:] / df[:-1].values) - 1
        return daily_returns
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "One does not simply think up a strategy"
