import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import gridspec
import numpy as np
import os
import pandas as pd

from util import get_data, plot_data

def author():
    return 'prao43'


def normalize_df(df):
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    return df/df.ix[0,:]

def compute_bollinger(symbols=['JPM'],
                      sd='2008-01-01',
                      ed='2009-12-31',
                      window=20):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(symbols, dates)
    normed_prices = normalize_df(prices_all)
    columns = ['lower', 'upper', 'band']
    bb = pd.DataFrame(0, index=normed_prices.index, columns=columns)
    bb['band'] = normed_prices.rolling(window=window, min_periods=window).std()
    sma = compute_sma(symbols, sd, ed, window)
    bb['upper'] = sma['SMA'] + (bb['band'] * 2)
    bb['lower'] = sma['SMA'] - (bb['band'] * 2)
    return bb

def compute_sma(symbols=['JPM'],
                sd='2008-01-01',
                ed='2009-12-31',
                window=20):
    """
    Simple Moving Average
    window size default of 20
    """
    dates = pd.date_range(sd, ed)
    prices_all = get_data(symbols, dates)
    normed_prices = normalize_df(prices_all)
    columns = ['SMA', 'Price/SMA']
    sma = pd.DataFrame(0, index = normed_prices.index, columns = columns)
    sma['SMA'] = normed_prices[symbols[0]].rolling(window=window,center=False).mean()
    sma['Price/SMA'] = normed_prices[symbols[0]]/sma['SMA']
    return sma

def compute_bb_percentage(bb, normed_syms, symbol):
    bb_percent = pd.DataFrame(0, index = normed_syms.index, columns =['BBP'])
    bb_percent['BBP'] = (normed_syms[symbol] - bb['lower']) / (bb['upper'] - bb['lower'])
    return bb_percent

def compute_momentum(symbols=['JPM'],
                     sd='2008-01-01',
                     ed='2009-12-31',
                     window=20):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(symbols, dates)
    normed_prices = normalize_df(prices_all)
    columns =['Momentum']
    momentum = pd.DataFrame(0, index = normed_prices[symbols[0]].index, columns = columns)
    momentum['Momentum'] = normed_prices[symbols[0]].diff(window)/normed_prices[symbols[0]].shift(window)
    return momentum

def compute_daily_returns(df):
        daily_returns = df.copy()
        daily_returns[1:] = (df[1:] / df[:-1].values) - 1
        return daily_returns

def author():
    return 'prao43'

def set_plot_values(first_plot):
    first_plot.xaxis.set_major_locator(months)
    first_plot.xaxis.set_major_formatter(monthsFmt)
    first_plot.xaxis.set_minor_locator(years)
    first_plot.xaxis.set_minor_formatter(yearsFmt)
    first_plot.xaxis.set_tick_params(which='minor', pad=20)
    sma_date_min = dt.date(sma_df.index.min().year, 1, 1)
    sma_date_max = dt.date(sma_df.index.max().year + 1, 1, 1)
    first_plot.set_xlabel("Date")
    first_plot.set_ylabel("Normalized Stock Price")
    first_plot.set_xlim(sma_date_min, sma_date_max)


if __name__ == "__main__":
    stock_ticker = ['JPM']
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,12,31)
    dates = pd.date_range(start_date, end_date)
    df = get_data(stock_ticker, dates)
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    normalized_df = df / df.ix[0, :]
    years = matplot_dates.YearLocator()  # every year
    months = matplot_dates.MonthLocator()  # every month
    yearsFmt = matplot_dates.DateFormatter('%Y')
    monthsFmt = matplot_dates.DateFormatter('%b')

    ## GET SMA
    columns_sma = ['SMA', 'Price/SMA']
    sma_df = pd.DataFrame(0, index = normalized_df.index, columns = columns_sma)
    sma_df['SMA'] = normalized_df[stock_ticker[0]].rolling(window=20, center=False).mean()
    sma_df['Price/SMA'] = normalized_df[stock_ticker[0]] / sma_df['SMA']
    sma_plot = pd.concat([normalized_df[stock_ticker[0]], sma_df['SMA'], sma_df['Price/SMA']], axis=1)
    sma_plot.columns = [stock_ticker[0], 'SMA', 'Price/SMA']
    first_plot = sma_plot.plot(grid=True, title='Simple Moving Average (SMA)', use_index=True)
    set_plot_values(first_plot)
    plt.legend((stock_ticker[0], 'SMA', 'Price/SMA', '1.05 norm line', '0.95 norm line'), loc='best', prop={'size': 8})
    plt.savefig('Prices per Simple Moving Average.png')

    ## Get BOLLINGER bands
    columns_bb = ['Lower', 'Upper', 'Deviation']
    bollinger_bands_df = pd.DataFrame(0, index=normalized_df.index, columns=columns_bb)
    bollinger_bands_df['Deviation'] = normalized_df.rolling(window=20).std()
    bollinger_bands_df['Upper'] = sma_df['SMA'] + (2 * bollinger_bands_df['Deviation'])
    bollinger_bands_df['Lower'] = sma_df['SMA'] - (2 * bollinger_bands_df['Deviation'])
    bb_plot = pd.concat([normalized_df[stock_ticker[0]], bollinger_bands_df['Lower'], bollinger_bands_df['Upper']], axis=1)
    bb_plot.columns = [stock_ticker[0], 'Lower BB', 'Upper BB']
    second_plot = bb_plot.plot(grid=True, title='Bollinger Bands', use_index=True)
    x_axis = bollinger_bands_df.index.get_level_values(0)
    second_plot.fill_between(x_axis, bollinger_bands_df['Upper'], bollinger_bands_df['Lower'], color='gray', label='Bollinger Bands', alpha=0.2)
    set_plot_values(second_plot)
    plt.savefig('Bollinger Bands for Stock.png')
    plt.clf()
    plt.cla()
    plt.close()

    ## GET SMA PERCENT
    bollinger_bands_percent_df = pd.DataFrame(0, index=normalized_df.index, columns=['Percent'])
    bollinger_bands_percent_df['Percent'] = (normalized_df[stock_ticker[0]] - bollinger_bands_df['Lower']) / (bollinger_bands_df['Upper'] - bollinger_bands_df['Lower'])
    third_plot = bollinger_bands_percent_df.plot(grid=True, title='Bollinger Bands Percentage', use_index=True)
    third_plot.legend()
    third_plot.xaxis.set_major_locator(months)
    third_plot.xaxis.set_major_formatter(monthsFmt)
    third_plot.xaxis.set_minor_locator(years)
    third_plot.xaxis.set_minor_formatter(yearsFmt)
    third_plot.xaxis.set_tick_params(which='minor', pad=20)
    percent_date_min = dt.date(bollinger_bands_percent_df.index.min().year, 1, 1)
    percent_date_max = dt.date(bollinger_bands_percent_df.index.max().year + 1, 1, 1)
    third_plot.set_xlabel("Date")
    third_plot.set_ylabel("BB Percentage")
    third_plot.set_xlim(percent_date_min, percent_date_max)
    plt.axhline(y=1.00, color='black', linestyle='--')
    plt.axhline(y=0.00, color='black', linestyle='--')
    plt.axhspan(1.00, 0.00, alpha=0.3, color='gray')
    plt.savefig('Bollinger Bands Percent for Stock.png')
    plt.clf()
    plt.cla()
    plt.close()

    ### Get Momentum
    momentum_df = pd.DataFrame(0, index=normalized_df.index, columns=['Momentum'])
    momentum_df['Momentum'] = normalized_df[stock_ticker[0]].diff(20) / normalized_df[stock_ticker[0]].shift(20)
    momentum_plot = pd.concat([normalized_df[stock_ticker[0]], momentum_df], axis=1)
    fourth_plot = momentum_plot.plot(grid=True, title='Momentum', use_index=True)
    set_plot_values(fourth_plot)
    plt.legend(('JPM', 'Momentum'), loc='best', prop={'size': 8})
    plt.savefig('Stock Momentum and Price.png', tight=True)
    plt.clf()
    plt.cla()
    plt.close()