
import datetime as dt
import pandas as pd
import marketsimcode
import ManualStrategy as ms
import StrategyLearner as sl

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def normalize_stocks(df):
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    return df/df.ix[0,:]

def author():
    return 'prao43'

if __name__ == "__main__":
    impact_list = [0.25, 0.05, 0.005, 0.001, 0]
    colors = ["red", "blue", "green", "orange", "yellow"]
    symbol = "JPM"
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,1,1)
    sv = 100000
    impact_data = []
    for i in range(5):
        strategy_learner = sl.StrategyLearner(verbose=False, impact=impact_list[i])
        strategy_learner.addEvidence(symbol=symbol)
        trades_df_sl = strategy_learner.testPolicyWithAdditionalStats(symbol="JPM", sd=sd, ed=ed, sv=sv)
        portvals_sl = marketsimcode.compute_portvals(trades_df_sl, start_val=sv, commission=0.0, impact=impact_list[i])

        df_trades_ms = ms.testPolicy(symbol=symbol, sd=sd, ed=ed, sv=sv)
        portvals_ms = marketsimcode.compute_portvals(df_trades_ms, start_val=sv, commission=0.0, impact=impact_list[i])
        benchmark = ms.testPolicyBenchmark(symbol=symbol, sd=sd, ed=ed, sv=sv)
        portvals_benchmark = marketsimcode.compute_portvals(benchmark, start_val=sv, commission=0.0,impact=impact_list[i])

        normed_prices_benchmark = normalize_stocks(portvals_benchmark)
        normed_prices_ms = normalize_stocks(portvals_ms)
        normed_prices_sl = normalize_stocks(portvals_sl)
        chart_df = pd.concat([normed_prices_ms, normed_prices_benchmark, normed_prices_sl], axis=1)
        chart_df.columns = ['Manual Strategy', 'Benchmark', 'Strategy Learner']
        f1 = chart_df.plot(grid=True, title='Manual Strategy vs Strategy Learner, Impact={}'.format(impact_list[i]),use_index=True, color=['Black', 'Blue', 'Green'])
        f1.xaxis.set_major_locator(mdates.MonthLocator())
        f1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        f1.xaxis.set_minor_locator(mdates.YearLocator())
        f1.xaxis.set_minor_formatter(mdates.DateFormatter('%Y'))
        f1.xaxis.set_tick_params(which='minor', pad=10)
        datemin = dt.date(normed_prices_benchmark.index.min().year, 1, 1)
        datemax = dt.date(normed_prices_benchmark.index.max().year + 1, 1, 1)
        f1.set_xlabel("Date")
        f1.set_ylabel("Normalized Portfolio Value")
        f1.set_xlim(datemin, datemax)
        plt.savefig('experiment2_impact{}.png'.format(impact_list[i]))
        plt.clf()
        plt.cla()
        plt.close()
        impact_data.insert(i,normalize_stocks(portvals_sl))

    chart_df = pd.concat(impact_data,axis=1)
    chart_df.columns = ['Impact 0.2', 'Impact 0.05', 'Impact 0.005', 'Impact 0.001', 'Impact 0.0']
    f1 = chart_df.plot(grid=True, title='Strategy Learner Impacts', use_index=True, color=colors)
    f1.xaxis.set_tick_params(which='minor', pad=20)
    datemin = dt.date(impact_data[4].index.min().year, 1, 1)
    datemax = dt.date(impact_data[4].index.max().year + 1, 1, 1)
    f1.set_xlabel("Date")
    f1.set_ylabel("Normalized Portfolio Value")
    f1.set_xlim(datemin, datemax)
    plt.savefig('experiment2.png')
    plt.show()
