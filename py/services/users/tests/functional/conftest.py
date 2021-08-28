import base64
import json
import uuid

import pytest
from hamcrest import assert_that
from pytest_toolbelt import matchers

from users import settings


@pytest.fixture()
def user_access_token():
    return "123"

@pytest.fixture()
def account_id():
    return "123"

@pytest.fixture()
def user(client, requests_mock, user_access_token, account_id):
    requests_mock.post(settings.AUTH_URL + "/jwt/encode/", json={"access_token": user_access_token})
    requests_mock.post(settings.BILLING_URL + "/accounts/", json={"id": account_id})

    password = "1234567890"

    response = client.post(
        "/register/",
        json={
            "email": f"test-{uuid.uuid4()}@example.com",
            "first_name": "晓鹏",
            "last_name": "郑",
            "password": password,
        },
    )

    assert_that(response, matchers.has_status(201))

    return (response.json, password)


@pytest.fixture()
def user_jwt_payload(user):
    user, _ = user

    return base64.b64encode(json.dumps({"user_id": user["id"]}).encode("utf-8"))
