import numpy as np
# import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime as dt
import time
import math
import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button
import smtplib
from email.mime.text import MIMEText


def data_extractor(coin_code, start, end, interval):
    data = yf.download(coin_code, start=start, end=end, interval=str(interval)+'m')
    df = pd.DataFrame(data)
    df = df.drop(['High', 'Low', 'Close', 'Adj Close'], axis=1)
    df = df.rename(columns={'Open':'Price'})

    return df

def volatility(coin_code, df, tr, interval):
    price = df['Price']
    window = int(tr*60/interval)
    norm_std_var = price.rolling(window=window).std()/price.rolling(window=window).mean()
    df_var = pd.DataFrame(norm_std_var)

    return df_var

def derivative(coin_code, df):
    dx = df['Price'].diff()
    dx = dx/df['Price']*1000 # Standardise derivative
    dx = pd.DataFrame(dx)

    return dx

def mail_notification(coin_code, sender, receiver, message):
    msg = MIMEText(message)
    msg['Subject'] = coin_code
    msg['From'] = sender
    msg['To'] = receiver

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server: 
        server.login(sender, 'Hasi4589')
        server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
        server.quit()

#=====================================================================================#
coin = ['DOGE-USD', 'DOT1-USD', 'XRP-USD', 'BTC-USD', 'ETH-USD', 'ADA-USD', 'LTC-USD']
# coin = ['ADA-USD']

# Sell & Buy Parameters
rent = 0.015
der_thresh = -5

# params to extract data
end = dt.datetime.now()
start = end - dt.timedelta(days=0.5)
interval = 1 # minutes

# params to calculate volatility
tr_vol = 0.5 # timerange for volatility in hours

# params for Mail notification
sender = 'darios.tbot.notifier@gmail.com'
receiver = 'darios.tbot.notifier@gmail.com'

msg_thresh_derivative = 'Lower derivative threshold has been reached! \n'

while(True):
    for coin_code in coin:
        # Extract price from yahoo finance
        df = data_extractor(coin_code, start, end, interval)

        # Calculate volatility 
        df_var = volatility(coin_code, df, tr_vol, interval)
        df_var = df_var.rename(columns={'Price':'Volatility'})
        df = df.join(df_var)

        # Calculate derivative
        df_dx = derivative(coin_code, df)
        df_dx = df_dx.rename(columns={'Price':'Derivative [dp/dt]'})
        df = df.join(df_dx)


        # Send Mail notifications
        latest_derivative = df['Derivative [dp/dt]'].iloc[-1]
        if latest_derivative <=der_thresh:
            sell_price = df['Price'].iloc[-1]*(1+rent)
            msg = msg_thresh_derivative + 'Buy at:' + str(df['Price'].iloc[-1]) + '\nSell at: ' + str(sell_price) 
            mail_notification(coin_code, sender, receiver, msg)


        # Plot volatility and price
        # fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
        # ax1.plot(df['Price'])
        # ax2.plot(df['Volatility'])
        # ax3.plot(df['Derivative [dt/dp]'])
        # plt.show()

        # fig, (ax1, ax2) = plt.subplots(2, sharex=True)
        # ax1.plot(df['Price'])
        # ax2.plot(df['Derivative [dp/dt]'])
        # plt.show()

        df.to_csv((coin_code + '.csv'), index=True, header=True)
    
    time.sleep(interval*60) # in seconds



