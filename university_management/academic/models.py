from datetime import datetime
from app import db
from sqlalchemy.dialects.sqlite import JSON

class Institution(db.Model):
    __tablename__ = 'institution'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    accreditation_status = db.Column(db.String(50))
    established_date = db.Column(db.Date)
    website = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    campuses = db.relationship('Campus', backref='institution', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'accreditation_status': self.accreditation_status,
            'established_date': self.established_date.isoformat() if self.established_date else None,
            'website': self.website,
            'logo_url': self.logo_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Campus(db.Model):
    __tablename__ = 'campus'
    
    id = db.Column(db.String(50), primary_key=True)
    institution_id = db.Column(db.String(50), db.ForeignKey('institution.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    address_id = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    schools = db.relationship('SchoolCollege', backref='campus', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'institution_id': self.institution_id,
            'name': self.name,
            'address_id': self.address_id,
            'phone': self.phone,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SchoolCollege(db.Model):
    __tablename__ = 'school_college'
    
    id = db.Column(db.String(50), primary_key=True)
    campus_id = db.Column(db.String(50), db.ForeignKey('campus.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    dean_person_id = db.Column(db.String(50))
    website = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    departments = db.relationship('Department', backref='school_college', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'campus_id': self.campus_id,
            'name': self.name,
            'dean_person_id': self.dean_person_id,
            'website': self.website,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    head_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    location = db.Column(db.String(100))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    head = db.relationship('Faculty', backref=db.backref('department_head', uselist=False))

class FacultyAssignment(db.Model):
    __tablename__ = 'faculty_assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    role = db.Column(db.String(50))  # professor, associate professor, assistant professor, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    is_primary = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    faculty = db.relationship('Faculty', backref=db.backref('assignments', lazy=True))
    department = db.relationship('Department', backref=db.backref('faculty_assignments', lazy=True))

class AcademicCalendar(db.Model):
    __tablename__ = 'academic_calendars'
    
    id = db.Column(db.Integer, primary_key=True)
    academic_year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # registration, classes_start, exams, etc.
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    is_holiday = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ResearchProject(db.Model):
    __tablename__ = 'research_projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    funding_amount = db.Column(db.Float)
    funding_agency = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, completed, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    faculty = db.relationship('Faculty', backref=db.backref('research_projects', lazy=True))
    department = db.relationship('Department', backref=db.backref('research_projects', lazy=True))

class Publication(db.Model):
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.Text)  # JSON string of authors
    publication_type = db.Column(db.String(50))  # journal, conference, book, etc.
    journal_name = db.Column(db.String(200))
    publication_date = db.Column(db.Date)
    doi = db.Column(db.String(100))
    abstract = db.Column(db.Text)
    keywords = db.Column(db.Text)  # JSON string of keywords
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    faculty = db.relationship('Faculty', backref=db.backref('publications', lazy=True))

class Program(db.Model):
    __tablename__ = 'program'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    degree_type = db.Column(db.String(50), nullable=False)  # bachelor, master, phd, etc.
    department_id = db.Column(db.String(50), db.ForeignKey('department.id'), nullable=False)
    total_credits_required = db.Column(db.Integer, nullable=False)
    duration_years = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    courses = db.relationship('ProgramCourse', backref='program', lazy=True)
    students = db.relationship('StudentProgram', backref='program', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'degree_type': self.degree_type,
            'department_id': self.department_id,
            'total_credits_required': self.total_credits_required,
            'duration_years': self.duration_years,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AcademicYear(db.Model):
    __tablename__ = 'academic_year'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    terms = db.relationship('Term', backref='academic_year', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Term(db.Model):
    __tablename__ = 'term'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Fall 2023, Spring 2024, etc.
    code = db.Column(db.String(20), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    registration_start = db.Column(db.Date)
    registration_end = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sections = db.relationship('Section', backref='term', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'registration_start': self.registration_start.isoformat() if self.registration_start else None,
            'registration_end': self.registration_end.isoformat() if self.registration_end else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Holiday(db.Model):
    __tablename__ = 'holiday'
    
    id = db.Column(db.String(50), primary_key=True)
    term_id = db.Column(db.String(50), db.ForeignKey('term.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    applicable_to = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'term_id': self.term_id,
            'name': self.name,
            'date_start': self.date_start.isoformat(),
            'date_end': self.date_end.isoformat(),
            'applicable_to': self.applicable_to,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Course(db.Model):
    __tablename__ = 'course'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.String(50), db.ForeignKey('department.id'), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String(50))  # undergraduate, graduate, etc.
    prerequisites = db.Column(JSON)  # List of course IDs
    corequisites = db.Column(JSON)  # List of course IDs
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sections = db.relationship('Section', backref='course', lazy=True)
    program_courses = db.relationship('ProgramCourse', backref='course', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'department_id': self.department_id,
            'credits': self.credits,
            'level': self.level,
            'prerequisites': self.prerequisites,
            'corequisites': self.corequisites,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Prerequisite(db.Model):
    __tablename__ = 'prerequisite'
    
    id = db.Column(db.String(50), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)
    prerequisite_course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'prerequisite_course_id': self.prerequisite_course_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Section(db.Model):
    __tablename__ = 'section'
    
    id = db.Column(db.String(50), primary_key=True)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)
    section_number = db.Column(db.String(10), nullable=False)
    term_id = db.Column(db.String(50), db.ForeignKey('term.id'), nullable=False)
    instructor_id = db.Column(db.String(50), db.ForeignKey('person.id'))
    capacity = db.Column(db.Integer, nullable=False)
    enrolled = db.Column(db.Integer, default=0)
    room_id = db.Column(db.String(50), db.ForeignKey('room.id'))
    schedule = db.Column(JSON)  # List of meeting times
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='section', lazy=True)
    grades = db.relationship('Grade', backref='section', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'section_number': self.section_number,
            'term_id': self.term_id,
            'instructor_id': self.instructor_id,
            'capacity': self.capacity,
            'enrolled': self.enrolled,
            'room_id': self.room_id,
            'schedule': self.schedule,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ScheduleSlot(db.Model):
    __tablename__ = 'schedule_slot'
    
    id = db.Column(db.String(50), primary_key=True)
    section_id = db.Column(db.String(50), db.ForeignKey('section.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0-6 for Monday-Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'room_id': self.room_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class CurriculumMapping(db.Model):
    __tablename__ = 'curriculum_mapping'
    
    id = db.Column(db.String(50), primary_key=True)
    program_id = db.Column(db.String(50), db.ForeignKey('program.id'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)
    requirement_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'course_id': self.course_id,
            'requirement_type': self.requirement_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class ProgramCourse(db.Model):
    __tablename__ = 'program_course'
    
    id = db.Column(db.String(50), primary_key=True)
    program_id = db.Column(db.String(50), db.ForeignKey('program.id'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)
    is_required = db.Column(db.Boolean, default=True)
    semester_number = db.Column(db.Integer)  # In which semester this course should be taken
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'program_id': self.program_id,
            'course_id': self.course_id,
            'is_required': self.is_required,
            'semester_number': self.semester_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text)
    dean_id = db.Column(db.String(50), db.ForeignKey('person.id'))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    departments = db.relationship('Department', backref='faculty', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'dean_id': self.dean_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Room(db.Model):
    __tablename__ = 'room'
    
    id = db.Column(db.String(50), primary_key=True)
    building_id = db.Column(db.String(50), db.ForeignKey('building.id'), nullable=False)
    room_number = db.Column(db.String(20), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.String(50))  # classroom, lab, office, etc.
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sections = db.relationship('Section', backref='room', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'building_id': self.building_id,
            'room_number': self.room_number,
            'capacity': self.capacity,
            'room_type': self.room_type,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Building(db.Model):
    __tablename__ = 'building'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(255))
    campus_id = db.Column(db.String(50), db.ForeignKey('campus.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    rooms = db.relationship('Room', backref='building', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'address': self.address,
            'campus_id': self.campus_id,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Campus(db.Model):
    __tablename__ = 'campus'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    buildings = db.relationship('Building', backref='campus', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 