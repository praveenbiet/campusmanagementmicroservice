from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Event, EventRegistration, Venue, EventCategory, EventSpeaker, EventFeedback, EventResource
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

events_bp = Blueprint('events', __name__)

# Event Routes
@events_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = Event.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'category_id': e.category_id,
        'venue_id': e.venue_id,
        'start_date': e.start_date.isoformat(),
        'end_date': e.end_date.isoformat(),
        'capacity': e.capacity,
        'status': e.status
    } for e in events])

@events_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'events'])
def create_event():
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data['description'],
        category_id=data['category_id'],
        venue_id=data['venue_id'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        capacity=data['capacity'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'id': event.id}), 201

# Event Registration Routes
@events_bp.route('/registrations', methods=['GET'])
@jwt_required()
def get_registrations():
    registrations = EventRegistration.query.all()
    return jsonify([{
        'id': r.id,
        'event_id': r.event_id,
        'user_id': r.user_id,
        'registration_date': r.registration_date.isoformat(),
        'status': r.status
    } for r in registrations])

@events_bp.route('/registrations', methods=['POST'])
@jwt_required()
def create_registration():
    data = request.get_json()
    registration = EventRegistration(
        event_id=data['event_id'],
        user_id=data['user_id'],
        registration_date=datetime.fromisoformat(data['registration_date']),
        status=data.get('status', 'confirmed')
    )
    db.session.add(registration)
    db.session.commit()
    return jsonify({'message': 'Registration created successfully', 'id': registration.id}), 201

# Venue Routes
@events_bp.route('/venues', methods=['GET'])
@jwt_required()
def get_venues():
    venues = Venue.query.all()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'location': v.location,
        'capacity': v.capacity,
        'facilities': v.facilities,
        'status': v.status
    } for v in venues])

@events_bp.route('/venues', methods=['POST'])
@jwt_required()
@role_required(['admin', 'events'])
def create_venue():
    data = request.get_json()
    venue = Venue(
        name=data['name'],
        location=data['location'],
        capacity=data['capacity'],
        facilities=data.get('facilities'),
        status=data.get('status', 'active')
    )
    db.session.add(venue)
    db.session.commit()
    return jsonify({'message': 'Venue created successfully', 'id': venue.id}), 201

# Event Category Routes
@events_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = EventCategory.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'status': c.status
    } for c in categories])

@events_bp.route('/categories', methods=['POST'])
@jwt_required()
@role_required(['admin', 'events'])
def create_category():
    data = request.get_json()
    category = EventCategory(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201

# Event Speaker Routes
@events_bp.route('/speakers', methods=['GET'])
@jwt_required()
def get_speakers():
    speakers = EventSpeaker.query.all()
    return jsonify([{
        'id': s.id,
        'event_id': s.event_id,
        'name': s.name,
        'title': s.title,
        'organization': s.organization,
        'bio': s.bio,
        'status': s.status
    } for s in speakers])

@events_bp.route('/speakers', methods=['POST'])
@jwt_required()
@role_required(['admin', 'events'])
def create_speaker():
    data = request.get_json()
    speaker = EventSpeaker(
        event_id=data['event_id'],
        name=data['name'],
        title=data.get('title'),
        organization=data.get('organization'),
        bio=data.get('bio'),
        status=data.get('status', 'confirmed')
    )
    db.session.add(speaker)
    db.session.commit()
    return jsonify({'message': 'Speaker added successfully', 'id': speaker.id}), 201

# Event Feedback Routes
@events_bp.route('/feedback', methods=['GET'])
@jwt_required()
def get_feedback():
    feedback = EventFeedback.query.all()
    return jsonify([{
        'id': f.id,
        'event_id': f.event_id,
        'user_id': f.user_id,
        'rating': f.rating,
        'comments': f.comments,
        'feedback_date': f.feedback_date.isoformat(),
        'status': f.status
    } for f in feedback])

@events_bp.route('/feedback', methods=['POST'])
@jwt_required()
def create_feedback():
    data = request.get_json()
    feedback = EventFeedback(
        event_id=data['event_id'],
        user_id=data['user_id'],
        rating=data['rating'],
        comments=data.get('comments'),
        feedback_date=datetime.fromisoformat(data['feedback_date']),
        status=data.get('status', 'active')
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': 'Feedback submitted successfully', 'id': feedback.id}), 201

# Event Resource Routes
@events_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    resources = EventResource.query.all()
    return jsonify([{
        'id': r.id,
        'event_id': r.event_id,
        'resource_type': r.resource_type,
        'file_path': r.file_path,
        'status': r.status
    } for r in resources])

@events_bp.route('/resources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'events'])
def create_resource():
    data = request.get_json()
    resource = EventResource(
        event_id=data['event_id'],
        resource_type=data['resource_type'],
        file_path=data['file_path'],
        status=data.get('status', 'active')
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({'message': 'Resource added successfully', 'id': resource.id}), 201 