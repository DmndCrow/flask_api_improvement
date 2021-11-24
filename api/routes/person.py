import uuid

from flask import Blueprint, request, jsonify

from api.db_connection.connection import DbConnection
from api.models import Person
from api.utils import remove_extra_keys

person_bp = Blueprint('person_bp', __name__)


@person_bp.route('/', methods=['GET', 'POST'])
def person_handle():
    if request.method == 'GET':
        person_set, status_code = DbConnection().get_people()
        return jsonify({'response': person_set}), status_code

    if request.method == 'POST':
        person, status_code = DbConnection().create_person(request.get_json())
        return jsonify({'response': person}), status_code


@person_bp.route('/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
def person_handle_by_id(_id: str):
    if request.method == 'GET':
        person, status_code = DbConnection().get_person_by_id(_id)
        return jsonify({'response': person}), status_code

    if request.method == 'PUT':
        return jsonify({'message': 'updated user1'}), 201

    if request.method == 'DELETE':
        return jsonify({'message': 'deleted user1'}), 202
