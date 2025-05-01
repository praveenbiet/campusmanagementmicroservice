from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Policy, Committee, Compliance, Meeting, Decision, Regulation, GovernanceReport
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

governance_bp = Blueprint('governance', __name__)

# Policy Routes
@governance_bp.route('/policies', methods=['GET'])
@jwt_required()
def get_policies():
    policies = Policy.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'category': p.category,
        'effective_date': p.effective_date.isoformat(),
        'status': p.status
    } for p in policies])

@governance_bp.route('/policies', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_policy():
    data = request.get_json()
    policy = Policy(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        effective_date=datetime.fromisoformat(data['effective_date']),
        status=data.get('status', 'active')
    )
    db.session.add(policy)
    db.session.commit()
    return jsonify({'message': 'Policy created successfully', 'id': policy.id}), 201

# Committee Routes
@governance_bp.route('/committees', methods=['GET'])
@jwt_required()
def get_committees():
    committees = Committee.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'chair_id': c.chair_id,
        'status': c.status
    } for c in committees])

@governance_bp.route('/committees', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_committee():
    data = request.get_json()
    committee = Committee(
        name=data['name'],
        description=data['description'],
        chair_id=data['chair_id'],
        status=data.get('status', 'active')
    )
    db.session.add(committee)
    db.session.commit()
    return jsonify({'message': 'Committee created successfully', 'id': committee.id}), 201

# Compliance Routes
@governance_bp.route('/compliance', methods=['GET'])
@jwt_required()
@role_required(['admin', 'governance'])
def get_compliance():
    compliance = Compliance.query.all()
    return jsonify([{
        'id': c.id,
        'policy_id': c.policy_id,
        'department_id': c.department_id,
        'compliance_status': c.compliance_status,
        'last_audit_date': c.last_audit_date.isoformat() if c.last_audit_date else None,
        'status': c.status
    } for c in compliance])

@governance_bp.route('/compliance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_compliance():
    data = request.get_json()
    compliance = Compliance(
        policy_id=data['policy_id'],
        department_id=data['department_id'],
        compliance_status=data['compliance_status'],
        last_audit_date=datetime.fromisoformat(data['last_audit_date']) if data.get('last_audit_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(compliance)
    db.session.commit()
    return jsonify({'message': 'Compliance record created successfully', 'id': compliance.id}), 201

# Meeting Routes
@governance_bp.route('/meetings', methods=['GET'])
@jwt_required()
def get_meetings():
    meetings = Meeting.query.all()
    return jsonify([{
        'id': m.id,
        'committee_id': m.committee_id,
        'title': m.title,
        'meeting_date': m.meeting_date.isoformat(),
        'location': m.location,
        'status': m.status
    } for m in meetings])

@governance_bp.route('/meetings', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_meeting():
    data = request.get_json()
    meeting = Meeting(
        committee_id=data['committee_id'],
        title=data['title'],
        meeting_date=datetime.fromisoformat(data['meeting_date']),
        location=data['location'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(meeting)
    db.session.commit()
    return jsonify({'message': 'Meeting scheduled successfully', 'id': meeting.id}), 201

# Decision Routes
@governance_bp.route('/decisions', methods=['GET'])
@jwt_required()
def get_decisions():
    decisions = Decision.query.all()
    return jsonify([{
        'id': d.id,
        'meeting_id': d.meeting_id,
        'title': d.title,
        'description': d.description,
        'decision_date': d.decision_date.isoformat(),
        'status': d.status
    } for d in decisions])

@governance_bp.route('/decisions', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_decision():
    data = request.get_json()
    decision = Decision(
        meeting_id=data['meeting_id'],
        title=data['title'],
        description=data['description'],
        decision_date=datetime.fromisoformat(data['decision_date']),
        status=data.get('status', 'active')
    )
    db.session.add(decision)
    db.session.commit()
    return jsonify({'message': 'Decision recorded successfully', 'id': decision.id}), 201

# Regulation Routes
@governance_bp.route('/regulations', methods=['GET'])
@jwt_required()
def get_regulations():
    regulations = Regulation.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'description': r.description,
        'category': r.category,
        'effective_date': r.effective_date.isoformat(),
        'status': r.status
    } for r in regulations])

@governance_bp.route('/regulations', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_regulation():
    data = request.get_json()
    regulation = Regulation(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        effective_date=datetime.fromisoformat(data['effective_date']),
        status=data.get('status', 'active')
    )
    db.session.add(regulation)
    db.session.commit()
    return jsonify({'message': 'Regulation created successfully', 'id': regulation.id}), 201

# Governance Report Routes
@governance_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'governance'])
def get_reports():
    reports = GovernanceReport.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'content': r.content,
        'report_type': r.report_type,
        'created_date': r.created_date.isoformat(),
        'status': r.status
    } for r in reports])

@governance_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'governance'])
def create_report():
    data = request.get_json()
    report = GovernanceReport(
        title=data['title'],
        content=data['content'],
        report_type=data['report_type'],
        created_date=datetime.fromisoformat(data['created_date']),
        status=data.get('status', 'draft')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Governance report created successfully', 'id': report.id}), 201 