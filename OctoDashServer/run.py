import os, signal, sys, threading
from app import create_app
from aggregate_socket_server import start_socket_server, stop_socket_server
from multiprocessing import Process


config_name = os.getenv('FLASK_CONFIG')
#config_name = 'production'
config_name = 'development'
app = create_app(config_name)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=6286)

    # def app_process_run(debug, host, port):
    #     app.run(debug = debug, host=host, port = port)

    # appProcess = threading.Thread(target=app.run(debug=True, host='0.0.0.0', port=6286,))
    # socket_server_process = threading.Thread(target=start_socket_server())
    # try:
        # appProcess = Process(target=app.run, args=(host="0.0.0.0", port=6286,))
        # socket_server_process.start()
        # appProcess.start()




    #
    # except:
    #     print "failure"
        # appProcess.terminate()
        # appProcess.join()
        # stop_socket_server()

    # except:
    #     e = sys.exc_info()[0]
    #     print("Caught exception:" + str(e))
        # appProcess.join()
        # socket_server_terminate()

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