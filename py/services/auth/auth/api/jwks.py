from authlib.jose import JsonWebKey

from auth import settings


def jwks():
    jwk = JsonWebKey.import_key(settings.JWT_PUBLIC_KEY, {"kty": "RSA"})
    return {"keys": [jwk.as_dict(add_kid=True)]}
