import server
import os

upload_folder = server.app.config['UPLOAD_FOLDER']

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

server.app.run()
