# Send prompt, Receive response, Handle failures
import os

from dotenv import load_dotenv

import vertexai
from vertexai.generative_models import GenerativeModel

load_dotenv()


class GeminiClient:

    def __init__(self):

        os.environ[
            "GOOGLE_APPLICATION_CREDENTIALS"
        ] = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

        vertexai.init(
            project=os.getenv(
                "VERTEX_PROJECT_ID"
            ),
            location="us-central1"
        )

        self.model = GenerativeModel(
            os.getenv(
                "VERTEX_MODEL"
            )
        )

    def generate(
        self,
        prompt: str
    ):

        response = self.model.generate_content(
            prompt
        )

        return response.text