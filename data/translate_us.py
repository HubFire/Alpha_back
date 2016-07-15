# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 15:05:51 2016

@author: HUYI
"""

import os

head="Date,Open,High,Low,Close,Volume,Adj Close,Amount\n"
us_path = 'E:\\USstock'
us_new_path =  'E:\\USstock_1'

def translate_US_one(code):
    filename = us_path+'\\'+code+'.csv'
    newfilename = us_new_path +'\\'+code+'.csv'
    if  not os.path.exists(filename):
        return 
    else:
        oldfile = open(filename,'r')
        newfile = open(newfilename,'w')
        newfile.write(head)
        
        lines=oldfile.readlines()
        lines=lines[1:]
        for line in lines:
            line=line.replace('\n','')
            line+=',0\n'
            newfile.write(line)
        oldfile.close()
        newfile.close
        print code
def translate():
    names = os.listdir(us_path)  
    for name in names:
        name = name.replace('.csv','')
        translate_US_one(name)


translate()      
