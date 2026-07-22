import asyncio

from mcp import ClientSession
from connectors.jira_mcp_connection import JiraMCPConnection


async def main():

    connection = JiraMCPConnection()

    async with await connection.create_session() as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                "getTeamworkGraphContext",
                {
                    "cloudId": "https://xoriant-coe-ai-for-engineering.atlassian.net",
                    "objectType": "JiraSpace",
                    "objectIdentifier": "KAN",
                    "detailLevel": "full"
                }
            )

            print(result)


asyncio.run(main())