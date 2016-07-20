#-*- coding: utf-8 -*-
from _curses import error

from  dbutils import DbConn
import time
import main
import pandas as pd
import sys
def  getTasks():
    db=DbConn()
    conn=db.cursor()
    sql='select * from testQuant_task where status=0'
    conn.execute(sql)
    rows=conn.fetchall()
    db.close()
    return rows
def updateTaskStatus(taskid,status=1):
    db=DbConn()
    conn=db.cursor()
    sql='update testQuant_task set status=%i where id= %i'%(status,taskid)
    conn.execute(sql)
    db.commit()
    db.close()

def getUserCode(str_id):
    db=DbConn()
    conn=db.cursor()
    sql='select content from testQuant_policy where id=%i'%str_id
    conn.execute(sql)
    row=conn.fetchone()
    print row
    db.close()
    code= str(row[0])
    return code

def findStraPathbyId(sta_id):
    db=DbConn()
    conn=db.cursor()
    sql='select code_path from policy where policy_id=%i'%sta_id
    conn.execute(sql)
    row=conn.fetchone()
    db.close()
    path= str(row[0])
    return path

def  prepareCodeFile(userCode):
     head_file=open('head.py','r')
     head_code=head_file.read()
     head_file.close()
     code=head_code+userCode

     code_file=open('./usercode.py','w')
     code_file.write(code)
     code_file.close()
     return

def prepare_data(code,start,end):
    print code
    read_path='/data/Astock_1/'+code+'.csv'
    write_path='./temp.csv'
    df=pd.read_csv(read_path,index_col=0)
    df.sort_index(axis=0,  ascending=True)
    #对时间进行处理,
    start = pd.Period(start)
    end = pd.Period(end)

    df = df[df.index>=str(start)]
    df = df[df.index<=str(end)]
    df.to_csv(write_path)

def saveComplieError(task_id,error):

    error_message=error[0]
    error_lineno=error[1][1]-20
    error_str="'there is error in line {0}\n,error message:{1}'".format(error_lineno,error_message)

    db = DbConn()
    conn = db.cursor()
    sql = 'insert into testQuant_complieerror set task_id={0} ,error_content={1},error_code=1'.format(
        task_id,error_str)
    print sql
    conn.execute(sql)
    db.commit()
    db.close()


def  doTask(task):
      task_id =task[0]
      task_uuid = task[1]
      task_parameter = task[2]
      task_type = task[3]
      task_status = task[4]
      task_stra_id = task[5]
      task_user_id = task[6]
      t=task_parameter.split(',')
      print task_stra_id
      userCode=getUserCode(task_stra_id)
      #print userCode

      prepareCodeFile(userCode)
      prepare_data(t[0],t[1],t[2])

      try:
        main.run(t, task_id)
      except Exception as e:
          saveComplieError(task_id,e)
      updateTaskStatus(task_id,1)

def  mainloop():
    while True:
     time.sleep(1)
     rows=getTasks()
     print rows
     if len(rows)==0:
         print 'empty'
         continue
     for row in rows:
        doTask(row)
mainloop()






