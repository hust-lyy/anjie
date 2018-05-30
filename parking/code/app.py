#gevent
from gevent import monkey
monkey.patch_all()
from gevent.pywsgi import WSGIServer

#gevent end
import logging;
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='myapp.log',
                    filemode='a')
import os
import EntityAccess.Access

#import flask
from flask import Flask, request, render_template,redirect,url_for,escape,session,jsonify



app = Flask(__name__)
app.config['DEBUG']=True
app.secret_key=os.urandom(12)
@app.route('/',methods=['GET'])
def home():
    return render_template('sentrybox.html')
# 入场信息流水
@app.route('/GetCarIn',methods=['GET','POST'])
def GetCarIn():
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.CarinDetail(['InTime','MachNo','CardID','CardType','CarNO'],' from Park_CarIn')
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/sentrybox',methods=['GET'])
def sentrybox():
    return render_template('sentrybox.html')
# 出场信息流水
# 长期滞留车辆
@app.route('/GetRetention',methods=['POST'])
def GetRetention():
    st=request.form['starttime']
    et=request.form['endtime']
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.CarinDetail(['ID','CardID','EmpName','CarNO','CardType','CarNoType','InWay','InTime','InUserName']," from Park_CarIn where InTime >= %s and InTime <= %s"%(carinA.gdy(st),carinA.gdy(et)))
    print(carinlist)
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/retention',methods=['GET'])
def Retention():
    return render_template('retention.html')
# 设备异常登记
@app.route('/GetAnomaly',methods=['POST'])
def GetAnomaly():
    st=request.form['starttime']
    et=request.form['endtime']
    # status=request.form['DeviceStatus']    
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.CarinDetail(['ID','DeviceIP','DeviceName','UserDate','DeviceStatus','CreateUserName']," from Park_AllDeviceStatus where  UserDate >= %s and UserDate <= %s"%(carinA.gdy(st),carinA.gdy(et)))
    print(carinlist)
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':300,'message':'Not Data'})
@app.route('/anomaly',methods=['GET'])
def anomaly():
    return render_template('anomaly.html')
@app.route('/ffkz',methods=['POST'])
def ffkz():
    st=request.form['starttime']
    et=request.form['endtime']
    logging.debug(st)
    logging.debug(et)
    print(st,et)
    return jsonify({'type':200,'message':'success','content':{'starttime':st,'endtime':et}})
@app.route('/illegality',methods=['GET'])
def illegality():
    return render_template('illegality.html')
if __name__ == '__main__':
    #app.run(host='0.0.0.0',port=8099)

    http_server=WSGIServer(('0.0.0.0',8099),app)
    #logging.debug('服务已启动当前为调试模式')
    # logging.debug('debug message')
    # logging.info('info message')
    # logging.warn('warn message')
    # logging.error('error message')
    # logging.critical('critical message')

    print('yiqidong')
    http_server.serve_forever()