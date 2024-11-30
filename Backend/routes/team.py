from flask import Blueprint, jsonify, request
from models.database import db, TeamMember

team = Blueprint('team', __name__)

@team.route('/team', methods=['GET'])
def get_team():
    members = TeamMember.query.all()
    return jsonify([{
        'id': member.id,
        'name': member.name,
        'role': member.role
    } for member in members])

@team.route('/team', methods=['POST'])
def add_team_member():
    data = request.json
    new_member = TeamMember(name=data['name'], role=data['role'])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({'message': 'Team member added successfully!'}), 201
