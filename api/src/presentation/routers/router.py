import json

from fastapi import APIRouter, File, UploadFile

from infrastructure.external_services.speech_task.yandex_speech_to_text import (
    speech_to_text,
)
from speech_task.abstract_text_processing import text_to_task

router = APIRouter()


@router.post("/speech-to-task")
async def speech_to_task(file: UploadFile = File(...)):
    text = await speech_to_text(file)
    task = await text_to_task(text)
    return json.loads(task)
