from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Tuition, Fee, Payment, FinancialAid, Scholarship, Budget, Expense, Revenue, Invoice, Refund
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

finance_bp = Blueprint('finance', __name__)

# Tuition Routes
@finance_bp.route('/tuition', methods=['GET'])
@jwt_required()
def get_tuition_rates():
    tuition_rates = Tuition.query.all()
    return jsonify([{
        'id': t.id,
        'program_id': t.program_id,
        'academic_year': t.academic_year,
        'term': t.term,
        'amount': t.amount,
        'currency': t.currency,
        'status': t.status
    } for t in tuition_rates])

@finance_bp.route('/tuition', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_tuition_rate():
    data = request.get_json()
    tuition = Tuition(
        program_id=data['program_id'],
        academic_year=data['academic_year'],
        term=data['term'],
        amount=data['amount'],
        currency=data['currency'],
        status=data.get('status', 'active')
    )
    db.session.add(tuition)
    db.session.commit()
    return jsonify({'message': 'Tuition rate created successfully', 'id': tuition.id}), 201

# Fee Routes
@finance_bp.route('/fees', methods=['GET'])
@jwt_required()
def get_fees():
    fees = Fee.query.all()
    return jsonify([{
        'id': f.id,
        'name': f.name,
        'description': f.description,
        'amount': f.amount,
        'currency': f.currency,
        'fee_type': f.fee_type,
        'status': f.status
    } for f in fees])

@finance_bp.route('/fees', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_fee():
    data = request.get_json()
    fee = Fee(
        name=data['name'],
        description=data.get('description'),
        amount=data['amount'],
        currency=data['currency'],
        fee_type=data['fee_type'],
        status=data.get('status', 'active')
    )
    db.session.add(fee)
    db.session.commit()
    return jsonify({'message': 'Fee created successfully', 'id': fee.id}), 201

# Payment Routes
@finance_bp.route('/payments', methods=['GET'])
@jwt_required()
def get_payments():
    payments = Payment.query.all()
    return jsonify([{
        'id': p.id,
        'student_id': p.student_id,
        'amount': p.amount,
        'currency': p.currency,
        'payment_date': p.payment_date.isoformat(),
        'payment_method': p.payment_method,
        'transaction_id': p.transaction_id,
        'status': p.status
    } for p in payments])

@finance_bp.route('/payments', methods=['POST'])
@jwt_required()
def create_payment():
    data = request.get_json()
    payment = Payment(
        student_id=data['student_id'],
        amount=data['amount'],
        currency=data['currency'],
        payment_date=datetime.fromisoformat(data['payment_date']),
        payment_method=data['payment_method'],
        transaction_id=data.get('transaction_id'),
        status=data.get('status', 'pending')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully', 'id': payment.id}), 201

# Financial Aid Routes
@finance_bp.route('/financial-aid', methods=['GET'])
@jwt_required()
def get_financial_aid():
    financial_aid = FinancialAid.query.all()
    return jsonify([{
        'id': fa.id,
        'student_id': fa.student_id,
        'aid_type': fa.aid_type,
        'amount': fa.amount,
        'currency': fa.currency,
        'start_date': fa.start_date.isoformat(),
        'end_date': fa.end_date.isoformat(),
        'status': fa.status
    } for fa in financial_aid])

@finance_bp.route('/financial-aid', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_financial_aid():
    data = request.get_json()
    financial_aid = FinancialAid(
        student_id=data['student_id'],
        aid_type=data['aid_type'],
        amount=data['amount'],
        currency=data['currency'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']),
        status=data.get('status', 'active')
    )
    db.session.add(financial_aid)
    db.session.commit()
    return jsonify({'message': 'Financial aid created successfully', 'id': financial_aid.id}), 201

# Scholarship Routes
@finance_bp.route('/scholarships', methods=['GET'])
@jwt_required()
def get_scholarships():
    scholarships = Scholarship.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'amount': s.amount,
        'currency': s.currency,
        'criteria': s.criteria,
        'status': s.status
    } for s in scholarships])

@finance_bp.route('/scholarships', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_scholarship():
    data = request.get_json()
    scholarship = Scholarship(
        name=data['name'],
        description=data.get('description'),
        amount=data['amount'],
        currency=data['currency'],
        criteria=data['criteria'],
        status=data.get('status', 'active')
    )
    db.session.add(scholarship)
    db.session.commit()
    return jsonify({'message': 'Scholarship created successfully', 'id': scholarship.id}), 201

# Budget Routes
@finance_bp.route('/budgets', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance'])
def get_budgets():
    budgets = Budget.query.all()
    return jsonify([{
        'id': b.id,
        'department_id': b.department_id,
        'fiscal_year': b.fiscal_year,
        'amount': b.amount,
        'currency': b.currency,
        'status': b.status
    } for b in budgets])

@finance_bp.route('/budgets', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_budget():
    data = request.get_json()
    budget = Budget(
        department_id=data['department_id'],
        fiscal_year=data['fiscal_year'],
        amount=data['amount'],
        currency=data['currency'],
        status=data.get('status', 'active')
    )
    db.session.add(budget)
    db.session.commit()
    return jsonify({'message': 'Budget created successfully', 'id': budget.id}), 201

# Expense Routes
@finance_bp.route('/expenses', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{
        'id': e.id,
        'department_id': e.department_id,
        'amount': e.amount,
        'currency': e.currency,
        'expense_date': e.expense_date.isoformat(),
        'category': e.category,
        'description': e.description,
        'status': e.status
    } for e in expenses])

@finance_bp.route('/expenses', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_expense():
    data = request.get_json()
    expense = Expense(
        department_id=data['department_id'],
        amount=data['amount'],
        currency=data['currency'],
        expense_date=datetime.fromisoformat(data['expense_date']),
        category=data['category'],
        description=data.get('description'),
        status=data.get('status', 'pending')
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense created successfully', 'id': expense.id}), 201

# Revenue Routes
@finance_bp.route('/revenues', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance'])
def get_revenues():
    revenues = Revenue.query.all()
    return jsonify([{
        'id': r.id,
        'source': r.source,
        'amount': r.amount,
        'currency': r.currency,
        'revenue_date': r.revenue_date.isoformat(),
        'category': r.category,
        'description': r.description,
        'status': r.status
    } for r in revenues])

@finance_bp.route('/revenues', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_revenue():
    data = request.get_json()
    revenue = Revenue(
        source=data['source'],
        amount=data['amount'],
        currency=data['currency'],
        revenue_date=datetime.fromisoformat(data['revenue_date']),
        category=data['category'],
        description=data.get('description'),
        status=data.get('status', 'pending')
    )
    db.session.add(revenue)
    db.session.commit()
    return jsonify({'message': 'Revenue created successfully', 'id': revenue.id}), 201

# Invoice Routes
@finance_bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    invoices = Invoice.query.all()
    return jsonify([{
        'id': i.id,
        'student_id': i.student_id,
        'amount': i.amount,
        'currency': i.currency,
        'due_date': i.due_date.isoformat(),
        'status': i.status
    } for i in invoices])

@finance_bp.route('/invoices', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_invoice():
    data = request.get_json()
    invoice = Invoice(
        student_id=data['student_id'],
        amount=data['amount'],
        currency=data['currency'],
        due_date=datetime.fromisoformat(data['due_date']),
        status=data.get('status', 'pending')
    )
    db.session.add(invoice)
    db.session.commit()
    return jsonify({'message': 'Invoice created successfully', 'id': invoice.id}), 201

# Refund Routes
@finance_bp.route('/refunds', methods=['GET'])
@jwt_required()
@role_required(['admin', 'finance'])
def get_refunds():
    refunds = Refund.query.all()
    return jsonify([{
        'id': r.id,
        'student_id': r.student_id,
        'amount': r.amount,
        'currency': r.currency,
        'refund_date': r.refund_date.isoformat(),
        'reason': r.reason,
        'status': r.status
    } for r in refunds])

@finance_bp.route('/refunds', methods=['POST'])
@jwt_required()
@role_required(['admin', 'finance'])
def create_refund():
    data = request.get_json()
    refund = Refund(
        student_id=data['student_id'],
        amount=data['amount'],
        currency=data['currency'],
        refund_date=datetime.fromisoformat(data['refund_date']),
        reason=data['reason'],
        status=data.get('status', 'pending')
    )
    db.session.add(refund)
    db.session.commit()
    return jsonify({'message': 'Refund created successfully', 'id': refund.id}), 201 