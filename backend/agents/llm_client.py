class LLMClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    async def call_llm(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama-3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error calling LLM: {str(e)}") 