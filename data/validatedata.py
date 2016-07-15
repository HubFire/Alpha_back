# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 10:12:56 2016

@author: HUYI
"""


import os

# high>=open
#high >=low
#high >=close
#low <= open
#low <= close


def validateData_A(filename):
    datafile = open(filename,'r')
    lines= datafile.readlines()
    lines=lines[1:]
    for line in lines:
        line =line.replace('\n','')
        bar=line.split(',')
        _date=str(bar[0])
        _open=float(bar[1])
        _high=float(bar[2])
        _close=float(bar[3])
        _low=float(bar[4])
        if _high<_open:
            print filename,_date,'high<open'
        if _high<_low:
            print filename,_date,'high<low'
        if _high<_close:
            print filename,_date,'high<close'
        if _low>_open:
            print filename,_date,'low>open'
        if _low>_close:
            print filename,_date,'low>close'
def validateData_US(filename):
    datafile = open(filename,'r')
    lines= datafile.readlines()
    lines=lines[1:]
    for line in lines:
        line =line.replace('\n','')
        bar=line.split(',')
        _date=str(bar[0])
        _open=float(bar[1])
        _high=float(bar[2])
        _low=float(bar[3])
        _close=float(bar[4])
        if _high<_open:
            print filename,_date,'high<open'
        if _high<_low:
            print filename,_date,'high<low'
        if _high<_close:
            print filename,_date,'high<close'
        if _low>_open:
            print filename,_date,'low>open'
        if _low>_close:
            print filename,_date,'low>close'
def validate_all():
     names = os.listdir('E:\\Astock')  
     for name in names:
         filename='E:\\Astock\\'+name
         validateData_A(filename)
         names = os.listdir('E:\\USstock')  
         
#     for name in names:
#         filename='E:\\USstock\\'+name
#         validateData_US(filename)
    
    
validate_all()           
           
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            