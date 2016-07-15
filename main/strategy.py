# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 09:08:18 2016

@author: HUYI
"""

from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade import plotter
from pyalgotrade.stratanalyzer import trades
import mycode


class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, args):
        feed=yahoofeed.Feed()
        dataPath='E://zwPython//zwrk//tmp//'+args[0]+'.csv'
        feed.addBarsFromCSV(args[0],dataPath)
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__args=args
        self.__instrument = args[0]
        self.__position = None
        # We'll use adjusted close values instead of regular close values.
        self.setUseAdjustedValues(True)
        self.__prices = feed[ args[0]].getPriceDataSeries()
        
    def getMa(self,period):
        return ma.SMA(self.__prices, period)
    

    def onEnterCanceled(self, position):
        self.__position = None

    def onExitOk(self, position):
        self.__position = None

    def onExitCanceled(self, position):
        # If the exit was canceled, re-submit it.
        self.__position.exitMarket()

    def onBars(self, bars):
        mycode.backtest(self.__args,bars)

    
args=mycode.args
myStrategy=MyStrategy(args)
myStrategy.run()


