import asyncio
import logging

from langbot.common import port_map
from langbot.common import service
from langbot.common.micro.api import app_pb2_grpc
from langbot.micro.shared import utils
from langbot.micro.api_service.interfaces import app_servicer


class ApiService(service.Service):
    def __init__(self, tag: port_map.Port):
        super().__init__(tag=tag)
        self.server = utils.create_grpc_server(workers=32)
        self.app_servicer = app_servicer.AppServicer()
        app_pb2_grpc.add_AppManagerServicer_to_server(
            self.app_servicer,
            self.server,
        )
        self.server.add_insecure_port('[::]:{}'.format(port_map.Port.get(self.tag)))


async def serve():
    logging.info('Start the api service.')
    server = ApiService(tag=port_map.Port.API_SERVICE).server
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve())
