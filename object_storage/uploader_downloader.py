from minio import Minio
from minio.error import S3Error
import io
from dotenv import dotenv_values

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

    def upload(self, object_name: str, sum_life):

        self.client.put_object(self.bucket, object_name, data=io.BytesIO(sum_life), length=-1,
                               part_size=10 * 1024 * 1024)

    def download(self, object_name: str):
        try:
            data = self.client.get_object(self.bucket, object_name)
            with open(object_name, 'wb') as file_data:
                for d in data.stream(32 * 1024):
                    file_data.write(d)
        except S3Error as exc:
            raise exc

        # try:
        #     res = self.client.get_object(self.bucket, object_name)
        #     return res.read()
        #
        # except S3Error as exc:
        #     raise exc
