from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Alumni, AlumniEvent, Donation, AlumniGroup, CareerUpdate, Mentorship, AlumniAchievement
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

alumni_bp = Blueprint('alumni', __name__)

# Alumni Profile Routes
@alumni_bp.route('/profiles', methods=['GET'])
@jwt_required()
def get_alumni():
    alumni = Alumni.query.all()
    return jsonify([{
        'id': a.id,
        'user_id': a.user_id,
        'graduation_year': a.graduation_year,
        'degree': a.degree,
        'current_position': a.current_position,
        'company': a.company,
        'status': a.status
    } for a in alumni])

@alumni_bp.route('/profiles', methods=['POST'])
@jwt_required()
def create_alumni():
    data = request.get_json()
    alumni = Alumni(
        user_id=data['user_id'],
        graduation_year=data['graduation_year'],
        degree=data['degree'],
        current_position=data.get('current_position'),
        company=data.get('company'),
        status=data.get('status', 'active')
    )
    db.session.add(alumni)
    db.session.commit()
    return jsonify({'message': 'Alumni profile created successfully', 'id': alumni.id}), 201

# Alumni Event Routes
@alumni_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = AlumniEvent.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'event_date': e.event_date.isoformat(),
        'location': e.location,
        'status': e.status
    } for e in events])

@alumni_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'alumni'])
def create_event():
    data = request.get_json()
    event = AlumniEvent(
        title=data['title'],
        description=data['description'],
        event_date=datetime.fromisoformat(data['event_date']),
        location=data['location'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Alumni event created successfully', 'id': event.id}), 201

# Donation Routes
@alumni_bp.route('/donations', methods=['GET'])
@jwt_required()
@role_required(['admin', 'alumni', 'finance'])
def get_donations():
    donations = Donation.query.all()
    return jsonify([{
        'id': d.id,
        'alumni_id': d.alumni_id,
        'amount': d.amount,
        'currency': d.currency,
        'donation_date': d.donation_date.isoformat(),
        'purpose': d.purpose,
        'status': d.status
    } for d in donations])

@alumni_bp.route('/donations', methods=['POST'])
@jwt_required()
def create_donation():
    data = request.get_json()
    donation = Donation(
        alumni_id=data['alumni_id'],
        amount=data['amount'],
        currency=data['currency'],
        donation_date=datetime.fromisoformat(data['donation_date']),
        purpose=data.get('purpose'),
        status=data.get('status', 'completed')
    )
    db.session.add(donation)
    db.session.commit()
    return jsonify({'message': 'Donation recorded successfully', 'id': donation.id}), 201

# Alumni Group Routes
@alumni_bp.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    groups = AlumniGroup.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'description': g.description,
        'created_date': g.created_date.isoformat(),
        'status': g.status
    } for g in groups])

@alumni_bp.route('/groups', methods=['POST'])
@jwt_required()
@role_required(['admin', 'alumni'])
def create_group():
    data = request.get_json()
    group = AlumniGroup(
        name=data['name'],
        description=data.get('description'),
        created_date=datetime.fromisoformat(data['created_date']),
        status=data.get('status', 'active')
    )
    db.session.add(group)
    db.session.commit()
    return jsonify({'message': 'Alumni group created successfully', 'id': group.id}), 201

# Career Update Routes
@alumni_bp.route('/career-updates', methods=['GET'])
@jwt_required()
def get_career_updates():
    updates = CareerUpdate.query.all()
    return jsonify([{
        'id': u.id,
        'alumni_id': u.alumni_id,
        'position': u.position,
        'company': u.company,
        'update_date': u.update_date.isoformat(),
        'status': u.status
    } for u in updates])

@alumni_bp.route('/career-updates', methods=['POST'])
@jwt_required()
def create_career_update():
    data = request.get_json()
    update = CareerUpdate(
        alumni_id=data['alumni_id'],
        position=data['position'],
        company=data['company'],
        update_date=datetime.fromisoformat(data['update_date']),
        status=data.get('status', 'active')
    )
    db.session.add(update)
    db.session.commit()
    return jsonify({'message': 'Career update recorded successfully', 'id': update.id}), 201

# Mentorship Routes
@alumni_bp.route('/mentorships', methods=['GET'])
@jwt_required()
def get_mentorships():
    mentorships = Mentorship.query.all()
    return jsonify([{
        'id': m.id,
        'alumni_id': m.alumni_id,
        'student_id': m.student_id,
        'start_date': m.start_date.isoformat(),
        'end_date': m.end_date.isoformat() if m.end_date else None,
        'status': m.status
    } for m in mentorships])

@alumni_bp.route('/mentorships', methods=['POST'])
@jwt_required()
def create_mentorship():
    data = request.get_json()
    mentorship = Mentorship(
        alumni_id=data['alumni_id'],
        student_id=data['student_id'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(mentorship)
    db.session.commit()
    return jsonify({'message': 'Mentorship created successfully', 'id': mentorship.id}), 201

# Alumni Achievement Routes
@alumni_bp.route('/achievements', methods=['GET'])
@jwt_required()
def get_achievements():
    achievements = AlumniAchievement.query.all()
    return jsonify([{
        'id': a.id,
        'alumni_id': a.alumni_id,
        'title': a.title,
        'description': a.description,
        'achievement_date': a.achievement_date.isoformat(),
        'status': a.status
    } for a in achievements])

@alumni_bp.route('/achievements', methods=['POST'])
@jwt_required()
def create_achievement():
    data = request.get_json()
    achievement = AlumniAchievement(
        alumni_id=data['alumni_id'],
        title=data['title'],
        description=data['description'],
        achievement_date=datetime.fromisoformat(data['achievement_date']),
        status=data.get('status', 'active')
    )
    db.session.add(achievement)
    db.session.commit()
    return jsonify({'message': 'Alumni achievement recorded successfully', 'id': achievement.id}), 201 