from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    report_type = db.Column(db.String(50), nullable=False)  # academic, financial, enrollment, etc.
    data_source = db.Column(db.String(100), nullable=False)
    query = db.Column(db.Text, nullable=False)
    parameters = db.Column(db.Text)  # JSON string of report parameters
    format = db.Column(db.String(20), default='table')  # table, chart, graph
    schedule = db.Column(db.String(50))  # daily, weekly, monthly, quarterly
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_reports', lazy=True))

class ReportExecution(db.Model):
    __tablename__ = 'report_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    execution_date = db.Column(db.DateTime, nullable=False)
    parameters_used = db.Column(db.Text)  # JSON string of parameters used
    status = db.Column(db.String(20), nullable=False)  # success, failed, in_progress
    error_message = db.Column(db.Text)
    result_path = db.Column(db.String(255))  # Path to the generated report file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    report = db.relationship('Report', backref=db.backref('executions', lazy=True))

class Dashboard(db.Model):
    __tablename__ = 'dashboards'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    layout = db.Column(db.Text)  # JSON string of dashboard layout
    is_public = db.Column(db.Boolean, default=False)
    refresh_interval = db.Column(db.Integer)  # in minutes
    last_refresh = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_dashboards', lazy=True))

class DashboardWidget(db.Model):
    __tablename__ = 'dashboard_widgets'
    
    id = db.Column(db.Integer, primary_key=True)
    dashboard_id = db.Column(db.Integer, db.ForeignKey('dashboards.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    widget_type = db.Column(db.String(50), nullable=False)  # chart, table, metric
    data_source = db.Column(db.String(100), nullable=False)
    query = db.Column(db.Text, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(20))  # small, medium, large
    refresh_interval = db.Column(db.Integer)  # in minutes
    last_refresh = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    dashboard = db.relationship('Dashboard', backref=db.backref('widgets', lazy=True))

class DataSource(db.Model):
    __tablename__ = 'data_sources'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    source_type = db.Column(db.String(50), nullable=False)  # database, api, file
    connection_details = db.Column(db.Text)  # JSON string of connection details
    refresh_interval = db.Column(db.Integer)  # in minutes
    last_refresh = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_data_sources', lazy=True))

class DataSourceRefresh(db.Model):
    __tablename__ = 'data_source_refreshes'
    
    id = db.Column(db.Integer, primary_key=True)
    data_source_id = db.Column(db.Integer, db.ForeignKey('data_sources.id'), nullable=False)
    refresh_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # success, failed, in_progress
    error_message = db.Column(db.Text)
    records_processed = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    data_source = db.relationship('DataSource', backref=db.backref('refreshes', lazy=True))

class AnalyticsAlert(db.Model):
    __tablename__ = 'analytics_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    alert_type = db.Column(db.String(50), nullable=False)  # threshold, anomaly, trend
    data_source = db.Column(db.String(100), nullable=False)
    query = db.Column(db.Text, nullable=False)
    condition = db.Column(db.Text)  # JSON string of alert conditions
    severity = db.Column(db.String(20), default='normal')  # low, normal, high, critical
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('created_alerts', lazy=True))

class AlertTrigger(db.Model):
    __tablename__ = 'alert_triggers'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_id = db.Column(db.Integer, db.ForeignKey('analytics_alerts.id'), nullable=False)
    trigger_date = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.Float)
    threshold = db.Column(db.Float)
    status = db.Column(db.String(20), default='active')  # active, acknowledged, resolved
    acknowledged_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    acknowledged_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    alert = db.relationship('AnalyticsAlert', backref=db.backref('triggers', lazy=True))
    acknowledger = db.relationship('User', foreign_keys=[acknowledged_by], backref=db.backref('acknowledged_alerts', lazy=True))
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref=db.backref('resolved_alerts', lazy=True)) 