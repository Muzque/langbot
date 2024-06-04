import asyncio
import logging
import threading

from langbot.common import port_map
from langbot.common import signaler


class Service:
    GRACE_STOP_TIME: int = 5  # secs

    def __init__(self, tag: port_map.Port):
        self.tag = tag
        self.server = None
        self.stopping = False
        signaler.Signaler().atexit(handler=self.atexit_handler)

    async def stop_server(self):
        await self.server.stop(grace=self.GRACE_STOP_TIME)

    def atexit_handler(self):
        if self.server is None:
            return
        if not self.stopping:
            self.stopping = True
            logging.info('Stopping service: %s, waiting for 5 secs' % self.tag.name)
            # TODO: Grace shutdown
            loop = asyncio.get_event_loop()
            loop.close()


def set_cancel_event(context):
    cancel_event = threading.Event()

    def on_rpc_cancel():
        cancel_event.set()

    context.add_callback(on_rpc_cancel)

    return cancel_event
