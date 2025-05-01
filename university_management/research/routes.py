from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import ResearchProject, Publication, Funding, ResearchTeam, Conference, Patent, ResearchEquipment
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

research_bp = Blueprint('research', __name__)

# Research Project Routes
@research_bp.route('/projects', methods=['GET'])
@jwt_required()
def get_projects():
    projects = ResearchProject.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'start_date': p.start_date.isoformat(),
        'end_date': p.end_date.isoformat() if p.end_date else None,
        'status': p.status
    } for p in projects])

@research_bp.route('/projects', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research'])
def create_project():
    data = request.get_json()
    project = ResearchProject(
        title=data['title'],
        description=data['description'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({'message': 'Research project created successfully', 'id': project.id}), 201

# Publication Routes
@research_bp.route('/publications', methods=['GET'])
@jwt_required()
def get_publications():
    publications = Publication.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'authors': p.authors,
        'journal': p.journal,
        'publication_date': p.publication_date.isoformat(),
        'doi': p.doi,
        'status': p.status
    } for p in publications])

@research_bp.route('/publications', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research'])
def create_publication():
    data = request.get_json()
    publication = Publication(
        title=data['title'],
        authors=data['authors'],
        journal=data['journal'],
        publication_date=datetime.fromisoformat(data['publication_date']),
        doi=data.get('doi'),
        status=data.get('status', 'published')
    )
    db.session.add(publication)
    db.session.commit()
    return jsonify({'message': 'Publication recorded successfully', 'id': publication.id}), 201

# Funding Routes
@research_bp.route('/funding', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research', 'finance'])
def get_funding():
    funding = Funding.query.all()
    return jsonify([{
        'id': f.id,
        'project_id': f.project_id,
        'source': f.source,
        'amount': f.amount,
        'currency': f.currency,
        'start_date': f.start_date.isoformat(),
        'end_date': f.end_date.isoformat() if f.end_date else None,
        'status': f.status
    } for f in funding])

@research_bp.route('/funding', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research', 'finance'])
def create_funding():
    data = request.get_json()
    funding = Funding(
        project_id=data['project_id'],
        source=data['source'],
        amount=data['amount'],
        currency=data['currency'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(funding)
    db.session.commit()
    return jsonify({'message': 'Funding recorded successfully', 'id': funding.id}), 201

# Research Team Routes
@research_bp.route('/teams', methods=['GET'])
@jwt_required()
def get_teams():
    teams = ResearchTeam.query.all()
    return jsonify([{
        'id': t.id,
        'project_id': t.project_id,
        'team_leader_id': t.team_leader_id,
        'team_name': t.team_name,
        'status': t.status
    } for t in teams])

@research_bp.route('/teams', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research'])
def create_team():
    data = request.get_json()
    team = ResearchTeam(
        project_id=data['project_id'],
        team_leader_id=data['team_leader_id'],
        team_name=data['team_name'],
        status=data.get('status', 'active')
    )
    db.session.add(team)
    db.session.commit()
    return jsonify({'message': 'Research team created successfully', 'id': team.id}), 201

# Conference Routes
@research_bp.route('/conferences', methods=['GET'])
@jwt_required()
def get_conferences():
    conferences = Conference.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'location': c.location,
        'start_date': c.start_date.isoformat(),
        'end_date': c.end_date.isoformat(),
        'status': c.status
    } for c in conferences])

@research_bp.route('/conferences', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research'])
def create_conference():
    data = request.get_json()
    conference = Conference(
        name=data['name'],
        location=data['location'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        status=data.get('status', 'scheduled')
    )
    db.session.add(conference)
    db.session.commit()
    return jsonify({'message': 'Conference created successfully', 'id': conference.id}), 201

# Patent Routes
@research_bp.route('/patents', methods=['GET'])
@jwt_required()
def get_patents():
    patents = Patent.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'inventors': p.inventors,
        'filing_date': p.filing_date.isoformat(),
        'grant_date': p.grant_date.isoformat() if p.grant_date else None,
        'patent_number': p.patent_number,
        'status': p.status
    } for p in patents])

@research_bp.route('/patents', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research'])
def create_patent():
    data = request.get_json()
    patent = Patent(
        title=data['title'],
        inventors=data['inventors'],
        filing_date=datetime.fromisoformat(data['filing_date']),
        grant_date=datetime.fromisoformat(data['grant_date']) if data.get('grant_date') else None,
        patent_number=data.get('patent_number'),
        status=data.get('status', 'pending')
    )
    db.session.add(patent)
    db.session.commit()
    return jsonify({'message': 'Patent recorded successfully', 'id': patent.id}), 201

# Research Equipment Routes
@research_bp.route('/equipment', methods=['GET'])
@jwt_required()
@role_required(['admin', 'research'])
def get_equipment():
    equipment = ResearchEquipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'type': e.type,
        'location': e.location,
        'status': e.status,
        'last_maintenance': e.last_maintenance.isoformat() if e.last_maintenance else None
    } for e in equipment])

@research_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'research'])
def create_equipment():
    data = request.get_json()
    equipment = ResearchEquipment(
        name=data['name'],
        type=data['type'],
        location=data['location'],
        status=data.get('status', 'active'),
        last_maintenance=datetime.fromisoformat(data['last_maintenance']) if data.get('last_maintenance') else None
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'Research equipment added successfully', 'id': equipment.id}), 201 