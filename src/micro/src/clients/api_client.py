import asyncio
import logging

import grpc

from langbot.common import port_map
from langbot.common import common_pb2
from langbot.common.micro.api import app_pb2_grpc


async def run() -> None:
    async with grpc.aio.insecure_channel(f"localhost:{port_map.Port.API_SERVICE}") as channel:
        stub = app_pb2_grpc.AppManagerStub(channel)
        response = await stub.Hello(common_pb2.GenericRequest())
    print("Greeter client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    asyncio.run(run())
