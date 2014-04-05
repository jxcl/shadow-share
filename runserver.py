from server import main
import os

upload_folder = main.app.config['UPLOAD_FOLDER']

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

main.app.run()
