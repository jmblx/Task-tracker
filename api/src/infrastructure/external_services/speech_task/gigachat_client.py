import json
import os
import uuid

import aiohttp
from aiohttp import BasicAuth
from dotenv import load_dotenv

from domain.services.text_processing.interface import ChatBot

load_dotenv()


class GigaChatBot(ChatBot):
    CLIENT_ID = os.getenv("CLIENT_ID")
    SECRET = os.getenv("SECRET")

    async def get_access_token(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
        }
        payload = {"scope": "GIGACHAT_API_PERS"}

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                url,
                headers=headers,
                auth=BasicAuth(self.CLIENT_ID, self.SECRET),
                data=payload,
                ssl=False,
            ) as response,
        ):
            res = await response.json()
            return res["access_token"]

    async def send_prompt(
        self, msg: str, access_token: str | None = None
    ) -> str:
        if access_token is None:
            access_token = await self.get_access_token()
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps(
            {
                "model": "GigaChat-Pro",
                "messages": [
                    {
                        "role": "user",
                        "content": msg,
                    }
                ],
            }
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                url, headers=headers, data=payload, ssl=False
            ) as response,
        ):
            res = await response.json()
            return res["choices"][0]["message"]["content"]
