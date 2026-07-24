import chromadb


class ChromaAgent:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

    def get_collection(
        self,
        repository_name
    ):

        return self.client.get_or_create_collection(
            name=repository_name
                .replace("/", "_")
                .replace("-", "_")
        )

    def store_chunks(
        self,
        repository_name,
        chunks,
        vectors
    ):

        collection_name = (
            repository_name
                .replace("/", "_")
                .replace("-", "_")
        )

        # Delete existing collection if it exists
        try:

            self.client.delete_collection(
                collection_name
            )

            print(
                f"Existing collection deleted: "
                f"{collection_name}"
            )

        except Exception:

            pass

        collection = self.get_collection(
            repository_name
        )

        documents = []
        ids = []
        metadatas = []

        for index, chunk in enumerate(
            chunks
        ):

            documents.append(
                chunk.get(
                    "content",
                    ""
                )
            )

            ids.append(
                f"chunk_{index}"
            )

            metadatas.append(
                {
                    "source_file": chunk.get(
                        "source_file",
                        ""
                    )
                }
            )

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=vectors.tolist()
        )

        print(
            f"Stored {len(chunks)} chunks in ChromaDB"
        )

    def search(
        self,
        repository_name,
        query_embedding,
        top_k=5
    ):

        collection = self.get_collection(
            repository_name
        )

        results = collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k
        )

        return results