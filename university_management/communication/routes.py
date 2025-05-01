from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Announcement, Message, Notification, EmailTemplate, SMS, CommunicationChannel, CommunicationGroup
from . import db
from datetime import datetime
from utils import role_required, validate_request, format_response, log_activity, handle_exception

communication_bp = Blueprint('communication', __name__)

# Announcement Routes
@communication_bp.route('/announcements', methods=['GET'])
@jwt_required()
def get_announcements():
    announcements = Announcement.query.all()
    return jsonify([{
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'author_id': a.author_id,
        'publish_date': a.publish_date.isoformat(),
        'expiry_date': a.expiry_date.isoformat() if a.expiry_date else None,
        'priority': a.priority,
        'status': a.status
    } for a in announcements])

@communication_bp.route('/announcements', methods=['POST'])
@jwt_required()
@role_required(['admin', 'communications'])
def create_announcement():
    data = request.get_json()
    announcement = Announcement(
        title=data['title'],
        content=data['content'],
        author_id=data['author_id'],
        publish_date=datetime.fromisoformat(data['publish_date']),
        expiry_date=datetime.fromisoformat(data['expiry_date']) if data.get('expiry_date') else None,
        priority=data.get('priority', 'normal'),
        status=data.get('status', 'draft')
    )
    db.session.add(announcement)
    db.session.commit()
    return jsonify({'message': 'Announcement created successfully', 'id': announcement.id}), 201

# Message Routes
@communication_bp.route('/messages', methods=['GET'])
@jwt_required()
def get_messages():
    messages = Message.query.all()
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'receiver_id': m.receiver_id,
        'content': m.content,
        'sent_date': m.sent_date.isoformat(),
        'read_date': m.read_date.isoformat() if m.read_date else None,
        'status': m.status
    } for m in messages])

@communication_bp.route('/messages', methods=['POST'])
@jwt_required()
def create_message():
    data = request.get_json()
    message = Message(
        sender_id=data['sender_id'],
        receiver_id=data['receiver_id'],
        content=data['content'],
        sent_date=datetime.fromisoformat(data['sent_date']),
        status=data.get('status', 'sent')
    )
    db.session.add(message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully', 'id': message.id}), 201

# Notification Routes
@communication_bp.route('/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([{
        'id': n.id,
        'user_id': n.user_id,
        'title': n.title,
        'content': n.content,
        'notification_type': n.notification_type,
        'created_date': n.created_date.isoformat(),
        'read_date': n.read_date.isoformat() if n.read_date else None,
        'status': n.status
    } for n in notifications])

@communication_bp.route('/notifications', methods=['POST'])
@jwt_required()
@role_required(['admin', 'communications'])
def create_notification():
    data = request.get_json()
    notification = Notification(
        user_id=data['user_id'],
        title=data['title'],
        content=data['content'],
        notification_type=data['notification_type'],
        created_date=datetime.fromisoformat(data['created_date']),
        status=data.get('status', 'unread')
    )
    db.session.add(notification)
    db.session.commit()
    return jsonify({'message': 'Notification created successfully', 'id': notification.id}), 201

# Email Template Routes
@communication_bp.route('/email-templates', methods=['GET'])
@jwt_required()
def get_email_templates():
    templates = EmailTemplate.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'subject': t.subject,
        'content': t.content,
        'status': t.status
    } for t in templates])

@communication_bp.route('/email-templates', methods=['POST'])
@jwt_required()
@role_required(['admin', 'communications'])
def create_email_template():
    data = request.get_json()
    template = EmailTemplate(
        name=data['name'],
        subject=data['subject'],
        content=data['content'],
        status=data.get('status', 'active')
    )
    db.session.add(template)
    db.session.commit()
    return jsonify({'message': 'Email template created successfully', 'id': template.id}), 201

# SMS Routes
@communication_bp.route('/sms', methods=['GET'])
@jwt_required()
def get_sms():
    sms_list = SMS.query.all()
    return jsonify([{
        'id': s.id,
        'recipient_id': s.recipient_id,
        'content': s.content,
        'sent_date': s.sent_date.isoformat(),
        'status': s.status
    } for s in sms_list])

@communication_bp.route('/sms', methods=['POST'])
@jwt_required()
@role_required(['admin', 'communications'])
def create_sms():
    data = request.get_json()
    sms = SMS(
        recipient_id=data['recipient_id'],
        content=data['content'],
        sent_date=datetime.fromisoformat(data['sent_date']),
        status=data.get('status', 'sent')
    )
    db.session.add(sms)
    db.session.commit()
    return jsonify({'message': 'SMS sent successfully', 'id': sms.id}), 201

# Communication Channel Routes
@communication_bp.route('/channels', methods=['GET'])
@jwt_required()
def get_channels():
    channels = CommunicationChannel.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'channel_type': c.channel_type,
        'status': c.status
    } for c in channels])

@communication_bp.route('/channels', methods=['POST'])
@jwt_required()
@role_required(['admin', 'communications'])
def create_channel():
    data = request.get_json()
    channel = CommunicationChannel(
        name=data['name'],
        description=data.get('description'),
        channel_type=data['channel_type'],
        status=data.get('status', 'active')
    )
    db.session.add(channel)
    db.session.commit()
    return jsonify({'message': 'Communication channel created successfully', 'id': channel.id}), 201

# Communication Group Routes
@communication_bp.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    groups = CommunicationGroup.query.all()
    return jsonify([{
        'id': g.id,
        'name': g.name,
        'description': g.description,
        'channel_id': g.channel_id,
        'status': g.status
    } for g in groups])

@communication_bp.route('/groups', methods=['POST'])
@jwt_required()
@role_required(['admin', 'communications'])
def create_group():
    data = request.get_json()
    group = CommunicationGroup(
        name=data['name'],
        description=data.get('description'),
        channel_id=data['channel_id'],
        status=data.get('status', 'active')
    )
    db.session.add(group)
    db.session.commit()
    return jsonify({'message': 'Communication group created successfully', 'id': group.id}), 201 