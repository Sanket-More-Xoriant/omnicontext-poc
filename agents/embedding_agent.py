from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingAgent:

    def __init__(self):

        print(
            "\nCreating TF-IDF Engine..."
        )

        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words="english"
        )

        print(
            "✅ TF-IDF Engine Ready"
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

        print(
            f"\nGenerating TF-IDF vectors "
            f"for {len(corpus)} chunks..."
        )

        vectors = (
            self.vectorizer
            .fit_transform(
                corpus
            )
        )

        print(
            f"\nVector Shape: "
            f"{vectors.shape}"
        )

        return (
            vectors,
            self.vectorizer
        )

    def create_query_embedding(
        self,
        question
    ):

        return (
            self.vectorizer
            .transform(
                [question]
            )
        )
