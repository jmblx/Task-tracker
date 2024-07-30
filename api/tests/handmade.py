import requests

url = 'http://localhost:8000/graphql'

query = """
query {
  authUser(authData: {
    email: "lapka@gmail.com"
    password: "string"
  })
}
"""

response = requests.post(url, json={'query': query})

cookies = response.cookies

print("Response JSON:", response.json())
print("Cookies:", cookies)

refresh_token = cookies.get('refreshToken')
if refresh_token:
    print("Refresh Token:", refresh_token)
else:
    print("Refresh Token not found in cookies.")
