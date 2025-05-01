from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Vehicle, Route, Schedule, Driver, Stop, Booking, Maintenance, FuelRecord
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception
from ..auth.models import User
from ..auth.utils import role_required

transportation_bp = Blueprint('transportation', __name__)

# Vehicle Routes
@transportation_bp.route('/vehicles', methods=['GET'])
@jwt_required()
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([{
        'id': v.id,
        'registration_number': v.registration_number,
        'vehicle_type': v.vehicle_type,
        'capacity': v.capacity,
        'status': v.status,
        'last_maintenance': v.last_maintenance.isoformat() if v.last_maintenance else None,
        'next_maintenance': v.next_maintenance.isoformat() if v.next_maintenance else None
    } for v in vehicles]), 200

@transportation_bp.route('/vehicles', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_vehicle():
    data = request.get_json()
    vehicle = Vehicle(
        registration_number=data['registration_number'],
        vehicle_type=data['vehicle_type'],
        capacity=data['capacity'],
        status=data.get('status', 'active')
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({'message': 'Vehicle created successfully', 'id': vehicle.id}), 201

# Route Routes
@transportation_bp.route('/routes', methods=['GET'])
@jwt_required()
def get_routes():
    routes = Route.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'start_location': r.start_location,
        'end_location': r.end_location,
        'distance': r.distance,
        'estimated_time': r.estimated_time,
        'status': r.status
    } for r in routes])

@transportation_bp.route('/routes', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_route():
    data = request.get_json()
    route = Route(
        name=data['name'],
        start_location=data['start_location'],
        end_location=data['end_location'],
        distance=data['distance'],
        estimated_time=data['estimated_time'],
        status=data.get('status', 'active')
    )
    db.session.add(route)
    db.session.commit()
    return jsonify({'message': 'Route created successfully', 'id': route.id}), 201

# Schedule Routes
@transportation_bp.route('/schedules', methods=['GET'])
@jwt_required()
def get_schedules():
    schedules = Schedule.query.all()
    return jsonify([{
        'id': s.id,
        'route_id': s.route_id,
        'vehicle_id': s.vehicle_id,
        'driver_id': s.driver_id,
        'departure_time': s.departure_time.isoformat(),
        'arrival_time': s.arrival_time.isoformat(),
        'status': s.status
    } for s in schedules])

@transportation_bp.route('/schedules', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_schedule():
    data = request.get_json()
    schedule = Schedule(
        route_id=data['route_id'],
        vehicle_id=data['vehicle_id'],
        driver_id=data['driver_id'],
        departure_time=datetime.fromisoformat(data['departure_time']),
        arrival_time=datetime.fromisoformat(data['arrival_time']),
        status=data.get('status', 'active')
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify({'message': 'Schedule created successfully', 'id': schedule.id}), 201

# Driver Routes
@transportation_bp.route('/drivers', methods=['GET'])
@jwt_required()
def get_drivers():
    drivers = Driver.query.all()
    return jsonify([{
        'id': d.id,
        'user_id': d.user_id,
        'license_number': d.license_number,
        'license_expiry': d.license_expiry.isoformat(),
        'status': d.status
    } for d in drivers])

@transportation_bp.route('/drivers', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_driver():
    data = request.get_json()
    driver = Driver(
        user_id=data['user_id'],
        license_number=data['license_number'],
        license_expiry=datetime.fromisoformat(data['license_expiry']),
        status=data.get('status', 'active')
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({'message': 'Driver created successfully', 'id': driver.id}), 201

# Stop Routes
@transportation_bp.route('/stops', methods=['GET'])
@jwt_required()
def get_stops():
    stops = Stop.query.all()
    return jsonify([{
        'id': s.id,
        'route_id': s.route_id,
        'name': s.name,
        'location': s.location,
        'sequence': s.sequence,
        'status': s.status
    } for s in stops])

@transportation_bp.route('/stops', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_stop():
    data = request.get_json()
    stop = Stop(
        route_id=data['route_id'],
        name=data['name'],
        location=data['location'],
        sequence=data['sequence'],
        status=data.get('status', 'active')
    )
    db.session.add(stop)
    db.session.commit()
    return jsonify({'message': 'Stop created successfully', 'id': stop.id}), 201

# Booking Routes
@transportation_bp.route('/bookings', methods=['GET'])
@jwt_required()
def get_bookings():
    bookings = Booking.query.all()
    return jsonify([{
        'id': b.id,
        'schedule_id': b.schedule_id,
        'user_id': b.user_id,
        'booking_date': b.booking_date.isoformat(),
        'status': b.status
    } for b in bookings])

@transportation_bp.route('/bookings', methods=['POST'])
@jwt_required()
def create_booking():
    data = request.get_json()
    booking = Booking(
        schedule_id=data['schedule_id'],
        user_id=data['user_id'],
        booking_date=datetime.fromisoformat(data['booking_date']),
        status=data.get('status', 'confirmed')
    )
    db.session.add(booking)
    db.session.commit()
    return jsonify({'message': 'Booking created successfully', 'id': booking.id}), 201

# Maintenance Routes
@transportation_bp.route('/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance():
    maintenance = Maintenance.query.all()
    return jsonify([{
        'id': m.id,
        'vehicle_id': m.vehicle_id,
        'maintenance_type': m.maintenance_type,
        'description': m.description,
        'date': m.date.isoformat(),
        'cost': m.cost,
        'currency': m.currency,
        'status': m.status
    } for m in maintenance])

@transportation_bp.route('/maintenance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_maintenance():
    data = request.get_json()
    maintenance = Maintenance(
        vehicle_id=data['vehicle_id'],
        maintenance_type=data['maintenance_type'],
        description=data['description'],
        date=datetime.fromisoformat(data['date']),
        cost=data['cost'],
        currency=data['currency'],
        status=data.get('status', 'pending')
    )
    db.session.add(maintenance)
    db.session.commit()
    return jsonify({'message': 'Maintenance record created successfully', 'id': maintenance.id}), 201

# Fuel Record Routes
@transportation_bp.route('/fuel-records', methods=['GET'])
@jwt_required()
def get_fuel_records():
    records = FuelRecord.query.all()
    return jsonify([{
        'id': r.id,
        'vehicle_id': r.vehicle_id,
        'date': r.date.isoformat(),
        'amount': r.amount,
        'cost': r.cost,
        'currency': r.currency,
        'status': r.status
    } for r in records])

@transportation_bp.route('/fuel-records', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_fuel_record():
    data = request.get_json()
    record = FuelRecord(
        vehicle_id=data['vehicle_id'],
        date=datetime.fromisoformat(data['date']),
        amount=data['amount'],
        cost=data['cost'],
        currency=data['currency'],
        status=data.get('status', 'active')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Fuel record created successfully', 'id': record.id}), 201

# Maintenance Record Routes
@transportation_bp.route('/maintenance', methods=['GET'])
@jwt_required()
def get_maintenance_records():
    records = MaintenanceRecord.query.all()
    return jsonify([{
        'id': r.id,
        'vehicle_id': r.vehicle_id,
        'maintenance_type': r.maintenance_type,
        'description': r.description,
        'cost': r.cost,
        'maintenance_date': r.maintenance_date.isoformat(),
        'next_maintenance_date': r.next_maintenance_date.isoformat() if r.next_maintenance_date else None,
        'status': r.status
    } for r in records])

@transportation_bp.route('/maintenance', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_maintenance_record():
    data = request.get_json()
    record = MaintenanceRecord(
        vehicle_id=data['vehicle_id'],
        maintenance_type=data['maintenance_type'],
        description=data.get('description'),
        cost=data.get('cost'),
        maintenance_date=datetime.fromisoformat(data['maintenance_date']),
        next_maintenance_date=datetime.fromisoformat(data['next_maintenance_date']) if data.get('next_maintenance_date') else None,
        status=data.get('status', 'completed')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Maintenance record created successfully', 'id': record.id}), 201

# Transportation Report Routes
@transportation_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'transport'])
def get_transportation_reports():
    reports = TransportationReport.query.all()
    return jsonify([{
        'id': r.id,
        'report_type': r.report_type,
        'content': r.content,
        'created_by': r.created_by,
        'created_at': r.created_at.isoformat(),
        'status': r.status
    } for r in reports])

@transportation_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'transport'])
def create_transportation_report():
    data = request.get_json()
    report = TransportationReport(
        report_type=data['report_type'],
        content=data['content'],
        created_by=get_jwt_identity(),
        status=data.get('status', 'draft')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Report created successfully', 'id': report.id}), 201 