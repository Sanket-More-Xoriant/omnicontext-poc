import json
import os


class GitHubAgent:

    SUPPORTED_EXTENSIONS = [
        "py",
        "md",
        "json",
        "yaml",
        "yml",
        "js",
        "java",
        "txt"
    ]

    def __init__(
        self,
        github_client
    ):
        self.github_client = github_client

    async def cache_repository(
        self,
        owner,
        repo
    ):

        repository = f"{owner}/{repo}"

        documents = []

        for extension in (
            self.SUPPORTED_EXTENSIONS
        ):

            print(
                f"Loading {extension} files..."
            )

            search_result = (
                await self.github_client
                .search_files(
                    repository,
                    extension
                )
            )

            print("\nRAW SEARCH RESULT:")
            print(search_result)

            raw_json = (
                search_result.content[0].text
            )

            data = json.loads(
                raw_json
            )

            items = data.get(
                "items",
                []
            )

            print(
                f"{extension} files found: "
                f"{len(items)}"
            )

            for item in items[:50]:

                try:

                    path = item["path"]

                    result = (
                        await self.github_client
                        .get_file(
                            owner,
                            repo,
                            path
                        )
                    )

                    content = ""

                    for obj in result.content:

                        if hasattr(
                            obj,
                            "resource"
                        ):

                            content = (
                                obj.resource.text
                            )

                    documents.append(
                        {
                            "file_path": path,
                            "content": content
                        }
                    )

                except Exception as ex:

                    print(
                        f"{path}: {ex}"
                    )

        cache_file = (
            f"data/cache/"
            f"{owner}_{repo}.json"
        )


        os.makedirs(
            "data/cache",
            exist_ok=True
        )

        with open(
            cache_file,
            "w",
            encoding="utf-8"
        ) as f:


            json.dump(
                documents,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\nSaved "
            f"{len(documents)} files"
        )

        return cache_file