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


async def main():

    mcp_connection = MCPConnection()

    async with mcp_connection.create_session() as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            github_client = GitHubMCPClient(
                session
            )

            graph_agent = GitHubGraphAgent()

            graph = await (
                graph_agent.build_mcp_repository_graph(
                    github_client,
                    "Sanket-More-Xoriant",
                    "omnicontext-poc"
                )
            )

            graph.print_graph()

            print("\nAUTHOR QUERY")
            print("-" * 50)

            result = graph_agent.find_commits_by_author(
                graph,
                "Sanket-More-Xoriant"
            )

            print(result)

            print("\nBRANCH HEAD QUERY")
            print("-" * 50)

            head_commit = (
                graph_agent.find_branch_head_commit(
                    graph,
                    "main"
                )
            )

            print(head_commit)


if __name__ == "__main__":
    asyncio.run(main())