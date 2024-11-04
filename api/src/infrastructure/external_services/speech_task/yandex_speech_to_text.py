import time

import aiohttp
import jwt
from fastapi import UploadFile

from config import FOLDER_ID, KEY_ID, SERVICE_ACCOUNT_ID, YANDEX_PRIVATE_KEY
from infrastructure.utils.speech_task import convert_to_ogg, get_iam_token


async def speech_to_text(speech_file: UploadFile) -> str:
    service_account_id = SERVICE_ACCOUNT_ID
    key_id = KEY_ID

    private_key = YANDEX_PRIVATE_KEY

    now = int(time.time())
    payload = {
        "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
        "iss": service_account_id,
        "iat": now,
        "exp": now + 360,
    }

    encoded_token = jwt.encode(
        payload, private_key, algorithm="PS256", headers={"kid": key_id}
    )

    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    headers = {"Content-Type": "application/json"}

    iam_token = await get_iam_token(encoded_token, url, headers)

    data = convert_to_ogg(await speech_file.read(), save=False)

    params = "&".join(["topic=general", f"folderId={FOLDER_ID}", "lang=ru-RU"])
    async with (
        aiohttp.ClientSession() as session,
        session.post(
            f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?{params}",
            data=data,
            headers={"Authorization": f"Bearer {iam_token}"},
        ) as response,
    ):
        decoded_data = await response.json()
    error_code = decoded_data.get("error_code")
    if error_code is None:

        return decoded_data.get("result")[
            : int(len(decoded_data.get("result")) / 2)
        ]
    else:
        return f"error: {error_code}"
