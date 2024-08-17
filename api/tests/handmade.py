import requests

url = "http://localhost:8000/graphql"

query = """
query {
  authUser(authData: {
    email: "lapka@gmail.com"
    password: "string"
  })
}
"""

response = requests.post(url, json={"query": query}, timeout=5)

cookies = response.cookies


refresh_token = cookies.get("refreshToken")
if refresh_token:
    pass
else:
    pass
