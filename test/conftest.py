import logging

import pytest
import tornado.httpclient
import tornado.httpserver
import tornado.web

from demo import config, runner, schemas, server, utils

logger = logging.getLogger()


@pytest.fixture
def input_schema():
    return schemas.input.InputSchema(
        events=[schemas.input.EventV1(
            id="id",
            dt=utils.now_with_timezone(),
            record=schemas.input.Record(x=i, y=i, name="name")
        ) for i in range(0, 10)])


@pytest.fixture
def app():
    app = server.make_app({"autoreload": False})
    return app


@pytest.fixture
def http_client(request, http_server):
    """Get an asynchronous HTTP client.
    """
    client = tornado.httpclient.AsyncHTTPClient(
        force_instance=True, defaults=dict(validate_cert=False))

    def _close():
        client.close()

    request.addfinalizer(_close)
    return client


@pytest.fixture
def base_url(request):
    return 'http://localhost:%s' % request.getfixturevalue('http_port')


@pytest.fixture(scope="function")
def init():
    config.init("DEVELOPMENT", "mysupertestsecret")
    runner.EventHandler.get_instance()
    yield
    runner.EventHandler._instance = None
