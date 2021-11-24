from flask import Blueprint, request, jsonify

from api.db_connection.connection import DbConnection

organization_bp = Blueprint('organization_bp', __name__)


@organization_bp.route('/', methods=['GET', 'POST'])
def organization_handle():
    if request.method == 'GET':
        organization_set, status_code = DbConnection().get_organizations()
        return jsonify({'response': organization_set}), status_code

    if request.method == 'POST':
        organization, status_code = DbConnection().create_organization(request.get_json())
        return jsonify({'response': organization}), status_code


@organization_bp.route('/<string:_id>', methods=['GET', 'PUT', 'DELETE'])
def organization_handle_by_id(_id: str):
    if request.method == 'GET':
        organization, status_code = DbConnection().get_organization_by_id(_id)
        return jsonify({'response': organization}), status_code

    if request.method == 'PUT':
        organization, status_code = DbConnection().update_organization(_id, request.get_json())
        return jsonify({'response': organization}), status_code

    if request.method == 'DELETE':
        response, status_code = DbConnection().delete_organization(_id)
        return jsonify({'response': response}), status_code
