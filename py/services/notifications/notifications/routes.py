from .views import liveness


def setup_routes(app):
    app.router.add_get("/liveness/", liveness)
