from mcp import ClientSession


class JiraMCPClient:

    def __init__(
        self,
        session: ClientSession
    ):
        self.session = session

    async def list_tools(self):
        return await self.session.list_tools()

    async def call_tool(
        self,
        tool_name: str,
        arguments: dict
    ):
        return await self.session.call_tool(
            tool_name,
            arguments
        )