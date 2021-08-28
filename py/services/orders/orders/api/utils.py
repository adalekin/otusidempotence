import base64
import json


def idempotency_key_read_from_header(request):
    return request.headers.get("Idempotency-Key")


def jwt_read_from_header(request):
    token = None
    payload = None

    token_string = request.headers.get("Authorization")

    if token_string:
        _, _, token = token_string.partition(" ")

    payload_string = request.headers.get("X-JWT-Payload")

    if payload_string:
        payload = json.loads(base64.b64decode(payload_string + "=" * ((4 - len(payload_string) % 4) % 4)))

    return token, payload
