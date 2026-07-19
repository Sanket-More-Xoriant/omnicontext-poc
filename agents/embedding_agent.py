import faiss
import numpy as np

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)


class EmbeddingAgent:

    def create_embeddings(
        self,
        chunks
    ):

        corpus = [
            chunk["content"]
            for chunk in chunks
        ]

        vectorizer = TfidfVectorizer(
            max_features=5000
        )

        vectors = (
            vectorizer
            .fit_transform(corpus)
            .toarray()
        )

        return vectors, vectorizer

    def create_faiss_index(
        self,
        vectors
    ):

        dimension = vectors.shape[1]

        index = faiss.IndexFlatL2(
            dimension
        )

        index.add(
            np.array(
                vectors,
                dtype=np.float32
            )
        )

        return index