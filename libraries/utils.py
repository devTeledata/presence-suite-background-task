import base64
from google.auth import transport
import google.oauth2.id_token


def decode_base64(data):
    return base64.b64decode(data)


def encode_base64(data):
    return base64.b64encode(data)


def generate_token(service_url) -> str:
    """
    Genarate id token for authentication service to service using container Service account
    """
    auth_req = transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)

    return id_token
