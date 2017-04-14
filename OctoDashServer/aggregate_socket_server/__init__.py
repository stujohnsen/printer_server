import json, threading
import octoprint_client
from sockjs.tornado import SockJSRouter, SockJSConnection
from tornado import web, ioloop
from sqlalchemy.orm import sessionmaker

import models

available_printers = {}

class SiteConnectionSocket(SockJSConnection):
    """Echo connection implementation"""
    clients = set()

    def on_open(self, info):
        # When new client comes in, will add it to the clients list
        self.clients.add(self)

        printer_info_to_send = {}

        for available in available_printers:
            current_printer_client = available_printers[available]
            printer_info_to_send[available] = { 'printer_id' : current_printer_client.printer_id,
                                                'url' : current_printer_client.client.baseurl,
                                                'is_connected' : current_printer_client.is_connected,
                                                'camera_rotation' : current_printer_client.camera_rotation,
                                                'printer_name' : current_printer_client.printer_name,
                                                'printer_type' : current_printer_client.printer_type
                                                }
        to_send = json.dumps({'message_type' : 'on_server_connect',
                              'num_printers' : str(len(available_printers)),
                              'message' : printer_info_to_send})
        self.send(to_send)

    def on_message(self, msg):
        # For every incoming message, broadcast it to all clients
        self.broadcast(self.clients, msg)

    def on_close(self):
        # If client disconnects, remove him from the clients list
        self.clients.remove(self)

    @classmethod
    def dump_stats(cls):
        print 'Clients: %d' % (len(cls.clients))

octoRouter = SockJSRouter(SiteConnectionSocket, '/sockJS', dict())

def start_socket_server():

    Session = sessionmaker(bind=models.engine)
    session = Session()

    printer_set = {}
    printer_list = session.query(models.Printer_db).order_by(models.Printer_db.printer_id)
    for p in printer_list:
        info = {'printer_id': str(p.printer_id),
                'url': str(p.url),
                'x_api_key': str(p.x_api_key),
                'camera_rotation': str(p.camera_rotation),
                'printer_name': str(p.printer_name),
                'printer_type': str(p.printer_type)
                }
        printer_set[str(p.printer_id)] = info

    # 2. Create Tornado web.Application
    tornado_server = web.Application(octoRouter.urls)
    #
    # # 3. Make application listen on port 8080
    tornado_server.listen(8080)
    #
    # # 4. Every 1 second dump current client count
    ioloop.PeriodicCallback(SiteConnectionSocket.dump_stats, 5000).start()
    #
    # # 5. Start IOLoop
    router_thread = threading.Thread(target=ioloop.IOLoop.instance().start, args=())
    router_thread.start()



    for p in printer_set:
        current_info = printer_set[p]
        client = client_wrapper(current_info['printer_id'],
                                current_info['url'],
                                current_info['x_api_key'],
                                current_info['camera_rotation'],
                                current_info['printer_name'],
                                current_info['printer_type'])
        available_printers[current_info['printer_id']] = client
        client_thread = threading.Thread(target=client.connect_client, args=())
        client_thread.start()


class client_wrapper(object):
    def __init__(self, printer_id, url, x_api_key, camera_rotation, printer_name, printer_type):
        self.printer_id = printer_id
        self.client = octoprint_client.Client("http://" + url, x_api_key)
        self.camera_rotation = camera_rotation
        self.printer_name = printer_name
        self.printer_type = printer_type
        self.socket = None
        self.is_connected = False

    def connect_client(self):

        if self.is_connected == True:
            return

        def on_heartbeat(ws):
            pass
            # print("{}: <3").format(self.printer_id)
            # m = str("{}: <3").format(self.printer_id)

            # octoRouter.broadcast(octoRouter._connection.clients, m)
            # aggregate_socket.send("{}: <3").format(self.printer_id)

        def on_message(ws, internal_type, internal_message):

            # m = str("{}: message, type: {}, message: {!r}").format(self.printer_id, internal_type, internal_message)

            to_send = {'printer_id': self.printer_id,
                       'message_type': internal_type,
                       'message': internal_message}

            print(json.dumps(to_send))
            octoRouter.broadcast(octoRouter._connection.clients, json.dumps(to_send))

        def on_open(ws):
            print("{}: open").format(self.printer_id)

        def on_close(ws):
            print("{}: closed").format(self.printer_id)

        def on_error(ws, error):
            print("{}: error: {}").format(self.printer_id, error)

        self.socket = self.client.create_socket(on_open=on_open,
                                                on_heartbeat=on_heartbeat,
                                                on_message=on_message,
                                                on_close=on_close,
                                                on_error=on_error)

        self.is_connected = self.socket.is_connected

        if self.is_connected == True:
            self.wait_thread = threading.Thread(target=self.socket.wait)
            self.wait_thread.start()

    def reconnnect_client(self):
        self.socket.reconnect(10, True)

        if self.socket.is_connected:
            self.is_connected == True
            self.wait_thread = threading.Thread(target=self.socket.wait)
            self.wait_thread.start()

    def disconnect_client(self):
        self.socket.disconnect()
        self.wait_thread.join(0)
        self.is_connected = False



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

