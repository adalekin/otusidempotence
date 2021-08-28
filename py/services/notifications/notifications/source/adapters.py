import aiohttp

from schemas.user import UserRegistered

from notifications import settings
from notifications.notificaiton import EmailNotification


def _users_api(path):
    return settings.USERS_URL + path


class WelcomeEmail(EmailNotification):
    session = aiohttp.ClientSession()

    async def __init__(self, event: UserRegistered):
        async with self.session.get(_users_api(f"/users/{event.user_id}/")) as resp:
            user = await resp.json()

            super().__init__(email=user["email"], subject="Welcome!", message="Yay! You're officially a user")
