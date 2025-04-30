import os
import uuid
import logging
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory

from app import db
from models import DetectionResult
from deepfake_detector import DeepfakeDetector

# Initialize logger
logger = logging.getLogger(__name__)

# Initialize the deepfake detector
detector = DeepfakeDetector()

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv'}

def allowed_file(filename, file_type):
    """Check if the file has an allowed extension"""
    if file_type == 'image':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    elif file_type == 'video':
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS
    return False

def setup_routes(app):
    @app.route('/')
    def index():
        """Render the index page"""
        return render_template('index.html')
    
    @app.route('/history')
    def history():
        """Render the history page with all past detection results"""
        results = DetectionResult.query.order_by(DetectionResult.timestamp.desc()).all()
        return render_template('history.html', results=results)
    
    @app.route('/result/<int:result_id>')
    def view_result(result_id):
        """View a specific detection result"""
        result = DetectionResult.query.get_or_404(result_id)
        return render_template('result.html', result=result)
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """Serve uploaded files"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    @app.route('/api/detect', methods=['POST'])
    def detect_deepfake():
        """API endpoint to detect deepfakes in uploaded media"""
        # Check if a file was uploaded
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if the user submitted an empty form
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            # Determine file type (image or video)
            file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            
            if file_extension in ALLOWED_IMAGE_EXTENSIONS:
                file_type = 'image'
            elif file_extension in ALLOWED_VIDEO_EXTENSIONS:
                file_type = 'video'
            else:
                flash('File type not supported')
                return redirect(url_for('index'))
            
            # Create a unique filename to prevent overwrites
            original_filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            # Save the file
            file.save(file_path)
            logger.debug(f"Saved file to {file_path}")
            
            # Analyze the file
            if file_type == 'image':
                result, confidence = detector.analyze_image(file_path)
            else:  # video
                result, confidence = detector.analyze_video(file_path)
            
            logger.debug(f"Detection result: {result} with confidence {confidence}")
            
            # Save the result to the database
            db_result = DetectionResult(
                filename=unique_filename,
                file_type=file_type,
                original_filename=original_filename,
                result=result,
                confidence=confidence
            )
            db.session.add(db_result)
            db.session.commit()
            
            # Redirect to the result page
            return redirect(url_for('view_result', result_id=db_result.id))
        
        return redirect(url_for('index'))
