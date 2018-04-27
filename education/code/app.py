import os
import time
import json
import rsa
from flask import Flask, request, render_template, redirect, url_for, escape, session, jsonify
from gevent import monkey
from gevent.pywsgi import WSGIServer
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S', filename='app.log', filemode='a')

monkey.patch_all()
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = os.urandom(12)


@app.route('/admin/question/input', methods=['POST'])
def question():
    if request.is_json():
        