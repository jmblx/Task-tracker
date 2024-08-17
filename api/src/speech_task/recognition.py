import json
import time
from io import BytesIO
from pathlib import Path

import aiohttp
import jwt
from fastapi import UploadFile
from pydub import AudioSegment

from config import FOLDER_ID, KEY_ID, SERVICE_ACCOUNT_ID, YANDEX_PRIVATE_KEY


def convert_to_ogg(input_file_content, output_file_path=None, *, save=False):
    audio = AudioSegment.from_file(BytesIO(input_file_content))

    output_io = BytesIO()

    audio.export(output_io, format="ogg", codec="libopus")

    if save and output_file_path:
        path = Path(output_file_path)
        with path.open("wb") as f:
            f.write(output_io.getvalue())

    return output_io.getvalue()


async def get_iam_token(encoded_token, url, headers):

    async with (
        aiohttp.ClientSession() as session,
        session.post(
            url,
            headers=headers,
            data=json.dumps({"jwt": encoded_token}),
            timeout=6,
        ) as response,
    ):

        return (await response.json()).get("iamToken")


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
