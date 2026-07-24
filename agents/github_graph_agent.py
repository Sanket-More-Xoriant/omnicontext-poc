import ast
import os

from data.graph_schema import (
    GraphNode,
    GraphEdge,
    KnowledgeGraph
)


class GitHubGraphAgent:

    def build_import_graph(self):

        graph = KnowledgeGraph()

        allowed_dirs = [
            "agents",
            "connectors",
            "data",
            "llm"
        ]

        python_files = []

        # Root-level Python files

        for file in os.listdir("."):

            if file.endswith(".py"):

                python_files.append(file)

        # Project folders

        for directory in allowed_dirs:

            if os.path.exists(directory):

                for file in os.listdir(directory):

                    if file.endswith(".py"):

                        python_files.append(
                            f"{directory}/{file}"
                        )

        # Create File Nodes

        for file_path in python_files:

            graph.add_node(
                GraphNode(
                    file_path,
                    "File"
                )
            )

        # Create IMPORT relationships

        for file_path in python_files:

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    source_code = file.read()

                tree = ast.parse(
                    source_code
                )

                for node in ast.walk(tree):

                    # import xyz

                    if isinstance(
                        node,
                        ast.Import
                    ):

                        for alias in node.names:

                            graph.add_edge(
                                GraphEdge(
                                    file_path,
                                    alias.name,
                                    "IMPORTS"
                                )
                            )

                    # from xyz import abc

                    elif isinstance(
                        node,
                        ast.ImportFrom
                    ):

                        if node.module:

                            graph.add_edge(
                                GraphEdge(
                                    file_path,
                                    node.module,
                                    "IMPORTS"
                                )
                            )

            except Exception as e:

                print(
                    f"Error parsing "
                    f"{file_path}: {e}"
                )

        return graph

    def build_github_graph(self):

        graph = KnowledgeGraph()

        # Repository Node

        repo = GraphNode(
            "omnicontext-poc",
            "Repository"
        )

        graph.add_node(repo)

        # Pull Request Node

        pr = GraphNode(
            "PR-101",
            "PullRequest",
            {
                "title": "Graph Schema Design"
            }
        )

        graph.add_node(pr)

        graph.add_edge(
            GraphEdge(
                "omnicontext-poc",
                "PR-101",
                "HAS_PR"
            )
        )

        # Commit Node

        commit = GraphNode(
            "commit-abc123",
            "Commit"
        )

        graph.add_node(commit)

        graph.add_edge(
            GraphEdge(
                "PR-101",
                "commit-abc123",
                "HAS_COMMIT"
            )
        )

        return graph

    async def build_mcp_repository_graph(
        self,
        github_client,
        owner,
        repo
    ):

        graph = KnowledgeGraph()

        repo_id = repo

        # Repository Node

        graph.add_node(
            GraphNode(
                repo_id,
                "Repository"
            )
        )

        # Pull Requests

        try:

            prs = await github_client.list_pull_requests(
                owner,
                repo
            )

            pr_text = str(prs)

            lines = pr_text.split("\n")

            for line in lines:

                if "number" in line.lower():

                    try:

                        pr_number = (
                            line.split(":")[-1]
                            .strip()
                        )

                        pr_id = (
                            f"PR-{pr_number}"
                        )

                        graph.add_node(
                            GraphNode(
                                pr_id,
                                "PullRequest"
                            )
                        )

                        graph.add_edge(
                            GraphEdge(
                                repo_id,
                                pr_id,
                                "HAS_PR"
                            )
                        )

                    except Exception:

                        pass

        except Exception as e:

            print(
                f"PR Error: {e}"
            )

        # Commits

        try:

            commits = (
                await github_client.list_commits(
                    owner,
                    repo
                )
            )

            commit_text = str(
                commits
            )

            lines = (
                commit_text.split("\n")
            )

            commit_count = 0

            for line in lines:

                if "sha" in line.lower():

                    try:

                        sha = (
                            line.split(":")[-1]
                            .strip()
                        )

                        commit_id = sha[:7]

                        graph.add_node(
                            GraphNode(
                                commit_id,
                                "Commit"
                            )
                        )

                        graph.add_edge(
                            GraphEdge(
                                repo_id,
                                commit_id,
                                "HAS_COMMIT"
                            )
                        )

                        commit_count += 1

                        if commit_count > 20:

                            break

                    except Exception:

                        pass

        except Exception as e:

            print(
                f"Commit Error: {e}"
            )

        return graph