import pandas as pd
import numpy as np
from strategy import Strategy
from backtesting import LongAndShort as LAS

candles = pd.read_csv("raw_data/BTCUSDT_01_Jan_2022_21_Apr_2023_2h.csv", sep=";")

strategy = Strategy(candles)
candles = strategy.MACDStrategyOnly(MACDslow=26, MACDfast=12, MACDsignal=9)

candles.to_csv("w_decision.csv")

backtesting = LAS("BTC", candles, 10000, 0).run_backtest()
backtesting["Transactions"].to_csv("transactions.csv", sep=";")