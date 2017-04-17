#app/__init__.py

import random

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    # app.config['DEBUG'] = True
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:releasethe@localhost:3306/octoslackdb'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = False

    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    CORS(app)
    migrate = Migrate(app, db)

    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app









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
#         printer = Printer_db.query.filter_by(printer_id=printer_id).first()
#         return str(printer.url)
#
#     @classmethod
#     def get_x_api_key(self, printer_id):
#         printer = Printer_db.query.filter_by(printer_id=printer_id).first()
#         return str(printer.x_api_key)
#
#     @classmethod
#     def get_camera_rotation_angle(self, printer_id):
#         printer = Printer_db.query.filter_by(printer_id=printer_id).first()
#         return str(printer.camera_rotation)
#
#     @classmethod
#     def get_on_startup(self):
#         result = {}
#         printer_list = Printer_db.query.order_by(Printer_db.printer_id).all()
#         for p in printer_list:
#             info = {'printer_id': str(p.printer_id),
#                     'url': str(p.url),
#                     'x_api_key': str(p.x_api_key),
#                     'camera_rotation': str(p.camera_rotation),
#                     'printer_name': str(p.printer_name),
#                     'printer_type': str(p.printer_type)
#                     }
#             result[str(p.printer_id)] = info
#         return result
#
# printer_info = Printer_db()
# # printer_list = printer_info.get_printer_id_list()
# available_printers = {}
#
# class SiteConnectionSocket(SockJSConnection):
#     """Echo connection implementation"""
#     clients = set()
#
#     def on_open(self, info):
#         # When new client comes in, will add it to the clients list
#         self.clients.add(self)
#
#         printer_info_to_send = {}
#
#         for available in available_printers:
#             current_printer_client = available_printers[available]
#             printer_info_to_send[available] = { 'printer_id' : current_printer_client.printer_id,
#                                                 'url' : current_printer_client.client.baseurl,
#                                                 'is_connected' : current_printer_client.is_connected,
#                                                 'camera_rotation' : current_printer_client.camera_rotation,
#                                                 'printer_name' : current_printer_client.printer_name,
#                                                 'printer_type' : current_printer_client.printer_type
#                                                 }
#         to_send = json.dumps({'message_type' : 'on_server_connect',
#                               'num_printers' : str(len(available_printers)),
#                               'message' : printer_info_to_send})
#         self.send(to_send)
#
#     def on_message(self, msg):
#         # For every incoming message, broadcast it to all clients
#         self.broadcast(self.clients, msg)
#
#     def on_close(self):
#         # If client disconnects, remove him from the clients list
#         self.clients.remove(self)
#
#     @classmethod
#     def dump_stats(cls):
#         print 'Clients: %d' % (len(cls.clients))
#
# octoRouter = SockJSRouter(SiteConnectionSocket, '/listen', dict())
#
# class client_wrapper(object):
#     def __init__(self, printer_id, url, x_api_key, camera_rotation, printer_name, printer_type):
#         self.printer_id = printer_id
#         self.client = octoprint_client.Client("http://" + url, x_api_key)
#         self.camera_rotation = camera_rotation
#         self.printer_name = printer_name
#         self.printer_type = printer_type
#         self.socket = None
#         self.is_connected = False
#
#     def connect_client(self):
#
#         if self.is_connected == True:
#             return
#
#         def on_heartbeat(ws):
#             pass
#             # print("{}: <3").format(self.printer_id)
#             # m = str("{}: <3").format(self.printer_id)
#
#             # octoRouter.broadcast(octoRouter._connection.clients, m)
#             # aggregate_socket.send("{}: <3").format(self.printer_id)
#
#         def on_message(ws, internal_type, internal_message):
#
#             # m = str("{}: message, type: {}, message: {!r}").format(self.printer_id, internal_type, internal_message)
#
#             to_send = {'printer_id' : self.printer_id,
#                        'message_type' : internal_type,
#                        'message' : internal_message}
#
#             print(json.dumps(to_send))
#             octoRouter.broadcast(octoRouter._connection.clients, json.dumps(to_send))
#
#
#         def on_open(ws):
#             print("{}: open").format(self.printer_id)
#
#         def on_close(ws):
#             print("{}: closed").format(self.printer_id)
#
#         def on_error(ws, error):
#             print("{}: error: {}").format(self.printer_id, error)
#
#         self.socket = self.client.create_socket(on_open=on_open,
#                                                 on_heartbeat=on_heartbeat,
#                                                 on_message=on_message,
#                                                 on_close=on_close,
#                                                 on_error=on_error)
#
#         self.is_connected = self.socket.is_connected
#
#         if self.is_connected == True:
#             self.wait_thread = threading.Thread(target=self.socket.wait)
#             self.wait_thread.start()
#
#     def reconnnect_client(self):
#         self.socket.reconnect(10, True)
#
#         if self.socket.is_connected:
#             self.is_connected == True
#             self.wait_thread = threading.Thread(target=self.socket.wait)
#             self.wait_thread.start()
#
#     def disconnect_client(self):
#         self.socket.disconnect()
#         self.wait_thread.join(0)
#         self.is_connected = False
#
# with app.app_context():
#
#     # 2. Create Tornado web.Application
#     tornado_server = web.Application(octoRouter.urls)
#     #
#     # # 3. Make application listen on port 8080
#     tornado_server.listen(8081)
#     #
#     # # 4. Every 1 second dump current client count
#     ioloop.PeriodicCallback(SiteConnectionSocket.dump_stats, 5000).start()
#     #
#     # # 5. Start IOLoop
#     router_thread = threading.Thread(target=ioloop.IOLoop.instance().start, args=())
#     router_thread.start()
#
#     # printer_info = Printer_db()
#     # # printer_list = printer_info.get_printer_id_list()
#     # printer_set = printer_info.get_on_startup()
#
#     printer_set = printer_info.get_on_startup()
#
#     # from config import app_config
#
#     # app.config['SERVER_NAME'] = 'localhost:6286'
#     # app.config.from_object(app_config['development'])
#     # app.config.from_pyfile('config.py')
#     # database.init_app(app)
#     # login_manager.init_app(app)
#     # login_manager.login_message = "You must be logged in to access this page."
#     # login_manager.login_view = "auth.login"
#     # CORS(app)
#
#     # database.create_all()
#
#     # if __name__ == "__main__":
#         # with app.app_context():
#
#     # client1 = client_wrapper("4", "http://155.97.12.124", "octopi4apikey")
#     # client_thread1 = threading.Thread(target=client1.connect_client, args=())
#     # #
#     # client_thread1.start()
#
#     for p in printer_set:
#         current_info = printer_set[p]
#         client = client_wrapper(current_info['printer_id'],
#                                 current_info['url'],
#                                 current_info['x_api_key'],
#                                 current_info['camera_rotation'],
#                                 current_info['printer_name'],
#                                 current_info['printer_type'])
#         available_printers[current_info['printer_id']] = client
#         client_thread = threading.Thread(target=client.connect_client, args=())
#         client_thread.start()

    # app.run()#, port = 6286)


# @app.route('/printer', methods = ['POST'])
#
# def parse_request():
# #     print request.json
#
#     status_code = ''
#     build_resp = {
#         'status' : '',
#         'message' : '',
#         'printer_id' : '',
#         'payload' : {}
#     }
#
#     try:
#         r = request.json
#         printer_id = str(r['printer_id'])
#         commands_to_interpret = r['commands']
#         build_resp['printer_id'] = printer_id
#     #    print "c\n"
#
#         if not printer_id:
#             build_resp['status'] = 'error'
#             build_resp['message'] = 'No printer ID given.'
#             status_code = '400'
#         elif printer_id not in printer_list:
#             build_resp['status'] = 'error'
#             build_resp['message'] = 'Invalid printer ID: ' + printer_id + '.'
#             status_code = '400'
#         elif not commands_to_interpret:
#             build_resp['status'] = 'error'
#             build_resp['message'] = 'No request specified.'
#         else:
#             build_resp['status'] = 'ok'
#             build_resp['message'] = 'Returning request from printer ' + printer_id + '.'
#             status_code = '200'
#             url = str(get_printer_address(printer_id))
#             header = {'X-Api-Key' : str(get_printer_api_key(printer_id))}
#             printer_received_dict = requests.get((url+"/api/printer"),headers=header).json()
#             print printer_received_dict
#             # print printer_received_dict
#             job_received_dict = requests.get((url+"/api/job"),headers=header).json()
#             for x in commands_to_interpret:
#                 build_resp['payload'].update({ x : get_info_from_command(x, printer_received_dict, job_received_dict) })
#             #build_resp['payload'] = received
#             status_code = '200'
#
#     except ValueError, e:
#         print "value error: " + str(e)
#         #print "Error: Printer has Disconnected", sys.exc_info()[0]
#         build_resp['status'] = 'Printer Error'
#         build_resp['message'] = 'Error encountered while querying data from printer ' + printer_id + ': ' + str(e)
#         status_code = '409'
#     except TypeError, e:
#         print "type error: " + str(e)
#         build_resp['status'] = 'Type Error'
#         build_resp['message'] = 'Error when parsing request: ' + str(e)
#         status_code = '400'
#     except requests.exceptions.ConnectionError, e:
#         print "connection error: " + str(e)
#         build_resp['status'] = 'Connection Error'
#         build_resp['message'] = 'Error encountered while connecting to printer ' + printer_id + ': ' + str(e)
#         status_code = '409'
#     except LookupError, e:
#         print "lookup error: " + str(e)
#         build_resp['status'] = 'Command Error'
#         build_resp['message'] = 'Invalid Command: ' + str(e)
#         status_code = '400'
#
#     response_str = json.dumps(build_resp, sort_keys=False)
#     response = make_response(response_str, status_code)
#     return response
#
#     def get_printer_api_key(printer_id):
#         return printer_info.get_x_api_key(printer_id)
#         #return printer_id_dict[printer_id]["X-Api-Key"]
#
#     def get_printer_address(printer_id):
#         return printer_info.get_ip_address(printer_id)
#
#         #return printer_id_dict[printer_id]["ip_address"]
#
#     def get_info_from_command(command, printer_received_dict, job_received_dict):
#         #print command + '\n'
#         if command == 'job_name':
#             return job_received_dict['job']['file']['name']
#         elif command == 'time_remaining':
#             return job_received_dict['progress']['printTimeLeft']
#         elif command == 'progress':
#             return job_received_dict['progress']
#         elif command == 'bed_temp':
#             return printer_received_dict['temperature']['bed']
#         elif command == 'extruder_temps':
#             result = printer_received_dict['temperature'].copy() # need to try this on a multiple-extruder printer.
#             if 'bed' in result.keys():
#                 del result['bed']
#             return result
#         else:
#             #print "failed on: " + command
#             raise LookupError(command)







