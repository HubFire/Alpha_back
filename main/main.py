# -*- coding: utf-8 -*-
"""
Created on Tue Apr 05 15:00:50 2016

@author: HUYI
"""
import os


from  template import  StrategyTemplate
from pyalgotrade.barfeed import yahoofeed



class MyStrategy(StrategyTemplate):
      def __init__(self,feed, instrument,arg1,arg2,task_id):

          StrategyTemplate.__init__(self,feed, instrument,arg1,arg2,task_id)
          self.initialize()

      def onBars(self,bars) :
          print 'onbars'

def run(arg1, task_id):
    if os.path.exists('usercode.py'):
        import usercode
        reload(usercode)
        MyStrategy.initialize=usercode.initialize
        MyStrategy.onBars=usercode.onBars
        arg2 = usercode.args
        inst = arg1[0]
        feed = yahoofeed.Feed()
        print inst
        feed.addBarsFromCSV(inst,'./temp.csv')
        strategy = MyStrategy(feed,inst,arg1,arg2, task_id)

        strategy.run()
    else:
         return



     
     
