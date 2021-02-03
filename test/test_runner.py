import json

import pytest
import tornado.httpclient

from demo import config, runner, schemas


@pytest.mark.usefixtures("init")
class TestDemoRunner:
    @pytest.mark.gen_test
    async def test_demo_simple_run(
            self, http_client, base_url, input_schema):
        event_handler = runner.EventHandler.get_instance()

        # Initial run without any data
        await event_handler._run_once()

        # Upload location data
        request = tornado.httpclient.HTTPRequest(
            base_url + "/events",
            method="POST",
            headers={"X-Auth-Token": config.POST_SECRET},
            body=input_schema.json().encode("utf-8"))
        response = await http_client.fetch(request)
        assert response.code == 200
        assert json.loads(response.body)["result"] == "success"
        assert len(event_handler._events_queue) == 10
        assert event_handler.total_events_received == 10
        assert all(isinstance(e, schemas.output.EventV1)
                   for e in event_handler._events_queue)

        # Second run with actual data
        await event_handler._run_once()
        assert len(event_handler._events_queue) == 0
        assert len(event_handler._events_queue) == 0
        assert event_handler.total_events_received == 0
