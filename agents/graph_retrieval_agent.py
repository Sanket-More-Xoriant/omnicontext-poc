class GraphRetrievalAgent:

    def get_latest_author(
        self,
        graph,
        graph_agent
    ):

        latest_commit = (
            graph_agent.get_latest_commit(
                graph
            )
        )

        if not latest_commit:
            return None

        author = (
            graph_agent.get_commit_author(
                graph,
                latest_commit
            )
        )

        return {
            "author": author,
            "commit": latest_commit
        }
    def answer_question(
        self,
        query,
        graph,
        graph_agent
    ):

        query = query.lower()

        if (
            "latest" in query
            and "change" in query
        ):

            return self.get_latest_author(
                graph,
                graph_agent
            )

        return {
            "message":
            "No graph answer found"
        }