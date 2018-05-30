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

    def CarinDetail(self, field, requirment):
        try:
            sql = 'select '
            for i in range(len(field) - 1):
                sql += field[i] + ','
            sql += field[len(field) - 1]
            sql += requirment
            logging.debug(sql)
            print(sql)
            rows = self.__CarinDao.select(sql)
            print(rows)
        except Exception as ex:
            logging.error(ex)
            return False
        else:
            result = []
            number = 0
            for row in rows:
                tempdict = {}
                for index in range(len(row)):
                    if isinstance(row[index], datetime.datetime):
                        tempdict[field[index]] = row[index].strftime(
                            "%Y-%m-%d %H:%M:%S")
                    # elif isinstance(row[index],str):
                    #     tempdict[field[index]] = row[index].encode('latin-1').decode('gbk')
                    else:
                        tempdict[field[index]] = str(row[index])
                number += 1
                # tempdict['id'] = str(number)
                result.append(tempdict)
            return result
    # 共单引

    def gdy(self, parameter):
        result = ''
        if parameter != '':
            result = "'" + parameter.replace("'", "''") + "'"
        else:
            result = "''"
        return result