import datetime
from app import db

class DetectionResult(db.Model):
    """Model for storing deepfake detection results"""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # 'image' or 'video'
    original_filename = db.Column(db.String(255), nullable=False)
    result = db.Column(db.String(20), nullable=False)  # 'real' or 'fake'
    confidence = db.Column(db.Float, nullable=False)  # Confidence score (0-1)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<DetectionResult {self.id} - {self.original_filename} - {self.result}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "file_type": self.file_type,
            "original_filename": self.original_filename,
            "result": self.result,
            "confidence": self.confidence,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
