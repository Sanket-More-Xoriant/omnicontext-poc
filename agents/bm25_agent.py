from rank_bm25 import BM25Okapi


class BM25Agent:

    def __init__(self, chunks):

        self.chunks = chunks

        tokenized_chunks = [
            chunk["content"].lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(
            tokenized_chunks
        )

    def search(
        self,
        query,
        top_k=10
    ):

        scores = self.bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for idx, score in ranked[:top_k]:

            results.append({
                "chunk": self.chunks[idx],
                "score": float(score),
                "retriever": "bm25"
            })

        return results
