from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Facility, Equipment, ResourceAllocation, MaintenanceRequest, ResourceCategory, ResourceBooking
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

resources_bp = Blueprint('resources', __name__)

# Facility Routes
@resources_bp.route('/facilities', methods=['GET'])
@jwt_required()
def get_facilities():
    facilities = Facility.query.all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'description': f.description,
        'location': f.location,
        'capacity': f.capacity,
        'facility_type': f.facility_type,
        'status': f.status
    } for f in facilities])

@resources_bp.route('/facilities', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_facility():
    data = request.get_json()
    facility = Facility(
        name=data['name'],
        description=data.get('description'),
        location=data['location'],
        capacity=data['capacity'],
        facility_type=data['facility_type'],
        status=data.get('status', 'active')
    )
    db.session.add(facility)
    db.session.commit()
    return jsonify({'message': 'Facility created successfully', 'id': facility.id}), 201

# Equipment Routes
@resources_bp.route('/equipment', methods=['GET'])
@jwt_required()
def get_equipment():
    equipment = Equipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'description': e.description,
        'category_id': e.category_id,
        'location': e.location,
        'status': e.status
    } for e in equipment])

@resources_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_equipment():
    data = request.get_json()
    equipment = Equipment(
        name=data['name'],
        description=data.get('description'),
        category_id=data['category_id'],
        location=data['location'],
        status=data.get('status', 'active')
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'Equipment created successfully', 'id': equipment.id}), 201

# Resource Allocation Routes
@resources_bp.route('/allocations', methods=['GET'])
@jwt_required()
def get_allocations():
    allocations = ResourceAllocation.query.all()
    return jsonify([{
        'id': a.id,
        'resource_id': a.resource_id,
        'resource_type': a.resource_type,
        'allocated_to': a.allocated_to,
        'start_date': a.start_date.isoformat(),
        'end_date': a.end_date.isoformat(),
        'status': a.status
    } for a in allocations])

@resources_bp.route('/allocations', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_allocation():
    data = request.get_json()
    allocation = ResourceAllocation(
        resource_id=data['resource_id'],
        resource_type=data['resource_type'],
        allocated_to=data['allocated_to'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        status=data.get('status', 'active')
    )
    db.session.add(allocation)
    db.session.commit()
    return jsonify({'message': 'Resource allocation created successfully', 'id': allocation.id}), 201

# Maintenance Request Routes
@resources_bp.route('/maintenance-requests', methods=['GET'])
@jwt_required()
def get_maintenance_requests():
    requests = MaintenanceRequest.query.all()
    return jsonify([{
        'id': r.id,
        'resource_id': r.resource_id,
        'resource_type': r.resource_type,
        'requested_by': r.requested_by,
        'description': r.description,
        'priority': r.priority,
        'status': r.status
    } for r in requests])

@resources_bp.route('/maintenance-requests', methods=['POST'])
@jwt_required()
def create_maintenance_request():
    data = request.get_json()
    request = MaintenanceRequest(
        resource_id=data['resource_id'],
        resource_type=data['resource_type'],
        requested_by=data['requested_by'],
        description=data['description'],
        priority=data['priority'],
        status=data.get('status', 'pending')
    )
    db.session.add(request)
    db.session.commit()
    return jsonify({'message': 'Maintenance request created successfully', 'id': request.id}), 201

# Resource Category Routes
@resources_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = ResourceCategory.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'status': c.status
    } for c in categories])

@resources_bp.route('/categories', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_category():
    data = request.get_json()
    category = ResourceCategory(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Resource category created successfully', 'id': category.id}), 201

# Resource Booking Routes
@resources_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    bookings = ResourceBooking.query.all()
    return jsonify([{
        'id': b.id,
        'resource_id': b.resource_id,
        'resource_type': b.resource_type,
        'booked_by': b.booked_by,
        'start_time': b.start_time.isoformat(),
        'end_time': b.end_time.isoformat(),
        'purpose': b.purpose,
        'status': b.status
    } for b in bookings])

@resources_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.get_json()
    booking = ResourceBooking(
        resource_id=data['resource_id'],
        resource_type=data['resource_type'],
        booked_by=data['booked_by'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        purpose=data['purpose'],
        status=data.get('status', 'pending')
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Resource booking created successfully', 'id': booking.id}), 201 