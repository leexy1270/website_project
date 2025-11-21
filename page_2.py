import streamlit as st
import pandas as pd
import numpy as np
import backtrader as bt
import backtrader.indicators as btind
from factors import Alpha12, Alpha23
import os
import matplotlib.pyplot as plt
st.title('Factor Strategy Backtest')
cerebro = bt.Cerebro()  
cerebro.broker.setcash(100000.0)

#信息


#数据加载选项
all_data=st.checkbox('是否加载全部数据(不建议)',value=False)
path='300stock_price'
list_of_files = os.listdir(path)
if not all_data:
    list_of_files = list_of_files[-20 :]
else:
    pass
for i in list_of_files:
    df=bt.feeds.PandasData(dataname=pd.read_csv(f'300stock_price\\\\{i}', index_col=0, parse_dates=True))
    cerebro.adddata(df,name=i.split('.')[0])

option=st.selectbox('factor',options=['Alpha12','Alpha23'],index=0)

if option=='Alpha12':
    Alpha=Alpha12
if option=='Alpha23':
    Alpha=Alpha23

class factor_strategy(bt.Strategy):
    params=(('rebalance_days',5),)

    def __init__(self):
        self.days = 0
        self.alpha_dict = {d._name: Alpha(d) for d in self.datas}
        self.rets = []
        self.values=[]
        self.n = len(self.datas) // 10
    

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')

    def next(self):
        
        self.days+=1
        # 当前总资产
        value_now = self.broker.getvalue()
        self.values.append(value_now)

        # 计算 daily return
        if len(self.values) > 1:
            ret = (self.values[-1] - self.values[-2]) / self.values[-2]
            self.rets.append(ret)
        else:
            self.rets.append(0)

    
        if self.days % self.p.rebalance_days != 0:
            return 
        if len(self.datas[0])>self.datas[0].buflen()-self.p.rebalance_days:
            return
        
        for d in self.datas:
            self.close(data=d)

        sorted_factors=sorted(self.alpha_dict.keys(),key=lambda x:x[1][0])

       
        long_stocks = sorted_factors[:self.n]
        short_stocks = sorted_factors[-self.n:]

        for stock in long_stocks:
            self.buy(data=self.getdatabyname(stock),size=1000)


cerebro.addstrategy(factor_strategy)
with st.spinner("Running backtest...",show_time=True):
    result = cerebro.run()[0]     # 获取策略实例
    returns = result.rets         # 策略内部记录的日收益

    #
    value=cerebro.broker.getvalue()
    st.write(f'{option}\'sFinal Portfolio Value: {value:.2f}')

    # 计算并绘制累计收益曲线
    cum_ret = np.cumsum(np.array(returns))
    plt.plot(cum_ret)
    plt.title(f"{option} Returns")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Return")
    st.pyplot(plt)
