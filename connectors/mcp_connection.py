# connectors/mcp_connection.py

import os

from dotenv import load_dotenv

from mcp import ClientSession
from mcp.client.streamable_http import (
    streamablehttp_client
)

load_dotenv()


class MCPConnection:

    MCP_URL = (
        "https://api.githubcopilot.com/mcp/"
    )

    def __init__(self):

        token = os.getenv(
            "GITHUB_PAT"
        )

        self.headers = {
            "Authorization":
                f"Bearer {token}"
        }

    async def create_session(self):

        return streamablehttp_client(
            self.MCP_URL,
            headers=self.headers
        )