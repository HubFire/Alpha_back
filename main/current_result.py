# -*- coding: utf-8 -*-
"""
Created on 4/11/16

@author: HUYI
"""
import json
import dbutils

class CurrentResult():
    def __init__(self,time,price,str_return,basic_return):
        self.__time=time
        self.__price=price
        self.__str_return=str_return
        self.__basic_return=basic_return
    def tojson(self):
        data={}
        list=[]
        list.append(self.__price)
        list.append(self.__str_return)
        list.append(self.__basic_return)
        data["time"]=self.__time
        data["content"] = list

        return data

class OneRecord():
    def __init__(self,id,offset=1,list=[],finish_flag=0):
        self.__id=id
        self.__offset=offset
        self.__list=list
        self.__finish=finish_flag
    def toDb(self):
        db=DbConn()
        conn=db.cursor()
        list_str=json.dumps(list)
        sql='insert into current_result values(%i,%i,%s,%i)'%(self.__id,self.__offset,self.__list,self.__finish)
        conn.execute(sql)
        conn.commit()
        db.close()
    def add(self,data):
        self.__list.append(data)
    def clean(self):
        self.__list=[]





