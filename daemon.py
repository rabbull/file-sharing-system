import socket
import argparse as ap

import multiprocessing

from daemon_config import DaemonConfig
from local_communicator_config import LocalCommunicatorConfig
from neighbor import NeighborList
from repository import Repository
import autoport
from local_communicator import LocalCommunicator
from search import SearchController
from search_config import SearchControllerConfig


class Daemon(object):
    BUFFER_SIZE = 1024
    LOCAL_COMMUNICATOR_SOCKET_FILE_PATH = '/tmp/fss.socket'

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
        searcher_port = autoport.get_available_port(ip=self.__ip, start_from=self.__port + 1, protocol='udp')
        searcher_cfg = SearchControllerConfig(self.__ip, searcher_port, self.__repository, self.__neighbor_list)
        searcher = SearchController(searcher_cfg)

        communicator_cfg = LocalCommunicatorConfig(socket_path=self.LOCAL_COMMUNICATOR_SOCKET_FILE_PATH,
                                                   repository=self.__repository, neighbors=self.__neighbor_list,
                                                   search_ip=self.__ip, search_port=searcher_port)
        communicator = LocalCommunicator(communicator_cfg)

        processes = [
            multiprocessing.Process(target=searcher),  # search controller
            multiprocessing.Process(target=communicator),  # local communicator
        ]

        for p in processes:
            p.start()
        for p in processes:
            p.join()
