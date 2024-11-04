import requests

url = "http://localhost:8000/graphql"
query = """
mutation SetUserAvatar($userId: UUID!, $file: Upload!) {
    setUserAvatar(userId: $userId, file: $file)
}
"""

variables = {"userId": "0f478e71-d0a3-401c-a4fe-a98d4f10a749", "file": None}

with open("chmo.webp", "rb") as file:
    multipart_form_data = {
        "operations": (
            "",
            '{"query": '
            + query
            + ', "variables": {"userId": "0f478e71-d0a3-401c-a4fe-a98d4f10a749", "file": null}}',
        ),
        "map": ("", '{"1": ["variables.file"]}'),
        "1": (file.name, file, "image/webp"),
    }

    response = requests.post(url, files=multipart_form_data)
    print(response.json())
