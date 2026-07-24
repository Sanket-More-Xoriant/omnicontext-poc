from neo4j import GraphDatabase


class Neo4jConnector:

    def __init__(self):

        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687",
            auth=(
                "neo4j",
                "India@#1998"
            )
        )

    def close(self):

        self.driver.close()