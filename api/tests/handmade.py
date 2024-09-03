import asyncio

import aiohttp

# URL вашего сервера для отправки запроса авторизации
AUTH_URL = "http://127.0.0.1:8000/graphql"  # замените на URL вашего сервера

# ГрафQL запрос авторизации
query = """
query {
  authUser(authData: {
    email: "admin@admin.com"
    password: "admin"
  })
}
"""


async def send_auth_request(session, url, headers, query):
    async with session.post(
        url, json={"query": query}, headers=headers
    ) as response:
        data = await response.json()
        print(f"Response status: {response.status}")
        print(f"Response data: {data}")
        return data


async def main():
    headers = {"Fingerprint": "3ccc784000c0c0c11cab8508dffaa578"}

    # Создаем сессию aiohttp
    async with aiohttp.ClientSession() as session:
        # Отправляем три одновременных запроса
        tasks = [
            send_auth_request(session, AUTH_URL, headers, query),
            send_auth_request(session, AUTH_URL, headers, query),
            send_auth_request(session, AUTH_URL, headers, query),
        ]
        # Выполняем все задачи одновременно
        results = await asyncio.gather(*tasks)
        print("All requests completed")


# Запускаем асинхронный цикл
asyncio.run(main())
