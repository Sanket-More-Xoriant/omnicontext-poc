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

            print("\nInitializing MCP Session...\n")

            await session.initialize()

            print("Connected Successfully\n")

            tools = await session.list_tools()

            print("=" * 100)
            print("AVAILABLE MCP TOOLS")
            print("=" * 100)

            for tool in tools.tools:

                print("\n" + "=" * 100)
                print(f"NAME: {tool.name}")
                print("=" * 100)

                try:
                    print("\nDESCRIPTION:")
                    print(tool.description)
                except Exception:
                    print("\nDESCRIPTION: N/A")

                try:
                    print("\nINPUT SCHEMA:")
                    print(tool.inputSchema)
                except Exception:
                    print("\nINPUT SCHEMA: N/A")

                try:
                    print("\nRAW TOOL OBJECT:")
                    print(tool)
                except Exception:
                    pass

            print("\n")
            print("=" * 100)
            print(f"TOTAL TOOLS FOUND: {len(tools.tools)}")
            print("=" * 100)


if __name__ == "__main__":
    asyncio.run(main())