# -*- coding: utf-8 -*-
"""
Created on 4/6/16

@author: HUYI
"""
import MySQLdb
class DbConn:
    def __init__(self):
        self.conn=None

    def getCon(self):
        self.conn=MySQLdb.connect(host='192.168.1.29',port=3306,user='root',
                         db='testQuant',charset='utf8',passwd='');
    def cursor(self):
        try:
            return self.conn.cursor()
        except(AttributeError,MySQLdb.OperationalError):
            self.getCon()
            return self.conn.cursor()

    def commit(self):
        return self.conn.commit()

    def close(self):
        return self.conn.close()
















