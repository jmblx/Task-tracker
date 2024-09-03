from groq import Groq

from domain.services.text_processing.interface import ChatBot


class LLamaChatBot(ChatBot):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    async def get_access_token(self) -> str:
        return ""

    async def send_prompt(self, msg: str, access_token: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a language model (LLM) expert and
                     answer questions from newbie programmers.
                     You should answer in a friendly manner and understandable
                    for beginners. Answer in Russian.""",
                },
                {
                    "role": "user",
                    "content": msg,
                },
            ],
            model="llama3-70b-8192",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
