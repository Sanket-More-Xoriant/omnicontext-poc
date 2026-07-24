import json


class RepositoryAnalysisAgent:

    def analyze(
        self,
        gemini,
        cache_file
    ):

        with open(
            cache_file,
            "r",
            encoding="utf-8"
        ) as file:

            docs = json.load(file)

        repository_content = ""

        for doc in docs[:30]:

            repository_content += (
                f"\nFILE: "
                f"{doc['file_path']}\n"
            )

            repository_content += (
                doc["content"][:1500]
            )

            repository_content += "\n"

        prompt = f"""
Analyze the repository.

Return:

1. Project Purpose

2. Major Modules

3. Main Packages

4. Languages

5. Frameworks

6. Architecture

7. Important Files

Repository Content:

{repository_content}
"""

        return gemini.generate(
            prompt
        )