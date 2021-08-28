import importlib
import logging
import sys

import connexion

import connexion_buzz

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from . import settings
from .extensions import cache

__all__ = ["create_app"]

logging.basicConfig(level=logging.INFO)


def create_app(settings_override=None):
    app = connexion.App(__name__, specification_dir="./spec/", options={"swagger_ui": False}, debug=settings.DEBUG)
    app.add_api("openapi.yaml", validate_responses=True)

    application = app.app
    application.config.from_object(settings)

    if settings_override:
        application.config.update(settings_override)

    app.add_error_handler(connexion_buzz.ConnexionBuzz, connexion_buzz.ConnexionBuzz.build_error_handler())

    # Initialize extensions/add-ons/plugins.

    sentry_sdk.init(integrations=[FlaskIntegration()], **application.config.get("SENTRY_CONFIG", {}))

    # Initialize the cache
    cache.init_app(application, config=application.config)

    return application
