import os

from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

vertexai.init(
    project=os.getenv("VERTEX_PROJECT_ID"),
    location="us-central1"
)

model = GenerativeModel(
    os.getenv("VERTEX_MODEL")
)

response = model.generate_content(
    "Explain Semantic Kernel in 3 lines."
)

print("\nRESULT:\n")
print(response.text) 