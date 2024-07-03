import json
import urllib.request
import time
from io import BytesIO

import requests
import jwt
from fastapi import UploadFile
from pydub import AudioSegment


def convert_to_ogg(input_file_content, save=False, output_file_path=None):
    audio = AudioSegment.from_file(BytesIO(input_file_content))

    output_io = BytesIO()

    audio.export(output_io, format='ogg', codec='libopus')

    if save and output_file_path:
        with open(output_file_path, 'wb') as f:
            f.write(output_io.getvalue())

    return output_io.getvalue()


async def speech_to_text(speech_file: UploadFile) -> str:
    service_account_id = "ajen4qb0kojndi7jo3os"
    key_id = "ajeu67ofjl5jg14immi7"

    private_key = "PLEASE DO NOT REMOVE THIS LINE! Yandex.Cloud SA Key ID \u003cajeu67ofjl5jg14immi7\u003e\n-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDOa9HMEJaYVts7\nKXe46M13XJYsGBC9O2tRSpbCRSndeB5o+6zW+SMR3dQtjSbbv7dPuDnx6gzw7Pk2\nCEYVnoXTY76bry+qLC2dKH2uQvw79g27bmyYVw7Xbrdo0CvZeRmJ/D/jGkpYFQ7m\nAoDH0nLH9sYvKog2TOrYIUt1A5h4Kge0nHm9MUzkGSEzBAFup7XeJ9NmOLB8J9ex\nD4UfIXZbdI508wvKeRCAVJXDvxu10rDCGfjgpLssgn0BUnbAWD9cZNDtaI6qtDyC\nByhdDvRrDfcaBnYnvER8kTJpcxW0p+PYkkCH2hacE+un3qqsaV0AoRkyxHQkLyI9\ndXKEwjktAgMBAAECggEACew+xYBDo6xDNX9wu6ZnSsuxhV+dHbeiQ6IMsryNPryk\nO5g47rbtvma16Sr9+Ut98KVdaw68/gTqQEnFXWCFiYv5MPXgL55C4r6Rohj4E/An\n/gCuKY7qeKU1cw1UxPYbFJoYE8mjABkiYktbAkq7IqKEfuZyGKgkaZeEz38eKyKF\n/lNxJJFF+BxkiAiczb/NX6sfT3wl+FI+aUmlzdY1urdryEk9xnirSjPEaMK1CV9m\nJRJkHimdCT9uT6PoKO6urWQAO4QEtxvsrsZ9lh/JUbl8sBPaVHpe99fCFdHwj7R8\nVXSTXYIEIFDVBQKS+mXmBv/02zqM+plCZHibxfDlSQKBgQDrX4pgmkoqPHNqj5du\n20inA8QWskpveTpXnB/gVQ/HsoKclgF4JnUXF0qIBeCzrQEg97tY7hgw5CSUPzpz\nN3mdZRN6IYQYP9h9YPLfMSLmsleUVL7YlUWbEoGzm+y+0yitOUspsjGyadYQrjEx\nrqnDRWSLAWdKr2I4TMkfkoFvGQKBgQDggsHRFfnXoNbssDzhQl4iRQWstpMvvVUP\nRy7sbWDe4uy+i7LVO7zPidmKKtrXN60tL1n4iSvHPrvJJ/mZOF5GaIK9yMON3uDU\nI4XzkcAECYpUiA+u04rhHROESA3/Xdi7C6Fo4s3m4Z2cvmDCGzi+WohjfVsBV76X\ntttyrkQhNQKBgQDaJDL4cyaXXG1PboNXv63m9EuRCW6JP959gfndDJjSaLQ6caAs\n/d95JiHyTRhDDe1E47RjqE8NSPRJ3QvL6rcw05OollV5r/pxwR93EXAaRWF73Mr/\nqeDX5uAEWVeiR8ukN7xciYUbqJE35mk7dXhqvO6BEizr//3U1f104HBLSQKBgQDS\n/G7SZHmgF6oDUvhTpQA76muTzRxzT9Wg/v9s9rmDnPRpeXV9iJ8+1shWXUG94bfg\nb9B4jchTfXQSbXvWby/BsTO00Phd2iellSCsLrupz6FtIVTDsk+gkKent+NXqkUk\nOqDcpdBkeoCZLhxWLijcUs472TFuCJy3jQOcOYMTRQKBgCFlodGkG9mFFVwIz0+K\nB619+NXXV3AAFOF0w7ncr1R48lBA563fcfnGq3D3UtA+M+SO7YKMwh1qiSPrxGAQ\nVwnN7spmaYXan3Tj53ojapRd9d2WfmdP8BBo0SkcrF8ga7S6CWrBhE0Fed/UrYpl\nhdwzCuhXk8DoKlJ5V5lOflfD\n-----END PRIVATE KEY-----\n"

    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 360
    }

    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id})

    url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
    headers = {'Content-Type': 'application/json'}
    data = {"jwt": encoded_token}

    response = requests.post(url, headers=headers, data=json.dumps(data))

    FOLDER_ID = "b1g2dk07gt1535ofpmtm"
    IAM_TOKEN = response.json().get("iamToken")
    # IAM_TOKEN = "t1.9euelZqLxpXJjc3Gnc2XzZ3KkIqYlO3rnpWakcuOnc-UkJWRm5bIlZDMkIzl9Pdrbg5N-e8jQGLV3fT3Kx0MTfnvI0Bi1c3n9euelZqPjp7Kz56PnpOTx53IlYrIlu_8zef1656VmorJyJCZlZPKlZjOy5aSkpbI7_3F656Vmo-OnsrPno-ek5PHnciVisiW.FaTOxbV30P3-GEgt3gZGi4YYhSDhNOAsXUkeuOF-6yhTSEXHV56jID_FRLd__ryOleyxSaM7xX31itx56sZYBQ" # IAM-токен
    data = convert_to_ogg(await speech_file.read())

    params = "&".join([
        "topic=general",
        "folderId=%s" % FOLDER_ID,
        "lang=ru-RU"
    ])

    response = requests.post("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data, headers={"Authorization": f"Bearer %s" % IAM_TOKEN})
    # url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)

    # responseData = urllib.request.urlopen(url).read().decode('UTF-8')
    # decodedData = json.loads(responseData)
    decodedData = response.json()
    if decodedData.get("error_code") is None:
        print(decodedData)
    else:
        print(decodedData.get("error_code"))
        print(decodedData.get("error_message"))

# data = {
#     "folderId": FOLDER_ID,
#     "texts": ["angel"],
#     "targetLanguageCode": "ru",
#     "sourceLanguageCode": "en"
# }

# response = requests.post("https://translate.api.cloud.yandex.net/translate/v2/translate", headers={
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {IAM_TOKEN}"
# }, data=json.dumps(data))
    result = decodedData.get("result")[:int(len(decodedData.get("result")) / 2)]
    return result
