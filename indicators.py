# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 16:27:28 2023

@author: t.binen
"""

import pandas as pd
import pandas_ta as ta
from constants import Terms, CandleColumns

class Indicators():
    """
    The indicators are calculated by pandas_ta library. The documentation is below:

    https://github.com/twopirllc/pandas-ta

    In this class, the undefined indicators in pandas_ta are defined.

    """

    def __init__(self, candles:pd.DataFrame):
        self.candles = candles

    def __get_close(self):
        return self.candles[CandleColumns.CLOSE.value]

    def __get_open(self):
        return self.candles[CandleColumns.OPEN.value]

    def __get_high(self):
        return self.candles[CandleColumns.HIGH.value]

    def __get_low(self):
        return self.candles[CandleColumns.LOW.value]

    def __get_hl2(self):
        series = (self.candles[CandleColumns.HIGH.value] + self.candles[CandleColumns.LOW.value]) / 2
        return pd.Series(series)

    def __get_hlc3(self):
        series = (self.candles[CandleColumns.HIGH.value] + self.candles[CandleColumns.LOW.value] + self.candles[CandleColumns.CLOSE.value]) / 3
        return pd.Series(series)

    def __get_ohlc4(self):
        series = (self.candles[CandleColumns.OPEN.value] + self.candles[CandleColumns.HIGH.value]  + self.candles[CandleColumns.CLOSE.value] + self.candles[CandleColumns.LOW.value] ) / 4
        return pd.Series(series)

    def __get_hlcc4(self):
        series = (self.candles[CandleColumns.HIGH.value] + self.candles[CandleColumns.LOW.value] + self.candles[CandleColumns.CLOSE.value] + self.candles[CandleColumns.CLOSE.value]) / 4
        return pd.Series(series)

    def source(self, source:CandleColumns):
        """
        This method is used for source parameter of an indicator.

        Parameters
        ----------
        source : Source class from constant module
                OPEN, CLOSE, LOW, HIGH, HL2, HLC3, OHLC4, HLCC4
                HL2 = (High + Low) / 2
                HLC3 = (High + Low + Close) / 3
                OHLC4 = (Open + High + Low + Close) / 4
                HLCC4 = (High + Low + Close + Close) / 4
        Returns
        -------
        TYPE Series object of pandas.core.series
            It returns a pandas series with one column.

        """
        source_dictionary = {
            CandleColumns.CLOSE.value : self.__get_close(),
            CandleColumns.OPEN.value : self.__get_open(),
            CandleColumns.HIGH.value : self.__get_high(),
            CandleColumns.LOW.value : self.__get_low(),
            CandleColumns.HL2.value : self.__get_hl2(),
            CandleColumns.HLC3.value : self.__get_hlc3(),
            CandleColumns.OHCL4.value : self.__get_ohlc4(),
            CandleColumns.HLCC4.value : self.__get_hlcc4()
            }

        return source_dictionary[source]

    def get_atr_bands(self, atr_period : int =3,
                      atr_multiplier_upper : float = 2.5,
                      src_upper:CandleColumns = CandleColumns.CLOSE.value,
                      atr_multiplier_lower : float = 2.5,
                      src_lower :CandleColumns = CandleColumns.CLOSE.value):
        """
        This function establishes ATR bands.

        Parameters
        ----------
        atrPeriod : int, optional
            DESCRIPTION. The default is 3.
        atrMultiplierUpper : float, optional
            DESCRIPTION. The default is 2.5.
        srcUpper : Source, optional
            DESCRIPTION. The default is Source.CLOSE.
        atrMultiplierLower : float, optional
            DESCRIPTION. The default is 2.5.
        srcLower : Source, optional
            DESCRIPTION. The default is Source.CLOSE.

        Returns
        -------
        df : TYPE
            DESCRIPTION.

        """
        atr = self.candles.ta.atr(atr_period)
        atr_upper = self.source(src_upper) + atr * atr_multiplier_upper
        atr_lower = self.source(src_lower) - atr * atr_multiplier_lower
        atr_bands = {Terms.RESISTENCE.value:atr_upper,
                    Terms.SUPPORT.value:atr_lower}
        return pd.DataFrame(atr_bands, index=None)

    def get_rsi(self, length:int = 14) -> pd.DataFrame:
        """
        This method returns RSI signal

        Parameters
        ----------
        length : int, optional
            DESCRIPTION. The default is 14.

        Returns
        -------
        TYPE pandas dataframe
            RSI signal

        """
        rsi = self.candles.ta.rsi(length = length)
        arr = rsi.to_numpy()
        return pd.DataFrame(arr, columns=[Terms.RSI.value])

    def get_macd(self,  slow: int = 26, fast: int = 12, signal: int = 9, fillna: bool = False)  -> pd.DataFrame:
        """
        This method returns MACD signal.

        Parameters
        ----------
        slow : int, optional
            DESCRIPTION. The default is 26.
        fast : int, optional
            DESCRIPTION. The default is 12.
        signal : int, optional
            DESCRIPTION. The default is 9.
        fillna : bool, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        TYPE pandas dataframe
        signals :
            Returns 3 signals. MACD, Signal, Histogram

        """
        signals = self.candles.ta.macd(slow, fast, signal, fillna)
        signals.columns.values[0] = Terms.MACD.value
        signals.columns.values[1] = Terms.HISTOGRAM.value
        signals.columns.values[2] = Terms.SIGNAL.value
        return signals

    def get_cmf(self)  -> pd.DataFrame:
        """
        This method returns CMF (Chaikin Money Flow) indicator.

        Returns
        -------
        TYPE pandas dataframe
            Returns CMF signal

        """
        return self.candles.ta.cmf().rename(Terms.CMF.value)
