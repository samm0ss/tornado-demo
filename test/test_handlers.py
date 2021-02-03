import json

import pytest
import tornado.httpclient

from demo import config, schemas, runner


@pytest.mark.usefixtures("init")
class TestHandlers:
    @pytest.mark.gen_test
    async def test_post_events(self, http_client, base_url, input_schema):
        event_handler = runner.EventHandler.get_instance()
        request = tornado.httpclient.HTTPRequest(
            base_url + "/events",
            method="POST",
            headers={"X-Auth-Token": config.POST_SECRET},
            body=input_schema.json().encode("utf-8"))
        response = await http_client.fetch(request)
        assert response.code == 200
        assert json.loads(response.body)["result"] == "success"
        assert len(event_handler._events_queue) == 10
        assert all(
            isinstance(e, schemas.output.EventV1)
            for e in event_handler._events_queue)

    @pytest.mark.gen_test
    async def test_post_events_missing_secret(
            self, http_client, base_url, input_schema):
        request = tornado.httpclient.HTTPRequest(
            base_url + "/events",
            method="POST",
            headers={},
            body=input_schema.json().encode("utf-8"))
        response = await http_client.fetch(request, raise_error=False)
        assert response.code == 403
        assert response.reason == "Forbidden"

    @pytest.mark.gen_test
    async def test_post_events_incorrect_secret(
            self, http_client, base_url, input_schema):
        request = tornado.httpclient.HTTPRequest(
            base_url + "/events",
            method="POST",
            headers={"X-Auth-Token": "INCORRECT"},
            body=input_schema.json().encode("utf-8"))
        response = await http_client.fetch(request, raise_error=False)
        assert response.code == 403
        assert response.reason == "Forbidden"

    @pytest.mark.gen_test
    async def test_post_events_incorrect_body(self, http_client, base_url):
        incorrect_input_schema = {"events": [{"id": 1, "x": 1}]}
        request = tornado.httpclient.HTTPRequest(
            base_url + "/events",
            method="POST",
            headers={"X-Auth-Token": config.POST_SECRET},
            body=json.dumps(incorrect_input_schema).encode("utf-8"))
        response = await http_client.fetch(request, raise_error=False)
        assert response.code == 422
        assert response.reason == "Invalid body"

    @pytest.mark.gen_test
    async def test_base_path(self, http_client, base_url):
        request = tornado.httpclient.HTTPRequest(
            base_url + "/",
            method="POST",
            body=b"")
        response = await http_client.fetch(request, raise_error=False)
        assert response.code == 404
