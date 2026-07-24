from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-key",
    base_url="http://localhost:4000"
)

class LiteLLMAgent:

    def generate(
        self,
        prompt
    ):

        response = client.chat.completions.create(
            model="vertex-gemini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response
            .choices[0]
            .message
            .content
        )