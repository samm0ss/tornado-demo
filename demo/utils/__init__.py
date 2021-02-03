import datetime
import logging

import pytz

from . import logutil

logger = logging.getLogger(__name__)
__all__ = ["logutil"]


def now_with_timezone(tz=pytz.utc):
    return datetime.datetime.utcnow().\
        replace(microsecond=0).\
        replace(tzinfo=pytz.utc).\
        astimezone(tz)


class Singleton:
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_instance()
        return cls._instance

    @classmethod
    def get_assert_instance(cls):
        assert cls._instance is not None
        return cls._instance

    @classmethod
    def _create_instance(cls):
        return cls()
