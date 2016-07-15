# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 18:06:00 2016

@author: HUYI
"""
from pyalgotrade.tools import yahoofinance
import datetime
import os
import time
#获得美股代码列表
def get_all_codes():
    code_file=open('Yahoo_us.csv')
    codes = code_file.readlines()
    return codes

def  update_one(code):
     f=open('E:\\USstock\\'+code+'.csv','r')
     data=f.readlines()
     t=data[-1].split(',')
     f.close()
     a=t[0]   
     b=time.strftime("%Y-%m-%d", time.localtime())
     if b!=a:
        start=datetime.datetime.strptime(a, "%Y-%m-%d").date()
        end=datetime.datetime.strptime(b, "%Y-%m-%d").date()
        start = start + datetime.timedelta(days=1)
        t=yahoofinance.download_csv(code, start, end, "d") 
        f=open('E:\\USstock\\'+code+'.csv','a')
        update=t.split('\n')
        update=update[1:]
        if len(update)<=0:
            return
        update.reverse()
        for bar in update:
            bar=bar+'\n'
            f.write(bar)
        f.close()
     

#获得单只股票上市至今的历史数据
def get_one_stock(code):
    
    filename = 'E:\\USstock\\'+code+'.csv'
    if os.path.exists(filename):
        update_one(code)
        print code+'   updated'
    else:
        data=yahoofinance.download_csv(code,datetime.date(1900, 1, 1),
                                     datetime.date(2016, 12, 31), "d")
        #先输出文件头，在按时间升序输出
        newdata=[]
        data=data.split('\n')
        head=data[0]+'\n'
        newdata.append(head)
        data=data[1:-2]
        data.reverse()    
        for line in data: 
            line=line+'\n'
            newdata.append(line)
        f= open(filename,'w')
        for line in newdata: 
            f.write(line)
        f.close()
        print code+'   downloaded'
        
def get_all():
    code_list=get_all_codes()
    for code in code_list:
        code =code.replace('\n','')
        try:
            get_one_stock(code)
        except Exception,e:
            print code,e
            continue

get_all()
