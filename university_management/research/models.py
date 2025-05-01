from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ResearchProject(db.Model):
    __tablename__ = 'research_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    project_type = db.Column(db.String(50), nullable=False)  # individual, collaborative, sponsored
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    principal_investigator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    budget = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    keywords = db.Column(db.String(255))  # comma-separated keywords
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = db.relationship('Department', backref=db.backref('research_projects', lazy=True))
    principal_investigator = db.relationship('User', backref=db.backref('led_projects', lazy=True))

class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('research_projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # co_investigator, researcher, assistant
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, withdrawn
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = db.relationship('ResearchProject', backref=db.backref('members', lazy=True))
    user = db.relationship('User', backref=db.backref('project_memberships', lazy=True))

class Publication(db.Model):
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.Text)
    publication_type = db.Column(db.String(50), nullable=False)  # journal, conference, book
    publication_date = db.Column(db.Date, nullable=False)
    journal_name = db.Column(db.String(200))
    conference_name = db.Column(db.String(200))
    publisher = db.Column(db.String(200))
    doi = db.Column(db.String(100))
    isbn = db.Column(db.String(20))
    issn = db.Column(db.String(20))
    volume = db.Column(db.String(20))
    issue = db.Column(db.String(20))
    pages = db.Column(db.String(50))
    status = db.Column(db.String(20), default='published')  # published, accepted, submitted
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PublicationAuthor(db.Model):
    __tablename__ = 'publication_authors'
    
    id = db.Column(db.Integer, primary_key=True)
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author_order = db.Column(db.Integer, nullable=False)
    is_corresponding_author = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    publication = db.relationship('Publication', backref=db.backref('authors', lazy=True))
    user = db.relationship('User', backref=db.backref('publications', lazy=True))

class Grant(db.Model):
    __tablename__ = 'grants'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    grant_type = db.Column(db.String(50), nullable=False)  # research, equipment, travel
    funding_agency = db.Column(db.String(200), nullable=False)
    grant_number = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='active')  # active, completed, terminated
    project_id = db.Column(db.Integer, db.ForeignKey('research_projects.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = db.relationship('ResearchProject', backref=db.backref('grants', lazy=True))

class ResearchEquipment(db.Model):
    __tablename__ = 'research_equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    equipment_type = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    purchase_date = db.Column(db.Date)
    purchase_cost = db.Column(db.Float)
    currency = db.Column(db.String(3), default='USD')
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='available')  # available, in_use, maintenance
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = db.relationship('Department', backref=db.backref('equipment', lazy=True))

class EquipmentReservation(db.Model):
    __tablename__ = 'equipment_reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_id = db.Column(db.Integer, db.ForeignKey('research_equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    equipment = db.relationship('ResearchEquipment', backref=db.backref('reservations', lazy=True))
    user = db.relationship('User', backref=db.backref('equipment_reservations', lazy=True)) 