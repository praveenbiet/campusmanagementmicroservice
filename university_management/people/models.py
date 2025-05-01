from datetime import datetime
from app import db
from sqlalchemy.dialects.sqlite import JSON
from werkzeug.security import generate_password_hash, check_password_hash

class Person(db.Model):
    __tablename__ = 'person'
    
    id = db.Column(db.String(50), primary_key=True)
    unique_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender_identity = db.Column(db.String(50))
    pronouns = db.Column(db.String(50))
    nationality = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    contact_info = db.relationship('ContactInfo', backref='person', lazy=True)
    relationships = db.relationship('Relationship', backref='person', lazy=True)
    identification_documents = db.relationship('IdentificationDocument', backref='person', lazy=True)
    profile_status = db.relationship('ProfileStatus', backref='person', lazy=True)
    biometric_data = db.relationship('BiometricData', backref='person', lazy=True)
    accessibility_needs = db.relationship('AccessibilityNeeds', backref='person', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'unique_id': self.unique_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth.isoformat(),
            'gender_identity': self.gender_identity,
            'pronouns': self.pronouns,
            'nationality': self.nationality,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ContactInfo(db.Model):
    __tablename__ = 'contact_info'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    contact_type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    geolocation = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'contact_type': self.contact_type,
            'value': self.value,
            'is_primary': self.is_primary,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'geolocation': self.geolocation,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Relationship(db.Model):
    __tablename__ = 'relationship'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id_a = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    person_id_b = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    relationship_type = db.Column(db.String(50), nullable=False)
    is_emergency_contact = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id_a': self.person_id_a,
            'person_id_b': self.person_id_b,
            'relationship_type': self.relationship_type,
            'is_emergency_contact': self.is_emergency_contact,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class IdentificationDocument(db.Model):
    __tablename__ = 'identification_document'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    document_number = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.Date)
    issue_date = db.Column(db.Date)
    issuing_authority = db.Column(db.String(255))
    document_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'document_type': self.document_type,
            'document_number': self.document_number,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'issue_date': self.issue_date.isoformat() if self.issue_date else None,
            'issuing_authority': self.issuing_authority,
            'document_url': self.document_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProfileStatus(db.Model):
    __tablename__ = 'profile_status'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    primary_role_id = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    profile_photo_url = db.Column(db.String(255))
    gdpr_consent_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'primary_role_id': self.primary_role_id,
            'status': self.status,
            'profile_photo_url': self.profile_photo_url,
            'gdpr_consent_status': self.gdpr_consent_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class BiometricData(db.Model):
    __tablename__ = 'biometric_data'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    biometric_type = db.Column(db.String(50), nullable=False)
    hash_value = db.Column(db.String(255), nullable=False)
    consent_status = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'biometric_type': self.biometric_type,
            'consent_status': self.consent_status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AccessibilityNeeds(db.Model):
    __tablename__ = 'accessibility_needs'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    disability_type = db.Column(db.String(100), nullable=False)
    accommodation_needed = db.Column(db.Text)
    documentation_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'disability_type': self.disability_type,
            'accommodation_needed': self.accommodation_needed,
            'documentation_url': self.documentation_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # student, faculty, staff, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    enrollment_date = db.Column(db.Date, nullable=False)
    graduation_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, graduated, withdrawn, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('student', uselist=False))

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    faculty_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    hire_date = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, on_leave, retired
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('faculty', uselist=False))

class Staff(db.Model):
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    staff_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    hire_date = db.Column(db.Date, nullable=False)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, on_leave, terminated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('staff', uselist=False)) 