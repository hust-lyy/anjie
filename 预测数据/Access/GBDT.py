#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import time
import decimal
import datetime
import calendar
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.externals import joblib
import cx_Oracle
lasttimestamp = -1
# class Prediction(object):
#导入数据
def load_data(path):
    df = pd.read_csv(path)   
    date = df['日期']
    x_train = df.drop(['日期','用电量'],1)
    y_train = df['用电量']
    return x_train, y_train, date

#特征工程
def pre_data(data, num=1, interate=False):
    #data.iloc[:,1] = 0.6*data.iloc[:,1].mean() + 0.4*data.iloc[:,1] 
    poly = PolynomialFeatures(degree=num, interaction_only=interate)
    poly.fit(data)
    return poly.transform(data)
    
#验证函数
def my_score(y_ture, y_pre):
    score = abs(sum(y_pre - y_ture))/sum(y_ture)
    print(score)
    return score


def train(input_path,model_path):
    #进行数据的读取与预处理
    X_train, y_train, _ = load_data(input_path)
    X_train = pre_data(X_train)
    #GBDT模型的参数进行定义
    clf=GradientBoostingRegressor(n_estimators=100,learning_rate=0.085,max_depth=20,min_samples_split=6,
                        min_weight_fraction_leaf=0.1,random_state=0,alpha=0.95,subsample=1,loss='huber')
    #模型训练
    rf=clf.fit(X_train,y_train)
    #模型保存
    joblib.dump(rf,model_path)
    #模型拟合度输出
    y_train_pre = clf.predict(X_train)
    my_score(y_train_pre, y_train)

def pre(input_path,model_path,output_path):
    #进行数据的读取与预处理
    X_pre, _,  date = load_data(input_path)
    X_pre = pre_data(X_pre)
    #加载训练好的模型
    clf=joblib.load(model_path)
    #进行预测
    y_test_pre = clf.predict(X_pre)
    #输出预测三个月用电量的总和
    print(np.sum(y_test_pre))
    #将预测量以csv格式的文件保存至指定的位置
    df=pd.DataFrame(date, columns=['日期'])
    df['用电量'] = y_test_pre
    df.to_csv(output_path,index=False)
def readcsv(docid=None):
    rdf=pd.read_csv("./uploads/csv/"+str(docid)+"/result.csv")
    
    # lastdate=datetime.datetime.strptime(str(int(rdf.head(1).get_values()[0][0])),'%Y%m%d')
    lastdate=None
    resultdata=[]
    # mresultdata=[]
    mtempdic={}#月份用电量统计
    for row in rdf.itertuples(index=False, name='Pandas'):
        # print(row)
        # print (type(), type(getattr(row, "用电量")))
        rtempdic={}
        tempdate=datetime.datetime.strptime(str(getattr(row, "日期")),'%Y%m%d')
        rtempdic['date']=tempdate.strftime('%Y-%m-%d')
        rtempdic['ele']=str(round(decimal.Decimal(getattr(row, "用电量")),3))
        if  lastdate!=None and tempdate.year==lastdate.year and tempdate.month==lastdate.month:
            mtempdic[tempdate.strftime('%Y%m')]=str(round(decimal.Decimal(mtempdic[tempdate.strftime('%Y%m')]),3)+round(decimal.Decimal(getattr(row, "用电量")),3)) 
        else:
            lastdate=tempdate
            mtempdic[tempdate.strftime('%Y%m')]=str(round(decimal.Decimal(getattr(row, "用电量")),3)) 
        # tempdic['ele']=str(int(elc))
        # mresultdata.append(mtempdic)        
        resultdata.append(rtempdic)
    hdf=pd.read_csv("./uploads/csv/"+str(docid)+"/input_data.csv")
    historydata=[]
    for row in hdf.itertuples(index=False, name='Pandas'):
        htempdic={}
        htempdic['date']=datetime.datetime.strptime(str(getattr(row, "日期")),'%Y%m%d').strftime('%Y-%m-%d')
        htempdic['ele']=str(round(decimal.Decimal(getattr(row, "用电量")),3))
        historydata.append(htempdic)
    result={'resultdata':resultdata,'historydata':historydata,'monthdata':mtempdic}
    return result
def readhistorycsv(docid=None):
    hdf=pd.read_csv("./uploads/csv/"+str(docid)+"/input_data.csv")
    historydata=[]
    for hdate,hele in hdf.values:     
        htempdic={}
        htempdic['date']=datetime.datetime.strptime(str(int(hdate)),'%Y%m%d').strftime('%Y-%m-%d')
        htempdic['ele']=round(decimal.Decimal(hele),3)
        historydata.append(htempdic)
    return historydata
def getorderid(programIndex=None):
    global lasttimestamp
    base_timestamp = 1287888001020
    timestamp = int(round(time.time() * 1000))  # 当前时间戳 毫秒级
    program_index_bit = 6  # 商户序号所占字符数
    if programIndex==None:
        program_index=1
    else:
        program_index = programIndex  # 商户序号
    if lasttimestamp == timestamp:
        return None
    else:
        temptime = timestamp - base_timestamp
        result = temptime << program_index_bit | program_index
        lasttimestamp = timestamp
        return result

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
    train(input_path="./uploads/csv/" + str(docid) + "/input_data.csv",model_path="./uploads/csv/" + str(docid) + "/rf.model")
def BuildPreCSV(startdate, enddate, docid):
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
    df.to_csv("./uploads/csv/" + str(docid) + "/pre_data.csv", index=False)

# if __name__=='__main__':
    # train(input_path = "input_data.csv",model_path = "./rf.model")
    # pre(input_path = "pre_data.csv",model_path = "./rf.model",output_path = "1.csv")
    # BuildPreCSV(startdate='2017-10-01',enddate='2017-12-31',docid='16115702750657')
    # print(readcsv(docid='16115748074113'))
# #     readcsv()
# print(readcsv('15888156279041','201807'))
