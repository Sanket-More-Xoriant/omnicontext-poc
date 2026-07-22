class HybridRetrievalAgent:

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
