import os
from werkzeug.utils import secure_filename
from flask import current_app

class FileHandler:
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'mp4', 'py', 'ipynb'}
    
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FileHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_file(file, subfolder=''):
        if file and FileHandler.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
            os.makedirs(path, exist_ok=True)
            file_path = os.path.join(path, filename)
            file.save(file_path)
            return file_path
        return None 