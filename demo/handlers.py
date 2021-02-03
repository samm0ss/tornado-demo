import json
import logging

import tornado.web
import pydantic

from demo import config, runner
from demo import schemas

logger = logging.getLogger(__name__)


class InvalidSecretApiError(tornado.web.HTTPError):
    pass


class ApiError(tornado.web.HTTPError):
    def __init__(self, reason: str):
        super().__init__(422, reason=reason)


class PostEventsHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def prepare(self):
        secret = self.request.headers.get("X-Auth-Token", None)
        if secret != config.POST_SECRET:
            raise InvalidSecretApiError(403, "Invalid secret")
        assert secret == config.POST_SECRET
        super().prepare()

    def post(self):
        data = json.loads(self.request.body.decode("utf-8"))
        try:
            input_schema = schemas.input.InputSchema.parse_obj(data)
        except pydantic.ValidationError:
            raise ApiError("Invalid body")
        event_handler = runner.EventHandler.get_assert_instance()
        output_events = [
            schemas.output.EventV1(
                id=event.id,
                dt=event.dt,
                name=event.record.name,
                x=event.record.x,
                y=event.record.y)
            for event in input_schema.events]
        event_handler.append_to_queue(output_events)
        self.write(json.dumps({"result": "success"}))

    def write_error(self, status_code, **kwargs):
        # TODO: monitor failed requests
        super().write_error(status_code, **kwargs)
