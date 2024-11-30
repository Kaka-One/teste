from flask import Blueprint, jsonify, request
from models.database import db, Service

services = Blueprint('services', __name__)

@services.route('/services', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([{
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': service.price
    } for service in services])

@services.route('/services', methods=['POST'])
def add_service():
    data = request.json
    new_service = Service(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_service)
    db.session.commit()
    return jsonify({'message': 'Service added successfully!'}), 201
