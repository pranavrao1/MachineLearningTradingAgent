import datetime as dt
import pandas as pd
from util import get_data, plot_data
import matplotlib.pyplot as plt
import matplotlib.dates as matplot_dates
import marketsimcode as ms

def testPolicy(symbol = "AAPL",
               sd=dt.datetime(2010,1,1),
               ed=dt.datetime(2011,12,31),
               sv=100000):
    stock_ticker = [symbol]
    dates = pd.date_range(sd, ed)
    prices_df = get_data([symbol], dates)
    prices_df.fillna(method='ffill', inplace=True)
    prices_df.fillna(method='bfill', inplace=True)
    prices_normalized_df = prices_df / prices_df.ix[0, :]

    shares_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Shares'])
    orders_df = pd.DataFrame('HOLD', index = prices_normalized_df.index, columns = ['Order'])
    symbols_df = pd.DataFrame(symbol, index = prices_normalized_df.index, columns = ['Symbol'])
    holdings_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Holdings'])

    total_holdings = 0

    #calculate SMA
    columns_sma = ['SMA', 'Price/SMA']
    sma_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = columns_sma)
    sma_df['SMA'] = prices_normalized_df[stock_ticker[0]].rolling(window=20, center=False).mean()
    sma_df['Price/SMA'] = prices_normalized_df[stock_ticker[0]] / sma_df['SMA']

    # calculate bollinger
    columns_bb = ['Lower', 'Upper', 'Deviation']
    bollinger_bands_df = pd.DataFrame(0, index=prices_normalized_df.index, columns=columns_bb)
    bollinger_bands_df['Deviation'] = prices_normalized_df.rolling(window=20).std()
    bollinger_bands_df['Upper'] = sma_df['SMA'] + (2 * bollinger_bands_df['Deviation'])
    bollinger_bands_df['Lower'] = sma_df['SMA'] - (2 * bollinger_bands_df['Deviation'])

    #calculate momentum
    momentum_df = pd.DataFrame(0, index=prices_normalized_df.index, columns=['JPM', 'Momentum'])
    momentum_df['Momentum'] = prices_normalized_df[stock_ticker[0]].diff(20) / prices_normalized_df[stock_ticker[0]].shift(20)

    for index, row in prices_normalized_df.iterrows():

        bbp_upper = bollinger_bands_df.loc[index]['Upper']
        bbp_lower = bollinger_bands_df.loc[index]['Lower']

        momentum_value = momentum_df.loc[index]['Momentum']
        current_price = row[symbol]
        bbp_perencet = (current_price-bbp_lower)/(bbp_upper-bbp_lower)
        if (momentum_value < -0.01) and (bbp_perencet < 0.05) and (total_holdings < 1000):
            orders_df.loc[index]['Order'] = 'BUY'
            if total_holdings == 0:
                shares_df.loc[index]['Shares'] = 1000
                total_holdings += 1000
                holdings_df.loc[index]['Holdings'] = total_holdings
            else:
                shares_df.loc[index]['Shares'] = 2000
                total_holdings += 2000
                holdings_df.loc[index]['Holdings'] = total_holdings
        elif (momentum_value > 0.01) and (bbp_perencet > 0.95) and (total_holdings > -1000):
            orders_df.loc[index]['Order'] = 'SELL'
            if total_holdings == 0:
                shares_df.loc[index]['Shares'] = 1000
                total_holdings -= 1000
                holdings_df.loc[index]['Holdings'] = total_holdings
            else:
                shares_df.loc[index]['Shares'] = 2000
                total_holdings -= 2000
                holdings_df.loc[index]['Holdings'] = total_holdings

    df_trades = pd.concat([symbols_df, orders_df, shares_df, holdings_df], axis=1)
    df_trades.columns = ['Symbol', 'Order', 'Shares', 'Holdings']
    return df_trades[df_trades.Shares != 0]

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
    orders_df = pd.DataFrame('BUY', index = prices_normalized_df.index, columns = ['Order'])
    symbols_df = pd.DataFrame(symbol, index = prices_normalized_df.index, columns = ['Symbol'])
    holdings_df = pd.DataFrame(0, index = prices_normalized_df.index, columns = ['Holdings'])

    number_of_entries = prices_normalized_df.shape[0]
    total_holdings = 0
    current_date = prices_normalized_df.index[0]
    shares_df.loc[current_date]['Shares'] = 1000
    df_trades = pd.concat([symbols_df, orders_df, shares_df, holdings_df], axis=1)
    df_trades.columns = ['Symbol', 'Order', 'Shares', 'Holdings']
    return df_trades


def generateSecondPlot():
    start_date = dt.datetime(2010, 1, 1)
    end_date = dt.datetime(2011, 12, 31)
    dates = pd.date_range(start_date, end_date)
    df = get_data(stock_ticker, dates)
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    normalized_df = df / df.ix[0, :]
    years = matplot_dates.YearLocator()  # every year
    months = matplot_dates.MonthLocator()  # every month
    yearsFmt = matplot_dates.DateFormatter('%Y')
    monthsFmt = matplot_dates.DateFormatter('%b')
    pd.set_option('chained_assignment', None)
    start_value = 100000
    df_trades = testPolicy(symbol="JPM", sd=start_date, ed=end_date, sv=start_value)
    portfolio_value_out = ms.compute_portvals(df_trades, start_val=start_value, commission=9.95, impact=0.005)
    portfolio_value_out.fillna(method='ffill', inplace=True)
    portfolio_value_out.fillna(method='bfill', inplace=True)
    portfolio_value_norm = portfolio_value_out / portfolio_value_out.ix[0, :]
    df_trades_benchmark_out = testPolicyBenchmark(symbol="JPM", sd=start_date, ed=end_date, sv=start_value)
    benchmark_value_out = ms.compute_portvals(df_trades_benchmark_out, start_val=start_value, commission=9.95,
                                              impact=0.005)
    benchmark_value_out.fillna(method='ffill', inplace=True)
    benchmark_value_out.fillna(method='bfill', inplace=True)
    benchmark_value_norm = benchmark_value_out / benchmark_value_out.ix[0, :]
    second_plot = portfolio_value_norm.plot(grid=True, title='Manual Strategy Out-Sample', use_index=True,
                                                color='black')
    second_plot.xaxis.set_major_locator(matplot_dates.MonthLocator())
    second_plot.xaxis.set_major_formatter(matplot_dates.DateFormatter('%b'))
    second_plot.xaxis.set_minor_locator(matplot_dates.YearLocator())
    second_plot.xaxis.set_minor_formatter(matplot_dates.DateFormatter('%Y'))
    second_plot.xaxis.set_tick_params(which='minor', pad=20)
    date_min = dt.date(df_trades.index.min().year, 1, 1)
    date_max = dt.date(df_trades.index.max().year + 1, 1, 1)
    second_plot.set_xlabel("Date")
    second_plot.set_ylabel("Normalized Portfolio Value")
    second_plot.set_xlim(date_min, date_max)
    second_plot = benchmark_value_norm.plot(grid=True, title='', use_index=True, color='blue')
    for index, row in df_trades.iterrows():
        if row['Order'] == 'BUY':
            plt.axvline(x=index, color='g', linestyle='-')
        elif row['Order'] == 'SELL':
            plt.axvline(x=index, color='r', linestyle='-')

    plt.legend(('Portfolio Value', 'Benchmark'), loc='best', prop={'size': 12})
    plt.savefig('Manual Strategy Out-Sample.png')
    plt.clf()
    plt.cla()
    plt.close()
    print "NORMALIZED OUT OF SAMPLE"
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = ms.compute_portfolio_stats(portfolio_value_norm)
    cum_ret_bench, avg_daily_ret_bench, std_daily_ret_bench, sharpe_ratio_bench = ms.compute_portfolio_stats(
        benchmark_value_norm)
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


def generate_second_plot():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    dates = pd.date_range(start_date, end_date)
    df = get_data(stock_ticker, dates)
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    normalized_df = df / df.ix[0, :]
    years = matplot_dates.YearLocator()  # every year
    months = matplot_dates.MonthLocator()  # every month
    yearsFmt = matplot_dates.DateFormatter('%Y')
    monthsFmt = matplot_dates.DateFormatter('%b')
    pd.set_option('chained_assignment', None)
    start_value = 100000
    df_trades = testPolicy(symbol="JPM", sd=start_date, ed=end_date, sv=start_value)
    portfolio_value = ms.compute_portvals(df_trades, start_val=start_value, commission=9.95, impact=0.005)
    portfolio_value.fillna(method='ffill', inplace=True)
    portfolio_value.fillna(method='bfill', inplace=True)
    portfolio_value_norm = portfolio_value / portfolio_value.ix[0, :]
    df_trades_benchmark = testPolicyBenchmark(symbol="JPM", sd=start_date, ed=end_date, sv=start_value)
    benchmark_value = ms.compute_portvals(df_trades_benchmark, start_val=start_value, commission=9.95, impact=0.005)
    benchmark_value.fillna(method='ffill', inplace=True)
    benchmark_value.fillna(method='bfill', inplace=True)
    benchmark_value_norm = benchmark_value / benchmark_value.ix[0, :]
    first_plot = portfolio_value_norm.plot(grid=True, title='Manual Strategy In-Sample', use_index=True, color='black')
    first_plot.xaxis.set_major_locator(matplot_dates.MonthLocator())
    first_plot.xaxis.set_major_formatter(matplot_dates.DateFormatter('%b'))
    first_plot.xaxis.set_minor_locator(matplot_dates.YearLocator())
    first_plot.xaxis.set_minor_formatter(matplot_dates.DateFormatter('%Y'))
    first_plot.xaxis.set_tick_params(which='minor', pad=20)
    date_min = dt.date(df_trades.index.min().year, 1, 1)
    date_max = dt.date(df_trades.index.max().year + 1, 1, 1)
    first_plot.set_xlabel("Date")
    first_plot.set_ylabel("Normalized Portfolio Value")
    first_plot.set_xlim(date_min, date_max)
    second_plot = benchmark_value_norm.plot(grid=True, title='', use_index=True, color='blue')
    for index, row in df_trades.iterrows():
        if row['Order'] == 'BUY':
            plt.axvline(x=index, color='g', linestyle='-')
        elif row['Order'] == 'SELL':
            plt.axvline(x=index, color='r', linestyle='-')
    plt.legend(('Portfolio Value', 'Benchmark'), loc='best', prop={'size': 12})
    plt.savefig('Manual Strategy In-Sample.png')
    plt.clf()
    plt.cla()
    plt.close()
    print "NORMALIZED IN SAMPLE"
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = ms.compute_portfolio_stats(portfolio_value_norm)
    cum_ret_bench, avg_daily_ret_bench, std_daily_ret_bench, sharpe_ratio_bench = ms.compute_portfolio_stats(
        benchmark_value_norm)
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


if __name__ == "__main__":
    stock_ticker = ['JPM']

    generate_second_plot()

    generateSecondPlot()