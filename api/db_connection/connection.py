import uuid
from typing import Tuple, List, Dict

from api.db_connection.elastic_connection import ElasticConnection
from api.db_connection.neo4j_connection import Neo4jConnection
from api.models import Organization, Person
from api.utils import remove_extra_keys


class DbConnection:
    def __init__(self):
        self.elastic = ElasticConnection()
        self.neo = Neo4jConnection()

    def get_organizations(self) -> Tuple[List[Dict], int]:
        organization_set_response = []

        organization_set, status_code = self.elastic.get_object_by_id('organization')
        for organization in organization_set:
            organization_set_response.append(organization)

        return organization_set_response, status_code

    def get_organization_by_id(self, organization_id: str) -> Tuple[Dict, int]:
        organization, status_code = self.elastic.get_object_by_id('organization', organization_id)
        return organization[0] if len(organization) else None, status_code

    def create_organization(self, form: Dict) -> Tuple[Dict, int]:
        organization_body: Organization = remove_extra_keys(form, Organization)
        organization_body.group_id = str(uuid.uuid4())

        organization, status_code = self.elastic.create_object(
            'organization', organization_body, organization_body.group_id
        )

        return organization[0] if len(organization) else None, status_code

    def get_people(self) -> Tuple[List[Dict], int]:
        person_set_response = []

        person_set, status_code = self.elastic.get_object_by_id('person')
        for person in person_set:
            person_set_response.append(person)

        return person_set_response, status_code

    def get_person_by_id(self, person_id: str) -> Tuple[Dict, int]:
        person, status_code = self.elastic.get_object_by_id('person', person_id)
        return person[0] if len(person) else None, status_code

    def create_person(self, form: Dict) -> Tuple[Dict, int]:
        person_body: Person = remove_extra_keys(form, Person)
        person_body.id = str(uuid.uuid4())

        person, status_code = self.elastic.create_object(
            'person', person_body, person_body.id
        )

        return person[0] if len(person) else None, status_code

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.elastic.close()
        self.neo.close()
