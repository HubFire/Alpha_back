# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 14:59:55 2016

@author: HUYI
"""
import os

head="Date,Open,High,Low,Close,Volume,Adj Close,Amount\n"
a_path = '/root/Desktop/alpha-data/Astock'
a_new_path = '/root/Desktop/alpha-data/Astock_1'

def translate_a_one(code):
    filename = a_path+'/'+code+'.csv'
    newfilename = a_new_path +'/'+code+'.csv'
    if  not os.path.exists(filename):
        return 
    else:
        oldfile = open(filename,'r')
        newfile = open(newfilename,'w')
        newfile.write(head)
        
        lines=oldfile.readlines()
        lines=lines[1:]
        for line in lines:
            line=line.replace('\r\n','')
            items=line.split(',')
            #以close代替Adj Close
            #low和close交换顺序
            newline=items[0]+','+items[1]+','+items[2]+','+items[4]+','+items[3]+','+items[5]+','+items[3]+','+items[6]+'\n'
            newfile.write(newline)
            print code
        oldfile.close()
        newfile.close

def translate():
    names = os.listdir(a_path)  
    for name in names:
        name = name.replace('.csv','')
        translate_a_one(name)
        
        
translate()