from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from .models import HealthStaff, Appointment, MedicalRecord, Prescription, HealthReport, HealthEquipment, HealthInventory
from ..auth.models import User
from ..auth.utils import role_required
from datetime import datetime

health_bp = Blueprint('health', __name__)

# Health Staff Routes
@health_bp.route('/staff', methods=['GET'])
@jwt_required()
def get_health_staff():
    staff = HealthStaff.query.all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'staff_type': s.staff_type,
        'specialization': s.specialization,
        'license_number': s.license_number,
        'license_expiry': s.license_expiry.isoformat(),
        'status': s.status
    } for s in staff]), 200

@health_bp.route('/staff', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_staff():
    data = request.get_json()
    staff = HealthStaff(
        user_id=data['user_id'],
        staff_type=data['staff_type'],
        specialization=data.get('specialization'),
        license_number=data['license_number'],
        license_expiry=datetime.fromisoformat(data['license_expiry']).date(),
        status=data.get('status', 'active')
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Health staff created successfully', 'id': staff.id}), 201

# Appointment Routes
@health_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'patient_id': a.patient_id,
        'staff_id': a.staff_id,
        'appointment_type': a.appointment_type,
        'scheduled_date': a.scheduled_date.isoformat(),
        'status': a.status,
        'notes': a.notes
    } for a in appointments]), 200

@health_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    appointment = Appointment(
        patient_id=get_jwt_identity(),
        staff_id=data['staff_id'],
        appointment_type=data['appointment_type'],
        scheduled_date=datetime.fromisoformat(data['scheduled_date']),
        status=data.get('status', 'scheduled'),
        notes=data.get('notes')
    )
    db.session.add(appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment created successfully', 'id': appointment.id}), 201

# Medical Record Routes
@health_bp.route('/medical-records', methods=['GET'])
@jwt_required()
def get_medical_records():
    records = MedicalRecord.query.all()
    return jsonify([{
        'id': r.id,
        'patient_id': r.patient_id,
        'appointment_id': r.appointment_id,
        'diagnosis': r.diagnosis,
        'treatment': r.treatment,
        'notes': r.notes,
        'follow_up_date': r.follow_up_date.isoformat() if r.follow_up_date else None,
        'status': r.status
    } for r in records]), 200

@health_bp.route('/medical-records', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_medical_record():
    data = request.get_json()
    record = MedicalRecord(
        patient_id=data['patient_id'],
        appointment_id=data['appointment_id'],
        diagnosis=data['diagnosis'],
        treatment=data.get('treatment'),
        notes=data.get('notes'),
        follow_up_date=datetime.fromisoformat(data['follow_up_date']) if data.get('follow_up_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(record)
    db.session.commit()
    return jsonify({'message': 'Medical record created successfully', 'id': record.id}), 201

# Prescription Routes
@health_bp.route('/prescriptions', methods=['GET'])
@jwt_required()
def get_prescriptions():
    prescriptions = Prescription.query.all()
    return jsonify([{
        'id': p.id,
        'medical_record_id': p.medical_record_id,
        'staff_id': p.staff_id,
        'medication': p.medication,
        'dosage': p.dosage,
        'frequency': p.frequency,
        'duration': p.duration,
        'instructions': p.instructions,
        'status': p.status
    } for p in prescriptions]), 200

@health_bp.route('/prescriptions', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_prescription():
    data = request.get_json()
    prescription = Prescription(
        medical_record_id=data['medical_record_id'],
        staff_id=get_jwt_identity(),
        medication=data['medication'],
        dosage=data['dosage'],
        frequency=data['frequency'],
        duration=data['duration'],
        instructions=data.get('instructions'),
        status=data.get('status', 'active')
    )
    db.session.add(prescription)
    db.session.commit()
    return jsonify({'message': 'Prescription created successfully', 'id': prescription.id}), 201

# Health Equipment Routes
@health_bp.route('/equipment', methods=['GET'])
@jwt_required()
def get_health_equipment():
    equipment = HealthEquipment.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'equipment_type': e.equipment_type,
        'serial_number': e.serial_number,
        'purchase_date': e.purchase_date.isoformat(),
        'last_maintenance': e.last_maintenance.isoformat() if e.last_maintenance else None,
        'next_maintenance': e.next_maintenance.isoformat() if e.next_maintenance else None,
        'status': e.status
    } for e in equipment]), 200

@health_bp.route('/equipment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_equipment():
    data = request.get_json()
    equipment = HealthEquipment(
        name=data['name'],
        equipment_type=data['equipment_type'],
        serial_number=data['serial_number'],
        purchase_date=datetime.fromisoformat(data['purchase_date']).date(),
        last_maintenance=datetime.fromisoformat(data['last_maintenance']) if data.get('last_maintenance') else None,
        next_maintenance=datetime.fromisoformat(data['next_maintenance']) if data.get('next_maintenance') else None,
        status=data.get('status', 'active')
    )
    db.session.add(equipment)
    db.session.commit()
    return jsonify({'message': 'Health equipment created successfully', 'id': equipment.id}), 201

# Health Inventory Routes
@health_bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_health_inventory():
    inventory = HealthInventory.query.all()
    return jsonify([{
        'id': i.id,
        'item_name': i.item_name,
        'item_type': i.item_type,
        'quantity': i.quantity,
        'unit': i.unit,
        'expiry_date': i.expiry_date.isoformat() if i.expiry_date else None,
        'status': i.status
    } for i in inventory]), 200

@health_bp.route('/inventory', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_inventory():
    data = request.get_json()
    inventory = HealthInventory(
        item_name=data['item_name'],
        item_type=data['item_type'],
        quantity=data['quantity'],
        unit=data['unit'],
        expiry_date=datetime.fromisoformat(data['expiry_date']).date() if data.get('expiry_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(inventory)
    db.session.commit()
    return jsonify({'message': 'Health inventory item created successfully', 'id': inventory.id}), 201

# Health Report Routes
@health_bp.route('/reports', methods=['GET'])
@jwt_required()
@role_required(['admin', 'health'])
def get_health_reports():
    reports = HealthReport.query.all()
    return jsonify([{
        'id': r.id,
        'report_type': r.report_type,
        'patient_id': r.patient_id,
        'content': r.content,
        'created_by': r.created_by,
        'created_at': r.created_at.isoformat(),
        'status': r.status
    } for r in reports]), 200

@health_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'health'])
def create_health_report():
    data = request.get_json()
    report = HealthReport(
        report_type=data['report_type'],
        patient_id=data['patient_id'],
        content=data['content'],
        created_by=get_jwt_identity(),
        status=data.get('status', 'draft')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': 'Health report created successfully', 'id': report.id}), 201 