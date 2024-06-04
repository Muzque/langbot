import sys
from concurrent import futures

import grpc


def get_funcname() -> str:
    return sys._getframe(1).f_code.co_name


def create_grpc_server(
    workers: int,
    send_buffer: int = 64,
    receive_buffer: int = 64,
    max_concurrent_rpcs: int = None,
) -> grpc.aio.server:
    return grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=workers),
        maximum_concurrent_rpcs=max_concurrent_rpcs,
        options=[
            ('grpc.max_send_message_length', send_buffer * 1024 * 1024),
            ('grpc.max_receive_message_length', receive_buffer * 1024 * 1024),
        ],
    )


def create_grpc_channel(
    addr: str,
    send_buffer: int = 64,
    receive_buffer: int = 64,
) -> grpc.insecure_channel:
    return grpc.insecure_channel(
        addr,
        options=[
            ('grpc.max_send_message_length', send_buffer * 1024 * 1024),
            ('grpc.max_receive_message_length', receive_buffer * 1024 * 1024),
        ],
    )
