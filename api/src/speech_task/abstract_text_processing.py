import json
import uuid
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any

from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
from groq import Groq

load_dotenv()


class ChatBot(ABC):
    @abstractmethod
    def get_access_token(self) -> str:
        pass

    @abstractmethod
    def send_prompt(self, msg: str, access_token: str) -> str:
        pass

    def render(self, data: str) -> str:
        print(data)
        return (
            """
В ответе нужен только результат твоей обработки задачи, ничего про процесс выполнения не нужно, ни кода,
 ни мыслительного процесса, только результат в json без лишних отступов и пробелов.
Пример входных данных 1:
json
{
  "text": "надо сделать лэндинг для цветочного магазина и использовать желтый и зеленый до конца пятницы, начать нужно завтра",
  "current_day": 11,
  "current_month": 6,
  "current_year": 2024
}
Шаги для выполнения:
    Извлечение текущей даты и дня недели из входных данных:
        Текущая дата: 11 июня 2024 года
        Если информации в поле text о том когда задача начинается и когда кончается нет, то поле оставь пустым и так для всех полей с датой.
    Анализ текста и определение дат начала и окончания задания:
        В тексте указано, что задание должно начаться "завтра". Значит, дата начала: 12 июня 2024 года.
        В тексте указано, что задание должно быть выполнено "до конца пятницы". Значит, дата окончания: пятница той же недели, т.е. 14 июня 2024 года.
    Определение названия и деталей задания из текста:
        Название задания: "Сделать лэндинг для цветочного магазина"
        Детали задания это вся полезная информация, которую нужно знать, чтобы выполнить задание также как оно и задумано и в данном случае:
            Корпоративные цвета: желтый и зеленый
            Тематика: цветочный магазин
    Формирование JSON с полной информацией:
Выходные данные 1:
json
{
  "day_start": 12,
  "month_start": 6,
  "year_start": 2024,
  "day_end": 14,
  "month_end": 6,
  "year_end": 2024,
  "name": "Сделать лэндинг для цветочного магазина",
  "details": "Корпоративные цвета: желтый и зеленый. Тематика: цветочный магазин."
}
Примеры других возможных входных данных и ожидаемых выходных данных:
Пример 2:
Входные данные:
json
{
  "text": "Разработать веб-сайт для кафе, использовать фреймворк React, и методологию БЭМ завершить до конца среды следующей недели",
  "current_day": 9,
  "current_month": 8,
  "current_year": 2024
}
Выходные данные:
json
{
  "day_start": null,
  "month_start": 6,
  "year_start": 2024,
  "day_end": 19,
  "month_end": 6,
  "year_end": 2024,
  "name": "Разработать веб-сайт для кафе",
  "details": "Фреймворк: React. Методология: БЭМ. Тематика: кафе."
}

Теперь выполни такой анализ с входными данными:
"""
            + data
        )

    def sent_prompt_and_get_response(self, msg: str, access_token: str = "") -> str:
        return self.send_prompt(msg, access_token)


class GigaChatBot(ChatBot):
    CLIENT_ID = os.getenv("CLIENT_ID")
    SECRET = os.getenv("SECRET")

    def get_access_token(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
        }
        payload = {"scope": "GIGACHAT_API_PERS"}
        res = requests.post(
            url=url,
            headers=headers,
            auth=HTTPBasicAuth(self.CLIENT_ID, self.SECRET),
            data=payload,
            verify=False,
        )
        access_token = res.json()["access_token"]
        return access_token

    def send_prompt(self, msg: str, access_token: str = None) -> str:
        if access_token is None:
            access_token = self.get_access_token()
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

        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response.json()["choices"][0]["message"]["content"]


class LLamaChatBot(ChatBot):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def get_access_token(self) -> str:
        return ""

    def send_prompt(self, msg: str, access_token: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a language model (LLM) expert and answer questions from newbie programmers.
                     You should answer in a friendly manner and understandable for beginners. Answer in Russian.""",
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


# def text_to_task(speech_text: str, api_key: str = "") -> str:
#     load_dotenv()
#     api_key = os.getenv("GROQ_KEY", "") if api_key == "" else api_key
#     if api_key == "":
#         raise Exception("API key not set")
#     llama_bot = LLamaChatBot(api_key=api_key)
#     input_dict = {"text": speech_text} | get_cur_date()
#     input_json = json.dumps(str(input_dict))
#     prompt = llama_bot.render(input_json)
#     response = llama_bot.sent_prompt_and_get_response(prompt)
#     return response


def text_to_task(speech_text: str, api_key: str = "") -> str:
    gigachat_bot = GigaChatBot()
    input_dict = {"text": speech_text} | get_cur_date()
    access_token = gigachat_bot.get_access_token()
    input_json = json.dumps(str(input_dict), ensure_ascii=False)
    prompt = gigachat_bot.render(input_json)
    response = gigachat_bot.sent_prompt_and_get_response(prompt, access_token)
    print(response)
    return response


def get_cur_date() -> Dict[str, Any]:
    now = datetime.now()
    return {
        "current_day": now.day,
        "current_month": now.month,
        "current_year": now.year,
    }


# if __name__ == "__main__":
#     data = '''{
#       "text": "нужно написать фичу для кинотеатра на FastApi или Flask, которая будет использовать внешний API графовой системы для составления рекомендаций пользователю. начать нужно сегодня, а закончить нужно до конца четверга.",
#       "current_day": 19,
#       "current_day_of_the_week": "Вторник",
#       "current_month": 3,
#       "current_year": 2024
#     }'''
#
#     # gigachat_bot = GigaChatBot()
#     # access_token = gigachat_bot.get_access_token()
#     # prompt = gigachat_bot.render(data)
#     # response = gigachat_bot.sent_prompt_and_get_response(prompt, access_token)
#     # print(response)
#
#     llama_bot = LLamaChatBot(api_key=os.getenv("GROQ_KEY"))
#     prompt = llama_bot.render(data)
#     response = llama_bot.sent_prompt_and_get_response(prompt, "")
#     print(response)
