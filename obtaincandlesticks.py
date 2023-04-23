# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 11:56:19 2023

@author: t.binen
"""

import pandas as pd
import numpy as np
#this module connects to the binance
from binance import Client
# Operation system module
import os

#Client object for getting the candlesticks
client = Client("", "")
# Type the coin name "BTCUSDT, AVAXUSDT, LTCUSDT etc...."
coin = "BTCUSDT"
# Type start date
start_date = "01 Jan, 2022"
# Type end date
end_date = "21 Apr, 2023"
#interval
interval = client.KLINE_INTERVAL_2HOUR



#Getting candles
klines = client.get_historical_klines(coin, interval , start_date, end_date)

array = np.array(klines)
candles = pd.DataFrame(array,columns=['Id','Open','High','Low','Close','Volume','Close_time','Quote_asset_volume','Number_of_trades','Taker_buy_base_asset_volume','Taker_buy_quote_asset_volume','Ignore.',])
candles = candles.iloc[:, lambda df: [0, 1, 2, 3, 4, 5]]
candles = candles[['Id','Open','Close','High','Low','Volume']]

candles = candles.astype({'Open':'float',
                             'Close':'float',
                             'High':'float',
                             'Low':'float',
                             'Volume':'float'})
candles["Volume"] = candles["Volume"] * 10000
candles['Id'] = candles['Id'].str.slice(0, 10)
candles = candles.astype({'Id':'int'})


outname = coin + "_" + start_date + "_" + end_date + "_" + interval + ".csv"
outname = outname.replace(",", "")
outname = outname.replace(" ", "_")

outdir = './raw_data'
if not os.path.exists(outdir):
    os.mkdir(outdir)

directory = os.path.join(outdir, outname)   

candles.to_csv(directory, sep=";", index=False)