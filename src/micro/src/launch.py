#!/usr/bin/env python3
import argparse
from importlib.util import find_spec
import logging
import pathlib
import subprocess
import sys

LANGBOT_PATH = pathlib.Path(find_spec('langbot').submodule_search_locations[0]).parent


def main(args):
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    processes: dict = dict()

    processes['api_service'] = subprocess.Popen(
        args=[sys.executable, '-m', 'langbot.micro.api_service.manager'],
        cwd=LANGBOT_PATH,
    )

    logging.info('Langbot micro-services launched.')

    for _, process in processes.items():
        try:
            process.wait()
        except KeyboardInterrupt:
            logging.info(f'Process {process.args[2]} terminated by SIGNIT.')
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Launch micro-services.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    main(args=parser.parse_args())
