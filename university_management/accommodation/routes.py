from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Dormitory, Room, RoomAssignment, MaintenanceRequest, RoomType, Amenity, RoomAmenity
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

accommodation_bp = Blueprint('accommodation', __name__)

# Dormitory Routes
@accommodation_bp.route('/dormitories', methods=['GET'])
@jwt_required()
def get_dormitories():
    dormitories = Dormitory.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'address': d.address,
        'capacity': d.capacity,
        'gender_type': d.gender_type,
        'status': d.status
    } for d in dormitories])

@accommodation_bp.route('/dormitories', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing'])
def create_dormitory():
    data = request.get_json()
    dormitory = Dormitory(
        name=data['name'],
        address=data['address'],
        capacity=data['capacity'],
        gender_type=data['gender_type'],
        status=data.get('status', 'active')
    )
    db.session.add(dormitory)
    db.session.commit()
    return jsonify({'message': 'Dormitory created successfully', 'id': dormitory.id}), 201

# Room Routes
@accommodation_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{
        'id': r.id,
        'dormitory_id': r.dormitory_id,
        'room_number': r.room_number,
        'room_type_id': r.room_type_id,
        'capacity': r.capacity,
        'status': r.status
    } for r in rooms])

@accommodation_bp.route('/rooms', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing'])
def create_room():
    data = request.get_json()
    room = Room(
        dormitory_id=data['dormitory_id'],
        room_number=data['room_number'],
        room_type_id=data['room_type_id'],
        capacity=data['capacity'],
        status=data.get('status', 'available')
    )
    db.session.add(room)
    db.session.commit()
    return jsonify({'message': 'Room created successfully', 'id': room.id}), 201

# Room Assignment Routes
@accommodation_bp.route('/assignments', methods=['GET'])
@jwt_required()
def get_assignments():
    assignments = RoomAssignment.query.all()
    return jsonify([{
        'id': a.id,
        'room_id': a.room_id,
        'user_id': a.user_id,
        'start_date': a.start_date.isoformat(),
        'end_date': a.end_date.isoformat(),
        'status': a.status
    } for a in assignments])

@accommodation_bp.route('/assignments', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing'])
def create_assignment():
    data = request.get_json()
    assignment = RoomAssignment(
        room_id=data['room_id'],
        user_id=data['user_id'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        status=data.get('status', 'active')
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'message': 'Room assignment created successfully', 'id': assignment.id}), 201

# Maintenance Request Routes
@accommodation_bp.route('/maintenance-requests', methods=['GET'])
@jwt_required()
def get_maintenance_requests():
    requests = MaintenanceRequest.query.all()
    return jsonify([{
        'id': r.id,
        'room_id': r.room_id,
        'user_id': r.user_id,
        'description': r.description,
        'priority': r.priority,
        'status': r.status
    } for r in requests])

@accommodation_bp.route('/maintenance-requests', methods=['POST'])
@jwt_required()
def create_maintenance_request():
    data = request.get_json()
    request = MaintenanceRequest(
        room_id=data['room_id'],
        user_id=data['user_id'],
        description=data['description'],
        priority=data['priority'],
        status=data.get('status', 'pending')
    )
    db.session.add(request)
    db.session.commit()
    return jsonify({'message': 'Maintenance request created successfully', 'id': request.id}), 201

# Room Type Routes
@accommodation_bp.route('/room-types', methods=['GET'])
@jwt_required()
def get_room_types():
    types = RoomType.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'description': t.description,
        'base_rate': t.base_rate,
        'currency': t.currency,
        'status': t.status
    } for t in types])

@accommodation_bp.route('/room-types', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing'])
def create_room_type():
    data = request.get_json()
    room_type = RoomType(
        name=data['name'],
        description=data.get('description'),
        base_rate=data['base_rate'],
        currency=data['currency'],
        status=data.get('status', 'active')
    )
    db.session.add(room_type)
    db.session.commit()
    return jsonify({'message': 'Room type created successfully', 'id': room_type.id}), 201

# Amenity Routes
@accommodation_bp.route('/amenities', methods=['GET'])
@jwt_required()
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'description': a.description,
        'status': a.status
    } for a in amenities])

@accommodation_bp.route('/amenities', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing'])
def create_amenity():
    data = request.get_json()
    amenity = Amenity(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(amenity)
    db.session.commit()
    return jsonify({'message': 'Amenity created successfully', 'id': amenity.id}), 201

# Room Amenity Routes
@accommodation_bp.route('/room-amenities', methods=['GET'])
@jwt_required()
def get_room_amenities():
    room_amenities = RoomAmenity.query.all()
    return jsonify([{
        'id': ra.id,
        'room_id': ra.room_id,
        'amenity_id': ra.amenity_id,
        'status': ra.status
    } for ra in room_amenities])

@accommodation_bp.route('/room-amenities', methods=['POST'])
@jwt_required()
@role_required(['admin', 'housing'])
def create_room_amenity():
    data = request.get_json()
    room_amenity = RoomAmenity(
        room_id=data['room_id'],
        amenity_id=data['amenity_id'],
        status=data.get('status', 'active')
    )
    db.session.add(room_amenity)
    db.session.commit()
    return jsonify({'message': 'Room amenity created successfully', 'id': room_amenity.id}), 201 