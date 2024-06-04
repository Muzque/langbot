import enum
from typing import Any

PORT_BASE = 50051


class PortAuto(int, enum.Enum):
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        if last_values:
            return last_values[-1] + 1
        return PORT_BASE


class Port(PortAuto):
    API_SERVICE = enum.auto()

    @classmethod
    def get(cls, port_enum) -> int:
        return port_enum.value
