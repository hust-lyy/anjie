import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='Access.log',
                    filemode='a')
import json
import random
import os
import re
import time
import datetime
from EntityAccess.connect import Dao
# from connect import Dao


class Carin(object):
    def __init__(self):
        self.__CarinDao = Dao()
    def delect(self,table,pre):
        try:
            result=self.__CarinDao.delect(table,pre)
            return result
        except Exception as ex:
            logging.error(ex)
            return False
    def select(self, field, requirment,isencode=[]):
        try:            
            sql = 'select '
            for i in range(len(field) - 1):
                sql += field[i] + ','
            sql += field[len(field) - 1]
            sql += requirment
            logging.debug(sql)            
            rows = self.__CarinDao.select(sql)            
        except Exception as ex:
            logging.error(ex)
            return False
        else:
            result = []
            for row in rows:
                tempdict = {}
                for index in range(len(row)):
                    if isinstance(row[index], datetime.datetime):
                        tempdict[field[index]] = row[index].strftime(
                            "%Y-%m-%d %H:%M:%S")                    
                    elif field[index] in isencode:                       
                        tempdict[field[index]] = row[index].encode('latin-1').decode('gbk')
                    else:
                        tempdict[field[index]] = str(row[index])
                # tempdict['id'] = str(number)
                result.append(tempdict)
            return result
    def CallProcedurec(self,proc,parameter):
        try:
            rows=self.__CarinDao.procedures(proc,parameter)
            result=[]
            for row in rows:
                tempdict={'ID':0,'datetime':'','BCar-In':0,'BCar-Out':0,'FreeCardA-In':0,'FreeCardA-Out':0,'Manual-In':0,'Manual-Out':0,'SCar-In':0,'SCar-Out':0,'MRentCardA-In':0,'MRentCardA-出':0,'InCount':0,'OutCount':0}
                for index in range(len(row)):
                    tempdict['ID']=row[0]
                    tempdict['datetime']=row[1]
                    tempdict['BCar-In']=row[3]
                    tempdict['BCar-Out']=row[4]
                    tempdict['FreeCardA-In']=row[5]
                    tempdict['FreeCardA-Out']=row[6]
                    tempdict['Manual-In']=row[7]
                    tempdict['Manual-Out']=row[8]
                    tempdict['SCar-In']=row[9]
                    tempdict['SCar-Out']=row[10]
                    tempdict['MRentCardA-In']=row[11]
                    tempdict['MRentCardA-Out']=row[12]
                    tempdict['InCount']=row[13]
                    tempdict['OutCount']=row[14]
                result.append(tempdict)
            return result
        except Exception as ex:
            logging.error(ex)
            return False
    # 共单引

    def gdy(self, parameter):
        result = ''
        if parameter != '':
            result = "'" + parameter.replace("'", "''") + "'"
        else:
            result = "''"
        return result