import os
import time
import json
import datetime
import requests
import cx_Oracle
import decimal
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'#oracle insert update 有中文时需要修改字符集设置  (方法1)  方法2:  在中文后面转换格式  .encode('latin1').decode('gbk')
def getTemperature():
    startdate = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    while startdate.strftime('%Y-%m-%d') != '2018-10-15':
        print('startdate:',startdate.strftime('%Y-%m-%d'))
        payload = {'city_id': '2018', 'weather_date': startdate.strftime(
            '%Y-%m-%d'), 'key': '0f464e19b3e27cd9613b801e1b236efe'}
        url = 'http://v.juhe.cn/historyWeather/weather'
        r = requests.get(url, params=payload)
        r.encoding = 'utf-8'
        res = json.loads(r.text)
        print('error_code:',res['error_code'])
        if 'error_code' in res and res['error_code'] == 0:
            T_MAX = res['result']['day_temp'][:-1]
            T_MIN = res['result']['night_temp'][:-1]
            T_AVG = str(decimal.Decimal(int(int(T_MAX) + int(T_MIN)) / 2))
            print('T_MAX:', T_MAX)
            print('T_MIN:', T_MIN)
            print('T_AVG:', T_AVG)
            sql="insert into CA_TEMPERATURE(SDATE,T_MAX,T_MIN,T_AVG,CITY_ID,CITY_NAME) VALUES (:ddd,:T_MAX,:T_MIN,:T_AVG,:C_ID,:C_N)"  
            cursor.execute(sql,{'ddd':startdate,'T_MAX':T_MAX,'T_MIN':T_MIN,'T_AVG':T_AVG,'C_ID':1,'C_N':'天津'})
            row = conn.commit()
        startdate = startdate + datetime.timedelta(days=1)
    # print(datetime.datetime.strptime('20170101','%Y%m%d')+datetime.timedelta(days=1).strftime('%Y%m%d')=='20181015')
    cursor.close()
    conn.close()
def inse():
    startdate = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    # payload = {'city_id': '2018', 'weather_date': startdate.strftime(
    #     '%Y-%m-%d'), 'key': '0f464e19b3e27cd9613b801e1b236efe'}
    # url = 'http://v.juhe.cn/historyWeather/weather'
    # r = requests.get(url, params=payload)
    # r.encoding = 'utf-8'
    # res = json.loads(r.text)
    # if 'error_code' in res and res['error_code'] == 0:
    #     T_MAX = res['result']['day_temp'][:-1]
    #     T_MIN = res['result']['night_temp'][:-1]
    #     T_AVG = str(int(int(int(T_MAX) + int(T_MIN)) / 2))
    #     print('T_MAX:', T_MAX)
    #     print('T_MIN:', T_MIN)
    #     print('T_AVG:', T_AVG)
    # print("sql:", "insert into CA_TEMPERATURE(SDATE,T_MAX,T_MIN,T_AVG,CITY_ID,CITY_NAME) VALUES (TO_DATE('" +
    #       startdate.strftime('%Y-%m-%d') + "','yyyy-mm-dd')," + T_MAX + "," + T_MIN + "," + T_AVG + ",1,'天津')")
    sql="insert into CA_TEMPERATURE(SDATE,T_MAX,T_MIN,T_AVG,CITY_ID,CITY_NAME) VALUES (:ddd,:T_MAX,:T_MIN,:T_AVG,:C_ID,:C_N)"
    
    cursor.execute(sql,{'ddd':startdate,'T_MAX':5,'T_MIN':-1,'T_AVG':2,'C_ID':1,'C_N':'天津'})
    row = conn.commit()
    print(row)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    getTemperature()
