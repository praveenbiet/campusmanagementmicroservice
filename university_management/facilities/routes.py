from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Building, Room, Maintenance, Equipment, FacilityStaff, FacilityBooking, FacilityReport
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

facilities_bp = Blueprint('facilities', __name__)

# Building Routes
@facilities_bp.route('/buildings', methods=['GET'])
@jwt_required()
def get_buildings():
    buildings = Building.query.all()
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'code': b.code,
        'address': b.address,
        'floors': b.floors,
        'status': b.status
    } for b in buildings])

@facilities_bp.route('/buildings', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_building():
    data = request.get_json()
    building = Building(
        name=data['name'],
        code=data['code'],
        address=data['address'],
        floors=data['floors'],
        status=data.get('status', 'active')
    )
    db.session.add(building)
    db.session.commit()
    return jsonify({'message': 'Building added successfully', 'id': building.id}), 201

# Room Routes
@facilities_bp.route('/rooms', methods=['GET'])
@jwt_required()
def get_rooms():
    rooms = Room.query.all()
    return jsonify([{
        'id': r.id,
        'building_id': r.building_id,
        'room_number': r.room_number,
        'room_type': r.room_type,
        'capacity': r.capacity,
        'status': r.status
    } for r in rooms])

@facilities_bp.route('/rooms', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_room():
    data = request.get_json()
    room = Room(
        building_id=data['building_id'],
        room_number=data['room_number'],
        room_type=data['room_type'],
        capacity=data['capacity'],
        status=data.get('status', 'available')
    )
    db.session.add(room)
    db.session.commit()
    return jsonify({'message': 'Room added successfully', 'id': room.id}), 201

# Maintenance Routes
@facilities_bp.route('/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance():
    maintenance = Maintenance.query.all()
    return jsonify([{
        'id': m.id,
        'building_id': m.building_id,
        'room_id': m.room_id,
        'maintenance_type': m.maintenance_type,
        'description': m.description,
        'scheduled_date': m.scheduled_date.isoformat(),
        'completed_date': m.completed_date.isoformat() if m.completed_date else None,
        'status': m.status
    } for m in maintenance])

@facilities_bp.route('/maintenance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_maintenance():
    data = request.get_json()
    maintenance = Maintenance(
        building_id=data['building_id'],
        room_id=data.get('room_id'),
        maintenance_type=data['maintenance_type'],
        description=data['description'],
        scheduled_date=datetime.fromisoformat(data['scheduled_date']),
        status=data.get('status', 'scheduled')
    )
    db.session.add(maintenance)
    db.session.commit()
    return jsonify({'message': 'Maintenance scheduled successfully', 'id': maintenance.id}), 201

# Equipment Routes
@facilities_bp.route('/equipment', methods=['GET'])
@jwt_required()
def get_equipment():
    equipment = Equipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'equipment_type': e.equipment_type,
        'location_id': e.location_id,
        'purchase_date': e.purchase_date.isoformat(),
        'last_maintenance': e.last_maintenance.isoformat() if e.last_maintenance else None,
        'status': e.status
    } for e in equipment])

@facilities_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_equipment():
    data = request.get_json()
    equipment = Equipment(
        name=data['name'],
        equipment_type=data['equipment_type'],
        location_id=data['location_id'],
        purchase_date=datetime.fromisoformat(data['purchase_date']),
        status=data.get('status', 'active')
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'Equipment added successfully', 'id': equipment.id}), 201

# Facility Staff Routes
@facilities_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities'])
def get_staff():
    staff = FacilityStaff.query.all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'role': s.role,
        'department': s.department,
        'status': s.status
    } for s in staff])

@facilities_bp.route('/staff', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_staff():
    data = request.get_json()
    staff = FacilityStaff(
        user_id=data['user_id'],
        role=data['role'],
        department=data['department'],
        status=data.get('status', 'active')
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Facility staff added successfully', 'id': staff.id}), 201

# Facility Booking Routes
@facilities_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    bookings = FacilityBooking.query.all()
    return jsonify([{
        'id': b.id,
        'room_id': b.room_id,
        'user_id': b.user_id,
        'purpose': b.purpose,
        'start_time': b.start_time.isoformat(),
        'end_time': b.end_time.isoformat(),
        'status': b.status
    } for b in bookings])

@facilities_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.get_json()
    booking = FacilityBooking(
        room_id=data['room_id'],
        user_id=data['user_id'],
        purpose=data['purpose'],
        start_time=datetime.fromisoformat(data['start_time']),
        end_time=datetime.fromisoformat(data['end_time']),
        status=data.get('status', 'pending')
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Facility booking created successfully', 'id': booking.id}), 201

# Facility Report Routes
@facilities_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'facilities'])
def get_reports():
    reports = FacilityReport.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'content': r.content,
        'report_type': r.report_type,
        'created_by': r.created_by,
        'created_at': r.created_at.isoformat(),
        'status': r.status
    } for r in reports])

@facilities_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'facilities'])
def create_report():
    data = request.get_json()
    report = FacilityReport(
        title=data['title'],
        content=data['content'],
        report_type=data['report_type'],
        created_by=data['created_by'],
        created_at=datetime.fromisoformat(data['created_at']),
        status=data.get('status', 'draft')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Facility report created successfully', 'id': report.id}), 201 