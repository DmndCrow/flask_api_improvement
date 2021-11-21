from typing import List, Union

from elasticsearch import Elasticsearch, helpers

from api.models import Person, Organization


class ElasticConnection:
    def __init__(self):
        host = 'localhost:9200'
        user = 'elastic'
        password = 'pSmCN8m95wNcxk2P'

        self.es = Elasticsearch([host], http_auth=(user, password))
        self.doc = '_doc'

    def get_object_by_id(self, index: str, _id: str = None):
        """
        Get person from db by person id, if not provided get all people
        @param index: person or org
        @type index: str
        @param _id: person id or organization id
        @type _id: str
        @return: list of people
        @rtype: List[Dict[str, str]]
        """
        if _id:
            try:
                res = self.es.get(index=index, doc_type=self.doc, id=_id)
                return [res['_source']], 200
            except:
                return [], 404
        else:
            query = {
                'query': {
                    'match_all': {}
                }
            }
        es_response = helpers.scan(
            self.es,
            index=index,
            doc_type=self.doc,
            query=query
        )
        return [record['_source'] for record in es_response], 200

    def build(self, people: List[Person], organizations: List[Organization]):
        for person in people:
            self.create_object('person', person, person.id)

        for organization in organizations:
            self.create_object('organization', organization, organization.group_id)

    def create_object(self, index: str, model: Union[Person, Organization], _id: str):
        """
        Create new person
        @param index: model index in elasticsearch
        @type index: str
        @param model: to be created Person or Organization
        @type model: Person or Organization
        @param _id: id of to be created Person or Organization
        @type _id: str
        @return: created person or organization
        @rtype: Person or Organization
        """
        res, code = self.get_object_by_id(index, _id)
        if code == 404:
            body = model.__dict__
            del body['_sa_instance_state']

            es_response = self.es.index(
                index=index,
                doc_type=self.doc,
                id=_id,
                body=body
            )
            return self.get_object_by_id(index, _id)
        return None, 403

    def close(self):
        self.es.transport.close()
