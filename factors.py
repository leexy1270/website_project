import backtrader as bt
import backtrader.indicators as btind
import math

 
#Alpha12 (sign(delta(VOLUME, 1)) * (-1 * delta(CLOSE, 1)))
class Alpha12(bt.Indicator):
    lines = ('alpha12',)
    params = (('period', 2),)

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        delta_volume = self.data.volume[0] - self.data.volume[-1]
        delta_close  = self.data.close[0] - self.data.close[-1]
        sign_delta_volume = 1 if delta_volume > 0 else (-1 if delta_volume < 0 else 0)
        self.lines.alpha12[0] = sign_delta_volume * (-1 * delta_close)

#Alpha23 (((sum(HIGH, 20) / 20) < HIGH) ? (-1 * delta(HIGH, 2)) : 0)
class Alpha23(bt.Indicator):
    lines = ('alpha23',)
    params = (('period', 20),)

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        avg_high = sum(self.data.high.get(size=self.p.period)) / self.p.period
        if avg_high < self.data.high[0]:
            delta_high = self.data.high[0] - self.data.high[-2]
            self.lines.alpha23[0] = -1 * delta_high
        else:
            self.lines.alpha23[0] = 0