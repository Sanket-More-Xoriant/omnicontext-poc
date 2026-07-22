from sklearn.metrics.pairwise import cosine_similarity


class RetrievalAgent:

    def tfidf_search(
        self,
        question,
        vectorizer,
        vectors,
        chunks,
        top_k=10
    ):

        query_vector = (
            vectorizer.transform(
                [question]
            )
        )

        similarities = (
            cosine_similarity(
                query_vector,
                vectors
            )
            .flatten()
        )

        top_indices = (
            similarities.argsort()
            [-top_k:]
            [::-1]
        )

        results = []

        for idx in top_indices:

            if 0 <= idx < len(chunks):

                results.append(
                    chunks[idx]
                )

        return results