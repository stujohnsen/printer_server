#app/__init__.py
import flask, time, requests, sys
from flask import Flask, request, Response, make_response, abort, url_for, json, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
 
#from config import app_config

   
app = Flask(__name__)#, instance_relative_config=True)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:releasethe@localhost:3306/PrinterInformation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
#app.config['SERVER_NAME'] = 'localhost:6286'
#app.config.from_object(app_config['development'])
# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
CORS(app)

from app import routes


