import datetime as dt
import pandas as pd

import marketsimcode as msc
import ManualStrategy as ms
import StrategyLearner as sl

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def author():
    return 'prao43'

def normalize_stocks(df):
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    return df/df.ix[0,:]

if __name__ == "__main__":
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    commission = 0.0
    impact = 0.0
    strategy_learner = sl.StrategyLearner(verbose = False, impact=impact)
    strategy_learner.addEvidence(symbol = "JPM", sd=sd, ed=ed, sv=sv)
    trades_df = strategy_learner.testPolicyWithAdditionalStats(symbol ="JPM", sd=sd, ed=ed, sv=sv)

    portvals_sl = msc.compute_portvals(trades_df, start_val = sv, commission=commission, impact=impact)
    df_trades_ms = ms.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = sv)
    portvals_ms = msc.compute_portvals(df_trades_ms, start_val = sv, commission=commission, impact=impact)

    benchmark = ms.testPolicyBenchmark(symbol="JPM", sd=sd, ed=ed, sv=sv)
    portvals_benchmark = msc.compute_portvals(benchmark, start_val=sv, commission=commission, impact=impact)


    normed_prices_benchmark = normalize_stocks(portvals_benchmark)
    normed_prices_ms = normalize_stocks(portvals_ms)
    normed_prices_sl = normalize_stocks(portvals_sl)
    chart_df = pd.concat([normed_prices_ms, normed_prices_benchmark, normed_prices_sl], axis=1)
    chart_df.columns = ['Manual Strategy', 'Benchmark', 'Strategy Learner']
    f1 = chart_df.plot(grid=True, title='Manual Strategy vs Strategy Learner', use_index=True,
                       color=['Black', 'Blue', 'Green'])
    f1.xaxis.set_major_locator(mdates.MonthLocator())
    f1.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    f1.xaxis.set_minor_locator(mdates.YearLocator())
    f1.xaxis.set_minor_formatter(mdates.DateFormatter('%Y'))
    f1.xaxis.set_tick_params(which='minor', pad=10)
    datemin = dt.date(normed_prices_benchmark.index.min().year, 1, 1)
    datemax = dt.date(normed_prices_benchmark.index.max().year + 1, 1, 1)
    f1.set_xlabel("Time (Date)")
    f1.set_ylabel("Normalized Portfolio Value")
    f1.set_xlim(datemin, datemax)

    cum_ret_sl, avg_daily_ret_sl, std_daily_ret_sl, sharpe_ratio_sl = msc.compute_portfolio_stats(normed_prices_sl)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = msc.compute_portfolio_stats(normed_prices_ms)
    cum_ret_bmk, avg_daily_ret_bmk, std_daily_ret_bmk, sharpe_ratio_bmk = msc.compute_portfolio_stats(normed_prices_benchmark)
    print"Sharpe Ratio Strategy Learner:{}".format(sharpe_ratio_sl)
    print"Sharpe Ratio Manual Strategy:{}".format(sharpe_ratio)
    print"Sharpe Ratio Benchmark:{}".format(sharpe_ratio_bmk)

    print"Cum Return Strategy Learner:{}".format(cum_ret_sl)
    print"Cum Return Manual Strategy:{}".format(cum_ret)
    print"Cum Return Benchmark:{}".format(cum_ret_bmk)

    print"Std Dev Strategy Learner:{}".format(std_daily_ret_sl)
    print"Std Dev Manual Strategy:{}".format(std_daily_ret)
    print"Std Dev Benchmark:{}".format(std_daily_ret_bmk)

    print"Avg Daily Ret Strategy Learner:{}".format(avg_daily_ret_sl)
    print"Avg Daily Ret Manual Strategy:{}".format(avg_daily_ret)
    print"Avg Daily Ret Benchmark:{}".format(avg_daily_ret_bmk)
    print"Strategy Learner,{},{},{},{},{}".format(sharpe_ratio_sl, cum_ret_sl, std_daily_ret_sl, avg_daily_ret_sl, trades_df.shape[0])
    print"Manual Strategy,{},{},{},{},{}".format(sharpe_ratio, cum_ret, std_daily_ret, avg_daily_ret,df_trades_ms.shape[0])
    print"Benchmark,{},{},{},{},1".format(sharpe_ratio_bmk, cum_ret_bmk, std_daily_ret_bmk, avg_daily_ret_bmk)
    plt.savefig("experiment1.png")
    plt.show()