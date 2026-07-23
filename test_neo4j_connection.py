from connectors.neo4j_connector import (
    Neo4jConnector
)

neo4j_conn = Neo4jConnector()

with neo4j_conn.driver.session() as session:

    result = session.run(
        "RETURN 'Neo4j Connected' AS message"
    )

    print(
        result.single()["message"]
    )

neo4j_conn.close()