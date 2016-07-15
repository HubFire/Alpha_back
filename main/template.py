# -*- coding: utf-8 -*-
"""
Created on 4/12/16

@author: HUYI
"""
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
import pandas as pd
from dbutils import DbConn
import json
from current_result import CurrentResult
import datetime
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown

def insertResult(taskid,str_return,basic_return,alpha,beta,sharp,maxdown):

    db=DbConn()
    conn=db.getCon()
    cursor=db.cursor()
    sql= 'insert into testQuant_result set task_id={},strategy_return={},basic_return={},alpha={},beta={},sharp={},maxdown={}'\
        .format(taskid,str_return,basic_return,alpha,beta,sharp,maxdown)
    print sql
    cursor.execute(sql)
    db.commit()
    db.close()



def toDb(taskid,offset,datalist,finish):
           db=DbConn()
           conn=db.getCon()
           cursor=db.cursor()


           sql='insert into testQuant_current_result set task_id=%i ,offset=%i, content="%s",finish_flag=%i'%(taskid,offset,str(datalist),finish)
           print  sql
           cursor.execute(sql)
           db.commit()
           db.close()

def insertlog(taskid,offset,datalist,finish):
    db=DbConn()
    conn=db.getCon()
    cursor=db.cursor()

    sql='insert into testQuant_log set task_id=%i ,offset=%i, content="%s", finish_flag=%i'%(taskid,offset,str(datalist),finish)
    print sql
    cursor.execute(sql)
    db.commit()
    db.close()


# 策略模板
class StrategyTemplate(strategy.BacktestingStrategy):

      def __init__(self, feed,instrument,arg1,arg2,task_id):



          strategy.BacktestingStrategy.__init__(self, feed,int(arg1[3]))
          self.instrument=instrument
          self.feed=feed
          self.args=arg2
          self.__currentRet = []
          self.__offset=0

          self.__logOffset=0
          self.__currentLog=[]

          self.__task_id=task_id

          self.sharpeRatioAnalyzer = sharpe.SharpeRatio()
          self.attachAnalyzerEx(self.sharpeRatioAnalyzer, 'sharpe')

          self.retAnalyzer = returns.Returns()
          self.attachAnalyzerEx(self.retAnalyzer,'return')

          self.drawDownAnalyzer = drawdown.DrawDown()
          self.attachAnalyzerEx(self.drawDownAnalyzer,'draw')
          #print '起始资产: %d'%self.getResult()




      def onFinish(self,  bars):
          self.__offset+=1
          print  'finish',self.__offset
          toDb(self.__task_id,self.__offset,self.__currentRet,finish=1)
          self.__logOffset +=1
          insertlog(self.__task_id,self.__logOffset,self.__currentLog,finish=1)

          stra_return = self.retAnalyzer.getCumulativeReturns()[-1] * 100
          basic_return = self.retAnalyzer.getCumulativeReturns()[-1] * 100

          alpha = 0
          beta = 0
          sharp = self.sharpeRatioAnalyzer.getSharpeRatio(0.05)
          maxdown = self.drawDownAnalyzer.getMaxDrawDown() * 100



          insertResult(self.__task_id, stra_return,basic_return,alpha,beta,sharp,maxdown)

          print("最终资产价值 Final portfolio value: $%.2f" % self.getResult())
          print("累计回报率 Cumulative returns: %.2f %%" % (self.retAnalyzer.getCumulativeReturns()[-1] * 100))
          print("夏普比率 Sharpe ratio: %.2f" % (self.sharpeRatioAnalyzer.getSharpeRatio(0.05)))
          print("最大回撤率 Max. drawdown: %.2f %%" % (self.drawDownAnalyzer.getMaxDrawDown() * 100))
          print("最长回撤时间 Longest drawdown duration: %s" % (self.drawDownAnalyzer.getLongestDrawDownDuration()))


      def afterOnBars(self, bars):
          time=self.getCurrentDateTime()
          time_str=datetime.datetime.strftime(time ,'%Y-%m-%d')
          price=bars[self.instrument].getPrice()
          str_return=self.retAnalyzer.getCumulativeReturns()[-1] * 100
          basic_return=self.retAnalyzer.getReturns()[-1]*100

          data = CurrentResult(time_str,price ,str_return,basic_return)

          self.addRet(data.tojson())

      def addRet(self,data):
          self.__currentRet.append(data)

          if len(self.__currentRet)==60:
             self.__offset+=1
             toDb(self.__task_id,self.__offset,self.__currentRet,finish=0)
             self.__currentRet=[]

      def addLog(self,data):
          self.__currentLog.append(data)
          if len(self.__currentLog)==20:
              self.__logOffset+=1
              insertlog(self.__task_id,self.__logOffset,self.__currentLog,finish=0)
              print self.__currentLog
              self.__currentLog=[]

      def info(self, msg):
          date=self.getCurrentDateTime()
          data= '%s ----%s'%(date,msg)
          self.addLog(data)




















