from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from .models import Student, Enrollment, Grade, AcademicStanding, AcademicHold, AcademicAchievement
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