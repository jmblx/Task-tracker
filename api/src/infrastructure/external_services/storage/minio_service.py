
import boto3
from botocore.client import Config

from config import MinIOConfig
from domain.services.storage.storage_service import StorageServiceInterface


class MinIOService(StorageServiceInterface):
    def __init__(self, config: MinIOConfig):
        self.config = config
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=config.endpoint_url,
            aws_access_key_id=config.access_key,
            aws_secret_access_key=config.secret_key,
            config=Config(signature_version="s3v4"),
        )

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
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=filename,
                Body=content,
                ContentType=content_type,
            )
            return f"{self.config.endpoint_url}/{bucket_name}/{filename}"
        except Exception as e:
            raise Exception(f"Ошибка при загрузке файла в MinIO: {e!s}")
