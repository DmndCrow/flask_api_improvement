from flask import current_app as app

from .utils import read_csv_file, remove_extra_keys
from .models import Person, Organization, Relationship
from .db_connection.neo4j_connection import Neo4jConnection


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
    people = []
    organizations = []
    memberships = {}

    for d in data:
        person_mapper = remove_extra_keys(d, Person)
        people.append(Person(**person_mapper))

        organization_mapper = remove_extra_keys(d, Organization)
        organizations.append(Organization(**organization_mapper))

        memberships[d['id']] = d['group_id']

    conn = Neo4jConnection()
    conn.build(people, organizations, memberships)
    conn.close()
    return 'test'
