import ast
import os
import json

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
    def find_commits_by_author(
        self,
        graph,
        author
    ):

        commits = []

        for edge in graph.edges:

            if (
                edge.source == author
                and edge.relationship == "AUTHORED"
            ):

                commits.append(
                    edge.target
                )

        return commits

    def find_branch_head_commit(
        self,
        graph,
        branch_name
    ):

        for edge in graph.edges:

            if (
                edge.source == branch_name
                and edge.relationship == "HEAD_COMMIT"
            ):

                return edge.target

        return None


    def get_latest_commit(
            self,
            graph
        ):

            for edge in graph.edges:

                if edge.relationship == "HEAD_COMMIT":

                    return edge.target

            return None


    def get_commit_author(
            self,
            graph,
            commit_id
        ):

            for edge in graph.edges:

                if (
                    edge.target == commit_id
                    and edge.relationship == "AUTHORED"
                ):

                    return edge.source

            return None



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

            print("\nPR RAW RESPONSE:")
            print(prs)
            print(type(prs))

            if prs.content:

                json_text = prs.content[0].text

                pr_data = json.loads(
                    json_text
                )

                for pr in pr_data:

                    pr_id = (
                        f"PR-{pr['number']}"
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

        except Exception as e:

            print(
                f"PR Error: {e}"
            )

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
                            "PullRequest",
                            {
                                "title": line
                            }
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

            commits = await github_client.list_commits(
                owner,
                repo
            )

            if commits.content:

                json_text = commits.content[0].text

                commit_data = json.loads(
                    json_text
                )

                for commit in commit_data:

                    sha = commit.get(
                        "sha",
                        ""
                    )

                    author = (
                        commit.get("author") or {}
                    ).get(
                        "login",
                        "Unknown"
                    )

                    graph.add_node(
                        GraphNode(
                            author,
                            "Contributor"
                        )
                    )

                    if not sha:
                        continue

                    commit_id = sha[:7]

                    graph.add_node(
                        GraphNode(
                            commit_id,
                            "Commit",
                            {
                                "message":
                                commit["commit"]["message"]
                            }
                        )
                    )

                    graph.add_edge(
                        GraphEdge(
                            repo_id,
                            commit_id,
                            "HAS_COMMIT"
                        )
                    )

                    graph.add_edge(
                        GraphEdge(
                            author,
                            commit_id,
                            "AUTHORED"
                        )
                    )

        except Exception as e:

            print(
                f"Commit Error: {e}"
            )

        # Branches
        try:

            branches = await github_client.list_branches(
                owner,
                repo
            )

            if branches.content:

                json_text = branches.content[0].text

                branch_data = json.loads(
                    json_text
                )

            for branch in branch_data:

                branch_name = branch["name"]

                branch_sha = branch["sha"][:7]

                graph.add_node(
                    GraphNode(
                        branch_name,
                        "Branch"
                    )
                )

                graph.add_edge(
                    GraphEdge(
                        repo_id,
                        branch_name,
                        "HAS_BRANCH"
                    )
                )

                graph.add_edge(
                    GraphEdge(
                        branch_name,
                        branch_sha,
                        "HEAD_COMMIT"
                    )
                )

        except Exception as e:

            print(
                f"Branch Error: {e}"
            )


        return graph