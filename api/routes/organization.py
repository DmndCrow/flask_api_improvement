from flask import Blueprint, request, jsonify

organization_bp = Blueprint('organization_bp', __name__)


@organization_bp.route('/', methods=['GET', 'POST'])
def organization_handle():
    if request.method == 'GET':
        return jsonify({'data': ['org1', 'org2']}), 200

    if request.method == 'POST':
        return jsonify({'message': 'created org1'}), 201


@organization_bp.route('/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
def organization_handle_by_id(_id: str):
    if request.method == 'GET':
        return jsonify({'data': 'org1'}), 200

    if request.method == 'PUT':
        return jsonify({'message': 'updated org1'}), 201

    if request.method == 'DELETE':
        return jsonify({'message': 'deleted org1'}), 202
