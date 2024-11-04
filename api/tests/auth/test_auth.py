# import pytest
# from httpx import AsyncClient
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "email, password, fingerprint, expected_error_message",
#     [
#         ("admin@admin.com", "admin", "3ccc784000c0c0c11cab8508dffaa578", None),
#         (
#             "user@example.com",
#             "wrongpassword",
#             "3ccc784000c0c0c11cab8508dffaa578",
#             "401: Unauthorized",
#         ),
#         (
#             "nonexistent@example.com",
#             "password",
#             "3ccc784000c0c0c11cab8508dffaa578",
#             "401: Unauthorized",
#         ),
#         ("admin@admin.com", "admin", None, "400: Fingerprint is required"),
#     ],
# )
# async def test_auth_user(
#     ac: AsyncClient,
#     email: str,
#     password: str,
#     fingerprint: str,
#     expected_error_message: str,
# ):
#     query = f"""
#         query {{
#           authUser(authData: {{
#             email: "{email}"
#             password: "{password}"
#           }})
#         }}
#     """
#
#     headers = {}
#     if fingerprint:
#         headers["Fingerprint"] = fingerprint
#
#     response = await ac.post(
#         "/graphql", headers=headers, json={"query": query}
#     )
#
#     assert response.status_code == 200
#     data = response.json()
#
#     if expected_error_message:
#         assert (
#             "errors" in data
#         ), "Expected errors in the response, but none were found."
#         error_messages = [error["message"] for error in data["errors"]]
#         assert (
#             expected_error_message in error_messages
#         ), f"Expected error message '{expected_error_message}' not found in response."
#     else:
#         assert (
#             "data" in data
#         ), "Expected data in the response, but none were found."
#         assert (
#             "authUser" in data["data"]
#         ), "Expected 'authUser' field in the response data, but none were found."
#         assert "token" in data["data"]["authUser"]["accessToken"]
#         assert "expires_in" in data["data"]["authUser"]["accessToken"]
#         assert "created_at" in data["data"]["authUser"]["accessToken"]
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(
#     "first_name, last_name, role_id, email, password, is_active, is_verified, pathfile, tg_id, tg_settings, github_name, expected_error_message",
#     [
#         (
#             "baron",
#             "bloody",
#             4,
#             "bloody_baron@velen.com",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             None,
#         ),  # Valid case
#         (
#             "baron",
#             "bloody",
#             4,
#             "existing_email@velen.com",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Email already exists",
#         ),
#         (
#             "baron",
#             "bloody",
#             99,
#             "valid_email@velen.com",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Role does not exist",
#         ),
#         (
#             "baron",
#             "bloody",
#             4,
#             "invalid_email.com",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Invalid email format",
#         ),
#         (
#             "baron",
#             "bloody",
#             4,
#             "new_user@velen.com",
#             "short",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Password too short or does not contain a digit",
#         ),
#         (
#             "",
#             "bloody",
#             4,
#             "new_user@velen.com",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "First name cannot be empty",
#         ),
#         (
#             "baron",
#             "",
#             4,
#             "new_user@velen.com",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Last name cannot be empty",
#         ),
#         (
#             "baron",
#             "bloody",
#             4,
#             "",
#             "uma12345",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Email cannot be empty",
#         ),
#         (
#             "baron",
#             "bloody",
#             4,
#             "new_user@velen.com",
#             "uma no digits",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Password must contain at least one digit",
#         ),
#         (
#             "baron",
#             "bloody",
#             4,
#             "another_user@velen.com",
#             "12345678",
#             True,
#             True,
#             None,
#             None,
#             None,
#             None,
#             "Password must contain at least one letter",
#         ),
#         (
#             "baron",
#             "bloody",
#             4,
#             "another_user@velen.com",
#             "validpass1",
#             True,
#             True,
#             None,
#             "333123",
#             None,
#             None,
#             "Invalid tg_id format",
#         ),
#     ],
# )
# async def test_register_user(
#     ac: AsyncClient,
#     first_name: str,
#     last_name: str,
#     role_id: int,
#     email: str,
#     password: str,
#     is_active: bool,
#     is_verified: bool,
#     pathfile: str,
#     tg_id: str,
#     tg_settings: dict,
#     github_name: str,
#     expected_error_message: str,
# ):
#     query = f"""
#     mutation {{
#         addUser(
#             data: {{
#                 firstName: "{first_name}"
#                 lastName: "{last_name}"
#                 roleId: {role_id}
#                 email: "{email}"
#                 password: "{password}"
#                 isActive: {str(is_active).lower()}
#                 isVerified: {str(is_verified).lower()}
#                 pathfile: "{pathfile}" if pathfile else null
#                 tgId: "{tg_id}" if tg_id else null
#                 tgSettings: {tg_settings} if tg_settings else null
#                 githubName: "{github_name}" if github_name else null
#             }}
#         ) {{
#             id
#         }}
#     }}
#     """
#
#     response = await ac.post("/graphql", json={"query": query})
#
#     assert response.status_code == 200
#     data = response.json()
#
#     if expected_error_message:
#         assert (
#             "errors" in data
#         ), "Expected errors in the response, but none were found."
#         error_messages = [error["message"] for error in data["errors"]]
#         assert (
#             expected_error_message in error_messages
#         ), f"Expected error message '{expected_error_message}' not found in response."
#     else:
#         assert (
#             "data" in data
#         ), "Expected data in the response, but none were found."
#         assert (
#             "addUser" in data["data"]
#         ), "Expected 'addUser' field in the response data, but none were found."
#         assert (
#             "id" in data["data"]["addUser"]
#         ), "Expected 'id' field in the 'addUser' response data, but none were found."
