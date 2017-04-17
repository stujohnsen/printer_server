import os, signal
from app import create_app
from aggregate_socket_server import start_socket_server
from multiprocessing import Process

config_name = os.getenv('FLASK_CONFIG')
#config_name = 'production'
config_name = 'development'
app = create_app(config_name)
def app_process_wrapper(debug, host, port):
    app.run(debug = debug, host=host, port = port)

if __name__ == '__main__':

    process_signal_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGINT, process_signal_handler)

    appProcess = Process(target=app_process_wrapper, args=(True, '0.0.0.0', 6286,))

    try:

        # appProcess = Process(target=app.run, args=(host="0.0.0.0", port=6286,))
        appProcess.start()
        # socketProcess = Process(target=start_socket_server)
        # socketProcess.start()

        # app.run(debug=True, port=6286)
        start_socket_server()

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        appProcess.terminate()
        
    # else:
    #     print("Normal termination")
    #     pool.close()
    # pool.join()



# config_name = 'development' #os.getenv('FLASK_CONFIG')
# app = create_app(config_name)
# 
# if __name__ == '__main__':
#     print "Attempting to start printer server...\n"
#     app.run()