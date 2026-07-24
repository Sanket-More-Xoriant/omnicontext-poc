from mcp import ClientSession


class GitHubMCPClient:

    def __init__(
        self,
        session: ClientSession
    ):
        self.session = session

    async def search_files(
        self,
        repository: str,
        extension: str
    ):

        query = (
            f"repo:{repository} "
            f"extension:{extension}"
        )

        query = (
    f"repo:{repository} "
    f"extension:{extension}"
)

        print(
            f"\nSEARCH QUERY: {query}"
        )

        return await self.session.call_tool(
            "search_code",
            {
                "query": query
            }
        )

    async def get_file(
        self,
        owner: str,
        repo: str,
        path: str
    ):

        return await self.session.call_tool(
            "get_file_contents",
            {
                "owner": owner,
                "repo": repo,
                "path": path
            }
        )

    async def list_commits(
        self,
        owner: str,
        repo: str
    ):

        return await self.session.call_tool(
            "list_commits",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def list_pull_requests(
        self,
        owner: str,
        repo: str
    ):

        return await self.session.call_tool(
            "list_pull_requests",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def list_branches(
        self,
        owner: str,
        repo: str
    ):

        return await self.session.call_tool(
            "list_branches",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def search_code(
        self,
        query: str
    ):

        return await self.session.call_tool(
            "search_code",
            {
                "query": query
            }
        )

    async def search_pull_requests(
        self,
        query: str
    ):

        return await self.session.call_tool(
            "search_pull_requests",
            {
                "query": query
            }
        )

    async def get_commit(
        self,
        owner: str,
        repo: str,
        sha: str
    ):

        return await self.session.call_tool(
            "get_commit",
            {
                "owner": owner,
                "repo": repo,
                "sha": sha
            }
        )

    async def get_latest_release(
        self,
        owner: str,
        repo: str
    ):

        return await self.session.call_tool(
            "get_latest_release",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def list_releases(
        self,
        owner: str,
        repo: str
    ):

        return await self.session.call_tool(
            "list_releases",
            {
                "owner": owner,
                "repo": repo
            }
        )

    async def get_repository_overview(
        self,
        repository: str
    ):

        result = await self.search_code(
            f"repo:{repository}"
        )

        return result