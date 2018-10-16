import cx_Oracle
import datetime
import pandas as pd


def BuildInputCSV(startdate, enddate, docid):
    tempstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    tempend = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    holiday = ['0101', '0405', '0501', '1001']
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    cursor.execute("select substr(DEVICE_CODE,0,6) device_code ,sdate,sum(yl) yl  from FBI_IVPD_DAY where sdate>=:ttt and sdate<=:ddd and DEVICE_CODE like 'K0bjcxd4%' group by substr(DEVICE_CODE,0,6) ,sdate ORDER BY sdate", {
                   'ttt': tempstart, 'ddd': tempend})
    row = cursor.fetchall()
    listdate = []
    electricity = []
    listholiday = []
    listweekday = []
    listmonthday = []
    listmax = []
    listmin = []
    listavg = []
    tempdata = {}
    for temprow in row:
        tempdate = temprow[1]
        # print(tempdate)
        # print(tempdate.isoweekday())
        #日期数据格式化
        listdate.append(tempdate.strftime('%Y%m%d'))
        cursor.execute('select T_MAX,T_MIN,T_AVG from CA_TEMPERATURE where SDATE=:ddd', {
                       'ddd': tempdate})
        rrr = cursor.fetchall()
        if len(rrr) == 0:
            payload = {'city_id': '2018', 'weather_date': tempdate.strftime(
                '%Y-%m-%d'), 'key': '0f464e19b3e27cd9613b801e1b236efe'}
            url = 'http://v.juhe.cn/historyWeather/weather'
            r = requests.get(url, params=payload)
            r.encoding = 'utf-8'
            res = json.loads(r.text)
            print('error_code:', res['error_code'])
            print(tempdate.strftime('%Y-%m-%d'))
            if 'error_code' in res and res['error_code'] == 0:
                T_MAX = res['result']['day_temp'][:-1]
                T_MIN = res['result']['night_temp'][:-1]
                T_AVG = str(decimal.Decimal(int(int(T_MAX) + int(T_MIN)) / 2))
                sql = "insert into CA_TEMPERATURE(SDATE,T_MAX,T_MIN,T_AVG,CITY_ID,CITY_NAME) VALUES (:ddd,:T_MAX,:T_MIN,:T_AVG,:C_ID,:C_N)"
                cursor.execute(sql, {'ddd': tempdate, 'T_MAX': T_MAX,
                                     'T_MIN': T_MIN, 'T_AVG': T_AVG, 'C_ID': 1, 'C_N': '天津'})
                conn.commit()
                listmax.append(T_MAX)
                listmin.append(T_MIN)
                listavg.append(T_AVG)
            else:
                listmax.append('0')
                listmin.append('0')
                listavg.append('0')
        else:
            listmax.append(rrr[0][0])
            listmin.append(rrr[0][1])
            listavg.append(rrr[0][2])
        if tempdate.isoweekday() == 7 or tempdate.isoweekday() == 6:  # 判断是否是周末
            listholiday.append('0.5')
        elif tempdate.strftime('%m%d') in holiday:  # 判断是否为法定节假日
            listholiday.append('0.5')
        else:
            listholiday.append('1')
        listweekday.append(str(tempdate.isoweekday()))  # 加入星期数据
        listmonthday.append(str(int(tempdate.strftime('%m'))))  # 加入月份数据
        electricity.append(temprow[2])  # 电量数据
    # print(listdate)
    cursor.close()
    conn.close()
    tempdata['日期'] = listdate
    tempdata['用电量'] = electricity
    tempdata['最高'] = listmax
    tempdata['最低'] = listmin
    tempdata['平均'] = listavg
    tempdata['节假日'] = listholiday
    tempdata['周几'] = listweekday
    tempdata['月份'] = listmonthday
    df = pd.DataFrame(tempdata)
    df.to_csv("./uploads/csv/" + str(docid) + "/input_data.csv", index=False)


def BuildPreCSV(startdate, enddate, outpath):
    tempstart = datetime.datetime.strptime(startdate, '%Y-%m-%d')
    tempend = datetime.datetime.strptime(enddate, '%Y-%m-%d')
    if tempstart.month < 10:
        tempstartmonth = '0' + str(tempstart.month)
    else:
        tempstartmonth=str(tempstart.month)
    if tempstart.day < 10:
        tempstartday = '0' + str(tempstart.day)
    else:
        tempstartday=str(tempstart.day)
    tempstart = datetime.datetime.strptime(
        '2017-' + tempstartmonth + '-' + tempstartday, '%Y-%m-%d')
    if tempend.month < 10:
        tempendmonth = '0' + str(tempend.month)
    else:
        tempendmonth = str(tempend.month)
    if tempend.day < 10:
        tempendday = '0' + str(tempend.day)
    else:
        tempendday = str(tempend.day)
    tempend = datetime.datetime.strptime(
        '2017-' + tempendmonth + '-' + tempendday, '%Y-%m-%d')
    holiday = ['0101', '0405', '0501', '1001']
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    listdate = []
    electricity = []
    listholiday = []
    listweekday = []
    listmonthday = []
    listmax = []
    listmin = []
    listavg = []
    tempdata = {}
    cursor.execute('select SDATE,T_MAX,T_MIN,T_AVG from CA_TEMPERATURE where SDATE>=:ddd and SDATE<=:ttt order by SDATE', {
                   'ddd': tempstart, 'ttt': tempend})
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    for temprow in row:
        tempdate = datetime.datetime.strptime(startdate, '%Y-%m-%d').strftime('%Y')+'-'+ temprow[0].strftime('%m')+'-'+temprow[0].strftime('%d')
        tempdate=datetime.datetime.strptime(tempdate,'%Y-%m-%d')
        #日期数据格式化
        listdate.append(tempdate.strftime('%Y%m%d'))
        listmax.append(temprow[1])
        listmin.append(temprow[2])
        listavg.append(temprow[3])
        if tempdate.isoweekday() == 7 or tempdate.isoweekday() == 6:  # 判断是否是周末
            listholiday.append('0.5')
        elif tempdate.strftime('%m%d') in holiday:  # 判断是否为法定节假日
            listholiday.append('0.5')
        else:
            listholiday.append('1')
        listweekday.append(str(tempdate.isoweekday()))  # 加入星期数据
        listmonthday.append(str(int(tempdate.strftime('%m'))))  # 加入月份数据
        electricity.append('')
    tempdata['日期'] = listdate
    tempdata['用电量'] = electricity
    tempdata['最高'] = listmax
    tempdata['最低'] = listmin
    tempdata['平均'] = listavg
    tempdata['节假日'] = listholiday
    tempdata['周几'] = listweekday
    tempdata['月份'] = listmonthday
    df = pd.DataFrame(tempdata)
    df.to_csv(outpath, index=False)


if __name__ == '__main__':
    BuildInputCSV('2017-10-01','2018-10-10',"./input_data.csv")
    BuildPreCSV('2018-11-01','2018-12-31',"./pre_data.csv")
