import requests

# URL для GraphQL-запроса
url = 'http://localhost:8000/graphql'

# GraphQL мутация
mutation = """
mutation {
  addUser(
    data: {
      firstName: "eblo"
      lastName: "slona"
      roleId: 1
      email: "babakapa729@gmail.com"
      password: "string"
    }
  )
  {
    id
  }
}
"""

# Заголовки HTTP
headers = {
    'Content-Type': 'application/json',
}

# Тело запроса
data = {
    'query': mutation
}

# Отправка POST-запроса
response = requests.post(url, json=data, headers=headers)

# Печать куки из ответа
print("Cookies:")
for cookie in response.cookies:
    print(f"{cookie.name}: {cookie.value}")

# Печать тела ответа
print("Response JSON:")
print(response.json())
