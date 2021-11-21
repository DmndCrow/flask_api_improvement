import uuid

from flask import Blueprint, request, jsonify

from api.db_connection.elastic_connection import ElasticConnection
from api.models import Organization
from api.utils import remove_extra_keys

organization_bp = Blueprint('organization_bp', __name__)


@organization_bp.route('/', methods=['GET', 'POST'])
def organization_handle():
    if request.method == 'GET':
        organization_set_response = []

        es = ElasticConnection()
        organization_set, status_code = es.get_object_by_id('organization')

        for organization in organization_set:
            organization_set_response.append(organization)
        es.close()

        return jsonify({'response': organization_set_response}), status_code

    if request.method == 'POST':
        organization_body = remove_extra_keys(request.get_json(), Organization)
        organization_body.group_id = str(uuid.uuid4())

        es = ElasticConnection()
        organization, status_code = es.create_object('organization', organization_body, organization_body.group_id)
        es.close()

        return jsonify({'response': organization[0] if len(organization) else None}), status_code


@organization_bp.route('/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
def organization_handle_by_id(_id: str):
    if request.method == 'GET':
        es = ElasticConnection()
        organization, status_code = es.get_object_by_id('organization', _id)
        es.close()

        return jsonify({'response': organization[0] if len(organization) else None}), status_code

    if request.method == 'PUT':
        return jsonify({'message': 'updated org1'}), 201

    if request.method == 'DELETE':
        return jsonify({'message': 'deleted org1'}), 202
