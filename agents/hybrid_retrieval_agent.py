class HybridRetrievalAgent:

    def retrieve(
        self,
        semantic_results,
        bm25_results,
        top_k=15
    ):

        fused = {}

        for result in (
            semantic_results +
            bm25_results
        ):

            chunk = result["chunk"]

            content = chunk.get(
                "content",
                ""
            )

            score = result["score"]

            if chunk.get("is_code"):
                score *= 1.25

            if content not in fused:

                fused[content] = {
                    "chunk": chunk,
                    "score": 0
                }

            fused[content]["score"] += score

        ranked = sorted(
            fused.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        return [
            item["chunk"]
            for item in ranked[:top_k]
        ]

    def build_context(
        self,
        technical_chunks,
        repository_context="",
        architecture_context="",
        documentation_context="",
        specification_context="",
        commit_context="",
        pr_context=""
    ):

        # =====================
        # TECHNICAL CONTEXT
        # =====================

        technical_context = "\n\n".join(
            [
                chunk.get(
                    "content",
                    ""
                )
                for chunk in technical_chunks
            ]
        )

        # =====================
        # BUILD OMNI CONTEXT
        # =====================

        context = f"""
========================
REPOSITORY CONTEXT
========================

{repository_context}

========================
ARCHITECTURE CONTEXT
========================

{architecture_context}

========================
SPECIFICATION CONTEXT
========================

{specification_context}

========================
DOCUMENTATION CONTEXT
========================

{documentation_context}

========================
COMMIT CONTEXT
========================

{commit_context}

========================
PULL REQUEST CONTEXT
========================

{pr_context}

========================
TECHNICAL CONTEXT
========================

{technical_context}
"""

        return context

    def get_context_statistics(
        self,
        technical_chunks=None,
        repository_context="",
        architecture_context="",
        documentation_context="",
        specification_context="",
        commit_context="",
        pr_context=""
    ):

        if technical_chunks is None:

            technical_chunks = []

        return {
            "repository_context":
                len(repository_context),

            "architecture_context":
                len(architecture_context),

            "documentation_context":
                len(documentation_context),

            "specification_context":
                len(specification_context),

            "commit_context":
                len(commit_context),

            "pr_context":
                len(pr_context),

            "retrieved_chunks":
                len(technical_chunks)
        }
