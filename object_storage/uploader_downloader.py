from minio import Minio
from minio.error import S3Error
import io
from dotenv import dotenv_values
from datetime import timedelta

config = dotenv_values(".env")


class Objectstorage:
    def __init__(self, bucket_name: str):
        self.client = Minio(

            endpoint=config["ENDPOINT"],
            access_key=config["ACCESS_KEY"],
            secret_key=config["SECRET_KEY"],
            secure=False
        )
        self.bucket = bucket_name

    def make_bucket(self, bucket_name):
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)
        else:
            return

    def upload(self, object_name: str, object_file):
        try:
            self.client.put_object(self.bucket, object_name, data=io.BytesIO(object_file), length=-1,
                                   part_size=10 * 1024 * 1024)
        except S3Error as exc:
            raise exc

    def download(self, object_name: str):
        try:
            self.client.stat_object(self.bucket, object_name, ssec=None, version_id=None, extra_query_params=None)

            return self.client.presigned_get_object(self.bucket, object_name, expires=timedelta(days=7),
                                                    response_headers=None, request_date=None, version_id=None,
                                                    extra_query_params=None)

        except S3Error:
            return None