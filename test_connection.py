import asyncio

from mcp import ClientSession

from connectors.mcp_connection import (
    MCPConnection
)


async def main():

    connection = MCPConnection()

    async with connection.create_session() as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            tools = await session.list_tools()

            for tool in tools.tools:
                print(tool.name)


asyncio.run(main())