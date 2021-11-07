from typing import List

from flask import current_app as app

from .utils import read_csv_file, remove_extra_keys
from .models import Person, Organization, Membership
from .db_connection.neo4j_connection import Neo4jConnection
from .db_connection.elastic_connection import ElasticConnection


@app.route('/', methods=['GET'])
def root():
    return 'Root'


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello world!'


@app.route('/clear/neo', methods=['GET'])
def clear_neo():
    conn = Neo4jConnection()
    conn.clear_database()
    return 'Success'


@app.route('/build', methods=['GET'])
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
