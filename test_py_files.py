import asyncio
import os
import json

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

load_dotenv()


async def main():

    async with streamablehttp_client(
        "https://api.githubcopilot.com/mcp/",
        headers={
            "Authorization":
                f"Bearer {os.getenv('GITHUB_PAT')}"
        }
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

            response = await session.call_tool(
                "search_code",
                {
                    "query":
                    "repo:microsoft/semantic-kernel extension:py"
                }
            )

            print(response.content[0].text[:3000])


if __name__ == "__main__":
    asyncio.run(main())