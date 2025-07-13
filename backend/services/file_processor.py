import os
import uuid
from werkzeug.utils import secure_filename

class FileProcessor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.allowed_extensions = {'csv', 'xlsx', 'xls'}
    
    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_file(self, file):
        print(f"Saving file: {file.filename}")
        if not self.allowed_file(file.filename):
            raise ValueError(f"File type not allowed. Supported: {', '.join(self.allowed_extensions)}")
        
        # Generate unique filename to avoid conflicts
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(self.upload_folder, unique_filename)
        
        file.save(file_path)
        return file_path
    
    def cleanup_file(self, file_path):
        print(f"Cleaning up file: {file_path}")
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not delete file {file_path}: {e}")