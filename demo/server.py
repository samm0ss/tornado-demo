import logging

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from demo import handlers

logger = logging.getLogger(__name__)


class SiteNotFoundHandler(tornado.web.RequestHandler):
    def head(self):
        self.set_status(404)
        self.write("This site does not exist")

    def get(self):
        self.set_status(404)
        self.write("This site does not exist")

    def post(self):
        self.set_status(404)
        self.write("This site does not exist")

    def delete(self):
        self.set_status(404)
        self.write("This site does not exist")

    def patch(self):
        self.set_status(404)
        self.write("This site does not exist")

    def put(self):
        self.set_status(404)
        self.write("This site does not exist")

    def options(self):
        self.set_status(404)
        self.write("This site does not exist")


class VersionSiteHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("VERSION")


def make_app(settings: dict):
    default_settings = {
        "compress_response": True,
    }
    default_settings.update(settings)
    app = tornado.web.Application(
        [(r"/.*", SiteNotFoundHandler, {})],
        **default_settings)  # type: ignore

    app.add_handlers(
        r".*", [
            ("/version", VersionSiteHandler, {}),
            ("/events", handlers.PostEventsHandler, {}),
        ]
    )
    return app


def make_server(app):
    return tornado.httpserver.HTTPServer(app, decompress_request=True)


def start_server():
    server = make_server(make_app({}))
    port = tornado.options.options.httpport
    if tornado.options.options.serve_world:
        logger.info("Listening to port %d on %s", port)
        server.bind(port, "0.0.0.0")
    else:
        logger.info("Listening to port %d on localhost only", port)
        server.bind(port)
    server.start()
