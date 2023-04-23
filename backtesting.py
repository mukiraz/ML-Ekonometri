# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 01:25:28 2023

@author: Murat Uğur KİRAZ
"""

from dataclasses import dataclass
import pandas as pd
from constants import Terms, CandleColumns, TransactionColumns as TC

@dataclass()
class TimeData:
    """
    This class contains time data.
    """
    buy_time:str = ""
    sell_time:str = ""
    operation_time:str = ""

@dataclass()
class OperationData:
    """
    This class contains operational data.
    """
    symbol:str
    candles_with_strategy:pd.DataFrame
    start_cash:float
    has_coin:bool = False
    has_cash:bool = True
    operation:str = ""
    position:str = ""

@dataclass()
class AssetAndPriceData:
    """
    This class contains asset and price data.
    """
    cash_ready:float = 0
    asset_cost:float = 0
    asset_amount:float = 0
    asset_buy_price:float = 0
    asset_sell_price:float = 0
    asset_stop_price:float = 0
    asset_operation_price:float = 0

@dataclass()
class ComissionData:
    """
    This class contains comission data.
    """
    comission_rate:float
    comission:float = 0 #comission is calculated over asset (BTC, ETH, etc.)
    comission_fee:float = 0 #comission fee is the parity value( USD, USDT,etc.)
    coin_amount_before_comission:float = 0
    coin_amount_after_comission:float = 0

@dataclass()
class TransactionsData:
    """
    This class contains transaction data.
    """
    explanation:float= ""
    total_value_of_wallet:float = 0
    df_transactions:pd.DataFrame = pd.DataFrame(columns = [
        TC.SYMBOL,
        TC.OPERATION_TIME,
        TC.OPERATION,
        TC.POSITION,
        TC.ASSET_AMOUNT,
        TC.ASSET_PRICE,
        TC.ASSET_COST,
        TC.COMISSION,
        TC.COMISSION_FEE,
        TC.ASSET_AMOUNT_AFTER_COMISSION,
        TC.STOP_PRICE,
        TC.SELL_PRICE,
        TC.WALLET_VALUE,
        TC.EXPLANATION])

@dataclass()
class MachineLearningData:
    """
    This class contains Machine Learning data.
    """
    position:str = ""
    volume:float = 0.0
    rsi:float = 0.0
    result:str = ""

class MarginCost():
    """
    This class contains the calculations of margin cost.
    """
    def __init__(self, daily_interest_rate:float, borrowed_money:float, buy_time:str, sell_time:str)->None:
        """
        The constructor initialize MarginCostData and the parameters:

        Parameters
        ----------
        daily_interest_rate : float
            Daily interest rate of the stock market
        borrowed_money : float
            The amount of money which is borrowed from stock market.
        buy_time : str
            The timestamp of start time or buy time.
        sell_time : str
            The timestamp of sell time or end time.

        Returns
        -------
        None

        """
        self.daily_interest_rate = daily_interest_rate
        self.borrowed_money = borrowed_money
        self.buy_time = buy_time
        self.sell_time = sell_time

    def calculate_hour_for_interest(self) -> int:
        """
        Calculates hour of the loaned money.
        Returns
        -------
        int
            Returns hour
        """
        start_time =  pd.Timestamp(self.buy_time)
        start_time = start_time - pd.DateOffset(minutes = start_time.minute)
        end_time =  pd.Timestamp(self.sell_time)
        end_time = end_time - pd.DateOffset(minutes = end_time.minute)
        end_time = end_time + pd.DateOffset(minutes = 60)
        time_delta = end_time - start_time
        time_delta = time_delta.seconds//3600
        return time_delta

    def calculate_interest_hourly(self) -> float:
        """
        This method calculates interest fee for borrowed money from stock market.

        Returns
        -------
        float
            Returns interest fee.

        """
        hours = self.calculate_hour_for_interest()
        return  self.borrowed_money * (self.daily_interest_rate / 24) * int(hours)

class BaseBacktesting():
    """
    This class is the base class for backtesting of an asset.
    """
    def __init__(self,
                 symbol:str,
                 candles_with_strategy:pd.DataFrame,
                 start_cash:float,
                 comission_rate:float = 0.0) ->None:
        """
        The constructor initialize Data Classes below:
            - TimeData
            - OperationData
            - AssetAndPriceData
            - ComissionData
            - TransactionData

        Parameters
        ----------
        symbol : str
            Asset symbol in stock market. "BTC, BNB, ETH etc."
        candles_with_strategy : pd.DataFrame
            he candles must contain "| Id | Open | Close | High | Low | Volume | Decision |" columns.
        start_cash : float
            The initial amount of cash for backtesting.
        comission_rate : float, optional
            Stock market's comission rate. The default is 0.0.

        Returns
        -------
        None.

        """
        self.time_data = TimeData()
        self.operation_data = OperationData(symbol, candles_with_strategy, start_cash)
        self.asset_and_price_data = AssetAndPriceData()
        self.asset_and_price_data.cash_ready = start_cash
        self.comission_data = ComissionData(comission_rate)
        self.transaction_data = TransactionsData()

    def toggle_has(self) -> None:
        """
        This function toggles has_cash and has_coin values.
        Two of them must be opposite of each other

        Returns
        -------
        None
        """
        if self.operation_data.has_cash:
            self.operation_data.has_cash = False
            self.operation_data.has_coin = True
        else:
            self.operation_data.has_cash = True
            self.operation_data.has_coin = False

    def calculate_asset_amount(self) -> None:
        """
        This function calculates the asset amount.

        Returns
        -------
        None.

        """
        self.asset_and_price_data.asset_amount = self.asset_and_price_data.cash_ready / self.asset_and_price_data.asset_buy_price

    def calculate_comission(self) -> None:
        """
        This function calculates the comission and change the coin amount.
        Stock market takes the comission fee over the asset.

        Returns
        -------
        None.

        """
        # comission is over asset. (BNB, BTC, ETH ...)
        self.comission_data.comission =  self.asset_and_price_data.asset_amount * self.comission_data.comission_rate
        self.comission_data.coin_amount_before_comission =  self.asset_and_price_data.asset_amount
        self.comission_data.coin_amount_after_comission =  self.asset_and_price_data.asset_amount - self.comission_data.comission
        self.asset_and_price_data.asset_amount = self.comission_data.coin_amount_after_comission

    def insert_transactions(self) -> None:
        """
        This function inserts data to transaction pandas dataframe.

        Returns
        -------
        None.

        """
        data = {
                TC.SYMBOL : self.operation_data.symbol,
                TC.OPERATION_TIME : self.time_data.operation_time,
                TC.OPERATION : self.operation_data.operation,
                TC.POSITION : self.operation_data.position,
                TC.ASSET_AMOUNT : self.asset_and_price_data.asset_amount,
                TC.ASSET_PRICE : self.asset_and_price_data.asset_operation_price,
                TC.ASSET_COST : self.asset_and_price_data.asset_cost,
                TC.COMISSION : self.comission_data.comission,
                TC.COMISSION_FEE : self.comission_data.comission_fee,
                TC.ASSET_AMOUNT_AFTER_COMISSION : self.comission_data.coin_amount_after_comission,
                TC.STOP_PRICE : self.asset_and_price_data.asset_stop_price,
                TC.SELL_PRICE : self.asset_and_price_data.asset_sell_price,
                TC.WALLET_VALUE : self.transaction_data.total_value_of_wallet,
                TC.EXPLANATION : self.transaction_data.explanation
                }
        new_row = pd.DataFrame(data, index=[0])
        self.transaction_data.df_transactions = pd.concat([new_row, self.transaction_data.df_transactions.loc[:]]).reset_index(drop=True)

    def prepare_to_buy(self, i:int) -> None:
        """
        This function buys asset and change parameters.

        Parameters
        ----------
        i : int
            Index of the candle dataframe row

        Returns
        -------
        None.

        """
        self.operation_data.operation = Terms.BUY #ok
        self.toggle_has() #ok
        self.time_data.operation_time = self.operation_data.candles_with_strategy[CandleColumns.ID][i+1] #ok
        self.time_data.buy_time = self.time_data.operation_time #ok
        self.asset_and_price_data.asset_buy_price = self.operation_data.candles_with_strategy[CandleColumns.CLOSE][i] #ok
        self.calculate_asset_amount() #ok
        self.calculate_comission() #ok
        # comission fee is the parity value( USD, USDT,etc.)
        self.comission_data.comission_fee = self.asset_and_price_data.asset_buy_price * self.comission_data.comission
        self.asset_and_price_data.asset_cost = self.comission_data.coin_amount_before_comission * self.asset_and_price_data.asset_buy_price
        self.asset_and_price_data.cash_ready -= self.asset_and_price_data.asset_cost #ok
        self.transaction_data.total_value_of_wallet = self.asset_and_price_data.cash_ready + self.asset_and_price_data.asset_amount * self.asset_and_price_data.asset_buy_price
        self.asset_and_price_data.asset_operation_price = self.asset_and_price_data.asset_buy_price
        self.transaction_data.explanation = "-"
        self.insert_transactions()

    def prepare_to_sell(self, i:int) -> None:
        """
        This function changes the type of operation (sell), calculates comission,
        changes the operation time parameters.
        Parameters
        ----------
        i : int
            Index of the candle dataframe row.

        Returns
        -------
        None.

        """
        self.operation_data.operation = Terms.SELL
        self.toggle_has()
        self.calculate_comission()
        self.asset_and_price_data.asset_sell_price = self.operation_data.candles_with_strategy[CandleColumns.CLOSE][i]
        self.asset_and_price_data.asset_operation_price = self.asset_and_price_data.asset_sell_price
        self.time_data.operation_time = self.operation_data.candles_with_strategy[CandleColumns.ID][i+1]
        self.time_data.sell_time = self.time_data.operation_time

    def calculate_win_rate_and_profit(self) -> tuple:
        """
        This function calculates win rate and profit percentage and returns a tuple.

        Win rate is calculated by counting "profit" and "loss" values
        which are in the explanation column of dataframe. If there is no data,
        it is calculated as zero (0)

        Profit is calculated by "total value of wallet" / "start cash."
        If there is no data, it is calculated as zero (0)

        Returns
        -------
        tuple
            First value of the tuple is "win_rate" and second one is profit.
            (win_rate, profit)
        """
        try:
            profit = self.transaction_data.df_transactions[TC.EXPLANATION].value_counts()[Terms.PROFIT]
        except KeyError:
            profit = 0
        try:
            loss = self.transaction_data.df_transactions[TC.EXPLANATION].value_counts()[Terms.LOSS]
        except KeyError:
            loss = 0

        try:
            win_rate = -(profit / (profit + loss))
        except ZeroDivisionError:
            win_rate = 0
        try:
            profit = -(self.transaction_data.total_value_of_wallet / self.operation_data.start_cash)
        except ZeroDivisionError:
            profit = 0

        return (win_rate, profit)

class LongAndShort(BaseBacktesting):
    """
    This class is used for backtesting only Long and Short operation.
    After the object instance, run run_backtest() method to get results.
    The operation is explained below:
    When "Long" or "Short" decision is satisfied, the class buys asset,
    and when is is needed to sell it sells the asset and immediately buy a
    new one.
    """
    def __init__(self, symbol:str, candles:pd.DataFrame, start_cash:float, comission_rate:float) -> None:
        """
        This constructor initialize Base class

        Parameters
        ----------
        symbol : str
            Asset symbol in stock market. "BTC, BNB, ETH etc."
        candles_with_strategy : pd.DataFrame
            he candles must contain "| Id | Open | Close | High | Low | Volume | Decision |" columns.
        start_cash : float
            The initial amount of cash for backtesting.
        comission_rate : float, optional
            Stock market's comission rate. The default is 0.0.

        Returns
        -------
        None
            DESCRIPTION.

        """
        super().__init__(symbol, candles, start_cash, comission_rate = 0.0)

    def prepare_sell_long_and_short(self, i) -> None:
        """
        Makes preparation to sell, changes asset_cost and
        asset_operation_price parameters.
        Parameters
        ----------
        i : TYPE
            Index of the candle dataframe row.

        Returns
        -------
        None.
        """
        self.prepare_to_sell(i)
        self.asset_and_price_data.asset_cost = self.asset_and_price_data.asset_sell_price * self.asset_and_price_data.asset_amount
        

    def sell_long(self, i:int) -> None:
        """
        Sells the asset in long position,
        changes cash_ready and total_value_of_wallet parameters.
        Finally inserts transactions data.

        Parameters
        ----------
        i : int
            Index of the candle dataframe row.

        Returns
        -------
        None
        """
        self.prepare_sell_long_and_short(i)

        if self.asset_and_price_data.asset_buy_price < self.asset_and_price_data.asset_sell_price:
            self.transaction_data.explanation = Terms.PROFIT
        else:
            self.transaction_data.explanation = Terms.LOSS

        self.asset_and_price_data.cash_ready += self.asset_and_price_data.asset_cost
        self.transaction_data.total_value_of_wallet = self.asset_and_price_data.cash_ready

        self.insert_transactions()

    def sell_short(self, i:int) -> None:
        """
        Sells the asset in short position,
        changes cash_ready and total_value_of_wallet parameters.
        Finally inserts transactions data.
        Parameters
        ----------
        i : int
            Index of the candle dataframe row.

        Returns
        -------
        None
        """
        self.prepare_sell_long_and_short(i)

        if self.asset_and_price_data.asset_buy_price > self.asset_and_price_data.asset_sell_price:
            #profit
            net_profit = (self.asset_and_price_data.asset_buy_price - self.asset_and_price_data.asset_sell_price) * self.asset_and_price_data.asset_amount
            self.transaction_data.total_value_of_wallet += net_profit
            self.transaction_data.explanation = Terms.PROFIT
        else:
            #loss
            net_loss = (self.asset_and_price_data.asset_sell_price - self.asset_and_price_data.asset_buy_price) * self.asset_and_price_data.asset_amount
            self.transaction_data.total_value_of_wallet -= net_loss
            self.transaction_data.explanation = Terms.LOSS

        self.asset_and_price_data.cash_ready = self.transaction_data.total_value_of_wallet
        self.asset_and_price_data.asset_cost = self.asset_and_price_data.asset_sell_price * self.asset_and_price_data.asset_amount

        self.insert_transactions()

    def run_backtest(self) -> dict:
        """
        Runs Long and Short Backtest. Buys and sells asset with the strategy
        results.

        Returns
        -------
        dict
            Returns a dictionary.
            "Out" key is the win rate and profit tuple
            "Transactions" key is the transactions dataframe

        """
        candles = self.operation_data.candles_with_strategy
        for i in range(len(candles) - 2):
            decision = candles[CandleColumns.DECISION][i]
            if self.operation_data.has_cash:
                if decision == Terms.LONG:
                    self.operation_data.position = Terms.LONG
                    self.prepare_to_buy(i)
                    continue
                if decision == Terms.SHORT:
                    self.operation_data.position = Terms.SHORT
                    self.prepare_to_buy(i)
                    continue
                continue
            if self.operation_data.has_coin:
                if decision == Terms.SHORT:
                    self.sell_long(i)
                    self.operation_data.position = Terms.SHORT
                    self.prepare_to_buy(i)
                    continue
                if decision == Terms.LONG:
                    self.sell_short(i)
                    self.operation_data.position = Terms.LONG
                    self.prepare_to_buy(i)
                    continue
                continue
            continue

        win_rate_and_profit = self.calculate_win_rate_and_profit()

        return {"Out":win_rate_and_profit,
                "Transactions": self.transaction_data.df_transactions
            }
