from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EnergyUsage(db.Model):
    __tablename__ = 'energy_usage'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    energy_type = db.Column(db.String(50), nullable=False)  # electricity, gas, water
    reading_date = db.Column(db.DateTime, nullable=False)
    reading_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)  # kWh, m³, etc.
    cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    source = db.Column(db.String(100))  # meter_id, provider, etc.
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('energy_usage', lazy=True))

class EnergyGoal(db.Model):
    __tablename__ = 'energy_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    energy_type = db.Column(db.String(50), nullable=False)
    target_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    current_value = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, achieved, failed
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('energy_goals', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_energy_goals', lazy=True))

class WasteManagement(db.Model):
    __tablename__ = 'waste_management'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)  # paper, plastic, organic, etc.
    collection_date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    disposal_method = db.Column(db.String(100))
    recycling_rate = db.Column(db.Float)  # percentage
    cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('waste_management', lazy=True))

class WasteReductionGoal(db.Model):
    __tablename__ = 'waste_reduction_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'), nullable=False)
    waste_type = db.Column(db.String(50), nullable=False)
    target_reduction = db.Column(db.Float, nullable=False)  # percentage
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    current_reduction = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, achieved, failed
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    building = db.relationship('Building', backref=db.backref('waste_reduction_goals', lazy=True))
    creator = db.relationship('User', backref=db.backref('created_waste_goals', lazy=True))

class SustainabilityProject(db.Model):
    __tablename__ = 'sustainability_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_type = db.Column(db.String(50), nullable=False)  # energy, waste, water, etc.
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    budget = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='planned')  # planned, in_progress, completed, cancelled
    impact_metrics = db.Column(db.Text)  # JSON string of impact metrics
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_projects', lazy=True))

class ProjectTeam(db.Model):
    __tablename__ = 'project_teams'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('sustainability_projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = db.relationship('SustainabilityProject', backref=db.backref('team_members', lazy=True))
    user = db.relationship('User', backref=db.backref('project_roles', lazy=True))

class SustainabilityEvent(db.Model):
    __tablename__ = 'sustainability_events'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)  # workshop, campaign, awareness
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    capacity = db.Column(db.Integer)
    status = db.Column(db.String(20), default='planned')  # planned, ongoing, completed, cancelled
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_events', lazy=True))

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('sustainability_events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    event = db.relationship('SustainabilityEvent', backref=db.backref('registrations', lazy=True))
    user = db.relationship('User', backref=db.backref('event_registrations', lazy=True)) 