from sentence_transformers import (
    SentenceTransformer
)

class EmbeddingAgent:

    def __init__(self):

        print(
            "\nLoading Sentence Transformer..."
        )

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print(
            "✅ Embedding Model Ready"
        )

    def create_embeddings(
        self,
        chunks
    ):

        corpus = [
            chunk.get(
                "content",
                ""
            )
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            corpus,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        print(
            f"Embedding Shape: {embeddings.shape}"
        )

        return embeddings

    def create_query_embedding(
        self,
        question
    ):

        return self.model.encode(
            question,
            convert_to_numpy=True
        )