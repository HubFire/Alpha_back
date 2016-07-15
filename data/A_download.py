# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 11:32:18 2016

@author: HUYI
"""

import tushare as ts 
import pandas as pd
import datetime
import os
import time
#获得股票基本信息：
#               code,代码
#               name,名称
#               industry,细分行业
#               area,地区
#               pe,市盈率
#               outstanding,流通股本
#               totals,总股本(万)
#               totalAssets,总资产(万)
#               liquidAssets,流动资产
#               fixedAssets,固定资产
#               reserved,公积金
#               reservedPerShare,每股公积金
#               eps,每股收益
#               bvps,每股净资
#               pb,市净率
#               timeToMarket,上市日期

def writeStockBasic():
    df = ts.get_stock_basics()
    df=df.sort_index(ascending=True)
    df.to_csv("/data/basics.csv")

#获得上市时间    
def getTimeToMarket(code):
    df = pd.read_csv('/data/basics.csv',sep=',',dtype={'code':'object'})
    df = df.set_index('code')
    time1=df.ix[code]['timeToMarket']
    time1=str(time1)
    if len(time1)==8:
        result=time1[0:4]+'-'+time1[4:6]+'-'+time1[6:8]
    else:
        #上市时间待定的
        result='1980-01-01'
    return result


def dateadd(date_str,n):
    time1=time.strptime(date_str, '%Y-%m-%d')
    time_stamp=time.mktime(time1)
    #8小时误差，现在还不知道原因
    time2=time_stamp + (n-1)*24*60*60.0+32*60*60
    time2=time.gmtime(time2)
    result=time.strftime('%Y-%m-%d',time2)
    return result


def  update_one(code):
     f=open('/data/Astock/'+code+'.csv','r')
     data=f.readlines()
     t=data[-1].split(',')
     f.close()
     a=t[0]
     b=time.strftime('%Y-%m-%d',time.localtime(time.time())) 
     if a!=b:
        start=dateadd(a,1)
        end=b
        data=ts.get_h_data(code,start=start, end=end)
        data=data.sort_index(ascending=True)
        data.to_csv('/data/Astock/'+code+'.csv',mode='a',header=False)
        


#获得单只股票的数据并写入文件，时间降序    
def get_stock(code):
    filename = '/data/Astock/'+code+'.csv'
    if os.path.exists(filename):
        update_one(code)
        print code+' updated'
    else:
        time_start=getTimeToMarket(code)
        #当前日期
        time_end=datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        #获取前复权数据,按照日期升序排序
        data=ts.get_h_data(code,start=time_start, end=time_end)
        data=data.sort_index(ascending=True)
        data.to_csv(filename)


def get_all_stock():
    
    df = pd.read_csv('/data/basics.csv',sep=',',dtype={'code':'object'})
    df = df.set_index('code')
    for code in df.index:
        try:
         get_stock(code)
        except Exception ,e:
            print e
            continue

get_all_stock()






















