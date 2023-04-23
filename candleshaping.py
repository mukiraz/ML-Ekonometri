# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 10:00:27 2023

@author:Murat Ugur KIRAZ

"""

import pandas as pd
from constants import CandleColumns

class CandleShaping:
    """
    This class shapes the candles.
    """

    @staticmethod
    def make_candle_dataframe(id_column,
                              open_column,
                              close_column,
                              high_column,
                              low_column,
                              volume_column) -> pd.DataFrame:
        """
        Parameters
        ----------
        Id : TYPE Array
             This is the time data, it is used for Id.
        Open : TYPE Array
             This is the Open value of the candlestick data.
        Close : TYPE Array
            This is the Close value of the candlestick data.
        High : TYPE Array
            This is the High value of the candlestick data.
        Low : TYPE Array
            This is the Low value of the candlestick data.
        Volume : TYPE Array
            his is the Volume value of the candlestick data.

        Returns
        -------
        TYPE Pandas dataframe.
           This method gets the candlestick data in array and returns a pandas dataframe.
        """

        #Here we are creating a dictionary for the DataFrame
        candles = {
            CandleColumns.ID : id_column,
            CandleColumns.OPEN : open_column,
            CandleColumns.CLOSE : close_column,
            CandleColumns.HIGH :high_column,
            CandleColumns.LOW : low_column,
            CandleColumns.VOLUME : volume_column
            }
        #Cconverting dictionary to dataframe
        candles = pd.DataFrame(candles, index=None)
        #Sorting dataframe.
        candles = candles.sort_values(by=[CandleColumns.ID])

        return candles.reset_index(drop=True)

    @staticmethod
    def convert_to_float(candles:pd.DataFrame) -> pd.DataFrame :
        """
        This method converts string values of candles dataframe into float.

        Parameters
        ----------
        candles : TYPE
            pandas dataframe containing the candle values. (Id, Open, Close, High, Low, Volume)

        Returns
        -------
        df : TYPE
            pandas dataframe containing the candle values. (Id, Open, Close, High, Low, Volume)

        """
        return candles.astype({CandleColumns.OPEN:'float',
                             CandleColumns.CLOSE:'float',
                             CandleColumns.HIGH:'float',
                             CandleColumns.LOW:'float',
                             CandleColumns.VOLUME:'float'})

    @staticmethod
    def to_date_time(candles:pd.DataFrame):
        """
        This method converts the integer milisecond values of the Id column of candles into timestamp value.

        Parameters
        ----------
        candles : TYPE
            pandas dataframe containing the candle values. (Id, Open, Close, High, Low, Volume)

        Returns
        -------
        candles : TYPE
            pandas dataframe containing the candle values. (Id, Open, Close, High, Low, Volume)

        """
        candles.astype({'Id':'int'})
        candles["Id"] = pd.to_datetime(candles['Id'], unit='s')
        candles.Id = candles.Id + pd.Timedelta('02:00:00')
        return candles

    @staticmethod
    def insert_signal_to_df(*args) -> pd.DataFrame:
        """

        Parameters
        ----------
        *args : TYPE list
            DESCRIPTION
            List of the signals and candles
            USAGE insert_signal_to_df([candles,rsi,macd,bollinger])

        Returns
        -------
        df : TYPE pandas dataframe
            DESCRIPTION
            Returns the added signals.

        """
        return pd.concat(args, axis=1, join='inner')
