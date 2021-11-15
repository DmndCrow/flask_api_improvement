from typing import List

from flask import Blueprint, request, jsonify


membership_bp = Blueprint('membership_bp', __name__)


@membership_bp.route('/', methods=['GET', 'POST'])
def membership_handle():
    if request.method == 'GET':
        return jsonify({'data': ['mem1', 'mem2']}), 200

    if request.method == 'POST':
        return jsonify({'message': 'created mem1'}), 201


@membership_bp.route('/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
def membership_handle_by_id(_id: str):
    if request.method == 'GET':
        return jsonify({'data': 'mem1'}), 200

    if request.method == 'PUT':
        return jsonify({'message': 'updated mem1'}), 201

    if request.method == 'DELETE':
        return jsonify({'message': 'deleted mem1'}), 202
