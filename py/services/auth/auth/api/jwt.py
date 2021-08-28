import datetime

from authlib.common.security import generate_token
from authlib.jose import jwt

import connexion

from auth import settings
from auth.extensions import cache


def encode(encode_data):
    header = {"alg": "RS256"}
    payload = {"iss": encode_data["iss"], "sub": encode_data["sub"], "jti": generate_token(36), **encode_data["payload"]}

    access_token = jwt.encode(header, payload, settings.JWT_PRIVATE_KEY).decode("utf-8")

    cache.set(payload["jti"], "false", int(datetime.timedelta(**settings.JWT_REFRESH_LIFESPAN).total_seconds()))

    return {"access_token": access_token}


def blacklist(token):
    claims = jwt.decode(token["access_token"], settings.JWT_PUBLIC_KEY)

    cache.set(claims["jti"], "true", int(datetime.timedelta(**settings.JWT_REFRESH_LIFESPAN).total_seconds()))

    return connexion.NoContent, 200
