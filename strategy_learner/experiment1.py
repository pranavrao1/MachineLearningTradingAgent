import datetime as dt
import pandas as pd
import numpy as np
import util as ut

import QLearner as ql
import marketsimcode
import ManualStrategy as ms
import indicators as ind
import StrategyLearner as sl

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def author():
    return 'prao43'

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
monthsFmt = mdates.DateFormatter('%b')

if __name__ == "__main__":
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    commission = 0.0
    impact = 0.0
    strategy_learner = sl.StrategyLearner(verbose = False, impact=impact)
    strategy_learner.addEvidence(symbol = "JPM", sd=sd, ed=ed, sv=sv)
    partial_df_trades_sl = strategy_learner.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv=sv)
    df_trades_sl = strategy_learner.tp_df_trades()
    #print df_trades_sl
    print df_trades_sl.shape[0]
    portvals_sl = marketsimcode.compute_portvals(df_trades_sl, start_val = sv, commission=commission, impact=impact)
    df_trades_ms = ms.testPolicy(symbol = "JPM", sd=sd, ed=ed, sv = sv)
    portvals_ms = marketsimcode.compute_portvals(df_trades_ms, start_val = sv, commission=commission, impact=impact)

    benchmark = ms.benchmarkPolicy(symbol="JPM", sd=sd, ed=ed, sv=sv)
    portvals_benchmark = marketsimcode.compute_portvals(benchmark, start_val=sv, commission=commission, impact=impact)