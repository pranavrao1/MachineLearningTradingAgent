import datetime as dt
import pandas as pd
import numpy as np
from util import get_data, plot_data
import marketsimcode as ms
import matplotlib.dates as matplot_dates
import matplotlib.pyplot as plt

def testPolicy(symbol = "AAPL",
               sd=dt.datetime(2010,1,1),
               ed=dt.datetime(2011,12,31),
               sv=100000):
    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    prices_df.fillna(method='ffill', inplace=True)
    prices_df.fillna(method='bfill', inplace=True)
    prices_normalized_df = prices_df / prices_df.ix[0, :]

    shares_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Shares'])
    orders_df = pd.DataFrame('HOLD', index = prices_normalized_df.index, columns = ['Order'])
    symbols_df = pd.DataFrame(symbol, index = prices_normalized_df.index, columns = ['Symbol'])
    holdings_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Holdings'])

    number_of_entries = prices_normalized_df.shape[0]
    total_holdings = 0
    for index in range(number_of_entries-1):
        current_date = prices_normalized_df.index[index]
        new_date = prices_normalized_df.index[index + 1]
        current_price = prices_normalized_df.loc[current_date][symbol]
        new_price = prices_normalized_df.loc[new_date][symbol]
        if (new_price > current_price) and (total_holdings < 1000):
            orders_df.loc[current_date]['Order'] = 'BUY'
            if total_holdings == 0:
                shares_df.loc[current_date]['Shares'] = 1000
                holdings_df.loc[current_date]['Holdings'] = 1000
                total_holdings += 1000
            else:
                shares_df.loc[current_date]['Shares'] = 2000
                holdings_df.loc[current_date]['Holdings'] = 2000
                total_holdings += 2000
        elif (new_price < current_price) and (total_holdings > -1000):
            orders_df.loc[current_date]['Order'] = 'SELL'
            if total_holdings == 0:
                shares_df.loc[current_date]['Shares'] = 1000
                holdings_df.loc[current_date]['Holdings'] = -10000
                total_holdings -= 1000
            else:
                shares_df.loc[current_date]['Shares'] = 2000
                holdings_df.loc[current_date]['Holdings'] = -20000
                total_holdings -= 2000
    df_trades = pd.concat([symbols_df, orders_df, shares_df, holdings_df], axis=1)
    df_trades.columns = ['Symbol', 'Order', 'Shares', 'Holdings']
    return df_trades[df_trades.Order != 'HOLD']

def testPolicyBenchmark(symbol = "AAPL",
               sd=dt.datetime(2010,1,1),
               ed=dt.datetime(2011,12,31),
               sv=100000):
    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    prices_df.fillna(method='ffill', inplace=True)
    prices_df.fillna(method='bfill', inplace=True)
    prices_normalized_df = prices_df / prices_df.ix[0, :]

    shares_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Shares'])
    orders_df = pd.DataFrame('HOLD', index = prices_normalized_df.index, columns = ['Order'])
    symbols_df = pd.DataFrame(symbol, index = prices_normalized_df.index, columns = ['Symbol'])
    holdings_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Holdings'])

    number_of_entries = prices_normalized_df.shape[0]
    total_holdings = 0
    current_date = prices_normalized_df.index[0]
    shares_df.loc[current_date]['Shares'] = 1000
    df_trades = pd.concat([symbols_df, orders_df, shares_df, holdings_df], axis=1)
    df_trades.columns = ['Symbol', 'Order', 'Shares', 'Holdings']
    return df_trades

if __name__ == "__main__":
    pd.set_option('chained_assignment', None)
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    start_value = 100000

    df_trades = testPolicy(symbol="JPM", sd=start_date, ed=end_date, sv=start_value)
    portfolio_value = ms.compute_portvals(df_trades, start_val=start_value, commission=0.00, impact=0.0)
    portfolio_value.fillna(method='ffill', inplace=True)
    portfolio_value.fillna(method='bfill', inplace=True)
    portfolio_value_norm = portfolio_value / portfolio_value.ix[0, :]

    df_trades_benchmark = testPolicyBenchmark(symbol="JPM", sd=start_date, ed=end_date, sv=start_value)
    benchmark_value = ms.compute_portvals(df_trades_benchmark, start_val=start_value, commission=0.00, impact=0.0)
    benchmark_value.fillna(method='ffill', inplace=True)
    benchmark_value.fillna(method='bfill', inplace=True)
    benchmark_value_norm = benchmark_value / benchmark_value.ix[0, :]

    first_plot = portfolio_value_norm.plot(grid=True, title='Best Possible Strategy', use_index=True, color='black')
    first_plot.xaxis.set_major_locator(matplot_dates.MonthLocator())
    first_plot.xaxis.set_major_formatter(matplot_dates.DateFormatter('%b'))
    first_plot.xaxis.set_minor_locator(matplot_dates.YearLocator())
    first_plot.xaxis.set_minor_formatter(matplot_dates.DateFormatter('%Y'))
    first_plot.xaxis.set_tick_params(which='minor', pad=20)
    date_min = dt.date(df_trades.index.min().year, 1, 1)
    date_max = dt.date(df_trades.index.max().year + 1, 1, 1)
    first_plot.set_xlabel("Date")
    first_plot.set_ylabel("Normed")
    first_plot.set_xlim(date_min, date_max)

    second_plot = benchmark_value_norm.plot(grid=True, title='Best Possible Strategy', use_index=True, color='blue')
    plt.legend(('Portfolio Value', 'Benchmark'), loc='best', prop={'size': 12})
    plt.savefig('Best Possible Strategy.png')
    plt.clf()
    plt.cla()
    plt.close()

    print "NORMALIZED IN SAMPLE"
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = ms.compute_portfolio_stats(portfolio_value_norm)
    cum_ret_bench, avg_daily_ret_bench, std_daily_ret_bench, sharpe_ratio_bench = ms.compute_portfolio_stats(benchmark_value_norm)
    print "Sharpe Ratio of Portfolio: {}".format(sharpe_ratio)
    print "Sharpe Ratio of Benchmark : {}".format(sharpe_ratio_bench)
    print
    print "Cumulative Return of Portfolio: {}".format(cum_ret)
    print "Cumulative Return of Benchmark: {}".format(cum_ret_bench)
    print
    print "Standard Deviation of Portfolio: {}".format(std_daily_ret)
    print "Standard Deviation of Benchmark: {}".format(std_daily_ret_bench)
    print
    print "Average Daily Return of Portfolio: {}".format(avg_daily_ret)
    print "Average Daily Return of Benchmark: {}".format(avg_daily_ret_bench)