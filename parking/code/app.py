import logging;
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='myapp.log',
                    filemode='a')
import os
import EntityAccess.Access
from flask import Flask, request, render_template,redirect,url_for,escape,session,jsonify
#import flask
#gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
monkey.patch_all()
#gevent end
app = Flask(__name__)
app.config['DEBUG']=True
app.secret_key=os.urandom(12)
@app.route('/GetCarIn',methods=['GET','POST'])
def GetCarIn():
    carinA=EntityAccess.Access.Carin()
    carinlist=carinA.CarinDetail(['InTime','MachNo','CardID','CardType','CarNO'],' from Park_CarIn')
    if carinlist:
        result={'data':carinlist}
        return jsonify(result)
    else:
        return jsonify({'type':500,'message':'fail'})
@app.route('/sentrybox',methods=['GET'])
def sentrybox():
    return render_template('sentrybox.html')
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