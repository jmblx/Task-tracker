import json

from fastapi import APIRouter, File, UploadFile

from speech_task.abstract_text_processing import text_to_task
from speech_task.recognition import speech_to_text

router = APIRouter()


@router.post("/speech-to-task")
async def speech_to_task(file: UploadFile = File(...)):
    text = await speech_to_text(file)
    task = text_to_task(text)
    return json.loads(task)
