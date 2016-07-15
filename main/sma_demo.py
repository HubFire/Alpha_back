# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 14:32:37 2016

@author: HUYI
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 14:04:49 2016

@author: HUYI
"""

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from  template import StrategyTemplate



class MyStrategy(StrategyTemplate):
    def __init__(self, feed, instrument):
        StrategyTemplate.__init__(self, feed,instrument)
        self.__instrument = arg1[0]
        self.__rsi = rsi.RSI(self.feed[self.__instrument].getCloseDataSeries(),14)
        self.__sma = ma.SMA(self.__rsi, arg2[0])



    def onBars(self, bars):
        # Wait for enough bars to be available to calculate a SMA.
        sma= self.__sma[-1]
        if sma is None:
            return

        #bar = bars[self.__instrument]
        price = bars[self.__instrument].getClose()
        shares=self.getBroker().getShares(self.__instrument)
        #price = bars[self.__instrument].getClose()

        if price > 1.01*sma:

            self.marketOrder(self.__instrument,shares*-1)
            self.info('SELL %i'%shares)

        if price < 0.9*sma:

            sharesToBuy=int(self.getBroker().getCash()/price)
            self.marketOrder(self.__instrument, sharesToBuy)
            self.info('BUY %d'%shares)






arg1 = ['orcl', '2008-01-01', '2016-01-01', 100000, 'day', 1]

arg2 = [5]



myStrategy=MyStrategy(arg1, arg2)
myStrategy.run()



