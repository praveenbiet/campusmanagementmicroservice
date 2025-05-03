from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Course, Section, Prerequisite, 
    CourseMaterial, Term, CourseSchedule, db
)
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

course_management_bp = Blueprint('course_management', __name__)

# Course Routes
@course_management_bp.route('/courses', methods=['GET'])
@jwt_required()
def get_courses():
    try:
        courses = Course.query.all()
        return jsonify([{
            'id': c.id,
            'code': c.code,
            'title': c.title,
            'description': c.description,
            'credits': c.credits,
            'department': c.department,
            'level': c.level,
            'status': c.status
        } for c in courses])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses/<id>', methods=['GET'])
@jwt_required()
def get_course(id):
    try:
        course = Course.query.get_or_404(id)
        
        # Get prerequisites
        prereqs = Prerequisite.query.filter_by(course_id=id, is_corequisite=False).all()
        prereq_list = [{
            'id': p.prerequisite_course_id,
            'code': p.prerequisite_course.code,
            'title': p.prerequisite_course.title,
            'minimum_grade': p.minimum_grade
        } for p in prereqs]
        
        # Get corequisites
        coreqs = Prerequisite.query.filter_by(course_id=id, is_corequisite=True).all()
        coreq_list = [{
            'id': c.prerequisite_course_id,
            'code': c.prerequisite_course.code,
            'title': c.prerequisite_course.title
        } for c in coreqs]
        
        return jsonify({
            'id': course.id,
            'code': course.code,
            'title': course.title,
            'description': course.description,
            'credits': course.credits,
            'department': course.department,
            'level': course.level,
            'prerequisites': prereq_list,
            'corequisites': coreq_list,
            'status': course.status,
            'created_at': course.created_at.isoformat(),
            'updated_at': course.updated_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses', methods=['POST'])
@jwt_required()
@role_required(['admin', 'academic'])
def create_course():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if course code already exists
        existing_course = Course.query.filter_by(code=data['code']).first()
        if existing_course:
            return jsonify({'message': 'Course code already exists'}), 400
        
        course = Course(
            code=data['code'],
            title=data['title'],
            description=data.get('description'),
            credits=data['credits'],
            department=data.get('department'),
            level=data.get('level'),
            prerequisites=data.get('prerequisites'),
            corequisites=data.get('corequisites'),
            status=data.get('status', 'active')
        )
        
        db.session.add(course)
        db.session.commit()
        
        log_activity(user_id, 'create', 'course', course.id)
        
        return jsonify({
            'message': 'Course created successfully',
            'id': course.id
        }), 201
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses/<id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'academic'])
def update_course(id):
    try:
        course = Course.query.get_or_404(id)
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if course code is being changed and already exists
        if 'code' in data and data['code'] != course.code:
            existing_course = Course.query.filter_by(code=data['code']).first()
            if existing_course:
                return jsonify({'message': 'Course code already exists'}), 400
        
        for key, value in data.items():
            if hasattr(course, key):
                setattr(course, key, value)
        
        db.session.commit()
        
        log_activity(user_id, 'update', 'course', id)
        
        return jsonify({
            'message': 'Course updated successfully'
        })
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses/<id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_course(id):
    try:
        course = Course.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if course has sections
        if course.sections:
            return jsonify({'message': 'Cannot delete course with active sections'}), 400
        
        db.session.delete(course)
        db.session.commit()
        
        log_activity(user_id, 'delete', 'course', id)
        
        return jsonify({
            'message': 'Course deleted successfully'
        })
    except Exception as e:
        return handle_exception(e)

# Section Routes
@course_management_bp.route('/sections', methods=['GET'])
@jwt_required()
def get_sections():
    try:
        sections = Section.query.all()
        return jsonify([{
            'id': s.id,
            'course_id': s.course_id,
            'course_code': s.course.code,
            'course_title': s.course.title,
            'section_number': s.section_number,
            'semester': s.semester,
            'academic_year': s.academic_year,
            'faculty_id': s.faculty_id,
            'capacity': s.capacity,
            'enrolled': s.enrolled,
            'status': s.status
        } for s in sections])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses/<course_id>/sections', methods=['GET'])
@jwt_required()
def get_course_sections(course_id):
    try:
        sections = Section.query.filter_by(course_id=course_id).all()
        return jsonify([{
            'id': s.id,
            'section_number': s.section_number,
            'semester': s.semester,
            'academic_year': s.academic_year,
            'faculty_id': s.faculty_id,
            'capacity': s.capacity,
            'enrolled': s.enrolled,
            'location': s.location,
            'status': s.status
        } for s in sections])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/sections/<id>', methods=['GET'])
@jwt_required()
def get_section(id):
    try:
        section = Section.query.get_or_404(id)
        
        # Parse schedule JSON if it exists
        schedule_data = []
        if section.schedule:
            import json
            try:
                schedule_data = json.loads(section.schedule)
            except:
                schedule_data = []
        
        return jsonify({
            'id': section.id,
            'course_id': section.course_id,
            'course_code': section.course.code,
            'course_title': section.course.title,
            'section_number': section.section_number,
            'semester': section.semester,
            'academic_year': section.academic_year,
            'faculty_id': section.faculty_id,
            'capacity': section.capacity,
            'enrolled': section.enrolled,
            'schedule': schedule_data,
            'location': section.location,
            'status': section.status,
            'created_at': section.created_at.isoformat(),
            'updated_at': section.updated_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/sections', methods=['POST'])
@jwt_required()
@role_required(['admin', 'academic'])
def create_section():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if course exists
        course = Course.query.get(data['course_id'])
        if not course:
            return jsonify({'message': 'Course not found'}), 404
        
        # Convert schedule to JSON string if provided
        schedule_str = None
        if 'schedule' in data:
            import json
            schedule_str = json.dumps(data['schedule'])
        
        section = Section(
            course_id=data['course_id'],
            section_number=data['section_number'],
            semester=data['semester'],
            academic_year=data['academic_year'],
            faculty_id=data['faculty_id'],
            capacity=data['capacity'],
            enrolled=data.get('enrolled', 0),
            schedule=schedule_str,
            location=data.get('location'),
            status=data.get('status', 'active')
        )
        
        db.session.add(section)
        db.session.commit()
        
        log_activity(user_id, 'create', 'section', section.id)
        
        return jsonify({
            'message': 'Section created successfully',
            'id': section.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Prerequisites Routes
@course_management_bp.route('/courses/<course_id>/prerequisites', methods=['GET'])
@jwt_required()
def get_prerequisites(course_id):
    try:
        prereqs = Prerequisite.query.filter_by(course_id=course_id).all()
        return jsonify([{
            'id': p.id,
            'course_id': p.course_id,
            'prerequisite_course_id': p.prerequisite_course_id,
            'prerequisite_course_code': p.prerequisite_course.code,
            'prerequisite_course_title': p.prerequisite_course.title,
            'is_corequisite': p.is_corequisite,
            'minimum_grade': p.minimum_grade
        } for p in prereqs])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses/<course_id>/prerequisites', methods=['POST'])
@jwt_required()
@role_required(['admin', 'academic'])
def add_prerequisite(course_id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if course exists
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Course not found'}), 404
        
        # Check if prerequisite course exists
        prereq_course = Course.query.get(data['prerequisite_course_id'])
        if not prereq_course:
            return jsonify({'message': 'Prerequisite course not found'}), 404
        
        # Check if prerequisite already exists
        existing_prereq = Prerequisite.query.filter_by(
            course_id=course_id,
            prerequisite_course_id=data['prerequisite_course_id']
        ).first()
        
        if existing_prereq:
            return jsonify({'message': 'Prerequisite already exists'}), 400
        
        prerequisite = Prerequisite(
            course_id=course_id,
            prerequisite_course_id=data['prerequisite_course_id'],
            is_corequisite=data.get('is_corequisite', False),
            minimum_grade=data.get('minimum_grade')
        )
        
        db.session.add(prerequisite)
        db.session.commit()
        
        log_activity(user_id, 'create', 'prerequisite', prerequisite.id)
        
        return jsonify({
            'message': 'Prerequisite added successfully',
            'id': prerequisite.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Course Materials Routes
@course_management_bp.route('/courses/<course_id>/materials', methods=['GET'])
@jwt_required()
def get_course_materials(course_id):
    try:
        materials = CourseMaterial.query.filter_by(course_id=course_id).all()
        return jsonify([{
            'id': m.id,
            'course_id': m.course_id,
            'title': m.title,
            'description': m.description,
            'file_path': m.file_path,
            'file_type': m.file_type,
            'upload_date': m.upload_date.isoformat(),
            'is_public': m.is_public
        } for m in materials])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/courses/<course_id>/materials', methods=['POST'])
@jwt_required()
@role_required(['admin', 'academic', 'faculty'])
def add_course_material(course_id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if course exists
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'message': 'Course not found'}), 404
        
        material = CourseMaterial(
            course_id=course_id,
            title=data['title'],
            description=data.get('description'),
            file_path=data.get('file_path'),
            file_type=data.get('file_type'),
            is_public=data.get('is_public', True)
        )
        
        db.session.add(material)
        db.session.commit()
        
        log_activity(user_id, 'create', 'course_material', material.id)
        
        return jsonify({
            'message': 'Course material added successfully',
            'id': material.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Term Routes
@course_management_bp.route('/terms', methods=['GET'])
@jwt_required()
def get_terms():
    try:
        terms = Term.query.all()
        return jsonify([term.to_dict() for term in terms])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/terms/<id>', methods=['GET'])
@jwt_required()
def get_term(id):
    try:
        term = Term.query.get_or_404(id)
        return jsonify(term.to_dict())
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/terms', methods=['POST'])
@jwt_required()
@role_required(['admin', 'academic'])
def create_term():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if term code already exists
        existing_term = Term.query.filter_by(term_code=data['term_code']).first()
        if existing_term:
            return jsonify({'message': 'Term code already exists'}), 400
        
        import uuid
        
        term = Term(
            id=str(uuid.uuid4()),
            term_code=data['term_code'],
            name=data['name'],
            start_date=datetime.fromisoformat(data['start_date']).date(),
            end_date=datetime.fromisoformat(data['end_date']).date(),
            registration_start=datetime.fromisoformat(data['registration_start']).date(),
            registration_end=datetime.fromisoformat(data['registration_end']).date(),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(term)
        db.session.commit()
        
        log_activity(user_id, 'create', 'term', term.id)
        
        return jsonify({
            'message': 'Term created successfully',
            'id': term.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Course Schedule Routes
@course_management_bp.route('/sections/<section_id>/schedule', methods=['GET'])
@jwt_required()
def get_section_schedule(section_id):
    try:
        schedules = CourseSchedule.query.filter_by(section_id=section_id).all()
        return jsonify([schedule.to_dict() for schedule in schedules])
    except Exception as e:
        return handle_exception(e)

@course_management_bp.route('/sections/<section_id>/schedule', methods=['POST'])
@jwt_required()
@role_required(['admin', 'academic'])
def add_section_schedule(section_id):
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if section exists
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        
        import uuid
        
        schedule = CourseSchedule(
            id=str(uuid.uuid4()),
            section_id=section_id,
            day_of_week=data['day_of_week'],
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            room=data.get('room')
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        log_activity(user_id, 'create', 'course_schedule', schedule.id)
        
        return jsonify({
            'message': 'Schedule added successfully',
            'id': schedule.id
        }), 201
    except Exception as e:
        return handle_exception(e)