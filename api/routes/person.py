from flask import Blueprint, request, jsonify


person_bp = Blueprint('person_bp', __name__)


@person_bp.route('/', methods=['GET', 'POST'])
def person_handle():
    if request.method == 'GET':
        return jsonify({'data': ['user1', 'user2']}), 200

    if request.method == 'POST':
        return jsonify({'message': 'created user1'}), 201


@person_bp.route('/<_id>', methods=['GET', 'PUT', 'DELETE'])
def person_handle_by_id(_id: str):
    if request.method == 'GET':
        return jsonify({'data': 'user1'}), 200

    if request.method == 'PUT':
        return jsonify({'message': 'updated user1'}), 201

    if request.method == 'DELETE':
        return jsonify({'message': 'deleted user1'}), 202
