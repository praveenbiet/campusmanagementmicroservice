from datetime import datetime
from app import db
from sqlalchemy.dialects.sqlite import JSON

class Student(db.Model):
    __tablename__ = 'student'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    program_id = db.Column(db.String(50), db.ForeignKey('program.id'), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    expected_graduation_date = db.Column(db.Date)
    current_status = db.Column(db.String(50), nullable=False)  # active, graduated, withdrawn, etc.
    academic_level = db.Column(db.String(50))  # freshman, sophomore, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    academic_standing = db.relationship('AcademicStanding', backref='student', lazy=True)
    academic_holds = db.relationship('AcademicHold', backref='student', lazy=True)
    academic_achievements = db.relationship('AcademicAchievement', backref='student', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'student_id': self.student_id,
            'program_id': self.program_id,
            'enrollment_date': self.enrollment_date.isoformat(),
            'expected_graduation_date': self.expected_graduation_date.isoformat() if self.expected_graduation_date else None,
            'current_status': self.current_status,
            'academic_level': self.academic_level,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    
    id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    section_id = db.Column(db.String(50), db.ForeignKey('section.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # enrolled, dropped, waitlisted, etc.
    enrollment_type = db.Column(db.String(50))  # regular, audit, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'section_id': self.section_id,
            'enrollment_date': self.enrollment_date.isoformat(),
            'status': self.status,
            'enrollment_type': self.enrollment_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Grade(db.Model):
    __tablename__ = 'grade'
    
    id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    section_id = db.Column(db.String(50), db.ForeignKey('section.id'), nullable=False)
    grade_value = db.Column(db.String(10))  # A, B, C, etc.
    grade_points = db.Column(db.Float)
    is_final = db.Column(db.Boolean, default=False)
    grade_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'section_id': self.section_id,
            'grade_value': self.grade_value,
            'grade_points': self.grade_points,
            'is_final': self.is_final,
            'grade_date': self.grade_date.isoformat() if self.grade_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AcademicStanding(db.Model):
    __tablename__ = 'academic_standing'
    
    id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    term_id = db.Column(db.String(50), db.ForeignKey('term.id'), nullable=False)
    standing_type = db.Column(db.String(50), nullable=False)  # good standing, probation, etc.
    gpa = db.Column(db.Float)
    credits_earned = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'term_id': self.term_id,
            'standing_type': self.standing_type,
            'gpa': self.gpa,
            'credits_earned': self.credits_earned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AcademicHold(db.Model):
    __tablename__ = 'academic_hold'
    
    id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    hold_type = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'hold_type': self.hold_type,
            'reason': self.reason,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AcademicAchievement(db.Model):
    __tablename__ = 'academic_achievement'
    
    id = db.Column(db.String(50), primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('student.id'), nullable=False)
    achievement_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    date_awarded = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'achievement_type': self.achievement_type,
            'description': self.description,
            'date_awarded': self.date_awarded.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Assessment(db.Model):
    __tablename__ = 'assessment'
    
    id = db.Column(db.String(50), primary_key=True)
    section_id = db.Column(db.String(50), db.ForeignKey('section.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # exam, quiz, assignment, etc.
    title = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    grade_submissions = db.relationship('GradeSubmission', backref='assessment', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'type': self.type,
            'title': self.title,
            'weight': self.weight,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class GradeSubmission(db.Model):
    __tablename__ = 'grade_submission'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    assessment_id = db.Column(db.String(50), db.ForeignKey('assessment.id'), nullable=False)
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    submitted_by = db.Column(db.String(50))
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'assessment_id': self.assessment_id,
            'score': self.score,
            'feedback': self.feedback,
            'submitted_by': self.submitted_by,
            'submission_date': self.submission_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class TranscriptRecord(db.Model):
    __tablename__ = 'transcript_record'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    term_id = db.Column(db.String(50), db.ForeignKey('term.id'), nullable=False)
    course_id = db.Column(db.String(50), db.ForeignKey('course.id'), nullable=False)
    grade = db.Column(db.String(10))
    credits_earned = db.Column(db.Float)
    status = db.Column(db.String(50))  # completed, in-progress, withdrawn, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'term_id': self.term_id,
            'course_id': self.course_id,
            'grade': self.grade,
            'credits_earned': self.credits_earned,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class GPASummary(db.Model):
    __tablename__ = 'gpa_summary'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    term_id = db.Column(db.String(50), db.ForeignKey('term.id'), nullable=False)
    term_gpa = db.Column(db.Float)
    cumulative_gpa = db.Column(db.Float)
    credits_attempted = db.Column(db.Float)
    credits_earned = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'term_id': self.term_id,
            'term_gpa': self.term_gpa,
            'cumulative_gpa': self.cumulative_gpa,
            'credits_attempted': self.credits_attempted,
            'credits_earned': self.credits_earned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class StudentProgram(db.Model):
    __tablename__ = 'student_program'
    
    id = db.Column(db.String(50), primary_key=True)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    program_id = db.Column(db.String(50), db.ForeignKey('program.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # active, graduated, withdrawn, etc.
    advisor_id = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    expected_graduation = db.Column(db.Date)
    actual_graduation = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    degree_audits = db.relationship('DegreeAudit', backref='student_program', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'person_id': self.person_id,
            'program_id': self.program_id,
            'status': self.status,
            'advisor_id': self.advisor_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expected_graduation': self.expected_graduation.isoformat() if self.expected_graduation else None,
            'actual_graduation': self.actual_graduation.isoformat() if self.actual_graduation else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AttendanceSession(db.Model):
    __tablename__ = 'attendance_session'
    
    id = db.Column(db.String(50), primary_key=True)
    section_id = db.Column(db.String(50), db.ForeignKey('section.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50))  # lecture, lab, discussion, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('AttendanceRecord', backref='attendance_session', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'section_id': self.section_id,
            'date': self.date.isoformat(),
            'type': self.type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_record'
    
    id = db.Column(db.String(50), primary_key=True)
    session_id = db.Column(db.String(50), db.ForeignKey('attendance_session.id'), nullable=False)
    person_id = db.Column(db.String(50), db.ForeignKey('person.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # present, absent, late, excused
    check_in_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'person_id': self.person_id,
            'status': self.status,
            'check_in_time': self.check_in_time.isoformat() if self.check_in_time else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class DegreeAudit(db.Model):
    __tablename__ = 'degree_audit'
    
    id = db.Column(db.String(50), primary_key=True)
    student_program_id = db.Column(db.String(50), db.ForeignKey('student_program.id'), nullable=False)
    progress_percentage = db.Column(db.Float)
    missing_requirements = db.Column(JSON)
    audit_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_program_id': self.student_program_id,
            'progress_percentage': self.progress_percentage,
            'missing_requirements': self.missing_requirements,
            'audit_date': self.audit_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class AcademicRecord(db.Model):
    __tablename__ = 'academic_records'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    gpa = db.Column(db.Float)
    credits_earned = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, probation, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('academic_records', lazy=True))
    program = db.relationship('Program', backref=db.backref('academic_records', lazy=True))

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='enrolled')  # enrolled, dropped, completed
    grade = db.Column(db.String(2))  # A, B, C, D, F, etc.
    credits = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('enrollments', lazy=True))
    course = db.relationship('Course', backref=db.backref('enrollments', lazy=True))

class Transcript(db.Model):
    __tablename__ = 'transcripts'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    total_credits = db.Column(db.Integer, default=0)
    cumulative_gpa = db.Column(db.Float)
    graduation_date = db.Column(db.Date)
    degree_awarded = db.Column(db.String(100))
    honors = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('transcripts', lazy=True))
    program = db.relationship('Program', backref=db.backref('transcripts', lazy=True))

class Program(db.Model):
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    department = db.Column(db.String(100))
    degree_type = db.Column(db.String(50))  # Bachelor, Master, PhD, etc.
    total_credits = db.Column(db.Integer, nullable=False)
    duration_years = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 