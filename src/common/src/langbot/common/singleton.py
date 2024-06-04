"""Provides a singleton definition via metaclass."""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Provides a code routine to provide/create instances."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]
