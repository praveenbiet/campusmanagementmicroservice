from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import (
    Report, ReportExecution, Dashboard, DashboardWidget, 
    DataSource, DataSourceRefresh, AnalyticsAlert, AlertTrigger, db
)
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

analytics_bp = Blueprint('analytics', __name__)

# Report Routes
@analytics_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    try:
        reports = Report.query.all()
        return jsonify([{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'report_type': r.report_type,
            'data_source': r.data_source,
            'format': r.format,
            'schedule': r.schedule,
            'last_run': r.last_run.isoformat() if r.last_run else None,
            'status': r.status
        } for r in reports])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/reports/<id>', methods=['GET'])
@jwt_required()
def get_report(id):
    try:
        report = Report.query.get_or_404(id)
        return jsonify({
            'id': report.id,
            'title': report.title,
            'description': report.description,
            'report_type': report.report_type,
            'data_source': report.data_source,
            'query': report.query,
            'parameters': report.parameters,
            'format': report.format,
            'schedule': report.schedule,
            'last_run': report.last_run.isoformat() if report.last_run else None,
            'next_run': report.next_run.isoformat() if report.next_run else None,
            'status': report.status,
            'created_by': report.created_by,
            'created_at': report.created_at.isoformat(),
            'updated_at': report.updated_at.isoformat()
        })
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/reports', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def create_report():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        report = Report(
            title=data['title'],
            description=data.get('description'),
            report_type=data['report_type'],
            data_source=data['data_source'],
            query=data['query'],
            parameters=data.get('parameters'),
            format=data.get('format', 'table'),
            schedule=data.get('schedule'),
            status=data.get('status', 'active'),
            created_by=user_id
        )
        
        db.session.add(report)
        db.session.commit()
        
        log_activity(user_id, 'create', 'report', report.id)
        
        return jsonify({
            'message': 'Report created successfully',
            'id': report.id
        }), 201
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/reports/<id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'analytics'])
def update_report(id):
    try:
        report = Report.query.get_or_404(id)
        data = request.get_json()
        user_id = get_jwt_identity()
        
        for key, value in data.items():
            if hasattr(report, key):
                setattr(report, key, value)
        
        db.session.commit()
        
        log_activity(user_id, 'update', 'report', id)
        
        return jsonify({
            'message': 'Report updated successfully'
        })
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/reports/<id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'analytics'])
def delete_report(id):
    try:
        report = Report.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        db.session.delete(report)
        db.session.commit()
        
        log_activity(user_id, 'delete', 'report', id)
        
        return jsonify({
            'message': 'Report deleted successfully'
        })
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/reports/<id>/execute', methods=['POST'])
@jwt_required()
def execute_report(id):
    try:
        report = Report.query.get_or_404(id)
        data = request.get_json() or {}
        user_id = get_jwt_identity()
        
        # Logic to execute report query would go here
        # This is a placeholder for actual execution logic
        
        execution = ReportExecution(
            report_id=report.id,
            execution_date=datetime.utcnow(),
            parameters_used=str(data.get('parameters', {})),
            status='success',
            result_path=f"/reports/{report.id}/executions/{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        )
        
        db.session.add(execution)
        
        # Update the report's last run time
        report.last_run = datetime.utcnow()
        
        db.session.commit()
        
        log_activity(user_id, 'execute', 'report', id)
        
        return jsonify({
            'message': 'Report executed successfully',
            'execution_id': execution.id,
            'result_path': execution.result_path
        })
    except Exception as e:
        return handle_exception(e)

# Dashboard Routes
@analytics_bp.route('/dashboards', methods=['GET'])
@jwt_required()
def get_dashboards():
    try:
        user_id = get_jwt_identity()
        dashboards = Dashboard.query.filter(
            (Dashboard.created_by == user_id) | (Dashboard.is_public == True)
        ).all()
        
        return jsonify([{
            'id': d.id,
            'title': d.title,
            'description': d.description,
            'is_public': d.is_public,
            'created_by': d.created_by,
            'created_at': d.created_at.isoformat()
        } for d in dashboards])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/dashboards/<id>', methods=['GET'])
@jwt_required()
def get_dashboard(id):
    try:
        dashboard = Dashboard.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        # Check if user has access to this dashboard
        if not dashboard.is_public and dashboard.created_by != user_id:
            return jsonify({'message': 'Unauthorized access'}), 403
        
        widgets = DashboardWidget.query.filter_by(dashboard_id=dashboard.id).order_by(DashboardWidget.position).all()
        
        return jsonify({
            'id': dashboard.id,
            'title': dashboard.title,
            'description': dashboard.description,
            'layout': dashboard.layout,
            'is_public': dashboard.is_public,
            'refresh_interval': dashboard.refresh_interval,
            'last_refresh': dashboard.last_refresh.isoformat() if dashboard.last_refresh else None,
            'status': dashboard.status,
            'created_by': dashboard.created_by,
            'created_at': dashboard.created_at.isoformat(),
            'updated_at': dashboard.updated_at.isoformat(),
            'widgets': [{
                'id': w.id,
                'title': w.title,
                'widget_type': w.widget_type,
                'data_source': w.data_source,
                'position': w.position,
                'size': w.size,
                'refresh_interval': w.refresh_interval,
                'last_refresh': w.last_refresh.isoformat() if w.last_refresh else None
            } for w in widgets]
        })
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/dashboards', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def create_dashboard():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        dashboard = Dashboard(
            title=data['title'],
            description=data.get('description'),
            layout=data.get('layout'),
            is_public=data.get('is_public', False),
            refresh_interval=data.get('refresh_interval'),
            status=data.get('status', 'active'),
            created_by=user_id
        )
        
        db.session.add(dashboard)
        db.session.commit()
        
        log_activity(user_id, 'create', 'dashboard', dashboard.id)
        
        return jsonify({
            'message': 'Dashboard created successfully',
            'id': dashboard.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Widget Routes
@analytics_bp.route('/dashboards/<dashboard_id>/widgets', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def create_widget(dashboard_id):
    try:
        dashboard = Dashboard.query.get_or_404(dashboard_id)
        user_id = get_jwt_identity()
        
        # Ensure user owns the dashboard
        if dashboard.created_by != user_id:
            return jsonify({'message': 'Unauthorized access'}), 403
        
        data = request.get_json()
        
        widget = DashboardWidget(
            dashboard_id=dashboard_id,
            title=data['title'],
            widget_type=data['widget_type'],
            data_source=data['data_source'],
            query=data['query'],
            position=data['position'],
            size=data.get('size', 'medium'),
            refresh_interval=data.get('refresh_interval')
        )
        
        db.session.add(widget)
        db.session.commit()
        
        return jsonify({
            'message': 'Widget created successfully',
            'id': widget.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Data Source Routes
@analytics_bp.route('/data-sources', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analytics'])
def get_data_sources():
    try:
        data_sources = DataSource.query.all()
        return jsonify([{
            'id': ds.id,
            'name': ds.name,
            'description': ds.description,
            'source_type': ds.source_type,
            'status': ds.status
        } for ds in data_sources])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/data-sources', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def create_data_source():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        data_source = DataSource(
            name=data['name'],
            description=data.get('description'),
            source_type=data['source_type'],
            connection_details=data['connection_details'],
            refresh_interval=data.get('refresh_interval'),
            status=data.get('status', 'active'),
            created_by=user_id
        )
        
        db.session.add(data_source)
        db.session.commit()
        
        return jsonify({
            'message': 'Data source created successfully',
            'id': data_source.id
        }), 201
    except Exception as e:
        return handle_exception(e)

# Alert Routes
@analytics_bp.route('/alerts', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analytics'])
def get_alerts():
    try:
        alerts = AnalyticsAlert.query.all()
        return jsonify([{
            'id': a.id,
            'title': a.title,
            'alert_type': a.alert_type,
            'severity': a.severity,
            'is_active': a.is_active
        } for a in alerts])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/alerts', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def create_alert():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        alert = AnalyticsAlert(
            title=data['title'],
            description=data.get('description'),
            alert_type=data['alert_type'],
            data_source=data['data_source'],
            query=data['query'],
            condition=data['condition'],
            severity=data.get('severity', 'normal'),
            is_active=data.get('is_active', True),
            created_by=user_id
        )
        
        db.session.add(alert)
        db.session.commit()
        
        return jsonify({
            'message': 'Alert created successfully',
            'id': alert.id
        }), 201
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/alerts/<id>/triggers', methods=['GET'])
@jwt_required()
@role_required(['admin', 'analytics'])
def get_alert_triggers(id):
    try:
        triggers = AlertTrigger.query.filter_by(alert_id=id).order_by(AlertTrigger.trigger_date.desc()).all()
        return jsonify([{
            'id': t.id,
            'alert_id': t.alert_id,
            'trigger_date': t.trigger_date.isoformat(),
            'value': t.value,
            'threshold': t.threshold,
            'status': t.status
        } for t in triggers])
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/alerts/triggers/<id>/acknowledge', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def acknowledge_trigger(id):
    try:
        trigger = AlertTrigger.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        trigger.status = 'acknowledged'
        trigger.acknowledged_by = user_id
        trigger.acknowledged_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Alert trigger acknowledged successfully'
        })
    except Exception as e:
        return handle_exception(e)

@analytics_bp.route('/alerts/triggers/<id>/resolve', methods=['POST'])
@jwt_required()
@role_required(['admin', 'analytics'])
def resolve_trigger(id):
    try:
        trigger = AlertTrigger.query.get_or_404(id)
        user_id = get_jwt_identity()
        
        trigger.status = 'resolved'
        trigger.resolved_by = user_id
        trigger.resolved_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Alert trigger resolved successfully'
        })
    except Exception as e:
        return handle_exception(e)