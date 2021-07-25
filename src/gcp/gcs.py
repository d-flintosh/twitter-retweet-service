import json

from google.api_core.exceptions import NotFound
from google.cloud.storage import Client


class Gcs:
    def __init__(self, bucket: str):
        self.client = Client(project='sports-data-service')
        self.bucket = self.client.bucket(bucket)

    def read_as_dict(self, url: str) -> dict:
        try:
            blob = self.bucket.blob(url)
            contents = blob.download_as_bytes().decode('utf-8')
            return json.loads(contents)
        except NotFound as e:
            return {}

    def write(self, url: str, contents: dict):
        blob = self.bucket.blob(url)
        blob.upload_from_string(json.dumps(contents))
