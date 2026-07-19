from agents.chunking_agent import ChunkingAgent
from agents.embedding_agent import EmbeddingAgent

chunks = ChunkingAgent().create_chunks()

embedding_agent = EmbeddingAgent()

vectors, vectorizer = (
    embedding_agent.create_embeddings(
        chunks
    )
)

print(
    "Vector Shape:",
    vectors.shape
)

embedding_agent.create_faiss_index(
    vectors
)

print(
    "FAISS Index Created"
)