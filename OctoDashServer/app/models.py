#app/models.py
from flask import Flask
from flask_login import  UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sockjs.tornado import SockJSRouter, SockJSConnection
from tornado import web, ioloop

# from app import database, login_manager
#
# import websocket, json
# from flask_sqlalchemy import SQLAlchemy
#
# class Printer_db(database.Model):
#     __tablename__ = 'printers'
#
#     printer_id = database.Column(database.Integer, primary_key = True)
#     url = database.Column(database.String(1024))
#     x_api_key = database.Column(database.String(1024))
#     camera_rotation = database.Column(database.Integer)
#     printer_name = database.Column(database.String(1024))
#     printer_type = database.Column(database.String(1024))
#
#     def __repr__(self):
#         return '<Printer_info %r>' % self.printer_id
#
#     @classmethod
#     def get_printer_id_list(self):
#         result = []
#         printer_list = Printer_db.query.order_by(Printer_db.printer_id).all()
#         for p in printer_list:
#             result.append(str(p.printer_id))
#         return result
#
#     @classmethod
#     def get_url(self, printer_id):
#         printer = Printer_db.query.filter_by(printer_id = printer_id).first()
#         return str(printer.url)
#
#     @classmethod
#     def get_x_api_key(self, printer_id):
#         printer = Printer_db.query.filter_by(printer_id = printer_id).first()
#         return str(printer.x_api_key)
#
#     @classmethod
#     def get_rotation_angle(self, printer_id):
#         printer = Printer_db.query.filter_by(printer_id = printer_id).first()
#         return str(printer.camera_rotation)
#
#     @classmethod
#     def get_on_startup(self):
#         result = {}
#         printer_list = Printer_db.query.order_by(Printer_db.printer_id).all()
#         for p in printer_list:
#             info = { 'printer_id' : str(p.printer_id),
#                      'url': str(p.url),
#                      'x_api_key' : str(p.x_api_key),
#                      'camera_rotation' : str(p.camera_rotation),
#                      'printer_name' : str(p.printer_name),
#                      'printer_type' : str(p.printer_type)
#                     }
#             result[str(p.printer_id)] = info
#         return result







# class Printer_module(object):
#
#     printer_id = None
#     x_api_key = None
#     ip_address = None
#     rotation = None
#     socket = None
#
#
#     def __init__(self, settings):
#         printer_id = settings['printer_id']
#         x_api_key = settings['x_api_key']
#         ip_address = settings['ip_address']
#         rotation = settings['rotation']
#
#         import uuid
#         import random
#         import json
#
#         url = "ws://{}/sockjs/{:0>3d}/{}/websocket".format(
#         ip_address,
#         random.randrange(0, stop=999),    # server_id
#         uuid.uuid4()                      # session_id
#         )
#
#
#         websocket.enableTrace(True)
#         socket = websocket.WebSocketApp(url,
#                                         on_open=on_open,
#                                         on_message=on_message,
#                                         on_close=on_close,
#                                         on_error=on_error)
#
#         socket.run_forever()
#
# def on_open(ws, message):
#     print "open\n"
#     print str(message) +'\n'
#
# def on_message(ws, message):
#     if message.startswith('o'):
#         print "o\n"
#     elif message.startswith('a'):
#         received = json.loads(message[1:])
#         print received + '\n'
#     elif message.startwith('h'):
#         print 'heartbeat' + message + '\n'
#     elif message.startswith('c'):
#         print "close\n"
#     else:
#         print "unknown message" + message + '\n'
#
# def on_close(ws):
#     print "closed\n"
#
# def on_heartbeat(ws, message):
#     print str(message) + '\n'
#
# def on_error(ws, error):
#     print str(error) + "\n"
        
    
        