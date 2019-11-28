import socket
import argparse as ap

import multiprocessing

from daemon_config import DaemonConfig
from neighbor import NeighborList
from repository import Repository
import autoport
from local_communicator import LocalCommunicator
from search import SearchController

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
        searcher_port = autoport.get_available_port(
            ip=self.__ip, start_from=self.__port + 1, protocol='udp')
        searcher = SearchController(
            self.__ip, searcher_port, self.__repository, self.__neighbor_list)
        communicator = LocalCommunicator(
            '/tmp/fss.socket', self.__repository, self.__neighbor_list, self.__ip, searcher_port)

        processes = []
        processes.append(multiprocessing.Process(target=searcher))
        processes.append(multiprocessing.Process(target=communicator))
        
        for p in processes:
            print(p)
            p.start()
        for p in processes:
            p.join()
