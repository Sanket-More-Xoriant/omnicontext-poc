import json


class DocumentationAnalysisAgent:

    def analyze(
        self,
        repository_cache_path="data/repository_cache.json"
    ):

        try:

            with open(
                repository_cache_path,
                "r",
                encoding="utf-8"
            ) as file:

                repository = json.load(
                    file
                )

        except Exception as e:

            print(
                f"Documentation loading failed: {e}"
            )

            return ""

        documentation = []

        documentation_keywords = [
            "readme",
            "docs",
            "documentation",
            "decision",
            "adr",
            "guide",
            "concept",
            "tutorial",
            "architecture"
        ]

        for item in repository:

            path = item.get(
                "path",
                ""
            )

            content = item.get(
                "content",
                ""
            )

            path_lower = path.lower()

            is_documentation = (
                path.endswith(".md")
                or
                any(
                    keyword in path_lower
                    for keyword in documentation_keywords
                )
            )

            if is_documentation:

                documentation.append(
                    f"""
========================
DOCUMENT
========================

PATH:
{path}

CONTENT:

{content[:3000]}
"""
                )

        print(
            f"\nDocumentation Files Loaded: "
            f"{len(documentation)}"
        )

        if not documentation:

            return ""

        documentation_context = (
            "\n".join(
                documentation
            )
        )[:15000]

        print(
            f"Documentation Context Length: "
            f"{len(documentation_context)}"
        )

        return documentation_context