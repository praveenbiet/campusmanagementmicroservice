from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class AccessLog(db.Model):
    __tablename__ = 'access_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 compatible
    user_agent = db.Column(db.String(255))
    action = db.Column(db.String(50), nullable=False)  # login, logout, access, modify
    resource = db.Column(db.String(255))  # URL or resource accessed
    status = db.Column(db.String(20), nullable=False)  # success, failure
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('access_logs', lazy=True))

class SecurityIncident(db.Model):
    __tablename__ = 'security_incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    incident_type = db.Column(db.String(50), nullable=False)  # unauthorized_access, data_breach, suspicious_activity
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    status = db.Column(db.String(20), default='open')  # open, investigating, resolved, closed
    reported_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolution = db.Column(db.Text)
    resolution_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    reporter = db.relationship('User', foreign_keys=[reported_by], backref=db.backref('reported_incidents', lazy=True))
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref=db.backref('assigned_incidents', lazy=True))

class AccessControl(db.Model):
    __tablename__ = 'access_controls'
    
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(255), nullable=False)
    permission = db.Column(db.String(20), nullable=False)  # read, write, delete, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SecurityPolicy(db.Model):
    __tablename__ = 'security_policies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    policy_type = db.Column(db.String(50), nullable=False)  # password, access, data_protection
    content = db.Column(db.Text, nullable=False)
    version = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_policies', lazy=True))

class SecurityAudit(db.Model):
    __tablename__ = 'security_audits'
    
    id = db.Column(db.Integer, primary_key=True)
    audit_type = db.Column(db.String(50), nullable=False)  # system, access, compliance
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, failed
    findings = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    auditor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    auditor = db.relationship('User', backref=db.backref('conducted_audits', lazy=True))

class SecurityAlert(db.Model):
    __tablename__ = 'security_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # suspicious_login, policy_violation, system_alert
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    status = db.Column(db.String(20), default='active')  # active, acknowledged, resolved
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    acknowledged_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    acknowledger = db.relationship('User', foreign_keys=[acknowledged_by], backref=db.backref('acknowledged_alerts', lazy=True))
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref=db.backref('resolved_alerts', lazy=True)) 