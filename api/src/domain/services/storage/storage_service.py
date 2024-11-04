from abc import ABC, abstractmethod


class StorageServiceInterface(ABC):
    @abstractmethod
    async def set_avatar(
        self,
        bucket_name: str,
        filename: str,
        content: bytes,
        content_type: str,
    ) -> str:
        """
        Загружает файл в указанный бакет.

        :param bucket_name: Название бакета
        :param filename: Имя файла в бакете
        :param content: Содержимое файла в байтах
        :param content_type: MIME-тип содержимого файла
        :return: URL загруженного файла
        """
