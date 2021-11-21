import uuid

from flask import Blueprint, request, jsonify

from api.models import Person
from api.db_connection.neo4j_connection import Neo4jConnection
from api.db_connection.elastic_connection import ElasticConnection
from api.utils import remove_extra_keys

person_bp = Blueprint('person_bp', __name__)


@person_bp.route('/', methods=['GET', 'POST'])
def person_handle():
    if request.method == 'GET':
        person_set_response = []

        es = ElasticConnection()
        person_set, status_code = es.get_object_by_id('person')

        for person in person_set:
            person_set_response.append(person)
        es.close()

        return jsonify({'response': person_set_response}), status_code

    if request.method == 'POST':
        person_body = remove_extra_keys(request.get_json(), Person)
        person_body.id = str(uuid.uuid4())

        es = ElasticConnection()
        person, status_code = es.create_object('person', person_body, person_body.id)
        es.close()

        return jsonify({'response': person[0] if len(person) else None}), status_code


@person_bp.route('/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
def person_handle_by_id(_id: str):
    if request.method == 'GET':
        es = ElasticConnection()
        person, status_code = es.get_object_by_id('person', _id)
        es.close()

        return jsonify({'response': person[0] if len(person) else None}), status_code

    if request.method == 'PUT':
        return jsonify({'message': 'updated user1'}), 201

    if request.method == 'DELETE':
        return jsonify({'message': 'deleted user1'}), 202
