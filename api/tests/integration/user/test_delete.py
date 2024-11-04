import pytest
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_update_user_via_graphql(
    graphql_client, mock_user, async_session: AsyncSession
):
    """
    Тестирование регистрации пользователя и обновления его данных через GraphQL.
    """
    mutation_query = f"""
        mutation {{
            deleteUsersWithResponse(
                searchData: {{ id: "{mock_user.id}" }}
                orderBy: {{ field: "id", direction: "desc" }}
                fullDelete: true
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
    updated_user = data["data"]["deleteUsersWithResponse"][0]
    assert updated_user["firstName"] == mock_user.first_name
    assert updated_user["email"] == mock_user.email
    assert updated_user["id"] == str(mock_user.id)

    with pytest.raises(InvalidRequestError):
        await async_session.refresh(mock_user)
