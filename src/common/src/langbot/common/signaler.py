import atexit
import signal as signal_module

from langbot.common import singleton


class Signaler(metaclass=singleton.Singleton):
    def __init__(self):
        self.handlers = {}
        self.atexit_handlers = {}

    def __handler(self, sig_num, frame):
        if sig_num in self.handlers:
            for handler in reversed(self.handlers[sig_num]):
                handler(sig_num, frame)

    def __atexit_handler(self, sig_num, _0):
        if sig_num in self.atexit_handlers:
            for handler in reversed(self.atexit_handlers[sig_num]):
                handler()

    def signal(
        self,
        sig_nums: tuple = (signal_module.SIGTERM, signal_module.SIGINT),
        handler=None,
    ):
        if not handler:
            return
        if isinstance(sig_nums, tuple):
            sig_nums = list(sig_nums)
        elif isinstance(sig_nums, str):
            sig_nums = [sig_nums]
        for sig_num in sig_nums:
            handlers = self.handlers.setdefault(sig_num, [])
            if not handlers:
                signal_module.signal(sig_num, self.__handler)
            if handler not in handlers:
                handlers.append(handler)

    def atexit(
        self,
        sig_nums: tuple = (signal_module.SIGTERM, signal_module.SIGINT),
        handler=None,
    ):
        if not handler:
            return
        atexit.register(handler)
        if isinstance(sig_nums, tuple):
            sig_nums = list(sig_nums)
        elif isinstance(sig_nums, str):
            sig_nums = [sig_nums]
        for sig_num in sig_nums:
            handlers = self.atexit_handlers.setdefault(sig_num, [])
            if handler not in handlers:
                handlers.append(handler)

        self.signal(sig_nums, self.__atexit_handler)
