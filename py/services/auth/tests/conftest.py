import pytest

TEST_DATABASE_URI = f"sqlite://"


@pytest.fixture(scope="session", autouse=True)
def app(request):
    from auth.application import create_app

    settings_override = {"TESTING": True, "CACHE_TYPE": "simple"}
    app = create_app(settings_override)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
