import asyncio
import os

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

MCP_URL = "https://api.githubcopilot.com/mcp/"


async def main():

    token = os.getenv("GITHUB_PAT")

    if not token:
        raise ValueError(
            "GITHUB_PAT not found"
        )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    print("Connecting to GitHub MCP Server...")

    async with streamablehttp_client(
        MCP_URL,
        headers=headers
    ) as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            print("Initializing session...")

            await session.initialize()

            print("Connected Successfully ✅")

            tools = await session.list_tools()

            print("\nAVAILABLE TOOLS:\n")

            for tool in tools.tools:
                print(f"✅ {tool.name}")


if __name__ == "__main__":
    asyncio.run(main())