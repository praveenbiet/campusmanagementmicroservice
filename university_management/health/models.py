from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    blood_type = db.Column(db.String(10))
    height = db.Column(db.Float)  # in cm
    weight = db.Column(db.Float)  # in kg
    allergies = db.Column(db.Text)  # JSON string of allergies
    medications = db.Column(db.Text)  # JSON string of current medications
    medical_conditions = db.Column(db.Text)  # JSON string of medical conditions
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))
    insurance_provider = db.Column(db.String(100))
    insurance_policy_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('medical_record', uselist=False))

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('health_services.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=30)  # in minutes
    reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, no_show
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('appointments', lazy=True))
    service = db.relationship('HealthService', backref=db.backref('appointments', lazy=True))
    staff = db.relationship('User', foreign_keys=[staff_id], backref=db.backref('staff_appointments', lazy=True))

class HealthService(db.Model):
    __tablename__ = 'health_services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    service_type = db.Column(db.String(50), nullable=False)  # general, dental, mental_health, emergency
    duration = db.Column(db.Integer, default=30)  # in minutes
    cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Visit(db.Model):
    __tablename__ = 'visits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False)
    visit_type = db.Column(db.String(50), nullable=False)  # walk_in, appointment, emergency
    symptoms = db.Column(db.Text)
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prescription = db.Column(db.Text)
    follow_up_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='completed')  # completed, follow_up_needed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('visits', lazy=True))
    staff = db.relationship('User', foreign_keys=[staff_id], backref=db.backref('staff_visits', lazy=True))

class Immunization(db.Model):
    __tablename__ = 'immunizations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vaccine_name = db.Column(db.String(100), nullable=False)
    date_administered = db.Column(db.Date, nullable=False)
    administered_by = db.Column(db.String(100))
    next_dose_date = db.Column(db.Date)
    batch_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('immunizations', lazy=True))

class HealthAlert(db.Model):
    __tablename__ = 'health_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # outbreak, advisory, reminder
    severity = db.Column(db.String(20), default='normal')  # low, normal, high, critical
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    target_audience = db.Column(db.String(50), default='all')  # all, students, staff
    status = db.Column(db.String(20), default='active')  # active, expired
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('health_alerts', lazy=True)) 