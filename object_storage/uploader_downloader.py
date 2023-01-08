from minio import Minio
from minio.error import S3Error
import io
from dotenv import dotenv_values


# config = dotenv_values(".env")

class Objectstorage:
    def __init__(self, bucket_name: str):
        self.client = Minio(
            endpoint="localhost:9000",
            access_key="4hTBLuRu0wRU9izO",
            secret_key="lSbP4pq3ME5f6BBnmvbyT2A91wgawLFu",
            secure=False
        )
        self.bucket = bucket_name

    def upload(self, object_name: str, sum_life):
        try:
            self.client.put_object(self.bucket, object_name, data=io.BytesIO(sum_life), length=-1,
                                   part_size=10 * 1024 * 1024)
        except S3Error as exc:
            print("error occurred.", exc)

    def download(self, object_name):
        try:
            result = self.client.get_object(self.bucket, object_name).data.decode('ascii')
        except S3Error as exc:
            print("error occurred.", exc)
        return result
