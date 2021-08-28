import asyncio

import aiohttp
import aiohttp_jinja2
import jinja2

from .middlewares import setup_middlewares
from .routes import setup_routes
from .source.kafka import KafkaNotificationSource


async def on_startup(app):
    kafka_notification_source = KafkaNotificationSource()
    app["kafka_notification_source"] = asyncio.create_task(kafka_notification_source.run())


async def on_shutdown(app):
    app["kafka_notification_source"].cancel()
    await app["kafka_notification_source"]


def init_app():
    app = aiohttp.web.Application()

    # Setup Jinja2 template renderer
    aiohttp_jinja2.setup(app, loader=jinja2.PackageLoader("notifications"))

    # Setup views and routes
    setup_routes(app)
    setup_middlewares(app)

    # Initialize
    app.on_startup.append(on_startup)

    # Graceful shutdown
    app.on_shutdown.append(on_shutdown)

    return app


app = init_app()
