import asyncio
import os

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.streamable_http import (
    streamablehttp_client
)

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

            result = await session.call_tool(
                "search_code",
                {
                    "query":
                        "repo:microsoft/semantic-kernel README"
                }
            )

            print(result)


if __name__ == "__main__":
    asyncio.run(main())