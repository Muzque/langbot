import logging

from langbot.common import common_pb2
from langbot.common.micro.api import app_pb2_grpc
from langbot.micro.shared import utils


class AppServicer(app_pb2_grpc.AppManagerServicer):

    async def Hello(self, request, context):
        logging.info(f'RPC {utils.get_funcname()}: {request}')

        response = common_pb2.GenericResponse(message='hello world')
        return response
