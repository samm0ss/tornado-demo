from __future__ import annotations

import datetime
import typing

from pydantic import BaseModel


class EventV1(BaseModel):
    """
    Processed event (e.g normally anonymised)
    """
    id: str
    dt: datetime.datetime
    x: int
    y: int
    name: str


class Metrics(BaseModel):
    """
    Basic metrics of the service, can be used for monitoring
    """
    dt: datetime.datetime
    run_id: str
    total_events_received: int
    events_dropped: int


class OutputSchema(BaseModel):
    events: typing.Sequence[EventV1]
    version: typing.Literal[1]
    metrics: Metrics
