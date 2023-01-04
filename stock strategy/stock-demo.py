#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pandas as pd
from decimal import *
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly import subplots
from datetime import datetime


# In[3]:


from alpha_vantage.timeseries import TimeSeries


# In[4]:


api_key = os.environ["MY_API_KEY"]


# In[5]:


class ScriptData:
    
    def __init__(self):
        self.stock_data = {}
        self.ts = TimeSeries(key=api_key)
    
    def __getitem__(self, stock):
        return self.stock_data[stock]
    
    def __setitem__(self, stock, df):
        self.stock_data[stock] = df
        
    def __contains__(self, stock):
        return stock in self.stock_data
    
    #fetch US Stock data in dictionary format point(a)
    def fetch_intraday_data(self, stock):
        df_data, meta_data = self.ts.get_intraday(stock)
#         self.stock_data[f"{stock}"] = df_data
        self.__setitem__(stock, df_data)
        return df_data, stock
        
    #Converts fetched intraday data (in point a.) as a pandas DataFrame
    def convert_intraday_data(self, stock):
        df = self.__getitem__(stock)
        df = pd.DataFrame(df).transpose().reset_index()
        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        
        df = df.astype({'timestamp': 'datetime64', 'open': 'float64', 'high':'float64', 'low':'float64', 'close':'float64', 'volume':'int64'})
        print(df.dtypes)
#         self.stock_data[f"{stock}"]=df
        self.__setitem__(stock, df)
        
        return df
    

#function: Moving Average of the ‘close’ column in ‘df’ of specified timeperiod    
def indicator1(df, timeperiod):
    ma_df = pd.DataFrame()
    ma_df['timestamp'] = df['timestamp']
    ma_df[f'MA{timeperiod}'] = df['close'].rolling(timeperiod).mean()
    
    return ma_df
    


# In[6]:


script_data = ScriptData()


# In[7]:


script_data.fetch_intraday_data('GOOGL')
script_data.convert_intraday_data('GOOGL')


# In[8]:


'GOOGL' in script_data


# In[9]:


script_data.fetch_intraday_data('AAPL')
script_data.convert_intraday_data('AAPL')


# In[10]:


'AAPL' in script_data


# In[11]:


'NVDA' in script_data


# In[12]:


indicator1(script_data['AAPL'], 5)


# In[13]:


indicator1(script_data['GOOGL'], timeperiod=5)


# In[14]:


class Strategy:
    
    
    def __init__(self, stock):
        self.stock = stock
        self.df = pd.DataFrame()
        
    '''Fetch intraday historical data using ScriptData class. 
    Compute indicator data on ‘close’ of ‘df’ using indicator1 function'''
    def get_script_data(self):
        self.script_data = ScriptData()
        self.script_data.fetch_intraday_data(self.stock)
        self.script_data.convert_intraday_data(self.stock)
        self.df = self.script_data[self.stock]
        self.timperiod = 5 
        self.indicator = indicator1(self.script_data[self.stock], self.timperiod)
        self.df['indicator'] = self.indicator[f'MA{self.timperiod}']
        
    #Generate a pandas DataFrame
    def get_signals(self):
        df = self.df
        df['position'] =  np.where(df['indicator']> df['close'], 1, 0)
        df['signal'] = df['position'].diff()
        df['trade_signal'] = df['signal'].replace(1.0, 'BUY').replace(-1.0, 'SELL').replace(0.0, None)
        df = self.df.dropna()
        return df[['timestamp','trade_signal']]
        
     
    #candlestick chart of ‘df and ‘indicator’ using ‘pyalgotrading’, plotly
    def plot(self):
        df = self.df
        fig = px.line(df, y=["close", 'indicator'])
        fig.show()
        fig = go.Figure(data=[go.Candlestick(
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
        fig.add_trace(go.Scatter(y=df['indicator'],
                    mode='lines',
                    name='moving_avg'))

        fig.show()


# In[15]:


strategy = Strategy('NVDA')


# In[16]:


strategy.get_script_data()


# In[17]:


strategy.get_signals()


# In[18]:


strategy.plot()


# In[ ]:




