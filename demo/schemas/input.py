from __future__ import annotations

import datetime
import typing

from pydantic import BaseModel


class Record(BaseModel):
    x: int
    y: int
    name: str


class EventV1(BaseModel):
    """
    Input event received from webhook
    """
    id: str
    dt: datetime.datetime
    record: Record


class InputSchema(BaseModel):
    events: typing.Sequence[EventV1]
