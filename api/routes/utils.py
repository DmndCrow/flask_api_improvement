from typing import List

from flask import Blueprint, redirect, url_for

from api.models import Person, Organization, Membership
from api.db_connection.neo4j_connection import Neo4jConnection
from api.db_connection.elastic_connection import ElasticConnection
from api.utils import read_csv_file, remove_extra_keys

utils_bp = Blueprint('utils_bp', __name__)


@utils_bp.route('/', methods=['GET'])
def root():
    return redirect(url_for('swagger'))


@utils_bp.route('/api/swagger', methods=['GET'])
def swagger():
    return 'swagger ui'


@utils_bp.route('/clear/neo', methods=['GET'])
def clear_neo():
    conn = Neo4jConnection()
    conn.clear_database()
    return 'Success'


@utils_bp.route('/api/build', methods=['GET'])
def build():
    data = read_csv_file()
    people: List[Person] = []
    organizations: List[Organization] = []
    memberships: List[Membership] = []

    for row in data:
        people.append(remove_extra_keys(row, Person))
        organizations.append(remove_extra_keys(row, Organization))
        memberships.append(remove_extra_keys(row, Membership))

    conn = Neo4jConnection()
    conn.build(people, organizations, memberships)
    conn.close()

    es_conn = ElasticConnection()
    es_conn.build(people, organizations)
    es_conn.close()

    return 'test'
