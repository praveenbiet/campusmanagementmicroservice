from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    JobPosting, Company, JobApplication, 
    Internship, InternshipApplication, 
    CareerEvent, EventRegistration, db
)
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

career_bp = Blueprint('career', __name__)

# Job Posting Routes
@career_bp.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = JobPosting.query.filter_by(status='active').all()
        return jsonify([{
            'id': j.id,
            'title': j.title,
            'company_id': j.company_id,
            'company_name': j.company.name,
            'job_type': j.job_type,
            'location': j.location,
            'application_deadline': j.application_deadline.isoformat() if j.application_deadline else None
        } for j in jobs])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/jobs/<id>', methods=['GET'])
def get_job(id):
    try:
        job = JobPosting.query.get_or_404(id)
        return jsonify({
            'id': job.id,
            'title': job.title,
            'company_id': job.company_id,
            'company_name': job.company.name,
            'description': job.description,
            'requirements': job.requirements,
            'responsibilities': job.responsibilities,
            'job_type': job.job_type,
            'location': job.location,
            'salary_min': job.salary_min,
            'salary_max': job.salary_max,
            'currency': job.currency,
            'application_deadline': job.application_deadline.isoformat() if job.application_deadline else None,
            'status': job.status,
            'created_at': job.created_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/jobs', methods=['POST'])
@jwt_required()
@role_required(['admin', 'career_admin', 'employer'])
def create_job():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        job = JobPosting(
            title=data['title'],
            company_id=data['company_id'],
            description=data['description'],
            requirements=data.get('requirements'),
            responsibilities=data.get('responsibilities'),
            job_type=data['job_type'],
            location=data.get('location'),
            salary_min=data.get('salary_min'),
            salary_max=data.get('salary_max'),
            currency=data.get('currency', 'USD'),
            application_deadline=datetime.fromisoformat(data['application_deadline']) if data.get('application_deadline') else None,
            status=data.get('status', 'active'),
            posted_by=user_id
        )
        
        db.session.add(job)
        db.session.commit()
        
        log_activity(user_id, 'create', 'job_posting', job.id)
        
        return jsonify({
            'message': 'Job posting created successfully',
            'id': job.id
        }), 201
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/jobs/<id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'career_admin', 'employer'])
def update_job(id):
    try:
        job = JobPosting.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user is authorized to update this job
        if job.posted_by != user_id and 'admin' not in get_jwt_identity():
            return jsonify({'message': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        for key, value in data.items():
            if key == 'application_deadline' and value:
                setattr(job, key, datetime.fromisoformat(value))
            elif hasattr(job, key):
                setattr(job, key, value)
        
        db.session.commit()
        
        log_activity(user_id, 'update', 'job_posting', id)
        
        return jsonify({
            'message': 'Job posting updated successfully'
        })
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/jobs/<id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'career_admin', 'employer'])
def delete_job(id):
    try:
        job = JobPosting.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user is authorized to delete this job
        if job.posted_by != user_id and 'admin' not in get_jwt_identity():
            return jsonify({'message': 'Unauthorized access'}), 403
        
        db.session.delete(job)
        db.session.commit()
        
        log_activity(user_id, 'delete', 'job_posting', id)
        
        return jsonify({
            'message': 'Job posting deleted successfully'
        })
    except Exception as e:
        return handle_exception(e)

# Company Routes
@career_bp.route('/companies', methods=['GET'])
def get_companies():
    try:
        companies = Company.query.filter_by(status='active').all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'industry': c.industry,
            'website': c.website
        } for c in companies])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/companies/<id>', methods=['GET'])
def get_company(id):
    try:
        company = Company.query.get_or_404(id)
        return jsonify({
            'id': company.id,
            'name': company.name,
            'description': company.description,
            'industry': company.industry,
            'website': company.website,
            'logo_path': company.logo_path,
            'contact_name': company.contact_name,
            'contact_email': company.contact_email,
            'contact_phone': company.contact_phone,
            'status': company.status,
            'created_at': company.created_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/companies', methods=['POST'])
@jwt_required()
@role_required(['admin', 'career_admin', 'employer'])
def create_company():
    try:
        data = request.get_json()
        
        company = Company(
            name=data['name'],
            description=data.get('description'),
            industry=data.get('industry'),
            website=data.get('website'),
            logo_path=data.get('logo_path'),
            contact_name=data.get('contact_name'),
            contact_email=data.get('contact_email'),
            contact_phone=data.get('contact_phone'),
            status=data.get('status', 'active')
        )
        
        db.session.add(company)
        db.session.commit()
        
        return jsonify({
            'message': 'Company created successfully',
            'id': company.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Job Application Routes
@career_bp.route('/job-applications', methods=['GET'])
@jwt_required()
def get_job_applications():
    try:
        user_id = get_jwt_identity()
        applications = JobApplication.query.filter_by(user_id=user_id).all()
        
        return jsonify([{
            'id': a.id,
            'job_id': a.job_id,
            'job_title': a.job.title,
            'company_name': a.job.company.name,
            'application_date': a.application_date.isoformat(),
            'status': a.status
        } for a in applications])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/job-applications/<id>', methods=['GET'])
@jwt_required()
def get_job_application(id):
    try:
        application = JobApplication.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user is authorized to view this application
        if application.user_id != user_id and application.job.posted_by != user_id and 'admin' not in get_jwt_identity():
            return jsonify({'message': 'Unauthorized access'}), 403
        
        return jsonify({
            'id': application.id,
            'job_id': application.job_id,
            'job_title': application.job.title,
            'company_name': application.job.company.name,
            'resume_path': application.resume_path,
            'cover_letter': application.cover_letter,
            'application_date': application.application_date.isoformat(),
            'status': application.status,
            'notes': application.notes,
            'created_at': application.created_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/jobs/<job_id>/apply', methods=['POST'])
@jwt_required()
def apply_for_job(job_id):
    try:
        job = JobPosting.query.get_or_404(job_id)
        
        # Check if job is still active
        if job.status != 'active':
            return jsonify({'message': 'This job is no longer accepting applications'}), 400
        
        # Check if deadline has passed
        if job.application_deadline and job.application_deadline < datetime.utcnow().date():
            return jsonify({'message': 'Application deadline has passed'}), 400
        
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Check if user has already applied
        existing_application = JobApplication.query.filter_by(job_id=job_id, user_id=user_id).first()
        if existing_application:
            return jsonify({'message': 'You have already applied for this job'}), 400
        
        application = JobApplication(
            job_id=job_id,
            user_id=user_id,
            resume_path=data.get('resume_path'),
            cover_letter=data.get('cover_letter')
        )
        
        db.session.add(application)
        db.session.commit()
        
        return jsonify({
            'message': 'Job application submitted successfully',
            'id': application.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Internship Routes
@career_bp.route('/internships', methods=['GET'])
def get_internships():
    try:
        internships = Internship.query.filter_by(status='active').all()
        return jsonify([{
            'id': i.id,
            'title': i.title,
            'company_id': i.company_id,
            'company_name': i.company.name,
            'duration': i.duration,
            'location': i.location,
            'application_deadline': i.application_deadline.isoformat() if i.application_deadline else None
        } for i in internships])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/internships/<id>', methods=['GET'])
def get_internship(id):
    try:
        internship = Internship.query.get_or_404(id)
        return jsonify({
            'id': internship.id,
            'title': internship.title,
            'company_id': internship.company_id,
            'company_name': internship.company.name,
            'description': internship.description,
            'requirements': internship.requirements,
            'responsibilities': internship.responsibilities,
            'duration': internship.duration,
            'start_date': internship.start_date.isoformat() if internship.start_date else None,
            'end_date': internship.end_date.isoformat() if internship.end_date else None,
            'location': internship.location,
            'stipend': internship.stipend,
            'currency': internship.currency,
            'application_deadline': internship.application_deadline.isoformat() if internship.application_deadline else None,
            'status': internship.status,
            'created_at': internship.created_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/internships', methods=['POST'])
@jwt_required()
@role_required(['admin', 'career_admin', 'employer'])
def create_internship():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        internship = Internship(
            title=data['title'],
            company_id=data['company_id'],
            description=data['description'],
            requirements=data.get('requirements'),
            responsibilities=data.get('responsibilities'),
            duration=data.get('duration'),
            start_date=datetime.fromisoformat(data['start_date']).date() if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date']).date() if data.get('end_date') else None,
            location=data.get('location'),
            stipend=data.get('stipend'),
            currency=data.get('currency', 'USD'),
            application_deadline=datetime.fromisoformat(data['application_deadline']).date() if data.get('application_deadline') else None,
            status=data.get('status', 'active'),
            posted_by=user_id
        )
        
        db.session.add(internship)
        db.session.commit()
        
        log_activity(user_id, 'create', 'internship', internship.id)
        
        return jsonify({
            'message': 'Internship created successfully',
            'id': internship.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Career Events Routes
@career_bp.route('/events', methods=['GET'])
def get_career_events():
    try:
        events = CareerEvent.query.filter(
            (CareerEvent.status == 'upcoming') | (CareerEvent.status == 'ongoing')
        ).all()
        
        return jsonify([{
            'id': e.id,
            'title': e.title,
            'event_type': e.event_type,
            'start_date': e.start_date.isoformat(),
            'end_date': e.end_date.isoformat(),
            'location': e.location,
            'status': e.status,
            'registration_fee': e.registration_fee,
            'currency': e.currency
        } for e in events])
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/events/<id>', methods=['GET'])
def get_career_event(id):
    try:
        event = CareerEvent.query.get_or_404(id)
        return jsonify({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'event_type': event.event_type,
            'start_date': event.start_date.isoformat(),
            'end_date': event.end_date.isoformat(),
            'location': event.location,
            'organizer_id': event.organizer_id,
            'capacity': event.capacity,
            'registration_deadline': event.registration_deadline.isoformat() if event.registration_deadline else None,
            'status': event.status,
            'registration_fee': event.registration_fee,
            'currency': event.currency,
            'created_at': event.created_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'career_admin'])
def create_career_event():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        event = CareerEvent(
            title=data['title'],
            description=data['description'],
            event_type=data['event_type'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            location=data.get('location'),
            organizer_id=user_id,
            capacity=data.get('capacity'),
            registration_deadline=datetime.fromisoformat(data['registration_deadline']) if data.get('registration_deadline') else None,
            status=data.get('status', 'upcoming'),
            registration_fee=data.get('registration_fee', 0.0),
            currency=data.get('currency', 'USD')
        )
        
        db.session.add(event)
        db.session.commit()
        
        log_activity(user_id, 'create', 'career_event', event.id)
        
        return jsonify({
            'message': 'Career event created successfully',
            'id': event.id
        }), 201
    except Exception as e:
        return handle_exception(e)

@career_bp.route('/events/<id>/register', methods=['POST'])
@jwt_required()
def register_for_event(id):
    try:
        event = CareerEvent.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if event is still accepting registrations
        if event.status != 'upcoming':
            return jsonify({'message': 'Registration is closed for this event'}), 400
        
        # Check if deadline has passed
        if event.registration_deadline and event.registration_deadline < datetime.utcnow():
            return jsonify({'message': 'Registration deadline has passed'}), 400
        
        # Check if capacity is reached
        if event.capacity:
            current_registrations = EventRegistration.query.filter_by(
                event_id=id, 
                status='registered'
            ).count()
            
            if current_registrations >= event.capacity:
                return jsonify({'message': 'Event is at full capacity'}), 400
        
        # Check if user is already registered
        existing_registration = EventRegistration.query.filter_by(
            event_id=id, 
            user_id=user_id
        ).first()
        
        if existing_registration and existing_registration.status != 'cancelled':
            return jsonify({'message': 'You are already registered for this event'}), 400
        
        data = request.get_json() or {}
        
        if existing_registration:
            existing_registration.status = 'registered'
            existing_registration.updated_at = datetime.utcnow()
            registration = existing_registration
        else:
            registration = EventRegistration(
                event_id=id,
                user_id=user_id,
                status='registered',
                payment_status='pending' if event.registration_fee > 0 else 'not_required'
            )
            db.session.add(registration)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Successfully registered for the event',
            'id': registration.id,
            'payment_required': event.registration_fee > 0,
            'amount': event.registration_fee,
            'currency': event.currency
        }), 201
    except Exception as e:
        return handle_exception(e)