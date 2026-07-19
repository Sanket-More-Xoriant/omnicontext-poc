from agents.chunking_agent import ChunkingAgent
from agents.embedding_agent import EmbeddingAgent
from agents.retrieval_agent import RetrievalAgent

chunks = ChunkingAgent().create_chunks()

embedding_agent = EmbeddingAgent()

vectors, vectorizer = (
    embedding_agent.create_embeddings(
        chunks
    )
)

index = (
    embedding_agent.create_faiss_index(
        vectors
    )
)

retrieval_agent = RetrievalAgent()

results = retrieval_agent.search(
    query="How does Semantic Kernel support MCP?",
    vectorizer=vectorizer,
    index=index,
    chunks=chunks,
    top_k=3
)

for r in results:

    print("\n")
    print(r["source_file"])
    print("-" * 50)
    print(r["content"][:500])