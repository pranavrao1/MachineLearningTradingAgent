"""MC2-P1: Market simulator.

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

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data


def author():
    return 'prao43'


# def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):
#     # this is the function the autograder will call to test your code
#     # NOTE: orders_file may be a string, or it may be a file object. Your
#     # code should work correctly with either input
#     # TODO: Your code here
#
#     # In the template, instead of computing the value of the portfolio, we just
#     # read in the value of IBM over 6 months
#     # start_date = dt.datetime(2008,1,1)
#     # end_date = dt.datetime(2008,6,1)
#     # portvals = get_data(['IBM'], pd.date_range(start_date, end_date))
#     # portvals = portvals[['IBM']]  # remove SPY
#     # rv = pd.DataFrame(index=portvals.index, data=portvals.as_matrix())
#     #
#     # return rv
#     orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

def compute_portvals(orders_df, start_val=1000000, commission=9.95, impact=0.005):
    orders_df.sort_index()
    start_date = orders_df.first_valid_index()
    end_date = orders_df.last_valid_index()
    date_range = pd.date_range(start_date, end_date)

    array_symbols = orders_df.Symbol.unique()
    prices_df = get_data(array_symbols.tolist(), date_range)
    prices_df.fillna(method="ffill", inplace=True)
    prices_df.fillna(method="bfill", inplace=True)

    trades_df_columns = np.append(array_symbols, ['Cash'])
    filtered_date_range = prices_df.index
    trades_df = pd.DataFrame(0.0, index=filtered_date_range, columns=trades_df_columns.tolist())

    # Enter Data into trades DF
    for date, row in orders_df.iterrows():
        symbol = row['Symbol']
        number_shares = row['Shares']
        multiplier = 1  # if it is a BUY
        if row['Order'] == 'SELL':
            multiplier = -1
        volume = multiplier * number_shares
        if date in prices_df.index:
            stock_price = prices_df.loc[date][symbol]
            transaction = volume * stock_price
            trades_impact = number_shares * stock_price * impact
            trades_df.loc[date][symbol] += volume
            trades_df.loc[date]['Cash'] += -1 * transaction - commission - trades_impact

    # Enter Data into holdings DF
    holdings_df = trades_df
    holdings_df['Cash'][0] += start_val
    holdings_df = holdings_df.cumsum()

    # Enter Data into value DF
    prices_df['Cash'] = 1.0
    value_df = prices_df * holdings_df
    portvals = value_df.sum(axis=1)
    return portvals


def compute_daily_returns(df):
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    return daily_returns[1:]


def compute_portfolio_stats(port_val, rfr=0.0, sf=252):
    daily_rets = compute_daily_returns(port_val)
    cr = (port_val[-1] / port_val[0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = np.sqrt(sf) * ((daily_rets - rfr).mean() / daily_rets.std())
    return cr, adr, sddr, sr


def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-00.csv"
    sv = 1000000
    commission = 9.95
    impact = 0.005

    # Process orders
    start_time = dt.datetime.now()
    print
    "Start Time:"
    print(start_time)
    portvals = compute_portvals(orders_file=of, start_val=sv, commission=commission, impact=impact)
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2008, 6, 1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals)
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]

    # Compare portfolio against $SPX
    end_time = dt.datetime.now()
    print
    "End Time:"
    print(end_time)

    print
    "Difference:"
    print(end_time - start_time)
    print
    "Date Range: {} to {}".format(start_date, end_date)
    print
    print
    "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print
    "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print
    "Cumulative Return of Fund: {}".format(cum_ret)
    print
    "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print
    "Standard Deviation of Fund: {}".format(std_daily_ret)
    print
    "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print
    "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print
    "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print
    "Final Portfolio Value: {}".format(portvals[-1])


if __name__ == "__main__":
    test_code()
