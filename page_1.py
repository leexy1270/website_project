import streamlit as st
import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
import plotly.graph_objects as go


import backtrader as bt
import backtrader.indicators as btind

st.title('BACKTEST WEB')

# reach data with cache
@st.cache_data
def get_data(symbol=None):
    d=ak.stock_zh_a_hist_tx(symbol=symbol,start_date='20200101',end_date='20240601')
    d=d.rename(columns={'date':'datetime','open':'open','close':'close','high':'high','low':'low','amount':'volume'})
    d['datetime']=pd.to_datetime(d['datetime'])
    d.set_index('datetime',inplace=True)
    return d

#参数
stock_code=st.text_input('输入股票代码',value='sz000001',placeholder='sz000001')
st.write('输入的股票代码为：',stock_code)
#start=st.date_input('输入起始日期',value='2025-01-01')
#end=st.date_input('输入截止日期',value='today')
#period=st.selectbox('选择周期',options=['daily','weekly','monthly'],index=0)
try:
    df=get_data(stock_code)
    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close']
    )])
    st.write(fig)
except ValueError:
    st.write("无法获取数据，请检查股票代码是否正确。")



class AStratege(bt.Strategy):
    def log(self,txt,dt=None):
        dt=  dt or self.datas[0].datetime.date(0)
        print('%s,%s'%(dt.isoformat(),txt))

    def __init__(self):
        self.dataclose=self.datas[0].close
        self.order=None
        self.bar_executed=0
        self.sma=btind.SimpleMovingAverage(self.datas[0],period=15)

    def next(self):
        if self.order:
            return
        
        if not self.position:
            if self.dataclose[0]<self.dataclose[-1]:
                if self.dataclose[-1]<self.dataclose[-2]:
                    self.log('BUY CREATE,%.2f'%self.dataclose[0])
                    self.order=self.buy()
        else:
            if len(self)>=(self.bar_executed+5):
                self.log('SELL CREATE,%.2f'%self.dataclose[0])
                self.order=self.sell()

    def notify_order(self,order):
        if order.status in [order.Submitted,order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED,%.2f'%order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED,%.2f'%order.executed.price)
            
            self.bar_executed=len(self)

        elif order.status in [order.Canceled,order.Margin,order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')  
        
        self.order=None

data=bt.feeds.PandasData(dataname=df)
cerebro=bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(AStratege)
cerebro.broker.setcash(100000.0)
cerebro.run()
value=cerebro.broker.getvalue()
st.write('回测结束，当前总资金：',value)