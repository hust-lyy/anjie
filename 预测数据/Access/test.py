import cx_Oracle
import datetime
import pandas as pd
def SaveCSV():
    holiday=['0101','0405','0501','1001']
    conn = cx_Oracle.connect('NEWBI/newBIdb123@192.168.51.55/orcl')
    cursor = conn.cursor()
    cursor.execute("select substr(DEVICE_CODE,0,6) device_code ,sdate,sum(yl) yl  from FBI_IVPD_DAY where DEVICE_CODE like 'K0bjcxd4%' group by substr(DEVICE_CODE,0,6) ,sdate ORDER BY sdate")
    row = cursor.fetchall()
    cursor.close()
    conn.close()
    # print(severdata)
    # print(type(row))
    listdate=[]
    electricity=[]
    listholiday=[]
    listweekday=[]
    listmonthday=[]
    tempdata={}
    for temprow in row:
        tempdate=temprow[1]
        # print(tempdate)
        # print(tempdate.isoweekday())
        #日期数据格式化
        listdate.append(tempdate.strftime('%Y%m%d'))
        if tempdate.isoweekday()==7 or tempdate.isoweekday()==6:#判断是否是周末
            listholiday.append('0.5')
        elif tempdate.strftime('%m%d') in holiday:#判断是否为法定节假日
            listholiday.append('0.5')
        else:
            listholiday.append('1')
        listweekday.append(str(tempdate.isoweekday()))#加入星期数据
        listmonthday.append(str(int(tempdate.strftime('%m'))))#加入月份数据
        electricity.append(temprow[2])#电量数据
    # print(listdate)
    tempdata['日期']=listdate
    tempdata['用电量']=electricity
    tempdata['最高']=[]
    tempdata['最低']=[]
    tempdata['平均']=[]
    tempdata['节假日']=listholiday
    tempdata['周几']=listweekday
    tempdata['月份']=listmonthday    
    print(tempdata)
    df=pd.DataFrame(tempdata)
    df.to_csv("./test.csv",index=False)
if __name__=='__main__':
    SaveCSV()
