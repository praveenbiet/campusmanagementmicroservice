from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Application, Requirement, AdmissionDecision, Interview, Document, ProgramRequirement, ApplicationStatus
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

admissions_bp = Blueprint('admissions', __name__)

# Application Routes
@admissions_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    applications = Application.query.all()
    return jsonify([{
        'id': a.id,
        'user_id': a.user_id,
        'program_id': a.program_id,
        'application_date': a.application_date.isoformat(),
        'status': a.status
    } for a in applications])

@admissions_bp.route('/applications', methods=['POST'])
@jwt_required()
def create_application():
    data = request.get_json()
    application = Application(
        user_id=data['user_id'],
        program_id=data['program_id'],
        application_date=datetime.fromisoformat(data['application_date']),
        status=data.get('status', 'pending')
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': 'Application created successfully', 'id': application.id}), 201

# Requirement Routes
@admissions_bp.route('/requirements', methods=['GET'])
@jwt_required()
def get_requirements():
    requirements = Requirement.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'description': r.description,
        'is_mandatory': r.is_mandatory,
        'status': r.status
    } for r in requirements])

@admissions_bp.route('/requirements', methods=['POST'])
@jwt_required()
@role_required(['admin', 'admissions'])
def create_requirement():
    data = request.get_json()
    requirement = Requirement(
        name=data['name'],
        description=data['description'],
        is_mandatory=data.get('is_mandatory', True),
        status=data.get('status', 'active')
    )
    db.session.add(requirement)
    db.session.commit()
    return jsonify({'message': 'Requirement created successfully', 'id': requirement.id}), 201

# Admission Decision Routes
@admissions_bp.route('/decisions', methods=['GET'])
@jwt_required()
def get_decisions():
    decisions = AdmissionDecision.query.all()
    return jsonify([{
        'id': d.id,
        'application_id': d.application_id,
        'decision': d.decision,
        'decision_date': d.decision_date.isoformat(),
        'comments': d.comments,
        'status': d.status
    } for d in decisions])

@admissions_bp.route('/decisions', methods=['POST'])
@jwt_required()
@role_required(['admin', 'admissions'])
def create_decision():
    data = request.get_json()
    decision = AdmissionDecision(
        application_id=data['application_id'],
        decision=data['decision'],
        decision_date=datetime.fromisoformat(data['decision_date']),
        comments=data.get('comments'),
        status=data.get('status', 'active')
    )
    db.session.add(decision)
    db.session.commit()
    return jsonify({'message': 'Admission decision created successfully', 'id': decision.id}), 201

# Interview Routes
@admissions_bp.route('/interviews', methods=['GET'])
@jwt_required()
def get_interviews():
    interviews = Interview.query.all()
    return jsonify([{
        'id': i.id,
        'application_id': i.application_id,
        'interviewer_id': i.interviewer_id,
        'scheduled_date': i.scheduled_date.isoformat(),
        'location': i.location,
        'status': i.status
    } for i in interviews])

@admissions_bp.route('/interviews', methods=['POST'])
@jwt_required()
@role_required(['admin', 'admissions'])
def create_interview():
    data = request.get_json()
    interview = Interview(
        application_id=data['application_id'],
        interviewer_id=data['interviewer_id'],
        scheduled_date=datetime.fromisoformat(data['scheduled_date']),
        location=data['location'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(interview)
    db.session.commit()
    return jsonify({'message': 'Interview scheduled successfully', 'id': interview.id}), 201

# Document Routes
@admissions_bp.route('/documents', methods=['GET'])
@jwt_required()
def get_documents():
    documents = Document.query.all()
    return jsonify([{
        'id': d.id,
        'application_id': d.application_id,
        'requirement_id': d.requirement_id,
        'document_type': d.document_type,
        'file_path': d.file_path,
        'status': d.status
    } for d in documents])

@admissions_bp.route('/documents', methods=['POST'])
@jwt_required()
def create_document():
    data = request.get_json()
    document = Document(
        application_id=data['application_id'],
        requirement_id=data['requirement_id'],
        document_type=data['document_type'],
        file_path=data['file_path'],
        status=data.get('status', 'pending')
    )
    db.session.add(document)
    db.session.commit()
    return jsonify({'message': 'Document uploaded successfully', 'id': document.id}), 201

# Program Requirement Routes
@admissions_bp.route('/program-requirements', methods=['GET'])
@jwt_required()
def get_program_requirements():
    requirements = ProgramRequirement.query.all()
    return jsonify([{
        'id': r.id,
        'program_id': r.program_id,
        'requirement_id': r.requirement_id,
        'status': r.status
    } for r in requirements])

@admissions_bp.route('/program-requirements', methods=['POST'])
@jwt_required()
@role_required(['admin', 'admissions'])
def create_program_requirement():
    data = request.get_json()
    requirement = ProgramRequirement(
        program_id=data['program_id'],
        requirement_id=data['requirement_id'],
        status=data.get('status', 'active')
    )
    db.session.add(requirement)
    db.session.commit()
    return jsonify({'message': 'Program requirement created successfully', 'id': requirement.id}), 201

# Application Status Routes
@admissions_bp.route('/application-statuses', methods=['GET'])
@jwt_required()
def get_application_statuses():
    statuses = ApplicationStatus.query.all()
    return jsonify([{
        'id': s.id,
        'application_id': s.application_id,
        'status': s.status,
        'status_date': s.status_date.isoformat(),
        'comments': s.comments
    } for s in statuses])

@admissions_bp.route('/application-statuses', methods=['POST'])
@jwt_required()
@role_required(['admin', 'admissions'])
def create_application_status():
    data = request.get_json()
    status = ApplicationStatus(
        application_id=data['application_id'],
        status=data['status'],
        status_date=datetime.fromisoformat(data['status_date']),
        comments=data.get('comments')
    )
    db.session.add(status)
    db.session.commit()
    return jsonify({'message': 'Application status updated successfully', 'id': status.id}), 201 