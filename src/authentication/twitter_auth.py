import json

from google.cloud import secretmanager_v1
from google.cloud.secretmanager_v1 import AccessSecretVersionRequest


def get_credentials() -> dict:
    client = secretmanager_v1.SecretManagerServiceClient()
    secret_request = AccessSecretVersionRequest({
        'name': 'projects/557888643787/secrets/twitter-automation-001/versions/latest'
    })
    secret = client.access_secret_version(request=secret_request)
    return json.loads(secret.payload.data.decode('UTF-8'))
