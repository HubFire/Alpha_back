# -*- coding: utf-8 -*-
import pyalgotrade
from pyalgotrade import strategy
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.technical import vwap
from pyalgotrade.technical import macd
from pyalgotrade.technical import stoch
from pyalgotrade.technical import roc
from pyalgotrade.technical import atr
from pyalgotrade.technical import bollinger
from pyalgotrade.technical import cross
from pyalgotrade.technical import cumret 
from pyalgotrade.technical import highlow
from pyalgotrade.technical import hurst
from pyalgotrade.technical import linebreak
from pyalgotrade.technical import linreg
from pyalgotrade.technical import stats


args=[14,5]
def initialize(self):

    self.__rsi = rsi.RSI(self.feed[self.instrument].getCloseDataSeries(),self.args[0])
    self.__sma = ma.SMA(self.__rsi, self.args[1])



def onBars(self, bars):

    sma= self.__sma[-1]
    if sma is None:
        return

    price = bars[self.instrument].getClose()
    shares=self.getBroker().getShares(self.instrument)

    if price > 1.01*sma:
        self.marketOrder(self.instrument,shares*-1)
        self.info('SELL %i'%shares)
    if price < 0.9*sma:
        sharesToBuy=int(self.getBroker().getCash()/price)
        self.marketOrder(self.instrument, sharesToBuy)
        self.info('BUY %d'%shares)

                    
                
                
                
                
                
                
                
                