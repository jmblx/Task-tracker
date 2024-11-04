import json
from io import BytesIO
from pathlib import Path

import aiohttp
from pydub import AudioSegment


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
