import datetime

from hamcrest import *

import pytest

from pytest_toolbelt import matchers

from users import settings


def test_auth_login(client, user, requests_mock):
    example_token = "000"
    user, password = user

    credentials = {"email": user["email"], "password": password}

    requests_mock.post(settings.AUTH_URL + "/jwt/encode/", json={"access_token": example_token})

    response = client.post("/login/", json=credentials)

    assert_that(response, matchers.has_status(200))
    assert_that(
        response.data.decode(),
        matchers.is_json(has_entries(access_token=equal_to(example_token))),
    )


def test_auth_login_failed(client):
    credentials = {"email": "test@example.com", "password": "1234567890"}

    response = client.post("/login/", json=credentials)
    assert_that(response, matchers.has_status(401))


def test_auth_logout(client, user_access_token, user_jwt_payload, requests_mock):
    requests_mock.post(settings.AUTH_URL + "/jwt/blacklist/", status_code=204)

    response = client.post(
        "/logout/", headers={"Authorization": f"Bearer {user_access_token}", "X-JWT-Payload": user_jwt_payload}
    )
    assert_that(response, matchers.has_status(204))
