from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from .models import (
    Institution, Campus, SchoolCollege, Department, Program,
    AcademicYear, Term, Holiday, Course, Prerequisite, Section,
    ScheduleSlot, CurriculumMapping, Faculty, ProgramCourse,
    Room, Building
)
from utils import role_required, validate_request, format_response, log_activity, handle_exception, paginate_query, format_paginated_response
from datetime import datetime
import uuid

academic_bp = Blueprint('academic', __name__)

# Institution routes
@academic_bp.route('/institutions', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_institution():
    try:
        data = request.get_json()
        
        institution_id = str(uuid.uuid4())
        institution = Institution(
            id=institution_id,
            name=data['name'],
            accreditation_status=data.get('accreditation_status'),
            established_date=datetime.strptime(data['established_date'], '%Y-%m-%d').date() if data.get('established_date') else None,
            website=data.get('website'),
            logo_url=data.get('logo_url')
        )
        
        db.session.add(institution)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'institution', institution_id)
        
        return format_response(institution.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@academic_bp.route('/institutions/<institution_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'faculty', 'student'])
def get_institution(institution_id):
    try:
        institution = Institution.query.get_or_404(institution_id)
        return format_response(institution.to_dict())
    except Exception as e:
        return handle_exception(e)

# Campus routes
@academic_bp.route('/institutions/<institution_id>/campuses', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_campus(institution_id):
    try:
        data = request.get_json()
        
        campus_id = str(uuid.uuid4())
        campus = Campus(
            id=campus_id,
            institution_id=institution_id,
            name=data['name'],
            address_id=data.get('address_id'),
            phone=data.get('phone'),
            email=data.get('email')
        )
        
        db.session.add(campus)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'campus', campus_id)
        
        return format_response(campus.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# School/College routes
@academic_bp.route('/campuses/<campus_id>/schools', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_school(campus_id):
    try:
        data = request.get_json()
        
        school_id = str(uuid.uuid4())
        school = SchoolCollege(
            id=school_id,
            campus_id=campus_id,
            name=data['name'],
            dean_person_id=data.get('dean_person_id'),
            website=data.get('website')
        )
        
        db.session.add(school)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'school', school_id)
        
        return format_response(school.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Department routes
@academic_bp.route('/schools/<school_id>/departments', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_department(school_id):
    try:
        data = request.get_json()
        
        department_id = str(uuid.uuid4())
        department = Department(
            id=department_id,
            school_college_id=school_id,
            name=data['name'],
            head_person_id=data.get('head_person_id'),
            website=data.get('website')
        )
        
        db.session.add(department)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'department', department_id)
        
        return format_response(department.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Program routes
@academic_bp.route('/departments/<department_id>/programs', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_program(department_id):
    try:
        data = request.get_json()
        
        program_id = str(uuid.uuid4())
        program = Program(
            id=program_id,
            department_id=department_id,
            name=data['name'],
            level=data['level'],
            credits_required=data['credits_required'],
            duration_years=data.get('duration_years'),
            description=data.get('description')
        )
        
        db.session.add(program)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'program', program_id)
        
        return format_response(program.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Course routes
@academic_bp.route('/programs/<program_id>/courses', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_course(program_id):
    try:
        data = request.get_json()
        
        course_id = str(uuid.uuid4())
        course = Course(
            id=course_id,
            program_id=program_id,
            code=data['code'],
            title=data['title'],
            credits=data['credits'],
            description=data.get('description'),
            learning_outcomes=data.get('learning_outcomes')
        )
        
        db.session.add(course)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'course', course_id)
        
        return format_response(course.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Section routes
@academic_bp.route('/courses/<course_id>/sections', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_section(course_id):
    try:
        data = request.get_json()
        
        section_id = str(uuid.uuid4())
        section = Section(
            id=section_id,
            course_id=course_id,
            term_id=data['term_id'],
            instructor_person_id=data.get('instructor_person_id'),
            capacity=data['capacity'],
            section_number=data['section_number']
        )
        
        db.session.add(section)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'section', section_id)
        
        return format_response(section.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Schedule slot routes
@academic_bp.route('/sections/<section_id>/schedule-slots', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_schedule_slot(section_id):
    try:
        data = request.get_json()
        
        slot_id = str(uuid.uuid4())
        slot = ScheduleSlot(
            id=slot_id,
            section_id=section_id,
            day_of_week=data['day_of_week'],
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            room_id=data.get('room_id')
        )
        
        db.session.add(slot)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'schedule_slot', slot_id)
        
        return format_response(slot.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Academic year routes
@academic_bp.route('/academic-years', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_academic_year():
    try:
        data = request.get_json()
        
        year_id = str(uuid.uuid4())
        academic_year = AcademicYear(
            id=year_id,
            name=data['name'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        )
        
        db.session.add(academic_year)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'academic_year', year_id)
        
        return format_response(academic_year.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Term routes
@academic_bp.route('/academic-years/<year_id>/terms', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_term(year_id):
    try:
        data = request.get_json()
        
        term_id = str(uuid.uuid4())
        term = Term(
            id=term_id,
            academic_year_id=year_id,
            name=data['name'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
            registration_start=datetime.strptime(data['registration_start'], '%Y-%m-%d').date() if data.get('registration_start') else None,
            registration_end=datetime.strptime(data['registration_end'], '%Y-%m-%d').date() if data.get('registration_end') else None
        )
        
        db.session.add(term)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'term', term_id)
        
        return format_response(term.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Holiday routes
@academic_bp.route('/terms/<term_id>/holidays', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_holiday(term_id):
    try:
        data = request.get_json()
        
        holiday_id = str(uuid.uuid4())
        holiday = Holiday(
            id=holiday_id,
            term_id=term_id,
            name=data['name'],
            date_start=datetime.strptime(data['date_start'], '%Y-%m-%d').date(),
            date_end=datetime.strptime(data['date_end'], '%Y-%m-%d').date(),
            applicable_to=data.get('applicable_to')
        )
        
        db.session.add(holiday)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'holiday', holiday_id)
        
        return format_response(holiday.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Curriculum mapping routes
@academic_bp.route('/programs/<program_id>/curriculum-mappings', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def create_curriculum_mapping(program_id):
    try:
        data = request.get_json()
        
        mapping_id = str(uuid.uuid4())
        mapping = CurriculumMapping(
            id=mapping_id,
            program_id=program_id,
            course_id=data['course_id'],
            requirement_type=data['requirement_type']
        )
        
        db.session.add(mapping)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'curriculum_mapping', mapping_id)
        
        return format_response(mapping.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

# Program Routes
@academic_bp.route('/programs', methods=['GET'])
@jwt_required()
def get_programs():
    programs = Program.query.all()
    return jsonify([program.to_dict() for program in programs])

@academic_bp.route('/programs/<id>', methods=['GET'])
@jwt_required()
def get_program(id):
    program = Program.query.get_or_404(id)
    return jsonify(program.to_dict())

@academic_bp.route('/programs', methods=['POST'])
@jwt_required()
def create_program():
    data = request.get_json()
    program = Program(**data)
    db.session.add(program)
    db.session.commit()
    return jsonify(program.to_dict()), 201

@academic_bp.route('/programs/<id>', methods=['PUT'])
@jwt_required()
def update_program(id):
    program = Program.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(program, key, value)
    db.session.commit()
    return jsonify(program.to_dict())

@academic_bp.route('/programs/<id>', methods=['DELETE'])
@jwt_required()
def delete_program(id):
    program = Program.query.get_or_404(id)
    db.session.delete(program)
    db.session.commit()
    return '', 204

# Department Routes
@academic_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    departments = Department.query.all()
    return jsonify([dept.to_dict() for dept in departments])

@academic_bp.route('/departments/<id>', methods=['GET'])
@jwt_required()
def get_department(id):
    department = Department.query.get_or_404(id)
    return jsonify(department.to_dict())

@academic_bp.route('/departments', methods=['POST'])
@jwt_required()
def create_department():
    data = request.get_json()
    department = Department(**data)
    db.session.add(department)
    db.session.commit()
    return jsonify(department.to_dict()), 201

@academic_bp.route('/departments/<id>', methods=['PUT'])
@jwt_required()
def update_department(id):
    department = Department.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(department, key, value)
    db.session.commit()
    return jsonify(department.to_dict())

@academic_bp.route('/departments/<id>', methods=['DELETE'])
@jwt_required()
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    return '', 204

# Faculty Routes
@academic_bp.route('/faculties', methods=['GET'])
@jwt_required()
def get_faculties():
    faculties = Faculty.query.all()
    return jsonify([faculty.to_dict() for faculty in faculties])

@academic_bp.route('/faculties/<id>', methods=['GET'])
@jwt_required()
def get_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    return jsonify(faculty.to_dict())

@academic_bp.route('/faculties', methods=['POST'])
@jwt_required()
def create_faculty():
    data = request.get_json()
    faculty = Faculty(**data)
    db.session.add(faculty)
    db.session.commit()
    return jsonify(faculty.to_dict()), 201

@academic_bp.route('/faculties/<id>', methods=['PUT'])
@jwt_required()
def update_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(faculty, key, value)
    db.session.commit()
    return jsonify(faculty.to_dict())

@academic_bp.route('/faculties/<id>', methods=['DELETE'])
@jwt_required()
def delete_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    db.session.delete(faculty)
    db.session.commit()
    return '', 204

# Course Routes
@academic_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@academic_bp.route('/courses/<id>', methods=['GET'])
@jwt_required()
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict())

@academic_bp.route('/courses', methods=['POST'])
@jwt_required()
def create_course():
    data = request.get_json()
    course = Course(**data)
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@academic_bp.route('/courses/<id>', methods=['PUT'])
@jwt_required()
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(course, key, value)
    db.session.commit()
    return jsonify(course.to_dict())

@academic_bp.route('/courses/<id>', methods=['DELETE'])
@jwt_required()
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return '', 204

# Section Routes
@academic_bp.route('/sections', methods=['GET'])
@jwt_required()
def get_sections():
    sections = Section.query.all()
    return jsonify([section.to_dict() for section in sections])

@academic_bp.route('/sections/<id>', methods=['GET'])
@jwt_required()
def get_section(id):
    section = Section.query.get_or_404(id)
    return jsonify(section.to_dict())

@academic_bp.route('/sections', methods=['POST'])
@jwt_required()
def create_section():
    data = request.get_json()
    section = Section(**data)
    db.session.add(section)
    db.session.commit()
    return jsonify(section.to_dict()), 201

@academic_bp.route('/sections/<id>', methods=['PUT'])
@jwt_required()
def update_section(id):
    section = Section.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(section, key, value)
    db.session.commit()
    return jsonify(section.to_dict())

@academic_bp.route('/sections/<id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return '', 204

# Term Routes
@academic_bp.route('/terms', methods=['GET'])
@jwt_required()
def get_terms():
    terms = Term.query.all()
    return jsonify([term.to_dict() for term in terms])

@academic_bp.route('/terms/<id>', methods=['GET'])
@jwt_required()
def get_term(id):
    term = Term.query.get_or_404(id)
    return jsonify(term.to_dict())

@academic_bp.route('/terms', methods=['POST'])
@jwt_required()
def create_term():
    data = request.get_json()
    term = Term(**data)
    db.session.add(term)
    db.session.commit()
    return jsonify(term.to_dict()), 201

@academic_bp.route('/terms/<id>', methods=['PUT'])
@jwt_required()
def update_term(id):
    term = Term.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(term, key, value)
    db.session.commit()
    return jsonify(term.to_dict())

@academic_bp.route('/terms/<id>', methods=['DELETE'])
@jwt_required()
def delete_term(id):
    term = Term.query.get_or_404(id)
    db.session.delete(term)
    db.session.commit()
    return '', 204

# Room Routes
@academic_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    rooms = Room.query.all()
    return jsonify([room.to_dict() for room in rooms])

@academic_bp.route('/rooms/<id>', methods=['GET'])
@jwt_required()
def get_room(id):
    room = Room.query.get_or_404(id)
    return jsonify(room.to_dict())

@academic_bp.route('/rooms', methods=['POST'])
@jwt_required()
def create_room():
    data = request.get_json()
    room = Room(**data)
    db.session.add(room)
    db.session.commit()
    return jsonify(room.to_dict()), 201

@academic_bp.route('/rooms/<id>', methods=['PUT'])
@jwt_required()
def update_room(id):
    room = Room.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(room, key, value)
    db.session.commit()
    return jsonify(room.to_dict())

@academic_bp.route('/rooms/<id>', methods=['DELETE'])
@jwt_required()
def delete_room(id):
    room = Room.query.get_or_404(id)
    db.session.delete(room)
    db.session.commit()
    return '', 204

# Building Routes
@academic_bp.route('/buildings', methods=['GET'])
@jwt_required()
def get_buildings():
    buildings = Building.query.all()
    return jsonify([building.to_dict() for building in buildings])

@academic_bp.route('/buildings/<id>', methods=['GET'])
@jwt_required()
def get_building(id):
    building = Building.query.get_or_404(id)
    return jsonify(building.to_dict())

@academic_bp.route('/buildings', methods=['POST'])
@jwt_required()
def create_building():
    data = request.get_json()
    building = Building(**data)
    db.session.add(building)
    db.session.commit()
    return jsonify(building.to_dict()), 201

@academic_bp.route('/buildings/<id>', methods=['PUT'])
@jwt_required()
def update_building(id):
    building = Building.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(building, key, value)
    db.session.commit()
    return jsonify(building.to_dict())

@academic_bp.route('/buildings/<id>', methods=['DELETE'])
@jwt_required()
def delete_building(id):
    building = Building.query.get_or_404(id)
    db.session.delete(building)
    db.session.commit()
    return '', 204

# Campus Routes
@academic_bp.route('/campuses', methods=['GET'])
@jwt_required()
def get_campuses():
    campuses = Campus.query.all()
    return jsonify([campus.to_dict() for campus in campuses])

@academic_bp.route('/campuses/<id>', methods=['GET'])
@jwt_required()
def get_campus(id):
    campus = Campus.query.get_or_404(id)
    return jsonify(campus.to_dict())

@academic_bp.route('/campuses', methods=['POST'])
@jwt_required()
def create_campus():
    data = request.get_json()
    campus = Campus(**data)
    db.session.add(campus)
    db.session.commit()
    return jsonify(campus.to_dict()), 201

@academic_bp.route('/campuses/<id>', methods=['PUT'])
@jwt_required()
def update_campus(id):
    campus = Campus.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(campus, key, value)
    db.session.commit()
    return jsonify(campus.to_dict())

@academic_bp.route('/campuses/<id>', methods=['DELETE'])
@jwt_required()
def delete_campus(id):
    campus = Campus.query.get_or_404(id)
    db.session.delete(campus)
    db.session.commit()
    return '', 204 