"""MC2-P1: Market simulator.

Copyright 2017, Georgia Tech Research Corporation
Atlanta, Georgia 30332-0415
All Rights Reserved
"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def author():
    """
    The use of 'Unladen African swallows' is apparently allowed.
    """
    return 'mhuang96'

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    orders_df.sort_index(inplace=True)
    start_date = orders_df.first_valid_index()
    end_date = orders_df.last_valid_index()
    dates = pd.date_range(start_date, end_date)
    symbols = np.array(orders_df.Symbol.unique()).tolist()
    prices = get_data(symbols, dates)
    cash = pd.DataFrame(index=dates, columns=['Cash'])
    cash = cash.fillna(1.0)
    prices = prices.join(cash)
    trades = create_trades(orders_df, prices, commission, impact)
    holdings = pd.DataFrame(0.0, columns=trades.columns, index=trades.index)
    holdings.loc[start_date, 'Cash'] = start_val
    holdings = (holdings + trades).cumsum()
    portvals = (prices * holdings).sum(axis = 1)
    return portvals

def create_trades(orders_df, prices, commission, impact):
    """
    https://www.youtube.com/watch?v=TstVUVbu-Tk
    Extra Credit: On June 15th, 2011 ignore all orders
    """
    trades = pd.DataFrame(0.0, columns=prices.columns, index=prices.index)
    spent = pd.DataFrame(index=prices.index, columns=['Commission', 'Impact'])
    spent = spent.fillna(0.0)
    #ignore_date = dt.datetime(2011,6,15,0,0) # Extra Credit??
    for date, row in orders_df.iterrows():
        # if date == ignore_date: # Extra Credit??
        #     continue
        sym = row['Symbol']
        shares = row['Shares']
        multiplier = -1 # SELL
        if (row['Order'] == 'BUY'):
            multiplier = 1
        trades.loc[date][sym] += (multiplier * shares)
        spent.loc[date]['Commission'] += commission
        spent.loc[date]['Impact'] += (prices.loc[date][sym] * shares * impact)
    trades['Cash'] = (-1.0 * (prices * trades).sum(axis = 1))
    trades['Cash'] = trades['Cash'] - spent['Commission'] - spent['Impact']
    return trades

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    #daily_returns.ix[0, :] = 0 # set daily returns for row 0 to 0
    return daily_returns[1:]

def compute_portfolio_stats(port_val, rfr=0.0, sf=252):
    daily_rets = compute_daily_returns(port_val)
    cr = (port_val[-1]/port_val[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = np.sqrt(sf)*((daily_rets - rfr).mean() / daily_rets.std())
    return cr, adr, sddr, sr

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-00.csv"
    sv = 1000000
    commission = 0.00
    impact = 0.0

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv, commission=commission, impact=impact)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals)
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
