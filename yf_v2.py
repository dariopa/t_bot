import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime as dt
import math
import matplotlib.pyplot as plt


def interval_60_days(coin_code, start, end, interval):

    data = yf.download(coin_code, start=start, end=end, interval=interval)
    df = pd.DataFrame(data)

    df = df.drop(['High', 'Low', 'Close', 'Adj Close'], axis=1)
    df = df.rename(columns={'Open':'Price'})

    return df

def vol(coin_code, df, tr):
    price = df['Price']
    window = int(round(tr*60,0)/2)
    norm_std_var = price.rolling(window=window).std()/price.rolling(window=window).mean()
    norm_std_var = pd.DataFrame(norm_std_var)
    # norm_std_var = norm_std_var.rename(columns={'':'st std var'})
    df.append(norm_std_var)
    print(df)
    return df



#=====================================================================================#
# coin = ['DOGE-USD', 'DOT1-USD', '^XRPLX', 'BTC-USD', 'ETH-USD', 'ADA-USD', 'LTC-USD']
coin = ['DOGE-USD']#, 'DOT1-USD']

# params to extract data
end = dt.datetime.now()
start = end - dt.timedelta(days=60)
interval = '2m'

# params to calculate volatility
tr_st_vol = 0.167 # timerange for short-term volatility in hours
tr_mt_vol = 24 # timerange for mid-term volatility in hours
tr_lt_vol = 168 # timerange for long-term volatility in hours


for coin_code in coin:
    df = interval_60_days(coin_code, start, end, interval)
    vol(coin_code, df, tr_st_vol)
    # df.to_csv((coin_code + '.csv'), index=True, header=True)



