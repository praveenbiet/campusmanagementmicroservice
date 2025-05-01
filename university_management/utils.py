import os
import json
import logging
from datetime import datetime
from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def role_required(roles):
    """
    Decorator to check if the user has the required role(s)
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            if current_user['role'] not in roles:
                return jsonify({'message': 'Insufficient permissions'}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

def validate_request(schema):
    """
    Decorator to validate request data against a schema
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                data = request.get_json()
                schema.validate(data)
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'message': str(e)}), 400
        return decorator
    return wrapper

def generate_unique_id(prefix):
    """
    Generate a unique ID with a prefix
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_str = os.urandom(4).hex()
    return f"{prefix}_{timestamp}_{random_str}"

def format_response(data, status_code=200, message=None):
    """
    Format API response consistently
    """
    response = {
        'status': 'success' if status_code < 400 else 'error',
        'data': data
    }
    if message:
        response['message'] = message
    return jsonify(response), status_code

def log_activity(user_id, action, entity_type, entity_id, details=None):
    """
    Log user activity
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'action': action,
        'entity_type': entity_type,
        'entity_id': entity_id,
        'details': details
    }
    logger.info(json.dumps(log_entry))

def handle_exception(e):
    """
    Handle exceptions consistently
    """
    logger.error(str(e))
    return format_response(
        None,
        status_code=500,
        message='An unexpected error occurred'
    )

def paginate_query(query, page, per_page):
    """
    Paginate SQLAlchemy query
    """
    return query.paginate(page=page, per_page=per_page, error_out=False)

def format_paginated_response(pagination):
    """
    Format paginated response
    """
    return {
        'items': [item.to_dict() for item in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': pagination.per_page
    } 