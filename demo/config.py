import enum
import os

import tornado.netutil
import tornado.options

ENVIRONMENT = None
POST_SECRET = None


class Env(enum.Enum):
    LIVE = "LIVE"
    DEVELOPMENT = "DEVELOPMENT"


def init(environment: str, post_secret: str):
    global ENVIRONMENT, POST_SECRET
    ENVIRONMENT = Env(environment)
    POST_SECRET = post_secret


def server_config():
    assert ENVIRONMENT
    tornado.options.define(
        "serve_world",
        default=ENVIRONMENT == Env.LIVE,
        help="if false, only serves on localhost", type=bool)

    tornado.options.define(
        "httpport", default=int(str(os.environ.get("PORT", 3000))),
        help="The port the webserver will run on", type=int)
