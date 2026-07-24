import numpy as np

from sklearn.metrics.pairwise import (
    cosine_similarity
)

class RetrievalAgent:

    def semantic_search(
        self,
        question,
        embedding_agent,
        embeddings,
        chunks,
        top_k=10
    ):

        query_embedding = (
            embedding_agent
            .create_query_embedding(
                question
            )
            .reshape(1, -1)
        )

        similarities = (
            cosine_similarity(
                query_embedding,
                embeddings
            )[0]
        )

        top_indices = (
            np.argsort(
                similarities
            )[::-1][:top_k]
        )

        results = []

        for idx in top_indices:

            results.append({
                "chunk": chunks[idx],
                "score": float(
                    similarities[idx]
                ),
                "retriever": "semantic"
            })

        return results