from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Book, Author, Publisher, Category, Loan, Reservation, LibraryCard, Fine, Resource, LibraryResource, LibraryMember, LibrarySection, LibraryStaff, LibraryEvent
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

library_bp = Blueprint('library', __name__)

# Book Routes
@library_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    return jsonify([{
        'id': b.id,
        'title': b.title,
        'author': b.author,
        'isbn': b.isbn,
        'section_id': b.section_id,
        'status': b.status,
        'available_copies': b.available_copies
    } for b in books])

@library_bp.route('/books', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_book():
    data = request.get_json()
    book = Book(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        section_id=data['section_id'],
        status=data.get('status', 'available'),
        available_copies=data.get('available_copies', 1)
    )
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully', 'id': book.id}), 201

# Author Routes
@library_bp.route('/authors', methods=['GET'])
@jwt_required()
def get_authors():
    authors = Author.query.all()
    return jsonify([{
        'id': a.id,
        'name': a.name,
        'biography': a.biography,
        'status': a.status
    } for a in authors])

@library_bp.route('/authors', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_author():
    data = request.get_json()
    author = Author(
        name=data['name'],
        biography=data.get('biography'),
        status=data.get('status', 'active')
    )
    db.session.add(author)
    db.session.commit()
    return jsonify({'message': 'Author created successfully', 'id': author.id}), 201

# Publisher Routes
@library_bp.route('/publishers', methods=['GET'])
@jwt_required()
def get_publishers():
    publishers = Publisher.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'address': p.address,
        'contact_info': p.contact_info,
        'status': p.status
    } for p in publishers])

@library_bp.route('/publishers', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_publisher():
    data = request.get_json()
    publisher = Publisher(
        name=data['name'],
        address=data.get('address'),
        contact_info=data.get('contact_info'),
        status=data.get('status', 'active')
    )
    db.session.add(publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher created successfully', 'id': publisher.id}), 201

# Category Routes
@library_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'status': c.status
    } for c in categories])

@library_bp.route('/categories', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_category():
    data = request.get_json()
    category = Category(
        name=data['name'],
        description=data.get('description'),
        status=data.get('status', 'active')
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully', 'id': category.id}), 201

# Loan Routes
@library_bp.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    loans = Loan.query.all()
    return jsonify([{
        'id': l.id,
        'book_id': l.book_id,
        'member_id': l.member_id,
        'loan_date': l.loan_date.isoformat(),
        'due_date': l.due_date.isoformat(),
        'return_date': l.return_date.isoformat() if l.return_date else None,
        'status': l.status
    } for l in loans])

@library_bp.route('/loans', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_loan():
    data = request.get_json()
    loan = Loan(
        book_id=data['book_id'],
        member_id=data['member_id'],
        loan_date=datetime.fromisoformat(data['loan_date']),
        due_date=datetime.fromisoformat(data['due_date']),
        status=data.get('status', 'active')
    )
    db.session.add(loan)
    db.session.commit()
    return jsonify({'message': 'Loan created successfully', 'id': loan.id}), 201

# Reservation Routes
@library_bp.route('/reservations', methods=['GET'])
@jwt_required()
def get_reservations():
    reservations = Reservation.query.all()
    return jsonify([{
        'id': r.id,
        'book_id': r.book_id,
        'user_id': r.user_id,
        'reservation_date': r.reservation_date.isoformat(),
        'status': r.status
    } for r in reservations])

@library_bp.route('/reservations', methods=['POST'])
@jwt_required()
def create_reservation():
    data = request.get_json()
    reservation = Reservation(
        book_id=data['book_id'],
        user_id=data['user_id'],
        reservation_date=datetime.fromisoformat(data['reservation_date']),
        status=data.get('status', 'pending')
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'message': 'Reservation created successfully', 'id': reservation.id}), 201

# Library Card Routes
@library_bp.route('/library-cards', methods=['GET'])
@jwt_required()
def get_library_cards():
    cards = LibraryCard.query.all()
    return jsonify([{
        'id': c.id,
        'user_id': c.user_id,
        'card_number': c.card_number,
        'issue_date': c.issue_date.isoformat(),
        'expiry_date': c.expiry_date.isoformat(),
        'status': c.status
    } for c in cards])

@library_bp.route('/library-cards', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_library_card():
    data = request.get_json()
    card = LibraryCard(
        user_id=data['user_id'],
        card_number=data['card_number'],
        issue_date=datetime.fromisoformat(data['issue_date']),
        expiry_date=datetime.fromisoformat(data['expiry_date']),
        status=data.get('status', 'active')
    )
    db.session.add(card)
    db.session.commit()
    return jsonify({'message': 'Library card created successfully', 'id': card.id}), 201

# Fine Routes
@library_bp.route('/fines', methods=['GET'])
@jwt_required()
def get_fines():
    fines = Fine.query.all()
    return jsonify([{
        'id': f.id,
        'loan_id': f.loan_id,
        'amount': f.amount,
        'currency': f.currency,
        'issue_date': f.issue_date.isoformat(),
        'payment_date': f.payment_date.isoformat() if f.payment_date else None,
        'status': f.status
    } for f in fines])

@library_bp.route('/fines', methods=['POST'])
@jwt_required()
@role_required(['admin', 'librarian'])
def create_fine():
    data = request.get_json()
    fine = Fine(
        loan_id=data['loan_id'],
        amount=data['amount'],
        currency=data['currency'],
        issue_date=datetime.fromisoformat(data['issue_date']),
        status=data.get('status', 'unpaid')
    )
    db.session.add(fine)
    db.session.commit()
    return jsonify({'message': 'Fine created successfully', 'id': fine.id}), 201

# Library Resource Routes
@library_bp.route('/resources', methods=['GET'])
@jwt_required()
def get_resources():
    resources = LibraryResource.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'resource_type': r.resource_type,
        'section_id': r.section_id,
        'status': r.status,
        'available_copies': r.available_copies
    } for r in resources])

@library_bp.route('/resources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_resource():
    data = request.get_json()
    resource = LibraryResource(
        title=data['title'],
        resource_type=data['resource_type'],
        section_id=data['section_id'],
        status=data.get('status', 'available'),
        available_copies=data.get('available_copies', 1)
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({'message': 'Library resource added successfully', 'id': resource.id}), 201

# Library Member Routes
@library_bp.route('/members', methods=['GET'])
@jwt_required()
def get_members():
    members = LibraryMember.query.all()
    return jsonify([{
        'id': m.id,
        'user_id': m.user_id,
        'membership_type': m.membership_type,
        'start_date': m.start_date.isoformat(),
        'end_date': m.end_date.isoformat() if m.end_date else None,
        'status': m.status
    } for m in members])

@library_bp.route('/members', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_member():
    data = request.get_json()
    member = LibraryMember(
        user_id=data['user_id'],
        membership_type=data['membership_type'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(member)
    db.session.commit()
    return jsonify({'message': 'Library member added successfully', 'id': member.id}), 201

# Library Section Routes
@library_bp.route('/sections', methods=['GET'])
@jwt_required()
def get_sections():
    sections = LibrarySection.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'floor': s.floor,
        'status': s.status
    } for s in sections])

@library_bp.route('/sections', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_section():
    data = request.get_json()
    section = LibrarySection(
        name=data['name'],
        description=data.get('description'),
        floor=data['floor'],
        status=data.get('status', 'active')
    )
    db.session.add(section)
    db.session.commit()
    return jsonify({'message': 'Library section created successfully', 'id': section.id}), 201

# Library Staff Routes
@library_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required(['admin', 'library'])
def get_staff():
    staff = LibraryStaff.query.all()
    return jsonify([{
        'id': s.id,
        'user_id': s.user_id,
        'role': s.role,
        'section_id': s.section_id,
        'status': s.status
    } for s in staff])

@library_bp.route('/staff', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_staff():
    data = request.get_json()
    staff = LibraryStaff(
        user_id=data['user_id'],
        role=data['role'],
        section_id=data['section_id'],
        status=data.get('status', 'active')
    )
    db.session.add(staff)
    db.session.commit()
    return jsonify({'message': 'Library staff added successfully', 'id': staff.id}), 201

# Library Event Routes
@library_bp.route('/events', methods=['GET'])
@jwt_required()
def get_events():
    events = LibraryEvent.query.all()
    return jsonify([{
        'id': e.id,
        'title': e.title,
        'description': e.description,
        'event_date': e.event_date.isoformat(),
        'location': e.location,
        'status': e.status
    } for e in events])

@library_bp.route('/events', methods=['POST'])
@jwt_required()
@role_required(['admin', 'library'])
def create_event():
    data = request.get_json()
    event = LibraryEvent(
        title=data['title'],
        description=data['description'],
        event_date=datetime.fromisoformat(data['event_date']),
        location=data['location'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Library event created successfully', 'id': event.id}), 201 