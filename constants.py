# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 04:34:34 2023

@author: Murat Ugur KIRAZ
"""
from enum import Enum


class Terms(Enum):
    """
    This class contains the Terms constants.
    """
    RESISTENCE = "resistence"
    SUPPORT = "support"
    BUY = "buy"
    SELL = "sell"
    LONG = "long"
    SHORT = "short"
    PROFIT = "profit"
    LOSS = "loss"
    MACD = "MACD"
    SIGNAL = "signal"
    HISTOGRAM = "histogram"
    CMF = "CMF"
    RSI = "RSI"

class CandleColumns(Enum):
    """
    This class contains the Candle Columns constants.
    """
    ID = "Id"
    OPEN = "Open"
    CLOSE = "Close"
    LOW = "Low"
    HIGH = "High"
    VOLUME = "Volume"
    HL2 = "HL2"
    HLC3 = "HLC3"
    OHCL4 = "OHCL4"
    HLCC4 = "HLCC4"
    DECISION = "Decision"

class TransactionColumns(Enum):
    """
    This class contains the Transaction Columns constants.
    """
    SYMBOL = "symbol"
    OPERATION_TIME = "operation_time"
    OPERATION = "operation"
    POSITION = "position"
    ASSET_AMOUNT = "asset_amount"
    ASSET_PRICE = "asset_operation_price"
    ASSET_COST = "asset_cost"
    COMISSION = "comission"
    COMISSION_FEE = "comission_fee"
    ASSET_AMOUNT_AFTER_COMISSION = "coin_amount_after_comission"
    STOP_PRICE = "asset_stop_price"
    SELL_PRICE = "asset_sell_price"
    WALLET_VALUE = "total_value_of_wallet"
    EXPLANATION = "explanation"
