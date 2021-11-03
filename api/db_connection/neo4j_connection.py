from typing import List, Dict

from neo4j import GraphDatabase
from dotenv import load_dotenv

from api.models import Person, Organization
from flask_config import DbConfig

load_dotenv()


class Neo4jConnection:
    def __init__(self):
        url = DbConfig.NEO4J_URL
        user = DbConfig.NEO4J_USERNAME
        password = DbConfig.NEO4J_PASSWORD

        self.driver = GraphDatabase.driver(url, auth=(user, password))
        self.session = self.driver.session()

    def create_person(self, person_id: str) -> None:
        """
        Create Person from @param person_id
        @param person_id: id of a person in elasticsearch db
        @type person_id: str
        """
        self.session.write_transaction(self._create_person, person_id)

    def create_organization(self, organization_id: str) -> None:
        """
        Create Organization from @param organization_id
        @param organization_id: id of an organization in elasticsearch db
        @type organization_id: str
        """
        self.session.write_transaction(self._create_organization, organization_id)

    def create_membership(self, person_id: str, group_id: str):
        """
        Create relation between person using person_id and organization using group_id
        @param person_id: id of the person
        @type person_id: str
        @param group_id: id of the organization
        @type group_id: str
        """
        if self.session.read_transaction(self._get_person_organization, person_id):
            return 'Person is already MEMBER_OF another org', 409
        return self.session.write_transaction(self._create_membership, person_id, group_id)

    def delete_membership(self, person_id: str):
        """
        Delete relation between person using _id and parent of person
        @param person_id: id of the person
        @type person_id: str
        @return: response to the request and status code
        @rtype: Tuple[str, int]
        """
        return self.session.write_transaction(self._delete_membership, person_id)

    def get_person_organization(self, _id: str) -> List[any]:
        """
        Get organization that person is MEMBER_OF using _id
        @param _id: person.id
        @type _id: str
        @return: list that contains organization
        @rtype: List[any]
        """
        return self.session.read_transaction(self._get_person_organization, _id)

    # def get_organization_person(self, _group_id) -> List[any]:
    #     """
    #     Get all person that are MEMBER_OF organization
    #     @param _group_id: organization.group_id
    #     @type _group_id: str
    #     @return: list that contains person of organization
    #     @rtype: List[any]
    #     """
    #     return self.session.read_transaction(self._get_organization_person, _group_id)

    def delete_person(self, _id: str) -> None:
        """
        Delete person using _id
        @param _id: person.id
        @type _id: str
        @return: no need to return anything
        @rtype: None
        """
        self.session.write_transaction(self._delete_person, _id)

    def delete_organization(self, _group_id: str) -> None:
        """
        Delete organization using _group_id
        @param _group_id: organization.group_id
        @type _group_id: str
        @return: no need to return anything
        @rtype: None
        """
        self.session.write_transaction(self._delete_organization, _group_id)

    def build(self, people: List[Person], organizations: List[Organization], memberships: Dict[str, str]) -> None:
        # self.session.write_transaction(
        #     self._create_multiple_people, [person.id for person in people]
        # )
        # self.session.write_transaction(
        #     self._create_multiple_organizations, [org.group_id for org in organizations]
        # )
        self.session.write_transaction(self._create_multiple_memberships, memberships)

    @staticmethod
    def _create_person(tx, person_id: str) -> None:
        tx.run('CREATE (p: Person {id: $id})', id=person_id)

    @staticmethod
    def _create_organization(tx, group_id: str) -> None:
        tx.run('CREATE (o: Organization {group_id: $group_id})', group_id=group_id)

    @staticmethod
    def _create_membership(tx, person_id: str, group_id: str) -> None:
        tx.run(
            'MATCH (p: Person {id: $id}), (o: Organization {group_id: $group_id}) '
            'CREATE (p) - [:MEMBER_OF] -> (o)', id=person_id, group_id=group_id
        )

    @staticmethod
    def _delete_membership(tx, person_id: str):
        tx.run(
            'MATCH (:Person {id: $id}) - [m:MEMBER_OF] -> (:Organization) DETACH delete m',
            id=person_id
        )

    @staticmethod
    def _delete_person(tx, person_id: str) -> None:
        tx.run('MATCH (p: Person {id: $id}) DETACH DELETE p', id=person_id)

    @staticmethod
    def _delete_organization(tx, group_id: str) -> None:
        tx.run(
            'MATCH (p: Organization {group_id: $group_id}) DETACH DELETE p',
            group_id=group_id
        )

    @staticmethod
    def _create_multiple_people(tx, people: List[str]) -> None:
        for person_id in people:
            tx.run('CREATE (p: Person {id: $id}) RETURN p', id=person_id)
            print('neo4j create', person_id)

    @staticmethod
    def _create_multiple_organizations(tx, organizations: List[str]) -> None:
        for group_id in organizations:
            tx.run('CREATE (o: Organization {group_id: $group_id})', group_id=group_id)
            print('neo4j create', group_id)

    @staticmethod
    def _create_multiple_memberships(tx, memberships: Dict[str, str]) -> None:
        for key in memberships:
            group_id = memberships[key]
            tx.run(
                'MERGE (p: Person {id: $id})'
                'MERGE (o: Organization {group_id: $group_id})'
                'MERGE (p)-[Memberships:MEMBER_OF]->(o)',
                id=key, group_id=group_id
            )

    @staticmethod
    def _get_person_organization(tx, person_id: str) -> List[any]:
        res = tx.run(
            'MATCH (p: Person {id: $id}) - [:MEMBER_OF] -> (o: Organization) return o',
            id=person_id
        )
        res = [record for record in res.data()]
        print(res)
        return []
        # return [
        #     Organization(db_dict=record['o']).__dict__ for record in res if 'o' in record
        # ]

    # @staticmethod
    # def _get_organization_person(tx, _group_id: str) -> List[any]:
    #     res = tx.run(
    #         'MATCH (p: Person) - [:MEMBER_OF] -> (o: Organization {group_id: $group_id}) return p',
    #         group_id=_group_id
    #     )
    #     res = [record for record in res.data()]
    #     return [
    #         Person(db_dict=record['p']).__dict__ for record in res if 'p' in record
    #     ]

    @staticmethod
    def _clear_database(tx):
        # remove relationships
        tx.run('match (a) -[r] -> () delete a, r')

        # delete nodes
        tx.run('match (a) delete a')

    def clear_database(self):
        self.session.write_transaction(self._clear_database)

    def close(self):
        self.driver.close()
