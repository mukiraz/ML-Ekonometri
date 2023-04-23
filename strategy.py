# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 16:26:43 2023

@author: Murat Ugur KIRAZ

"""

from constants import Terms, CandleColumns
from numpy import nan
import pandas as pd
from indicators import Indicators as Ind
from candleshaping import CandleShaping as CS


class Strategy():

    def __init__(self, candles):
        self.candles = candles

    def crossOver(self, signal1, signal2):
        position = False
        decision = []
        for i in range(len(signal1)):
            if signal1[i] > signal2[i]:
                if position == False :
                    decision.append(Terms.LONG)
                    position = True
                else:
                    decision.append(nan)
            elif signal1[i] < signal2[i]:
                if position == True:
                    decision.append(Terms.SHORT)
                    position = False
                else:
                    decision.append(nan)
            else:
                decision.append(nan)
        decisionSignal = {CandleColumns.DECISION:decision}
        return pd.DataFrame(decisionSignal)

    def deleteFirstSignal(self, decison_signal):
        long_index = decison_signal[decison_signal.Decision == Terms.LONG].first_valid_index()
        short_index = decison_signal[decison_signal.Decision == Terms.SHORT].first_valid_index()
        if long_index < short_index:
            decison_signal.at[long_index, CandleColumns.DECISION] = nan
        else:
            decison_signal.at[short_index, CandleColumns.DECISION] = nan
        return decison_signal

    def MACDStrategyOnly(self, MACDslow:int, MACDfast:int, MACDsignal:int):
        try:
            MACD = Ind(self.candles).get_macd(slow = MACDslow, fast = MACDfast, signal =MACDsignal)
            candles = CS.to_date_time(self.candles)
            decisionSignal = self.crossOver(MACD[Terms.MACD], MACD[Terms.SIGNAL])
            CMF = Ind(self.candles).get_cmf()
            RSI = Ind(self.candles).get_rsi()
            #decisionSignal = self.deleteFirstSignal(decisionSignal)
            cand = CS.insert_signal_to_df(candles, MACD, CMF, RSI, decisionSignal)
            return cand

        except Exception as e:
            print(f"An error occured, error code{e}")

    def MACDStrategy(self, macd_slow:int, macd_fast:int, macd_signal:int, atr_period:int, atr_multiplier_upper:float, atr_multiplier_lower:float):
        try:
            MACD = Ind(self.candles).get_macd(slow = macd_slow, fast = macd_fast, signal = macd_signal)
            atrBands = Ind(self.candles).get_atr_bands(atr_period = atr_period, 
                                                     atr_multiplier_upper = atr_multiplier_upper, 
                                                     src_upper = CandleColumns.CLOSE, 
                                                     atr_multiplier_lower = atr_multiplier_lower, 
                                                     src_lower = CandleColumns.CLOSE)
            candles = CS.to_date_time(self.candles)
            decisionSignal = self.crossOver(MACD[Terms.MACD], MACD[Terms.SIGNAL])
            cand = CS.insert_signal_to_df([candles, MACD, atrBands, decisionSignal])
            cand.rename(columns={'CMF_20': Terms.CMF})
            return cand
        except Exception as e:
            print(f"An error occured, error code{e}")
