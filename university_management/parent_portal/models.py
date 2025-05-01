from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Parent(db.Model):
    __tablename__ = 'parents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)  # mother, father, guardian
    occupation = db.Column(db.String(100))
    employer = db.Column(db.String(100))
    work_phone = db.Column(db.String(50))
    work_email = db.Column(db.String(100))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    preferred_contact_method = db.Column(db.String(50))  # email, phone, sms
    preferred_language = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('parent_profile', lazy=True))

class StudentParent(db.Model):
    __tablename__ = 'student_parents'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)  # mother, father, guardian
    is_primary = db.Column(db.Boolean, default=False)
    has_custody = db.Column(db.Boolean, default=True)
    can_view_grades = db.Column(db.Boolean, default=True)
    can_view_attendance = db.Column(db.Boolean, default=True)
    can_view_finances = db.Column(db.Boolean, default=True)
    can_view_health = db.Column(db.Boolean, default=True)
    can_view_discipline = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('parents', lazy=True))
    parent = db.relationship('Parent', foreign_keys=[parent_id], backref=db.backref('students', lazy=True))

class ParentNotification(db.Model):
    __tablename__ = 'parent_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # academic, attendance, financial, etc.
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    action_required = db.Column(db.Boolean, default=False)
    action_taken = db.Column(db.Boolean, default=False)
    action_taken_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent = db.relationship('Parent', backref=db.backref('notifications', lazy=True))

class ParentAccessLog(db.Model):
    __tablename__ = 'parent_access_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    access_type = db.Column(db.String(50), nullable=False)  # login, view_grades, view_attendance, etc.
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(255))
    status = db.Column(db.String(20), default='success')  # success, failed
    details = db.Column(db.Text)  # JSON string of additional details
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    parent = db.relationship('Parent', backref=db.backref('access_logs', lazy=True))

class ParentMeeting(db.Model):
    __tablename__ = 'parent_meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meeting_type = db.Column(db.String(50), nullable=False)  # academic, behavioral, general
    scheduled_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    location = db.Column(db.String(200))
    purpose = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('User', foreign_keys=[student_id], backref=db.backref('parent_meetings', lazy=True))
    parent = db.relationship('Parent', backref=db.backref('meetings', lazy=True))
    staff = db.relationship('User', foreign_keys=[staff_id], backref=db.backref('conducted_meetings', lazy=True))

class ParentFeedback(db.Model):
    __tablename__ = 'parent_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    feedback_type = db.Column(db.String(50), nullable=False)  # academic, facilities, services, etc.
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolution = db.Column(db.Text)
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent = db.relationship('Parent', backref=db.backref('feedback', lazy=True))
    assignee = db.relationship('User', backref=db.backref('assigned_feedback', lazy=True))

class ParentDocument(db.Model):
    __tablename__ = 'parent_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # consent, authorization, etc.
    title = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)  # in bytes
    is_required = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='active')  # active, expired, revoked
    expiry_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    parent = db.relationship('Parent', backref=db.backref('documents', lazy=True)) 