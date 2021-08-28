import enum
import pickle
import time

import redis
from flask import _request_ctx_stack, abort, request

try:
    from uwsgi import async_sleep as sleep
except ImportError:
    try:
        from gevent import sleep
    except ImportError:
        from time import sleep


class IdempotencyRequestStatus(str, enum.Enum):
    in_progress = "in_progress"
    complete = "complete"


class Idempotency:
    def __init__(self, app=None):
        self.app = app
        self.redis = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        self.app.config.setdefault("REDIS_URL", "redis://")
        self.app.config.setdefault("IDEMPOTENCY_REQUEST_TIMEOUT", 60)
        self.app.config.setdefault("IDEMPOTENCY_KEY_HTTP_HEADER", "X-Idempotency-Key")
        self.app.config.setdefault("IDEMPOTENCY_KEY_PREFIX", "idempotency_")
        self.app.config.setdefault("IDEMPOTENCY_KEY_EXPIRE", 240)

        self.redis = redis.StrictRedis.from_url(self.app.config.get("REDIS_URL"))

        self.app.before_request(self._before_request)
        self.app.after_request(self._after_request)

    def _get_redis_keys(self, idempotency_key):
        return (
            f'{self.app.config.get("IDEMPOTENCY_KEY_PREFIX")}{idempotency_key}_status',
            f'{self.app.config.get("IDEMPOTENCY_KEY_PREFIX")}{idempotency_key}_response',
        )

    def _init_idempotency_request(self, idempotency_key):
        redis_key_status, _ = self._get_redis_keys(idempotency_key)

        return (
            self.redis.set(
                redis_key_status,
                IdempotencyRequestStatus.in_progress,
                nx=True,
                ex=self.app.config.get("IDEMPOTENCY_KEY_EXPIRE"),
            )
            is True
        )

    def _update_idempotency_request(self, idempotency_key, status):
        redis_key_status, _ = self._get_redis_keys(idempotency_key)

        self.redis.set(redis_key_status, status, ex=self.app.config.get("IDEMPOTENCY_KEY_EXPIRE"))

    def _get_idempotency_status(self, idempotency_key):
        redis_key_status, _ = self._get_redis_keys(idempotency_key)
        return IdempotencyRequestStatus[self.redis.get(redis_key_status).decode("utf-8")]

    def _get_idempotency_response(self, idempotency_key):
        _, redis_key_response = self._get_redis_keys(idempotency_key)

        pickled_response = self.redis.get(redis_key_response)
        return pickle.loads(pickled_response)

    def _set_idempotency_response(self, idempotency_key, response):
        _, redis_key_response = self._get_redis_keys(idempotency_key)
        self.redis.set(redis_key_response, pickle.dumps(response), ex=self.app.config.get("IDEMPOTENCY_KEY_EXPIRE"))

    def _before_request(self):
        idempotency_key = request.headers.get(self.app.config.get("IDEMPOTENCY_KEY_HTTP_HEADER"))

        if not idempotency_key:
            return

        ctx = _request_ctx_stack.top
        setattr(ctx, "idempotency_key", idempotency_key)

        if self._init_idempotency_request(idempotency_key):
            return

        endtime = time.time() + self.app.config.get("IDEMPOTENCY_REQUEST_TIMEOUT")
        status = IdempotencyRequestStatus.in_progress

        while time.time() < endtime:
            status = self._get_idempotency_status(idempotency_key)

            if status == IdempotencyRequestStatus.complete:
                break

            sleep(1)

        if status == IdempotencyRequestStatus.in_progress:
            abort(408)

        return self._get_idempotency_response(idempotency_key)

    def _after_request(self, response):
        ctx = _request_ctx_stack.top

        if ctx is not None and hasattr(ctx, "idempotency_key"):
            self._set_idempotency_response(idempotency_key=ctx.idempotency_key, response=response)
            self._update_idempotency_request(
                idempotency_key=ctx.idempotency_key, status=IdempotencyRequestStatus.complete
            )

        return response
