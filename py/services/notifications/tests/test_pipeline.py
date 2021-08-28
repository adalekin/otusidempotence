import pytest

from notifications.pipeline import Pipeline


@pytest.mark.asyncio
async def test_pipeline_await(notification_queue):
    await Pipeline(queue=notification_queue).run_nowait()
