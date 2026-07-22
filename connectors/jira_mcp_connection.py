# connectors/jira_mcp_connection.py

import os

from dotenv import load_dotenv

from mcp.client.streamable_http import (
    streamablehttp_client
)

load_dotenv()


class JiraMCPConnection:

    MCP_URL = "https://mcp.atlassian.com/v1/mcp"

    def __init__(self):

        token = os.getenv(
            "JIRA_API_TOKEN"
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