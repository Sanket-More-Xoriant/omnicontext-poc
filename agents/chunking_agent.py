import json
import os

from dotenv import load_dotenv
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

load_dotenv()


class ChunkingAgent:

    def __init__(self):

        self.chunk_size = int(
            os.getenv(
                "CHUNK_SIZE",
                500
            )
        )

        self.chunk_overlap = int(
            os.getenv(
                "CHUNK_OVERLAP",
                50
            )
        )

        self.splitter = (
            RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        )

        self.skip_patterns = [

            ".github/",
            ".vscode/",
            ".idea/",

            "CONTRIBUTING.md",
            "TRANSPARENCY_FAQS.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",

            "docs/decisions/",
            "UnitTests/TestData/",
            "TestData/"
        ]

    def should_skip_file(
        self,
        file_path
    ):

        return any(
            pattern.lower()
            in file_path.lower()
            for pattern in self.skip_patterns
        )

    def is_code_file(
        self,
        file_path
    ):

        code_extensions = [
            ".py",
            ".cs",
            ".java",
            ".js",
            ".ts",
            ".tsx",
            ".jsx",
            ".go",
            ".cpp",
            ".c",
            ".hpp",
            ".h"
        ]

        return any(
            file_path.lower().endswith(ext)
            for ext in code_extensions
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

        skipped_files = 0

        for doc in documents:

            file_path = doc.get(
                "file_path",
                ""
            )

            if self.should_skip_file(
                file_path
            ):

                skipped_files += 1
                continue

            text = doc.get(
                "content",
                ""
            )

            if (
                not text
                or
                not text.strip()
            ):
                continue

            pieces = (
                self.splitter
                .split_text(text)
            )

            MAX_CHUNKS_PER_FILE = 15

            pieces = pieces[:MAX_CHUNKS_PER_FILE]

            for piece in pieces:

                chunks.append(
                    {
                        "chunk_id":
                            f"chunk_{counter}",

                        "source_file":
                            file_path,

                        "content":
                            piece,

                        "is_code":
                            self.is_code_file(
                                file_path
                            )
                    }
                )

                counter += 1

        print(
            f"\nSkipped Files: "
            f"{skipped_files}"
        )

        print(
            f"Total Chunks Created: "
            f"{len(chunks)}"
        )

        return chunks