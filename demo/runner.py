from __future__ import annotations

import asyncio
import datetime
import logging
import typing as t
import uuid

from demo import schemas
from demo import utils

logger = logging.getLogger(__name__)

# Max queue size is to prevent the current process to run out of memory
MAX_QUEUE_SIZE: int = 100000
MAX_BATCH_SIZE: int = 20000
UPLOAD_FREQUENCY: datetime.timedelta = datetime.timedelta(seconds=20)


class EventHandler(utils.Singleton):
    """
    Very minimal implementation of event handler that forwards the received
    events to another service.
    """
    _instance = None

    def __init__(self):
        self._events_queue: t.MutableSequence[schemas.input.EventV1] = []
        self.run_id: str = str(uuid.uuid4())
        self.total_events_received: int = 0
        self.events_dropped: int = 0

    async def _run_once(self):
        # TODO: Refresh other api integrations/services
        await self.upload_events()

    async def run_until_crash(self):
        while True:
            try:
                await self._run_once()
                await asyncio.sleep(UPLOAD_FREQUENCY.total_seconds())
            except Exception as e:
                logger.exception("Exception: %s", e)
                await asyncio.sleep(10)

    def append_to_queue(
            self, events: t.Sequence[schemas.output.EventV1]) -> None:
        # TODO: Drop events if queue is larger than MAX_QUEUE_SIZE
        self._events_queue += events
        self.total_events_received += len(events)

    def popleft_from_queue(
            self, max_items: int) -> t.Sequence[schemas.output.EventV1]:
        """
        First in First out
        """
        events = self._events_queue[:max_items]
        del self._events_queue[:max_items]
        return events

    async def upload_events(self) -> None:
        """
        Upload received events to another service
        """
        upload_object = schemas.output.OutputSchema(
            version=1,
            events=self.popleft_from_queue(max_items=MAX_QUEUE_SIZE),
            metrics=schemas.output.Metrics(
                dt=utils.now_with_timezone(),
                run_id=self.run_id,
                total_events_received=self.total_events_received,
                events_dropped=self.events_dropped)
        )
        try:
            logger.info("uploading %d records", len(upload_object.events))
            print(upload_object.json())  # noqa
            # TODO: Forward the requests here to another service
        except Exception:
            # TODO: Implement retry and exception handling
            raise
        else:
            # Refresh the metrics after successful upload
            self.total_events_received = 0
            self.events_dropped = 0
