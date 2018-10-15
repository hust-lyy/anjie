import time
import json
import datetime
import requests
import cx_Oracle
def getTemperature():        
    # payload = {'city_id': '2018','weather_date':'2011-01-01','key':'0f464e19b3e27cd9613b801e1b236efe'}
    # url = 'http://v.juhe.cn/historyWeather/weather'    
    # r = requests.get(url, params=payload)
    # r.encoding = 'utf-8'
    # res=json.loads(r.text)
    # print(res)
    # print(res.keys())
    # if 'error_code' in res and res['error_code']==0:
    #     print(res['result']['day_temp'])
    #     print(res['result']['day_temp'][:-1])
    #     print(res['result']['night_temp'][:-1])
    #     print('T_AVG',int((int(res['result']['day_temp'][:-1])+int(res['result']['night_temp'][:-1]))/2))
        #insert into table1 (id,name) values ('aa','bb')

    #     conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    # cursor = conn.cursor()
    # cursor.execute("select substr(DEVICE_CODE,0,6) device_code ,sdate,sum(yl) yl  from FBI_IVPD_DAY where DEVICE_CODE like 'K0bjcxd4%' group by substr(DEVICE_CODE,0,6) ,sdate ORDER BY sdate")
    # row = cursor.fetchall()
    # cursor.close()
    # conn.close()
    startdate=datetime.datetime.strptime('2017-01-01','%Y-%m-%d')
    while startdate.strftime('%Y-%m-%d')!='2018-10-16':
        print(startdate)
        payload = {'city_id': '2018','weather_date':startdate.strftime('%Y-%m-%d'),'key':'0f464e19b3e27cd9613b801e1b236efe'}
        url = 'http://v.juhe.cn/historyWeather/weather'
        r = requests.get(url, params=payload)
        r.encoding = 'utf-8'
        res=json.loads(r.text)
        if 'error_code' in res and res['error_code']==0:
            T_MAX=res['result']['day_temp'][:-1]
            T_MIN=res['result']['night_temp'][:-1]
            T_AVG=str(int(int(T_MAX+T_MIN)/2))
            print('T_MAX:',T_MAX)
            print('T_MIN:',T_MIN)
            print('T_AVG:',T_AVG)
            
        startdate=startdate+datetime.timedelta(days=1)
    # print(datetime.datetime.strptime('20170101','%Y%m%d')+datetime.timedelta(days=1).strftime('%Y%m%d')=='20181015')
def inse():
    startdate=datetime.datetime.strptime('2017-01-01','%Y-%m-%d')
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    payload = {'city_id': '2018','weather_date':startdate.strftime('%Y-%m-%d'),'key':'0f464e19b3e27cd9613b801e1b236efe'}
    url = 'http://v.juhe.cn/historyWeather/weather'
    r = requests.get(url, params=payload)
    r.encoding = 'utf-8'
    res=json.loads(r.text)
    if 'error_code' in res and res['error_code']==0:
        T_MAX=res['result']['day_temp'][:-1]
        T_MIN=res['result']['night_temp'][:-1]
        T_AVG=str(int(int(T_MAX+T_MIN)/2))
        print('T_MAX:',T_MAX)
        print('T_MIN:',T_MIN)
    print("sql:","insert into CA_TEMPERATURE(SDATE,T_MAX,T_MIN,T_AVG,CITY_ID,CITY_NAME) VALUES (TO_DATE("+startdate.strftime('%Y-%m-%d')+",'yyyy-mm-dd'),"+T_MAX+","+T_MIN+","+T_AVG+",2,'天津')")
    cursor.execute("insert into CA_TEMPERATURE(SDATE,T_MAX,T_MIN,T_AVG,CITY_ID,CITY_NAME) VALUES (TO_DATE("+startdate.strftime('%Y-%m-%d')+",'yyyy-mm-dd'),"+T_MAX+","+T_MIN+","+T_AVG+",2,'天津')")
    row = cursor.commit()
    print(row)
    cursor.close()
    conn.close()
if __name__ == '__main__':
    inse()
