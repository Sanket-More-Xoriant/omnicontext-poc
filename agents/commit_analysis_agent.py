class CommitAnalysisAgent:

    def analyze(
        self,
        commits,
        gemini
    ):

        prompt = f"""
Analyze these commits.

Provide:

1. Recent Development Focus

2. Bug Fixes

3. New Features

4. Architectural Changes

5. Future Direction

Commits:

{commits}
"""

        return gemini.generate(
            prompt
        )