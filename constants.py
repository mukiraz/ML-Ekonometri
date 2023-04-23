# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 04:34:34 2023

@author: Murat Ugur KIRAZ
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Terms:
    RESISTENCE:str = "resistence"
    SUPPORT:str = "support"
    BUY:str = "buy"
    SELL:str = "sell"
    LONG:str = "long"
    SHORT:str = "short"
    PROFIT:str = "profit"
    LOSS:str = "loss"
    MACD:str = "MACD"
    SIGNAL:str = "signal"
    HISTOGRAM:str = "histogram"
    CMF:str = "CMF"
    RSI:str = "RSI"

@dataclass(frozen=True)
class CandleColumns:
    ID:str = "Id"
    OPEN:str = "Open"
    CLOSE:str = "Close"
    LOW:str = "Low"
    HIGH:str = "High"
    VOLUME:str = "Volume"
    HL2:str = "HL2"
    HLC3:str = "HLC3"
    OHCL4:str = "OHCL4"
    HLCC4:str = "HLCC4"
    DECISION:str = "Decision"

@dataclass(frozen = True)
class TransactionColumns:
    SYMBOL:str = "symbol"
    OPERATION_TIME:str = "operation_time"
    OPERATION:str = "operation"
    POSITION:str = "position"
    ASSET_AMOUNT:str = "asset_amount"
    ASSET_PRICE :str = "asset_operation_price"
    ASSET_COST:str = "asset_cost"
    COMISSION:str = "comission"
    COMISSION_FEE:str = "comission_fee"
    ASSET_AMOUNT_AFTER_COMISSION:str = "coin_amount_after_comission"
    STOP_PRICE:str = "asset_stop_price"
    SELL_PRICE:str = "asset_sell_price"
    WALLET_VALUE:str = "total_value_of_wallet"
    EXPLANATION:str = "explanation"
