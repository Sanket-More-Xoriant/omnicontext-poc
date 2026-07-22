import re


class QuestionRouter:

    REPO_OVERVIEW_WORDS = [
        "architecture",
        "overview",
        "modules",
        "repository",
        "framework",
        "languages",
        "structure",
        "components",
        "design",
        "high level"
    ]

    COMMIT_WORDS = [
        "commit",
        "commits",
        "development trends"
    ]

    PR_WORDS = [
        "pull request",
        "pull requests"
    ]

    @staticmethod
    def is_overview_question(
        question
    ):

        question = question.lower()

        return any(
            word in question
            for word in (
                QuestionRouter
                .REPO_OVERVIEW_WORDS
            )
        )

    @staticmethod
    def is_commit_question(
        question
    ):

        question = question.lower()

        return (
            re.search(
                r"\bcommit\b",
                question
            ) is not None
            or
            re.search(
                r"\bcommits\b",
                question
            ) is not None
            or
            "development trends" in question
        )

    @staticmethod
    def is_pr_question(
        question
    ):

        question = question.lower()

        return (
            re.search(
                r"\bpr\b",
                question
            ) is not None
            or
            "pull request" in question
            or
            "pull requests" in question
        )