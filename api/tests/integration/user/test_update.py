import os
import sys

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src"))
)


@pytest.mark.asyncio
async def test_update_user_via_graphql(
    graphql_client, mock_user, async_session: AsyncSession
):
    """
    Тестирование регистрации пользователя и обновления его данных через GraphQL.
    """
    updated_data = {
        "firstName": "lari",
        "lastName": "updated_last_name",
    }
    mutation_query = f"""
        mutation UpdateUsers {{
            updateUsers(
                searchData: {{ id: "{mock_user.id}" }}
                data: {{
                    firstName: "{updated_data['firstName']}",
                    lastName: "{updated_data['lastName']}",
                }}
                orderBy: {{ field: "id", direction: "desc" }}
            ) {{
                id
                firstName
                lastName
                roleId
                email
                isActive
                isVerified
                pathfile
                tgId
                tgSettings
                isEmailConfirmed
                registeredAt
            }}
        }}
        """

    response = await graphql_client.execute(mutation_query)
    assert response.status_code == 200
    data = response.json()

    assert "data" in data
    updated_user = data["data"]["updateUsers"][0]
    assert updated_user["firstName"] == updated_data["firstName"]
    assert updated_user["lastName"] == updated_data["lastName"]
    assert updated_user["id"] == str(mock_user.id)
    await async_session.refresh(mock_user)
    assert mock_user.first_name == updated_data["firstName"]
    assert mock_user.last_name == updated_data["lastName"]
