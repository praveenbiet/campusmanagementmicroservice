from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alumni(db.Model):
    __tablename__ = 'alumni'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    major = db.Column(db.String(100))
    current_employer = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    location = db.Column(db.String(100))
    is_mentor = db.Column(db.Boolean, default=False)
    mentor_availability = db.Column(db.String(50))  # full_time, part_time, not_available
    interests = db.Column(db.Text)  # JSON string of interests
    social_media = db.Column(db.Text)  # JSON string of social media links
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('alumni_profile', uselist=False))

class AlumniEvent(db.Model):
    __tablename__ = 'alumni_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # reunion, networking, workshop
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

    organizer = db.relationship('User', backref=db.backref('organized_alumni_events', lazy=True))

class EventRegistration(db.Model):
    __tablename__ = 'alumni_event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('alumni_events.id'), nullable=False)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship('AlumniEvent', backref=db.backref('registrations', lazy=True))
    alumni = db.relationship('Alumni', backref=db.backref('event_registrations', lazy=True))

class Donation(db.Model):
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    donation_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    purpose = db.Column(db.String(100))  # general, scholarship, research, building
    is_recurring = db.Column(db.Boolean, default=False)
    recurring_frequency = db.Column(db.String(20))  # monthly, quarterly, yearly
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    alumni = db.relationship('Alumni', backref=db.backref('donations', lazy=True))

class MentorshipProgram(db.Model):
    __tablename__ = 'mentorship_programs'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    max_participants = db.Column(db.Integer)
    status = db.Column(db.String(20), default='active')  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Mentorship(db.Model):
    __tablename__ = 'mentorships'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('mentorship_programs.id'), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey('alumni.id'), nullable=False)
    mentee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, terminated
    goals = db.Column(db.Text)
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    program = db.relationship('MentorshipProgram', backref=db.backref('mentorships', lazy=True))
    mentor = db.relationship('Alumni', backref=db.backref('mentoring_relationships', lazy=True))
    mentee = db.relationship('User', backref=db.backref('mentorship_relationships', lazy=True)) 