from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tuition(db.Model):
    __tablename__ = 'tuitions'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    academic_year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    due_date = db.Column(db.Date, nullable=False)
    late_fee = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    program = db.relationship('Program', backref=db.backref('tuitions', lazy=True))

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    tuition_id = db.Column(db.Integer, db.ForeignKey('tuitions.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50))  # credit_card, bank_transfer, etc.
    transaction_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed, refunded
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('payments', lazy=True))
    tuition = db.relationship('Tuition', backref=db.backref('payments', lazy=True))

class FinancialAid(db.Model):
    __tablename__ = 'financial_aid'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    aid_type = db.Column(db.String(50), nullable=False)  # scholarship, grant, loan, etc.
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    academic_year = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')  # active, disbursed, cancelled
    disbursement_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship('Student', backref=db.backref('financial_aid', lazy=True))

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    fiscal_year = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # research, equipment, salaries, etc.
    allocated_amount = db.Column(db.Float, nullable=False)
    spent_amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    department = db.relationship('Department', backref=db.backref('budgets', lazy=True))

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    expense_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    budget = db.relationship('Budget', backref=db.backref('expenses', lazy=True)) 