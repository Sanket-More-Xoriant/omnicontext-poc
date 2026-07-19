import asyncio
import os

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()

MCP_URL = "https://api.githubcopilot.com/mcp/"


async def main():

    headers = {
        "Authorization":
            f"Bearer {os.getenv('GITHUB_PAT')}"
    }

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

            await session.initialize()

            result = await session.call_tool(
                "get_file_contents",
                {
                    "owner": "microsoft",
                    "repo": "semantic-kernel",
                    "path": "README.md"
                }
            )

            print(result)


if __name__ == "__main__":
    asyncio.run(main())