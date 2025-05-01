from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Employee, Department, Position, Payroll, Leave, Attendance, Training, PerformanceReview, Recruitment
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

hr_bp = Blueprint('hr', __name__)

# Employee Routes
@hr_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': e.id,
        'user_id': e.user_id,
        'department_id': e.department_id,
        'position_id': e.position_id,
        'hire_date': e.hire_date.isoformat(),
        'employment_type': e.employment_type,
        'status': e.status
    } for e in employees])

@hr_bp.route('/employees', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_employee():
    data = request.get_json()
    employee = Employee(
        user_id=data['user_id'],
        department_id=data['department_id'],
        position_id=data['position_id'],
        hire_date=datetime.fromisoformat(data['hire_date']),
        employment_type=data['employment_type'],
        status=data.get('status', 'active')
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({'message': 'Employee created successfully', 'id': employee.id}), 201

# Department Routes
@hr_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    departments = Department.query.all()
    return jsonify([{
        'id': d.id,
        'name': d.name,
        'description': d.description,
        'manager_id': d.manager_id,
        'status': d.status
    } for d in departments])

@hr_bp.route('/departments', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_department():
    data = request.get_json()
    department = Department(
        name=data['name'],
        description=data.get('description'),
        manager_id=data.get('manager_id'),
        status=data.get('status', 'active')
    )
    db.session.add(department)
    db.session.commit()
    return jsonify({'message': 'Department created successfully', 'id': department.id}), 201

# Position Routes
@hr_bp.route('/positions', methods=['GET'])
@jwt_required()
def get_positions():
    positions = Position.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'department_id': p.department_id,
        'description': p.description,
        'salary_range': p.salary_range,
        'status': p.status
    } for p in positions])

@hr_bp.route('/positions', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_position():
    data = request.get_json()
    position = Position(
        title=data['title'],
        department_id=data['department_id'],
        description=data.get('description'),
        salary_range=data['salary_range'],
        status=data.get('status', 'active')
    )
    db.session.add(position)
    db.session.commit()
    return jsonify({'message': 'Position created successfully', 'id': position.id}), 201

# Payroll Routes
@hr_bp.route('/payroll', methods=['GET'])
@jwt_required()
@role_required(['admin', 'hr', 'finance'])
def get_payroll():
    payroll = Payroll.query.all()
    return jsonify([{
        'id': p.id,
        'employee_id': p.employee_id,
        'month': p.month,
        'year': p.year,
        'basic_salary': p.basic_salary,
        'allowances': p.allowances,
        'deductions': p.deductions,
        'net_salary': p.net_salary,
        'currency': p.currency,
        'status': p.status
    } for p in payroll])

@hr_bp.route('/payroll', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr', 'finance'])
def create_payroll():
    data = request.get_json()
    payroll = Payroll(
        employee_id=data['employee_id'],
        month=data['month'],
        year=data['year'],
        basic_salary=data['basic_salary'],
        allowances=data.get('allowances', 0),
        deductions=data.get('deductions', 0),
        net_salary=data['net_salary'],
        currency=data['currency'],
        status=data.get('status', 'pending')
    )
    db.session.add(payroll)
    db.session.commit()
    return jsonify({'message': 'Payroll record created successfully', 'id': payroll.id}), 201

# Leave Routes
@hr_bp.route('/leaves', methods=['GET'])
@jwt_required()
def get_leaves():
    leaves = Leave.query.all()
    return jsonify([{
        'id': l.id,
        'employee_id': l.employee_id,
        'leave_type': l.leave_type,
        'start_date': l.start_date.isoformat(),
        'end_date': l.end_date.isoformat(),
        'reason': l.reason,
        'status': l.status
    } for l in leaves])

@hr_bp.route('/leaves', methods=['POST'])
@jwt_required()
def create_leave():
    data = request.get_json()
    leave = Leave(
        employee_id=data['employee_id'],
        leave_type=data['leave_type'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        reason=data['reason'],
        status=data.get('status', 'pending')
    )
    db.session.add(leave)
    db.session.commit()
    return jsonify({'message': 'Leave request created successfully', 'id': leave.id}), 201

# Attendance Routes
@hr_bp.route('/attendance', methods=['GET'])
@jwt_required()
def get_attendance():
    attendance = Attendance.query.all()
    return jsonify([{
        'id': a.id,
        'employee_id': a.employee_id,
        'date': a.date.isoformat(),
        'check_in': a.check_in.isoformat() if a.check_in else None,
        'check_out': a.check_out.isoformat() if a.check_out else None,
        'status': a.status
    } for a in attendance])

@hr_bp.route('/attendance', methods=['POST'])
@jwt_required()
def create_attendance():
    data = request.get_json()
    attendance = Attendance(
        employee_id=data['employee_id'],
        date=datetime.fromisoformat(data['date']),
        check_in=datetime.fromisoformat(data['check_in']) if data.get('check_in') else None,
        check_out=datetime.fromisoformat(data['check_out']) if data.get('check_out') else None,
        status=data.get('status', 'present')
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'message': 'Attendance record created successfully', 'id': attendance.id}), 201

# Training Routes
@hr_bp.route('/trainings', methods=['GET'])
@jwt_required()
def get_trainings():
    trainings = Training.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'start_date': t.start_date.isoformat(),
        'end_date': t.end_date.isoformat(),
        'trainer': t.trainer,
        'status': t.status
    } for t in trainings])

@hr_bp.route('/trainings', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_training():
    data = request.get_json()
    training = Training(
        title=data['title'],
        description=data['description'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        trainer=data['trainer'],
        status=data.get('status', 'scheduled')
    )
    db.session.add(training)
    db.session.commit()
    return jsonify({'message': 'Training created successfully', 'id': training.id}), 201

# Performance Review Routes
@hr_bp.route('/performance-reviews', methods=['GET'])
@jwt_required()
def get_performance_reviews():
    reviews = PerformanceReview.query.all()
    return jsonify([{
        'id': r.id,
        'employee_id': r.employee_id,
        'reviewer_id': r.reviewer_id,
        'review_date': r.review_date.isoformat(),
        'rating': r.rating,
        'comments': r.comments,
        'status': r.status
    } for r in reviews])

@hr_bp.route('/performance-reviews', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_performance_review():
    data = request.get_json()
    review = PerformanceReview(
        employee_id=data['employee_id'],
        reviewer_id=data['reviewer_id'],
        review_date=datetime.fromisoformat(data['review_date']),
        rating=data['rating'],
        comments=data['comments'],
        status=data.get('status', 'draft')
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({'message': 'Performance review created successfully', 'id': review.id}), 201

# Recruitment Routes
@hr_bp.route('/recruitment', methods=['GET'])
@jwt_required()
def get_recruitment():
    recruitment = Recruitment.query.all()
    return jsonify([{
        'id': r.id,
        'position_id': r.position_id,
        'job_title': r.job_title,
        'description': r.description,
        'requirements': r.requirements,
        'status': r.status
    } for r in recruitment])

@hr_bp.route('/recruitment', methods=['POST'])
@jwt_required()
@role_required(['admin', 'hr'])
def create_recruitment():
    data = request.get_json()
    recruitment = Recruitment(
        position_id=data['position_id'],
        job_title=data['job_title'],
        description=data['description'],
        requirements=data['requirements'],
        status=data.get('status', 'open')
    )
    db.session.add(recruitment)
    db.session.commit()
    return jsonify({'message': 'Recruitment record created successfully', 'id': recruitment.id}), 201 