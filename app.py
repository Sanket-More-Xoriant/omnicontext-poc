import asyncio
import os

from dotenv import load_dotenv
from agents.bm25_agent import BM25Agent

from mcp import ClientSession
from mcp.client.streamable_http import (
    streamablehttp_client
)

from connectors.github_mcp_client import (
    GitHubMCPClient
)

from agents.chunking_agent import (
    ChunkingAgent
)

from agents.embedding_agent import (
    EmbeddingAgent
)

from agents.retrieval_agent import (
    RetrievalAgent
)

from agents.question_router import (
    QuestionRouter
)

from agents.repository_analysis_agent import (
    RepositoryAnalysisAgent
)

from agents.commit_analysis_agent import (
    CommitAnalysisAgent
)

from agents.pr_analysis_agent import (
    PRAnalysisAgent
)

from llm.gemini_client import (
    GeminiClient
)

from agents.hybrid_retrieval_agent import (
    HybridRetrievalAgent
)

from agents.architecture_analysis_agent import (
    ArchitectureAnalysisAgent
)

from agents.documentation_analysis_agent import (
    DocumentationAnalysisAgent
)

from agents.specification_analysis_agent import (
    SpecificationAnalysisAgent
)


load_dotenv()


MCP_URL = "https://api.githubcopilot.com/mcp/"


async def main():

    print("\nStarting Retrosync...\n")

    repository = os.getenv(
        "GITHUB_REPOSITORY"
    )

    owner, repo = repository.split("/")

    token = os.getenv(
        "GITHUB_PAT"
    )

    print(
        f"Repository: {repository}"
    )

    print(
        "\nConnecting to GitHub MCP..."
    )

    async with streamablehttp_client(
        MCP_URL,
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    ) as (
        read_stream,
        write_stream,
        _
    ):

        async with ClientSession(
            read_stream,
            write_stream
        ) as session:

            await session.initialize()

            print(
                "GitHub MCP Connected ✅"
            )

            github_client = (
                GitHubMCPClient(
                    session
                )
            )

            print(
                "\nLoading Chunks..."
            )

            chunks = (
                ChunkingAgent()
                .create_chunks()
            )

            print(
                f"Chunks Loaded: "
                f"{len(chunks)}"
            )
            
            print(
    "\nBuilding BM25 Index..."
            )

            bm25_agent = BM25Agent(
                chunks
            )

            print(
                "BM25 Ready ✅"
            )

            print(
                "\nCreating Embeddings..."
            )

            embedding_agent = (
                EmbeddingAgent()
            )

            vectors, vectorizer = (
                embedding_agent
                .create_embeddings(
                    chunks
                )
            )

            print(
                "\nTF-IDF Ready ✅"
            )

            retrieval_agent = (
                RetrievalAgent()
            )
            
            hybrid_agent = (
                HybridRetrievalAgent()
            )

            gemini = GeminiClient()

            print(
                "\nRepository Intelligence Platform Ready ✅"
            )

            while True:

                question = input(
                    "\nAsk Question (exit to quit): "
                )

                if (
                    question.lower()
                    == "exit"
                ):

                    print(
                        "\nGoodbye!"
                    )

                    break

                try:

                    # =====================
                    # REPOSITORY OVERVIEW
                    # =====================

                    if (
                        QuestionRouter
                        .is_overview_question(
                            question
                        )
                        and
                        "architecture" not in question.lower()
                        and
                        "integration" not in question.lower()
                    ):

                        print(
                            "\nGenerating Repository Overview..."
                        )

                        answer = (
                            RepositoryAnalysisAgent()
                            .analyze(
                                gemini
                            )
                        )

                        print(
                            "\nANSWER\n"
                        )

                        print(
                            answer
                        )

                        continue

                    # =====================
                    # COMMIT ANALYSIS
                    # =====================

                    if (
                        QuestionRouter
                        .is_commit_question(
                            question
                        )
                    ):

                        print(
                            "\nAnalyzing Commits..."
                        )

                        commits = (
                            await github_client
                            .list_commits(
                                owner,
                                repo
                            )
                        )

                        answer = (
                            CommitAnalysisAgent()
                            .analyze(
                                str(commits),
                                gemini
                            )
                        )

                        print(
                            "\nCOMMIT ANALYSIS\n"
                        )

                        print(
                            answer
                        )

                        continue

                    # =====================
                    # PR ANALYSIS
                    # =====================

                    if (
                        QuestionRouter
                        .is_pr_question(
                            question
                        )
                    ):

                        print(
                            "\nAnalyzing Pull Requests..."
                        )

                        prs = (
                            await github_client
                            .list_pull_requests(
                                owner,
                                repo
                            )
                        )

                        answer = (
                            PRAnalysisAgent()
                            .analyze(
                                str(prs),
                                gemini
                            )
                        )

                        print(
                            "\nPR ANALYSIS\n"
                        )

                        print(
                            answer
                        )

                        continue

                    # =====================
                    # HYBRID RAG FLOW
                    # =====================

                    try:

                        tfidf_chunks = (
                            retrieval_agent
                            .tfidf_search(
                                question,
                                vectorizer,
                                vectors,
                                chunks,
                                top_k=10
                            )
                        )

                    except Exception as ex:

                        print(
                            f"\nTF-IDF Retrieval Error: {ex}"
                        )

                        tfidf_chunks = []


                    bm25_chunks = (
                        bm25_agent
                        .search(
                            question,
                            top_k=10
                        )
                    )

                    combined_chunks = []

                    seen = set()

                    for chunk in (
                        tfidf_chunks +
                        bm25_chunks
                    ):

                        content = chunk.get(
                            "content",
                            ""
                        )

                        if content not in seen:

                            combined_chunks.append(
                                chunk
                            )

                            seen.add(
                                content
                            )

                    print(
                        f"\nBM25 Chunks: "
                        f"{len(bm25_chunks)}"
                    )

                    print(
                        f"TF-IDF Chunks: "
                        f"{len(tfidf_chunks)}"
                    )

                    print(
                        f"Combined Chunks: "
                        f"{len(combined_chunks)}"
                    )

                    sources = []

                    for chunk in combined_chunks:

                        if "source_file" in chunk:

                            sources.append(
                                chunk["source_file"]
                            )
                    # -----------------------
                    # Hybrid RAG Decision
                    # -----------------------

                    repository_context = ""
                    commit_context = ""
                    pr_context = ""

                    hybrid_keywords = [
                        "commit",
                        "commits",
                        "pr",
                        "prs",
                        "pull request",
                        "history",
                        "trend",
                        "trends",
                        "evolution",
                        "evolving",
                        "recent",
                        "change",
                        "changes",
                        "development",
                        "roadmap",
                        "future",
                        "growth",
                        "progress",

                        # Omni Context
                        "architecture",
                        "architectural",
                        "integration",
                        "integrated",
                        "component",
                        "components",
                        "module",
                        "modules",
                        "design",
                        "system",
                        "workflow",
                        "flow"
                    ]

                    use_hybrid_context = any(
                        keyword in question.lower()
                        for keyword in hybrid_keywords
                    )
                    # -----------------------
                    # Repository Context
                    # -----------------------

                    repository_keywords = [
                        "architecture",
                        "architectural",
                        "module",
                        "modules",
                        "overview",
                        "repository",
                        "framework",
                        "design",
                        "integration",
                        "component",
                        "components",
                        "system"
                    ]

                    use_repository_context = any(
                        keyword in question.lower()
                        for keyword in repository_keywords
                    )

                    if use_repository_context:

                        try:

                            repository_context = (
                                RepositoryAnalysisAgent()
                                .analyze(
                                    gemini
                                )
                            )

                        except Exception:

                            repository_context = ""

                    # -----------------------
                    # Architecture Context
                    # -----------------------

                    try:

                        architecture_context = (
                            ArchitectureAnalysisAgent()
                            .analyze()
                        )
                        print(
                            "\nARCHITECTURE CONTEXT PREVIEW:\n"
                        )

                        print(
                            architecture_context[:500]
                        )

                    except Exception:

                        architecture_context = ""

                    # -----------------------
                    # Specification Context
                    # -----------------------

                    try:

                        specification_context = (
                            SpecificationAnalysisAgent()
                            .analyze(
                                repository_context=
                                    repository_context,

                                architecture_context=
                                    architecture_context
                            )
                        )

                    except Exception:

                        specification_context = ""

                    # -----------------------
                    # Documentation Context
                    # -----------------------

                    try:

                        documentation_context = (
                            DocumentationAnalysisAgent()
                            .analyze()
                        )

                        print(
                            "\nDOCUMENTATION CONTEXT PREVIEW:\n"
                        )

                        print(
                            documentation_context[:500]
                        )

                    except Exception:

                        documentation_context = "" 

                    # -----------------------
                    # Commit Context
                    # -----------------------

                    if use_hybrid_context:

                        try:

                            commits = await (
                                github_client
                                .list_commits(
                                    owner,
                                    repo
                                )
                            )

                            commit_context = (
                                CommitAnalysisAgent()
                                .analyze(
                                    str(commits),
                                    gemini
                                )
                            )

                        except Exception:

                            commit_context = ""

                    # -----------------------
                    # PR Context
                    # -----------------------

                    if use_hybrid_context:

                        try:

                            prs = await (
                                github_client
                                .list_pull_requests(
                                    owner,
                                    repo
                                )
                            )

                            pr_context = (
                                PRAnalysisAgent()
                                .analyze(
                                    str(prs),
                                    gemini
                                )
                            )

                        except Exception:

                            pr_context = ""

                    # -----------------------
                    # Build Hybrid Context
                    # -----------------------

                    context = (
                        hybrid_agent
                        .build_context(
                            technical_chunks=
                                combined_chunks,

                            repository_context=
                                repository_context,

                            architecture_context=
                                architecture_context,

                            documentation_context=
                                documentation_context,

                            specification_context=
                                specification_context,

                            commit_context=
                                commit_context,

                            pr_context=
                                pr_context
                        )
                    )

                    print("\n========== HYBRID RAG DEBUG ==========")

                    print(
                        f"Repository Context Length: "
                        f"{len(repository_context)}"
                    )

                    print(
                        f"Architecture Context: "
                        f"{len(architecture_context)}"
                    )

                    print(
                    f"Specification Context: "
                    f"{len(specification_context)}"
                )

                    print(
                        f"Documentation Context: "
                        f"{len(documentation_context)}"
                    )

                    print(
                        f"Commit Context Length: "
                        f"{len(commit_context)}"
                    )

                    print(
                        f"PR Context Length: "
                        f"{len(pr_context)}"
                    )

                    print(
                        f"Retrieved Chunks: "
                        f"{len(combined_chunks)}"
                    )

                    print(
                        f"Total Context Length: "
                        f"{len(context)}"
                    )

                    print("=====================================\n")

                    prompt = f"""
                    You are an expert Repository Intelligence Assistant.

                    Use ALL provided context.

                    Context:

                    {context}

                    Question:

                    {question}

                    Provide:

                    1. Detailed Answer
                    2. Technical Explanation
                    3. Repository Impact
                    4. Summary
                    """
                    if use_hybrid_context:

                        print(
                            "\n✅ Hybrid RAG Mode Enabled"
                        )

                        print(
                            f"Repository Context: "
                            f"{len(repository_context)}"
                        )

                        print(
                            f"Commit Context: "
                            f"{len(commit_context)}"
                        )

                        print(
                            f"PR Context: "
                            f"{len(pr_context)}"
                        )

                        print(
                            f"Chunks Retrieved: "
                            f"{len(combined_chunks)}"
                        )

                    else:

                        print(
                            "\n✅ Standard RAG Mode"
                        )

                    answer = (
                        gemini.generate(
                            prompt
                        )
                    )

                    print(
                        "\nANSWER\n"
                    )

                    print(
                        answer
                    )

                    print(
                        "\nSOURCES\n"
                    )

                    for source in sorted(
                        set(sources)
                    ):

                        print(
                            f"- {source}"
                        )

                except Exception as ex:

                    print(
                        f"\nError: {ex}"
                    )


if __name__ == "__main__":

    asyncio.run(main())