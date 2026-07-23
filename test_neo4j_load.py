import asyncio

from mcp import ClientSession

from connectors.mcp_connection import (
    MCPConnection
)

from connectors.github_mcp_client import (
    GitHubMCPClient
)

from agents.github_graph_agent import (
    GitHubGraphAgent
)

from agents.neo4j_graph_loader import (
    Neo4jGraphLoader
)


async def main():

    graph_agent = GitHubGraphAgent()

    connection = MCPConnection()

    async with (
        connection.create_session()
        as (
            read_stream,
            write_stream,
            _
        )
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            github_client = (
                GitHubMCPClient(
                    session
                )
            )

            graph = (
                await graph_agent
                .build_mcp_repository_graph(
                    github_client,
                    "Sanket-More-Xoriant",
                    "omnicontext-poc"
                )
            )

            print("\nGRAPH CREATED")
            print("-" * 50)

            graph.print_graph()

            loader = Neo4jGraphLoader()

            loader.load_graph(graph)

            print(
                "\nGraph loaded into Neo4j successfully!"
            )


if __name__ == "__main__":
    asyncio.run(main())
