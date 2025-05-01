from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Applicant(db.Model):
    __tablename__ = 'applicants'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('applicant', uselist=False))

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    intake_term = db.Column(db.String(20), nullable=False)  # e.g., Fall 2024
    application_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='draft')  # draft, submitted, under_review, accepted, rejected
    documents = db.Column(db.Text)  # JSON string of required documents
    test_scores = db.Column(db.Text)  # JSON string of test scores (SAT, TOEFL, etc.)
    previous_education = db.Column(db.Text)  # JSON string of previous education
    recommendation_letters = db.Column(db.Text)  # JSON string of recommendation letters
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    applicant = db.relationship('Applicant', backref=db.backref('applications', lazy=True))
    program = db.relationship('Program', backref=db.backref('applications', lazy=True))

class AdmissionDecision(db.Model):
    __tablename__ = 'admission_decisions'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    decision = db.Column(db.String(20), nullable=False)  # accepted, rejected, waitlisted
    decision_date = db.Column(db.Date, nullable=False)
    decision_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.Column(db.Text)
    scholarship_offered = db.Column(db.Float)
    conditions = db.Column(db.Text)  # JSON string of conditions if any
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = db.relationship('Application', backref=db.backref('decision', uselist=False))
    decision_maker = db.relationship('User', backref=db.backref('admission_decisions', lazy=True))

class ApplicationDocument(db.Model):
    __tablename__ = 'application_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, verified, rejected
    verified_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = db.relationship('Application', backref=db.backref('documents', lazy=True))
    verifier = db.relationship('User', backref=db.backref('verified_documents', lazy=True))

class ApplicationFee(db.Model):
    __tablename__ = 'application_fees'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    application = db.relationship('Application', backref=db.backref('fee', uselist=False)) 