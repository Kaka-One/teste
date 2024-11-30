from flask import Blueprint, jsonify, request
from models.database import db, ContactMessage

contact = Blueprint('contact', __name__)

@contact.route('/contact', methods=['POST'])
def send_message():
    data = request.json
    new_message = ContactMessage(name=data['name'], email=data['email'], message=data['message'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully!'}), 201

@contact.route('/contact', methods=['GET'])
def get_messages():
    messages = ContactMessage.query.all()
    return jsonify([{
        'id': message.id,
        'name': message.name,
        'email': message.email,
        'message': message.message
    } for message in messages])
