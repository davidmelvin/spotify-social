from neo4j import GraphDatabase
import requests
from urllib.error import HTTPError

from credentials import api_access_token
from utils.requests import get_data_from_url


def get_followed_accounts_of_user(user_id: str):
    url = "https://spclient.wg.spotify.com/user-profile-view/v3/profile/{params[user_id]}/following?market=from_token"

    params = {"user_id": user_id}

    print(f"getting followed accounts of {user_id}")

    return get_data_from_url(url, params)


def test():
    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

    def create_person(tx, name):
        tx.run("CREATE (a:Person {name: $name})", name=name)

    def create_friend_of(tx, name, friend):
        tx.run("MATCH (a:Person) WHERE a.name = $name "
               "CREATE (a)-[:KNOWS]->(:Person {name: $friend})",
               name=name, friend=friend)

    with driver.session() as session:
        session.write_transaction(create_person, "Alice")
        session.write_transaction(create_friend_of, "Alice", "Bob")
        session.write_transaction(create_friend_of, "Alice", "Carl")

    driver.close()
