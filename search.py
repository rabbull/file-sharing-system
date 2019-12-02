import os
import socket
import json
import multiprocessing
import threading

import autoport
from download import FileHost
from repository import Repository
from neighbor import NeighborList
from search_config import SearchControllerConfig


class SearchController(object):
    def __init__(self, cfg: SearchControllerConfig):
        self.__r = cfg.repository
        self.__n = cfg.neighbors

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((cfg.ip, cfg.port))
        self.__ip = cfg.ip
        self.__port = cfg.port

        self.__ignore_query_ids = []

    def __call__(self, *args, **kwargs):
        self.run()

    def run(self):
        while True:
            buff, _ = self.__socket.recvfrom(1024)
            print(buff)
            buff = json.loads(buff.decode())

            if buff['query_id'] in self.__ignore_query_ids:
                print(f'ignore {buff}')
                continue

            self.__ignore_query_ids.append(buff['query_id'])
            if len(self.__ignore_query_ids) > 1024:
                self.__ignore_query_ids.pop(0)
            result = self.__r.find(buff['filename'])

            # hit
            if result:
                if 'checksum' not in buff.keys() or buff['checksum'] == result.checksum:
                    host_port = autoport.get_available_port(self.__ip, self.__port, protocol='tcp')
                    host = FileHost(ip=self.__ip, port=host_port, repo_entry=result)
                    host_proc = multiprocessing.Process(target=host)
                    host_proc.start()
                    result = result.__dict__
                    result['address'] = (self.__ip, host_port)
                    self.__socket.sendto(json.dumps(result).encode(), tuple(buff['sentry_address']))
                    continue

            # miss
            search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for neighbor in self.__n.as_list():
                search_socket.sendto(json.dumps(buff).encode(), tuple(neighbor))


if __name__ == '__main__':
    search_controller_cfg = SearchControllerConfig('127.0.0.1', 10000, Repository('repository'),
                                                   NeighborList('neighbors'))
    search_controller = SearchController(cfg=search_controller_cfg)
    search_controller()
