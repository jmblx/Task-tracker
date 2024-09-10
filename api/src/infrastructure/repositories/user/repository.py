from application.dtos.user import UserCreateDTO
from infrastructure.repositories.base_repository import BaseRepositoryImpl


class UserRepository:
    def __init__(self, base_repo: BaseRepositoryImpl):
        self.base_repo = base_repo

    # def get_selected_fields_by_id(
    #     self, user_id: int, selected_fields: dict[Any, dict[Any, dict]]
    # ):
    #     return self.base_repo.read(user_id)
    #
    # def get_user_by_email(self, email: str):
    #     return self.base_repo.get_user_by_email(email)
    #
    # def get_user_by_username(self, username: str):
    #     return self.base_repo.get_user_by_username(username)

    async def create_user(self, user_data: UserCreateDTO):
        return await self.base_repo.create(user_data)
