

args = ["orcl", "2008-01-01", "2008-03-01", "1000000", "day",5,0.01]

def init(self, feed,args):
        strategy.BacktestingStrategy.__init__(self, feed)
        self.__instrument = args[0]
        self.__vwap = vwap.VWAP(feed[self.__instrument], args[-2])
        self.__threshold = args[-1]
        
def onBars(self, bars):
        vwap = self.__vwap[-1]
        if vwap is None:
            return

        shares = self.getBroker().getShares(self.__instrument)
        price = bars[self.__instrument].getClose()
        notional = shares * price

        if price > vwap * (1 + self.__threshold) and notional < 1000000:
            self.marketOrder(self.__instrument, 100)   #买入
            self.info("++ %.2f,%.2f,$%.2f,$%.2f,$%.2f" % (vwap,shares,price,notional,self.getBroker().getCash() ))
            print self.getNamedAnalyzer('return').getReturns()[-1]*100
            
       
        elif price < vwap * (1 - self.__threshold) and notional > 0:
            self.marketOrder(self.__instrument, -100)  #卖出
            self.info("-- %.2f,%.2f,$%.2f,$%.2f,$%.2f" % (vwap,shares,price,notional,self.getBroker().getCash() ))
