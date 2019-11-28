import socket
import argparse as ap

import threading

from daemon_config import DaemonConfig
from neighbor import NeighborList
from repository import Repository
from local_communicator import LocalCommunicator

BUFSIZE = 1024


class Daemon(object):
    def __init__(self, cfg: DaemonConfig):
        print(cfg.__dict__)
        self.__ip = cfg.ip
        self.__port = cfg.port
        self.__addr = (self.__ip, self.__port)
        self.__neighbor_list = NeighborList(cfg.neighbor_list_path)
        self.__repository = Repository(cfg.repository_path)

    def __call__(self, *args, **kwargs):
        self.start(*args, **kwargs)

    def start(self):
        communicator = LocalCommunicator('/tmp/fss.socket', self.__repository, self.__neighbor_list)
        local_communicator_thread = threading.Thread(target=communicator)
        local_communicator_thread.start()
        local_communicator_thread.join()
