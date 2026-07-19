class PRAnalysisAgent:

    def analyze(
        self,
        prs,
        gemini
    ):

        prompt = f"""
Analyze these Pull Requests.

Provide:

1. Major Themes

2. New Features

3. Bug Fixes

4. Architectural Changes

5. Active Engineering Areas

PRs:

{prs}
"""

        return gemini.generate(
            prompt
        )