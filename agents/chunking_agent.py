import json
import os

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


class ChunkingAgent:

    def __init__(self):

        self.chunk_size = int(
            os.getenv("CHUNK_SIZE", 500)
        )

        self.chunk_overlap = int(
            os.getenv("CHUNK_OVERLAP", 50)
        )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def create_chunks(
    self,
    cache_file
):

        with open(
            cache_file,
            "r",
            encoding="utf-8"
        ) as f:

            documents = json.load(f)

        chunks = []

        counter = 1

        for doc in documents:

            text = doc["content"]

            if not text:
                continue

            pieces = self.splitter.split_text(text)

            for piece in pieces:

                chunks.append(
                    {
                        "chunk_id": f"chunk_{counter}",
                        "source_file": doc["file_path"],
                        "content": piece
                    }
                )

                counter += 1

        return chunks