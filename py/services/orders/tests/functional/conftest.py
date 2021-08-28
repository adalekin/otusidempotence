import base64
import json

import pytest


@pytest.fixture()
def user_id():
    return 123


@pytest.fixture()
def user_jwt_payload(user_id):
    return base64.b64encode(json.dumps({"user_id": user_id}).encode("utf-8"))
