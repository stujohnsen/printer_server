from app import create_app
from aggregate_socket_server import start_socket_server
from multiprocessing import Process

app = create_app()
def app_process_wrapper(debug, host, port):
    app.run(debug = debug, host=host, port = port)

if __name__ == '__main__':
    appProcess = Process(target=app_process_wrapper, args=(True,'0.0.0.0', 6286,))
    appProcess.start()
    # socketProcess = Process(target=start_socket_server)
    # socketProcess.start()

    # app.run(debug=True, port=6286)
    start_socket_server()




# config_name = 'development' #os.getenv('FLASK_CONFIG')
# app = create_app(config_name)
# 
# if __name__ == '__main__':
#     print "Attempting to start printer server...\n"
#     app.run()