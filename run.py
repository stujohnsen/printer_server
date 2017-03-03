from app import app

if __name__ == '__main__':
    app.run(debug=True, port=6286)



# config_name = 'development' #os.getenv('FLASK_CONFIG')
# app = create_app(config_name)
# 
# if __name__ == '__main__':
#     print "Attempting to start printer server...\n"
#     app.run()