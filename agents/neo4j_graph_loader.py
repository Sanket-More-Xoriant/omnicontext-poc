from connectors.neo4j_connector import (
    Neo4jConnector
)


class Neo4jGraphLoader:

    def __init__(self):

        self.neo4j = Neo4jConnector()

    def load_graph(
        self,
        graph
    ):

        with self.neo4j.driver.session() as session:

            for node in graph.nodes.values():

                session.run(
                    """
                    MERGE (n:Entity {id:$id})
                    SET n.type = $type
                    """,
                    id=node.id,
                    type=node.type
                )

            for edge in graph.edges:

                query = f"""
                MATCH (a:Entity {{id:$source}})
                MATCH (b:Entity {{id:$target}})
                MERGE (a)-[:{edge.relationship}]->(b)
                """

                session.run(
                    query,
                    source=edge.source,
                    target=edge.target
                )