import uuid

from hamcrest import assert_that, equal_to, has_entries
from pytest_toolbelt import matchers

from users import settings


def test_users_utf8mb4(client, requests_mock, account_id):
    example_token = "000"

    first_name = "晓鹏"
    last_name = "郑"

    requests_mock.post(settings.AUTH_URL + "/jwt/encode/", json={"access_token": example_token})
    requests_mock.post(settings.BILLING_URL + "/accounts/", json={"id": account_id})

    response = client.post(
        "/register/",
        json={
            "email": f"test-{uuid.uuid4()}@example.com",
            "phone": "+0987654321",
            "first_name": first_name,
            "last_name": last_name,
            "password": None,
        },
    )

    assert_that(response, matchers.has_status(201))
    assert_that(
        response.data.decode(),
        matchers.is_json(has_entries(first_name=equal_to(first_name), last_name=equal_to(last_name))),
    )


def test_user_current_get(client, user, user_access_token, user_jwt_payload):
    user, _ = user

    response = client.get(
        "/user/",
        headers={"Authorization": f"Bearer {user_access_token}", "X-JWT-Payload": user_jwt_payload},
    )

    assert_that(response, matchers.has_status(200))
    assert_that(response.data.decode(), matchers.is_json(has_entries(id=equal_to(user["id"]))))


def test_user_current_update(client, user, user_access_token, user_jwt_payload):
    user, _ = user

    response = client.patch(
        "/user/",
        json={"first_name": "test"},
        headers={"Authorization": f"Bearer {user_access_token}", "X-JWT-Payload": user_jwt_payload},
    )

    assert_that(response, matchers.has_status(200))
    assert_that(response.data.decode(), matchers.is_json(has_entries(first_name=equal_to("test"))))


def test_users_get(client, user):
    user, _ = user

    response = client.get(f'/users/{user["id"]}/')

    assert_that(response, matchers.has_status(200))
    assert_that(response.data.decode(), matchers.is_json(has_entries(id=equal_to(user["id"]))))


def test_users_update(client, user):
    user, _ = user

    response = client.patch(f'/users/{user["id"]}/', json={"first_name": "test"})

    assert_that(response, matchers.has_status(200))
    assert_that(response.data.decode(), matchers.is_json(has_entries(first_name=equal_to("test"))))
