from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.String(50), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    preferences = db.Column(db.Text)  # JSON string
    
    # Relationships
    hazard_reports = db.relationship('HazardReport', backref='user_session', lazy=True)
    chat_messages = db.relationship('ChatMessage', backref='user_session', lazy=True)
    
    def __repr__(self):
        return f'<UserSession {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'preferences': json.loads(self.preferences) if self.preferences else {}
        }
    
    def update_activity(self):
        self.last_active = datetime.utcnow()
        db.session.commit()

class HazardReport(db.Model):
    __tablename__ = 'hazard_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_session_id = db.Column(db.String(50), db.ForeignKey('user_sessions.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location_lat = db.Column(db.Numeric(10, 8))
    location_lng = db.Column(db.Numeric(11, 8))
    address = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(20), default='submitted')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<HazardReport {self.id}: {self.category}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_session_id': self.user_session_id,
            'category': self.category,
            'description': self.description,
            'location_lat': float(self.location_lat) if self.location_lat else None,
            'location_lng': float(self.location_lng) if self.location_lng else None,
            'address': self.address,
            'image_url': self.image_url,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class EmergencyAlert(db.Model):
    __tablename__ = 'emergency_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # weather, traffic, emergency, etc.
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    area_affected = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<EmergencyAlert {self.id}: {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'area_affected': self.area_affected,
            'active': self.active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }
    
    @classmethod
    def get_active_alerts(cls):
        now = datetime.utcnow()
        return cls.query.filter(
            cls.active == True,
            db.or_(cls.expires_at.is_(None), cls.expires_at > now)
        ).order_by(cls.created_at.desc()).all()

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_session_id = db.Column(db.String(50), db.ForeignKey('user_sessions.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    intent = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatMessage {self.id}: {self.intent}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_session_id': self.user_session_id,
            'message': self.message,
            'response': self.response,
            'intent': self.intent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Predefined categories for hazard reports
HAZARD_CATEGORIES = [
    'road_traffic',
    'infrastructure',
    'environmental',
    'public_safety',
    'other'
]

# Predefined alert types
ALERT_TYPES = [
    'weather',
    'traffic',
    'emergency',
    'public_safety',
    'infrastructure',
    'community'
]

# Severity levels
SEVERITY_LEVELS = [
    'low',
    'medium',
    'high',
    'critical'
]

