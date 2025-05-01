from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Policy(db.Model):
    __tablename__ = 'policies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    policy_type = db.Column(db.String(50), nullable=False)  # academic, administrative, financial
    version = db.Column(db.String(20), nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    review_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, draft, archived
    document_path = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', foreign_keys=[created_by], backref=db.backref('created_policies', lazy=True))
    approver = db.relationship('User', foreign_keys=[approved_by], backref=db.backref('approved_policies', lazy=True))

class Committee(db.Model):
    __tablename__ = 'committees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    committee_type = db.Column(db.String(50), nullable=False)  # academic, administrative, advisory
    chair_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    chair = db.relationship('User', backref=db.backref('chaired_committees', lazy=True))

class CommitteeMember(db.Model):
    __tablename__ = 'committee_members'
    
    id = db.Column(db.Integer, primary_key=True)
    committee_id = db.Column(db.Integer, db.ForeignKey('committees.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # member, secretary, treasurer
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    committee = db.relationship('Committee', backref=db.backref('members', lazy=True))
    user = db.relationship('User', backref=db.backref('committee_memberships', lazy=True))

class Meeting(db.Model):
    __tablename__ = 'meetings'
    
    id = db.Column(db.Integer, primary_key=True)
    committee_id = db.Column(db.Integer, db.ForeignKey('committees.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    meeting_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    meeting_type = db.Column(db.String(50), nullable=False)  # regular, special, emergency
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    committee = db.relationship('Committee', backref=db.backref('meetings', lazy=True))

class MeetingAgenda(db.Model):
    __tablename__ = 'meeting_agendas'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    item_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    presenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    duration = db.Column(db.Integer)  # in minutes
    status = db.Column(db.String(20), default='pending')  # pending, completed, postponed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meeting = db.relationship('Meeting', backref=db.backref('agenda_items', lazy=True))
    presenter = db.relationship('User', backref=db.backref('presented_agenda_items', lazy=True))

class MeetingMinutes(db.Model):
    __tablename__ = 'meeting_minutes'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    action_items = db.Column(db.Text)
    decisions = db.Column(db.Text)
    next_meeting_date = db.Column(db.DateTime)
    prepared_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approval_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, approved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meeting = db.relationship('Meeting', backref=db.backref('minutes', lazy=True))
    preparer = db.relationship('User', foreign_keys=[prepared_by], backref=db.backref('prepared_minutes', lazy=True))
    approver = db.relationship('User', foreign_keys=[approved_by], backref=db.backref('approved_minutes', lazy=True))

class MeetingAttendance(db.Model):
    __tablename__ = 'meeting_attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    attendance_status = db.Column(db.String(20), nullable=False)  # present, absent, excused
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    meeting = db.relationship('Meeting', backref=db.backref('attendance', lazy=True))
    user = db.relationship('User', backref=db.backref('meeting_attendance', lazy=True)) 