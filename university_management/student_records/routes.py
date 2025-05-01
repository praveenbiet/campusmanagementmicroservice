from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from .models import Student, Enrollment, Grade, AcademicStanding, AcademicHold, AcademicAchievement, Transcript, AcademicHistory, Attendance, DisciplineRecord, Achievement
from utils import role_required, validate_request, format_response, log_activity, handle_exception, paginate_query, format_paginated_response
from datetime import datetime
import uuid

student_records_bp = Blueprint('student_records', __name__)

# Student routes
@student_records_bp.route('/students', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def create_student():
    try:
        data = request.get_json()
        
        student_id = str(uuid.uuid4())
        student = Student(
            id=student_id,
            person_id=data['person_id'],
            student_id=data['student_id'],
            program_id=data['program_id'],
            enrollment_date=datetime.strptime(data['enrollment_date'], '%Y-%m-%d').date(),
            expected_graduation_date=datetime.strptime(data['expected_graduation_date'], '%Y-%m-%d').date() if data.get('expected_graduation_date') else None,
            current_status=data['current_status'],
            academic_level=data.get('academic_level')
        )
        
        db.session.add(student)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'student', student_id)
        
        return format_response(student.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@student_records_bp.route('/students/<student_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'registrar', 'faculty', 'student'])
def get_student(student_id):
    try:
        student = Student.query.get_or_404(student_id)
        return format_response(student.to_dict())
    except Exception as e:
        return handle_exception(e)

# Enrollment routes
@student_records_bp.route('/students/<student_id>/enrollments', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def create_enrollment(student_id):
    try:
        data = request.get_json()
        
        enrollment_id = str(uuid.uuid4())
        enrollment = Enrollment(
            id=enrollment_id,
            student_id=student_id,
            section_id=data['section_id'],
            enrollment_date=datetime.strptime(data['enrollment_date'], '%Y-%m-%d %H:%M:%S'),
            status=data['status'],
            enrollment_type=data.get('enrollment_type')
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'enrollment', enrollment_id)
        
        return format_response(enrollment.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Grade routes
@student_records_bp.route('/students/<student_id>/grades', methods=['POST'])
@jwt_required()
@role_required(['admin', 'faculty'])
def create_grade(student_id):
    try:
        data = request.get_json()
        
        grade_id = str(uuid.uuid4())
        grade = Grade(
            id=grade_id,
            student_id=student_id,
            section_id=data['section_id'],
            grade_value=data['grade_value'],
            grade_points=data.get('grade_points'),
            is_final=data.get('is_final', False),
            grade_date=datetime.strptime(data['grade_date'], '%Y-%m-%d %H:%M:%S') if data.get('grade_date') else None
        )
        
        db.session.add(grade)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'grade', grade_id)
        
        return format_response(grade.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Academic standing routes
@student_records_bp.route('/students/<student_id>/academic-standing', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def create_academic_standing(student_id):
    try:
        data = request.get_json()
        
        standing_id = str(uuid.uuid4())
        standing = AcademicStanding(
            id=standing_id,
            student_id=student_id,
            term_id=data['term_id'],
            standing_type=data['standing_type'],
            gpa=data.get('gpa'),
            credits_earned=data.get('credits_earned')
        )
        
        db.session.add(standing)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'academic_standing', standing_id)
        
        return format_response(standing.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Academic hold routes
@student_records_bp.route('/students/<student_id>/holds', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def create_academic_hold(student_id):
    try:
        data = request.get_json()
        
        hold_id = str(uuid.uuid4())
        hold = AcademicHold(
            id=hold_id,
            student_id=student_id,
            hold_type=data['hold_type'],
            reason=data.get('reason'),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d %H:%M:%S'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d %H:%M:%S') if data.get('end_date') else None,
            is_active=data.get('is_active', True)
        )
        
        db.session.add(hold)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'academic_hold', hold_id)
        
        return format_response(hold.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Academic achievement routes
@student_records_bp.route('/students/<student_id>/achievements', methods=['POST'])
@jwt_required()
@role_required(['admin', 'faculty'])
def create_academic_achievement(student_id):
    try:
        data = request.get_json()
        
        achievement_id = str(uuid.uuid4())
        achievement = AcademicAchievement(
            id=achievement_id,
            student_id=student_id,
            achievement_type=data['achievement_type'],
            description=data.get('description'),
            date_awarded=datetime.strptime(data['date_awarded'], '%Y-%m-%d %H:%M:%S')
        )
        
        db.session.add(achievement)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'academic_achievement', achievement_id)
        
        return format_response(achievement.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Transcript Routes
@student_records_bp.route('/transcripts/<int:student_id>', methods=['GET'])
def get_transcript(student_id):
    transcript = Transcript.query.filter_by(student_id=student_id).first_or_404()
    return jsonify({
        'id': transcript.id,
        'student_id': transcript.student_id,
        'issue_date': transcript.issue_date.isoformat(),
        'gpa': transcript.gpa,
        'total_credits': transcript.total_credits,
        'status': transcript.status
    })

@student_records_bp.route('/transcripts', methods=['POST'])
def create_transcript():
    data = request.get_json()
    transcript = Transcript(
        student_id=data['student_id'],
        issue_date=datetime.fromisoformat(data['issue_date']),
        gpa=data['gpa'],
        total_credits=data['total_credits'],
        status=data.get('status', 'active')
    )
    db.session.add(transcript)
    db.session.commit()
    return jsonify({'message': 'Transcript created successfully', 'id': transcript.id}), 201

# Academic History Routes
@student_records_bp.route('/academic-history/<int:student_id>', methods=['GET'])
def get_academic_history(student_id):
    history = AcademicHistory.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': h.id,
        'student_id': h.student_id,
        'term_id': h.term_id,
        'gpa': h.gpa,
        'credits_earned': h.credits_earned,
        'status': h.status
    } for h in history])

@student_records_bp.route('/academic-history', methods=['POST'])
def create_academic_history():
    data = request.get_json()
    history = AcademicHistory(
        student_id=data['student_id'],
        term_id=data['term_id'],
        gpa=data['gpa'],
        credits_earned=data['credits_earned'],
        status=data.get('status', 'active')
    )
    db.session.add(history)
    db.session.commit()
    return jsonify({'message': 'Academic history created successfully', 'id': history.id}), 201

# Attendance Routes
@student_records_bp.route('/attendance/<int:student_id>', methods=['GET'])
def get_student_attendance(student_id):
    attendance = Attendance.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': a.id,
        'student_id': a.student_id,
        'course_id': a.course_id,
        'date': a.date.isoformat(),
        'status': a.status,
        'notes': a.notes
    } for a in attendance])

@student_records_bp.route('/attendance', methods=['POST'])
def record_attendance():
    data = request.get_json()
    attendance = Attendance(
        student_id=data['student_id'],
        course_id=data['course_id'],
        date=datetime.fromisoformat(data['date']),
        status=data['status'],
        notes=data.get('notes')
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance recorded successfully', 'id': attendance.id}), 201

# Discipline Record Routes
@student_records_bp.route('/discipline-records/<int:student_id>', methods=['GET'])
def get_discipline_records(student_id):
    records = DisciplineRecord.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': r.id,
        'student_id': r.student_id,
        'incident_date': r.incident_date.isoformat(),
        'incident_type': r.incident_type,
        'description': r.description,
        'action_taken': r.action_taken,
        'status': r.status
    } for r in records])

@student_records_bp.route('/discipline-records', methods=['POST'])
def create_discipline_record():
    data = request.get_json()
    record = DisciplineRecord(
        student_id=data['student_id'],
        incident_date=datetime.fromisoformat(data['incident_date']),
        incident_type=data['incident_type'],
        description=data['description'],
        action_taken=data['action_taken'],
        status=data.get('status', 'active')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Discipline record created successfully', 'id': record.id}), 201

# Achievement Routes
@student_records_bp.route('/achievements/<int:student_id>', methods=['GET'])
def get_student_achievements(student_id):
    achievements = Achievement.query.filter_by(student_id=student_id).all()
    return jsonify([{
        'id': a.id,
        'student_id': a.student_id,
        'achievement_type': a.achievement_type,
        'description': a.description,
        'date_awarded': a.date_awarded.isoformat(),
        'status': a.status
    } for a in achievements])

@student_records_bp.route('/achievements', methods=['POST'])
def create_achievement():
    data = request.get_json()
    achievement = Achievement(
        student_id=data['student_id'],
        achievement_type=data['achievement_type'],
        description=data['description'],
        date_awarded=datetime.fromisoformat(data['date_awarded']),
        status=data.get('status', 'active')
    )
    db.session.add(achievement)
    db.session.commit()
    return jsonify({'message': 'Achievement created successfully', 'id': achievement.id}), 201 