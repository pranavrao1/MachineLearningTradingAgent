import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as matplot_dates
import matplotlib.ticker as mticker
from matplotlib import gridspec
import numpy as np
import os
import pandas as pd

from util import get_data, plot_data

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
    plt.axhline(y=1.05, color='r', linestyle='-')
    plt.axhline(y=0.95, color='g', linestyle='-')
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
    second_plot.xaxis.set_major_locator(months)
    second_plot.xaxis.set_major_formatter(monthsFmt)
    second_plot.xaxis.set_minor_locator(years)
    second_plot.xaxis.set_minor_formatter(yearsFmt)
    second_plot.xaxis.set_tick_params(which='minor', pad=20)
    bollinger_band_date_min = dt.date(bollinger_bands_df.index.min().year, 1, 1)
    bollinger_date_max = dt.date(bollinger_bands_df.index.max().year + 1, 1, 1)
    second_plot.set_xlabel("Date")
    second_plot.set_ylabel("Normalized Stock Price")
    second_plot.set_xlim(bollinger_band_date_min, bollinger_date_max)
    second_plot.set_xlabel("Date")
    second_plot.set_ylabel("Normalized Stock Price")
    second_plot.set_xlim(bollinger_band_date_min, bollinger_date_max)
    plt.savefig('Bollinger Bands for Stock.png')

    ### Get Momentum
    momentum_df = pd.DataFrame(0, index=normalized_df.index, columns=['JPM', 'Momentum'])
    momentum_df['Momentum'] = normalized_df[stock_ticker[0]].diff(20) / normalized_df[stock_ticker[0]].shift(20)
    momentum_plot = pd.concat([normalized_df[stock_ticker[0]], momentum_df], axis=1)
    third_plot = momentum_plot.plot(grid=True, title='Momentum', use_index=True)
    third_plot.xaxis.set_major_locator(months)
    third_plot.xaxis.set_major_formatter(monthsFmt)
    third_plot.xaxis.set_minor_locator(years)
    third_plot.xaxis.set_minor_formatter(yearsFmt)
    third_plot.xaxis.set_tick_params(which='minor', pad=20)
    datemin = dt.date(momentum_df.index.min().year, 1, 1)
    datemax = dt.date(momentum_df.index.max().year + 1, 1, 1)
    third_plot.set_xlabel("Date")
    third_plot.set_ylabel("Normalized Stock Price")
    third_plot.set_xlim(datemin, datemax)
    plt.savefig('Stock Momentum and Price.png', tight=True)

    pass