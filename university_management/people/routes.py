from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from .models import Person, ContactInfo, Relationship, IdentificationDocument, ProfileStatus, BiometricData, AccessibilityNeeds
from utils import role_required, validate_request, format_response, log_activity, handle_exception, paginate_query, format_paginated_response
from datetime import datetime
import uuid

people_bp = Blueprint('people', __name__)

@people_bp.route('/persons', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def create_person():
    try:
        data = request.get_json()
        
        # Generate unique IDs
        person_id = str(uuid.uuid4())
        unique_id = f"P{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6]}"
        
        # Create person
        person = Person(
            id=person_id,
            unique_id=unique_id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date(),
            gender_identity=data.get('gender_identity'),
            pronouns=data.get('pronouns'),
            nationality=data.get('nationality')
        )
        
        db.session.add(person)
        
        # Create contact info if provided
        if 'contact_info' in data:
            for contact in data['contact_info']:
                contact_id = str(uuid.uuid4())
                contact_info = ContactInfo(
                    id=contact_id,
                    person_id=person_id,
                    contact_type=contact['contact_type'],
                    value=contact['value'],
                    is_primary=contact.get('is_primary', False),
                    address_line1=contact.get('address_line1'),
                    address_line2=contact.get('address_line2'),
                    city=contact.get('city'),
                    state=contact.get('state'),
                    postal_code=contact.get('postal_code'),
                    country=contact.get('country'),
                    geolocation=contact.get('geolocation')
                )
                db.session.add(contact_info)
        
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'person', person_id)
        
        return format_response(person.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@people_bp.route('/persons/<person_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'registrar', 'faculty', 'student'])
def get_person(person_id):
    try:
        person = Person.query.get_or_404(person_id)
        return format_response(person.to_dict())
    except Exception as e:
        return handle_exception(e)

@people_bp.route('/persons', methods=['GET'])
@jwt_required()
@role_required(['admin', 'registrar'])
def list_persons():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Person.query
        pagination = paginate_query(query, page, per_page)
        
        return format_response(format_paginated_response(pagination))
    except Exception as e:
        return handle_exception(e)

@people_bp.route('/persons/<person_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'registrar'])
def update_person(person_id):
    try:
        person = Person.query.get_or_404(person_id)
        data = request.get_json()
        
        # Update person fields
        for field in ['first_name', 'last_name', 'gender_identity', 'pronouns', 'nationality']:
            if field in data:
                setattr(person, field, data[field])
        
        if 'date_of_birth' in data:
            person.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'update', 'person', person_id)
        
        return format_response(person.to_dict())
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@people_bp.route('/persons/<person_id>/contact-info', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def add_contact_info(person_id):
    try:
        person = Person.query.get_or_404(person_id)
        data = request.get_json()
        
        contact_id = str(uuid.uuid4())
        contact_info = ContactInfo(
            id=contact_id,
            person_id=person_id,
            contact_type=data['contact_type'],
            value=data['value'],
            is_primary=data.get('is_primary', False),
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country'),
            geolocation=data.get('geolocation')
        )
        
        db.session.add(contact_info)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'contact_info', contact_id)
        
        return format_response(contact_info.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@people_bp.route('/persons/<person_id>/relationships', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def add_relationship(person_id):
    try:
        data = request.get_json()
        
        relationship_id = str(uuid.uuid4())
        relationship = Relationship(
            id=relationship_id,
            person_id_a=person_id,
            person_id_b=data['person_id_b'],
            relationship_type=data['relationship_type'],
            is_emergency_contact=data.get('is_emergency_contact', False)
        )
        
        db.session.add(relationship)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'relationship', relationship_id)
        
        return format_response(relationship.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@people_bp.route('/persons/<person_id>/documents', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def add_document(person_id):
    try:
        data = request.get_json()
        
        document_id = str(uuid.uuid4())
        document = IdentificationDocument(
            id=document_id,
            person_id=person_id,
            document_type=data['document_type'],
            document_number=data['document_number'],
            expiry_date=datetime.strptime(data['expiry_date'], '%Y-%m-%d').date() if data.get('expiry_date') else None,
            issue_date=datetime.strptime(data['issue_date'], '%Y-%m-%d').date() if data.get('issue_date') else None,
            issuing_authority=data.get('issuing_authority'),
            document_url=data.get('document_url')
        )
        
        db.session.add(document)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'document', document_id)
        
        return format_response(document.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@people_bp.route('/persons/<person_id>/biometric', methods=['POST'])
@jwt_required()
@role_required(['admin', 'security'])
def add_biometric_data(person_id):
    try:
        data = request.get_json()
        
        biometric_id = str(uuid.uuid4())
        biometric = BiometricData(
            id=biometric_id,
            person_id=person_id,
            biometric_type=data['biometric_type'],
            hash_value=data['hash_value'],
            consent_status=data.get('consent_status', False)
        )
        
        db.session.add(biometric)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'biometric', biometric_id)
        
        return format_response(biometric.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e)

@people_bp.route('/persons/<person_id>/accessibility', methods=['POST'])
@jwt_required()
@role_required(['admin', 'registrar'])
def add_accessibility_needs(person_id):
    try:
        data = request.get_json()
        
        accessibility_id = str(uuid.uuid4())
        accessibility = AccessibilityNeeds(
            id=accessibility_id,
            person_id=person_id,
            disability_type=data['disability_type'],
            accommodation_needed=data.get('accommodation_needed'),
            documentation_url=data.get('documentation_url')
        )
        
        db.session.add(accessibility)
        db.session.commit()
        
        # Log activity
        current_user = get_jwt_identity()
        log_activity(current_user['id'], 'create', 'accessibility', accessibility_id)
        
        return format_response(accessibility.to_dict(), 201)
    except Exception as e:
        db.session.rollback()
        return handle_exception(e) 