import asyncio
import os

from dotenv import load_dotenv

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
                "\nBuilding FAISS Index..."
            )

            index = (
                embedding_agent
                .create_faiss_index(
                    vectors
                )
            )

            print(
                "FAISS Ready ✅"
            )

            retrieval_agent = (
                RetrievalAgent()
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
                    # NORMAL RAG FLOW
                    # =====================

                    retrieved_chunks = (
                        retrieval_agent
                        .search(
                            question,
                            vectorizer,
                            index,
                            chunks,
                            top_k=15
                        )
                    )

                    sources = []

                    context = ""

                    for chunk in retrieved_chunks:

                        context += (
                            chunk["content"]
                            + "\n\n"
                        )

                        sources.append(
                            chunk[
                                "source_file"
                            ]
                        )

                    prompt = f"""
You are a GitHub repository expert.

Answer only from the repository context.

Repository Context:

{context}

Question:

{question}

Provide a detailed answer.
"""

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