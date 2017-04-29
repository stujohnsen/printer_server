import json, threading, Queue
import octoprint_client
from sockjs.tornado import SockJSRouter, SockJSConnection
from tornado import web, ioloop
from sqlalchemy.orm import sessionmaker

main_alive = False
restart_main = False
available_printers = {}
client_threads = {}
message_queue = Queue.Queue()

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
                                                'printer_type' : current_printer_client.printer_type,
                                                'horizontal_flip' : current_printer_client.horizontal_flip,
                                                'vertical_flip' : current_printer_client.vertical_flip,
                                                }
        to_send = json.dumps({'message_type' : 'on_server_connect',
                              'num_printers' : str(len(available_printers)),
                              'message' : printer_info_to_send})
        self.send(to_send)

    def on_message(self, message):
        pass
        # this method has been removed for the time being. In future implementation,
        # it will need to process incoming messages from web clients and
        # make appropriate printer requests and database changes.

    def on_close(self):
        # If client disconnects, remove it from the clients list
        self.clients.remove(self)

    # track connected clients
    @classmethod
    def dump_stats(cls):
        print 'Clients: %d' % (len(cls.clients))


# OctoPrint client wrapper object for spinning off a connetion thread and
# storing necessary database related information
class client_wrapper(object):
    def __init__(self, printer_id, url, x_api_key, camera_rotation, printer_name, printer_type, horizontal_flip, vertical_flip):
        self.printer_id = printer_id
        self.client = octoprint_client.Client("http://" + url, x_api_key)
        self.camera_rotation = camera_rotation
        self.printer_name = printer_name
        self.printer_type = printer_type
        self.horizontal_flip = horizontal_flip
        self.vertical_flip = vertical_flip
        self.socket = None
        self.is_connected = False

    def connect_client(self):

        if self.is_connected == True:
            return

        def on_heartbeat(ws):
            to_send = {'printer_id': self.printer_id,
                                 'message_type': "heartbeat",
                                 'message': ""}

            message_queue.put(to_send)

        def on_message(ws, internal_type, internal_message):

            to_send = {'printer_id': self.printer_id,
                       'message_type': internal_type,
                       'message': internal_message}

            message_queue.put(to_send)

        def on_open(ws):
            print("{}: open").format(self.printer_id)

        def on_close(ws):
            print("{}: closed").format(self.printer_id)
            self.reconnnect_client()

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

# create the OctoPrint client router for data broadcast
octoRouter = SockJSRouter(SiteConnectionSocket, '/sockJS', dict())

def start_socket_server():

    import models

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
                'printer_type': str(p.printer_type),
                'horizontal_flip': str(p.horizontal_flip),
                'vertical_flip': str(p.vertical_flip),
                }
        printer_set[str(p.printer_id)] = info


    # Create Tornado web.Application
    tornado_server = web.Application(octoRouter.urls)

    #  Make application listen on port 8080
    tornado_server.listen(8080)

    # Every 1 second dump current client count
    ioloop.PeriodicCallback(SiteConnectionSocket.dump_stats, 5000).start()
    #
    # Start IOLoop
    router_thread = threading.Thread(target=ioloop.IOLoop.instance().start, args=())
    router_thread.start()

    # initialize client connections from database information
    for p in printer_set:
        current_info = printer_set[p]
        client = client_wrapper(current_info['printer_id'],
                                current_info['url'],
                                current_info['x_api_key'],
                                current_info['camera_rotation'],
                                current_info['printer_name'],
                                current_info['printer_type'],
                                current_info['horizontal_flip'],
                                current_info['vertical_flip'])
        available_printers[current_info['printer_id']] = client
        client_thread = threading.Thread(target=client.connect_client, args=())
        client_thread.start()
        client_threads[current_info['printer_id']] = client_thread

# while there is any information in the message queue, broadcast to all clients
def send_messages():
    while True:
        if message_queue.qsize() > 0:
            to_send = message_queue.get()
            octoRouter.broadcast(octoRouter._connection.clients, json.dumps(to_send))

def stop_socket_server():
    for a in available_printers:
        current = available_printers[a]
        current.disconnect_client()
    for c in client_threads:
        client_threads[c].join()

def run_main():

    global main_alive, restart_main

    send_messages_thread = threading.Thread(target=send_messages)

    if main_alive == False:
        try:
            start_socket_server()
            send_messages_thread.start()
            main_alive = True
            restart_main = False
        except AssertionError:
            send_messages_thread.join()
            send_messages_thread.start()
            stop_socket_server()
            restart_main = True
            main_alive = False

if __name__ == '__main__':

    main_thread = threading.Thread(target=run_main)

    while True:
        if main_alive == True:
            pass
        elif restart_main == True:
            main_thread.join()
        else:
            main_thread.start()
