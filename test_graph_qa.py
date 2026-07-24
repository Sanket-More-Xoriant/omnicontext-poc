import asyncio

from agents.github_graph_agent import (
    GitHubGraphAgent
)

from agents.graph_retrieval_agent import (
    GraphRetrievalAgent
)

from connectors.mcp_connection import (
    MCPConnection
)

from connectors.github_mcp_client import (
    GitHubMCPClient
)

from mcp import ClientSession


async def main():

    graph_agent = GitHubGraphAgent()

    retrieval_agent = (
        GraphRetrievalAgent()
    )

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

            question = (
                "Who made the latest changes?"
            )

            print("\nQUESTION")
            print("-" * 50)
            print(question)

            result = (
                retrieval_agent.answer_question(
                    question,
                    graph,
                    graph_agent
                )
            )

            print("\nANSWER")
            print("-" * 50)
            print(result)


if __name__ == "__main__":
    asyncio.run(main())