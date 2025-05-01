from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ExchangeProgram(db.Model):
    __tablename__ = 'exchange_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    partner_institution_id = db.Column(db.Integer, db.ForeignKey('partner_institutions.id'), nullable=False)
    program_type = db.Column(db.String(50), nullable=False)  # semester, year, summer
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    requirements = db.Column(db.Text)  # JSON string of requirements
    status = db.Column(db.String(20), default='active')  # active, inactive, full
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    partner_institution = db.relationship('PartnerInstitution', backref=db.backref('exchange_programs', lazy=True))

class PartnerInstitution(db.Model):
    __tablename__ = 'partner_institutions'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    website = db.Column(db.String(255))
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(50))
    agreement_start_date = db.Column(db.DateTime)
    agreement_end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ExchangeApplication(db.Model):
    __tablename__ = 'exchange_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('exchange_programs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, withdrawn
    motivation_statement = db.Column(db.Text)
    academic_transcript = db.Column(db.String(255))  # file path
    recommendation_letter = db.Column(db.String(255))  # file path
    language_proficiency = db.Column(db.String(50))
    additional_documents = db.Column(db.Text)  # JSON string of additional documents
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    program = db.relationship('ExchangeProgram', backref=db.backref('applications', lazy=True))
    user = db.relationship('User', backref=db.backref('exchange_applications', lazy=True))

class VisaApplication(db.Model):
    __tablename__ = 'visa_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    visa_type = db.Column(db.String(50), nullable=False)  # student, work, tourist
    country = db.Column(db.String(100), nullable=False)
    application_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    passport_number = db.Column(db.String(50))
    passport_expiry = db.Column(db.DateTime)
    visa_expiry = db.Column(db.DateTime)
    documents = db.Column(db.Text)  # JSON string of submitted documents
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('visa_applications', lazy=True))

class InternationalStudent(db.Model):
    __tablename__ = 'international_students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    country_of_origin = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    passport_number = db.Column(db.String(50))
    passport_expiry = db.Column(db.DateTime)
    visa_type = db.Column(db.String(50))
    visa_expiry = db.Column(db.DateTime)
    arrival_date = db.Column(db.DateTime)
    departure_date = db.Column(db.DateTime)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(50))
    emergency_contact_email = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, graduated, withdrawn
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('international_profile', lazy=True))

class LanguageProficiency(db.Model):
    __tablename__ = 'language_proficiencies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    proficiency_level = db.Column(db.String(20), nullable=False)  # A1, A2, B1, B2, C1, C2
    test_type = db.Column(db.String(50))  # TOEFL, IELTS, etc.
    score = db.Column(db.Float)
    test_date = db.Column(db.DateTime)
    certificate_path = db.Column(db.String(255))  # file path
    status = db.Column(db.String(20), default='active')  # active, expired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('language_proficiencies', lazy=True))

class CulturalEvent(db.Model):
    __tablename__ = 'cultural_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # workshop, festival, orientation
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    target_audience = db.Column(db.String(100))  # international, all students
    status = db.Column(db.String(20), default='planned')  # planned, ongoing, completed, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_cultural_events', lazy=True))

class EventRegistration(db.Model):
    __tablename__ = 'cultural_event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('cultural_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship('CulturalEvent', backref=db.backref('registrations', lazy=True))
    user = db.relationship('User', backref=db.backref('cultural_event_registrations', lazy=True)) 