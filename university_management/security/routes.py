from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import AccessControl, SecurityIncident, SecurityPersonnel, SecurityCheck, SecurityZone, SecurityEquipment, SecurityReport
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

security_bp = Blueprint('security', __name__)

# Access Control Routes
@security_bp.route('/access-controls', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_access_controls():
    controls = AccessControl.query.all()
    return jsonify([{
        'id': c.id,
        'user_id': c.user_id,
        'zone_id': c.zone_id,
        'access_type': c.access_type,
        'start_date': c.start_date.isoformat(),
        'end_date': c.end_date.isoformat() if c.end_date else None,
        'status': c.status
    } for c in controls])

@security_bp.route('/access-controls', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def create_access_control():
    data = request.get_json()
    control = AccessControl(
        user_id=data['user_id'],
        zone_id=data['zone_id'],
        access_type=data['access_type'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(control)
    db.session.commit()
    return jsonify({'message': 'Access control created successfully', 'id': control.id}), 201

# Security Incident Routes
@security_bp.route('/incidents', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_incidents():
    incidents = SecurityIncident.query.all()
    return jsonify([{
        'id': i.id,
        'zone_id': i.zone_id,
        'reported_by': i.reported_by,
        'incident_type': i.incident_type,
        'description': i.description,
        'severity': i.severity,
        'status': i.status,
        'reported_at': i.reported_at.isoformat()
    } for i in incidents])

@security_bp.route('/incidents', methods=['POST'])
@jwt_required()
def create_incident():
    data = request.get_json()
    incident = SecurityIncident(
        zone_id=data['zone_id'],
        reported_by=data['reported_by'],
        incident_type=data['incident_type'],
        description=data['description'],
        severity=data.get('severity', 'medium'),
        status=data.get('status', 'reported'),
        reported_at=datetime.fromisoformat(data['reported_at'])
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify({'message': 'Incident reported successfully', 'id': incident.id}), 201

# Security Personnel Routes
@security_bp.route('/personnel', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_personnel():
    personnel = SecurityPersonnel.query.all()
    return jsonify([{
        'id': p.id,
        'user_id': p.user_id,
        'role': p.role,
        'shift': p.shift,
        'zone_id': p.zone_id,
        'status': p.status
    } for p in personnel])

@security_bp.route('/personnel', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def create_personnel():
    data = request.get_json()
    personnel = SecurityPersonnel(
        user_id=data['user_id'],
        role=data['role'],
        shift=data['shift'],
        zone_id=data['zone_id'],
        status=data.get('status', 'active')
    )
    db.session.add(personnel)
    db.session.commit()
    return jsonify({'message': 'Security personnel added successfully', 'id': personnel.id}), 201

# Security Check Routes
@security_bp.route('/checks', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_checks():
    checks = SecurityCheck.query.all()
    return jsonify([{
        'id': c.id,
        'personnel_id': c.personnel_id,
        'zone_id': c.zone_id,
        'check_type': c.check_type,
        'check_time': c.check_time.isoformat(),
        'status': c.status
    } for c in checks])

@security_bp.route('/checks', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def create_check():
    data = request.get_json()
    check = SecurityCheck(
        personnel_id=data['personnel_id'],
        zone_id=data['zone_id'],
        check_type=data['check_type'],
        check_time=datetime.fromisoformat(data['check_time']),
        status=data.get('status', 'completed')
    )
    db.session.add(check)
    db.session.commit()
    return jsonify({'message': 'Security check recorded successfully', 'id': check.id}), 201

# Security Zone Routes
@security_bp.route('/zones', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_zones():
    zones = SecurityZone.query.all()
    return jsonify([{
        'id': z.id,
        'name': z.name,
        'description': z.description,
        'access_level': z.access_level,
        'status': z.status
    } for z in zones])

@security_bp.route('/zones', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def create_zone():
    data = request.get_json()
    zone = SecurityZone(
        name=data['name'],
        description=data.get('description'),
        access_level=data['access_level'],
        status=data.get('status', 'active')
    )
    db.session.add(zone)
    db.session.commit()
    return jsonify({'message': 'Security zone created successfully', 'id': zone.id}), 201

# Security Equipment Routes
@security_bp.route('/equipment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_equipment():
    equipment = SecurityEquipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'type': e.type,
        'location': e.location,
        'status': e.status,
        'last_maintenance': e.last_maintenance.isoformat() if e.last_maintenance else None
    } for e in equipment])

@security_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def create_equipment():
    data = request.get_json()
    equipment = SecurityEquipment(
        name=data['name'],
        type=data['type'],
        location=data['location'],
        status=data.get('status', 'active'),
        last_maintenance=datetime.fromisoformat(data['last_maintenance']) if data.get('last_maintenance') else None
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'Security equipment added successfully', 'id': equipment.id}), 201

# Security Report Routes
@security_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'security'])
def get_reports():
    reports = SecurityReport.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'content': r.content,
        'created_by': r.created_by,
        'created_at': r.created_at.isoformat(),
        'report_type': r.report_type,
        'status': r.status
    } for r in reports])

@security_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def create_report():
    data = request.get_json()
    report = SecurityReport(
        title=data['title'],
        content=data['content'],
        created_by=data['created_by'],
        created_at=datetime.fromisoformat(data['created_at']),
        report_type=data['report_type'],
        status=data.get('status', 'draft')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Security report created successfully', 'id': report.id}), 201 