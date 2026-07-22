# test_model.py

import os

os.environ["HF_HUB_DISABLE_XET"] = "1"
os.environ["HF_HUB_DOWNLOAD_TIMEOUT"] = "300"

from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer(
    "paraphrase-MiniLM-L3-v2"
)

print("Loaded ✅")