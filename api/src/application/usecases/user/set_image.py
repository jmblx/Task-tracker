from uuid import UUID

from application.dtos.set_image import ImageDTO
from domain.services.storage.storage_service import StorageServiceInterface
from domain.services.user.user_service_interface import UserServiceInterface


class SetAvatarUseCase:
    def __init__(
        self,
        user_service: UserServiceInterface,
        minio_service: StorageServiceInterface,
    ):
        self.user_service = user_service
        self.minio_service = minio_service

    async def __call__(
        self,
        user_id: UUID,
        image: ImageDTO,
    ) -> str:
        pathfile = await self.minio_service.set_avatar(
            bucket_name="users",
            filename=image.filename,  # Формирование названия файла можно оставить на бизнес-логику
            content=image.content,
            content_type=image.content_type,
        )
        await self.user_service.update_by_fields(
            search_params={"id": user_id}, upd_data={"pathfile": pathfile}
        )
        return pathfile
