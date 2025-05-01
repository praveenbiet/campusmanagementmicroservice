from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    job_type = db.Column(db.String(50), nullable=False)  # full_time, part_time, contract
    location = db.Column(db.String(100))
    salary_min = db.Column(db.Float)
    salary_max = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, closed, draft
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = db.relationship('Company', backref=db.backref('job_postings', lazy=True))
    poster = db.relationship('User', backref=db.backref('posted_jobs', lazy=True))

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    website = db.Column(db.String(255))
    logo_path = db.Column(db.String(255))
    contact_name = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class JobApplication(db.Model):
    __tablename__ = 'job_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_path = db.Column(db.String(255))
    cover_letter = db.Column(db.Text)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')  # submitted, under_review, shortlisted, rejected, hired
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    job = db.relationship('JobPosting', backref=db.backref('applications', lazy=True))
    user = db.relationship('User', backref=db.backref('job_applications', lazy=True))

class Internship(db.Model):
    __tablename__ = 'internships'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    responsibilities = db.Column(db.Text)
    duration = db.Column(db.String(50))  # e.g., "3 months", "6 months"
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(100))
    stipend = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    application_deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, closed, draft
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = db.relationship('Company', backref=db.backref('internships', lazy=True))
    poster = db.relationship('User', backref=db.backref('posted_internships', lazy=True))

class InternshipApplication(db.Model):
    __tablename__ = 'internship_applications'
    
    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_path = db.Column(db.String(255))
    cover_letter = db.Column(db.Text)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='submitted')  # submitted, under_review, shortlisted, rejected, accepted
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    internship = db.relationship('Internship', backref=db.backref('applications', lazy=True))
    user = db.relationship('User', backref=db.backref('internship_applications', lazy=True))

class CareerEvent(db.Model):
    __tablename__ = 'career_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # job_fair, workshop, networking
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    organizer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    capacity = db.Column(db.Integer)
    registration_deadline = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, ongoing, completed, cancelled
    registration_fee = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    organizer = db.relationship('User', backref=db.backref('organized_career_events', lazy=True))

class EventRegistration(db.Model):
    __tablename__ = 'career_event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('career_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship('CareerEvent', backref=db.backref('registrations', lazy=True))
    user = db.relationship('User', backref=db.backref('career_event_registrations', lazy=True)) 