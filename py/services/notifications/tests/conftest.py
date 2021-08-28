import asyncio

import pytest

from notifications.notificaiton import EmailNotification


@pytest.fixture
async def notification_queue():
    queue = asyncio.Queue()
    await queue.put(EmailNotification(email="example@example.com", subject="Test", message="Test message"))

    return queue
