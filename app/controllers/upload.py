import os
import time
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app import ABSOLUTE_UPLOAD_FOLDER
from app.utils import allowed_file, api_response, upload_file_to_gcs

upload_bp = Blueprint('upload', __name__)

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return api_response(message='No file part', status=400)

    file = request.files['file']
    if file.filename == '':
        return api_response(message="No selected file", status = 400)

    if not file or not allowed_file(file.filename):
        return api_response(message=="Invalid file type", status=400)

    # Sanitise the original filename first
    sanitised_filename = secure_filename(file.filename)

    # Create an unique filename using timestamp prefix
    unique_filename = str(int(time.time())) + "_" + sanitised_filename

    # Construct the full path using the absolute upload folder path
    # filepath = os.path.join(ABSOLUTE_UPLOAD_FOLDER, unique_filename)
    
    try:
        # file.save(filepath)
        # Return the generated unique filename
        public_url = upload_file_to_gcs(file, "uploads")
        return api_response(message="Upload successful", data={'public_url': public_url}, status=201)
    except Exception as e:
        # Log the error ideally
        print(f"Error uploading file: {e}")
        return api_response(message="Error saving file", status=500)
        