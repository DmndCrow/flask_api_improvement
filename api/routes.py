from flask import current_app as app

from .utils import read_csv_file, remove_extra_keys
from .models import Person, Organization, Relationship
from . import db

@app.route('/', methods=['GET'])
def root():
    return 'Root'


@app.route('/hello', methods=['GET'])
def hello_world():
    return 'Hello world!'


@app.route('/build', methods=['GET'])
def build():
    data = read_csv_file()

    for d in data:
        person_mapper = remove_extra_keys(d, Person)
        person = Person(**person_mapper)

        organization_mapper = remove_extra_keys(d, Organization)
        organization = Organization(**organization_mapper)
        
        relationship_mapper = {'id': d['id'], 'group_id': d['group_id']}
        relationship = Relationship(**relationship_mapper)

        db.session.add(person)
        db.session.add(organization)
        db.session.add(relationship)

        db.session.commit()
    
    return 'Commited'
