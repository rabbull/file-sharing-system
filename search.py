import os
import socket
import json

from repository import Repository
from neighbor import NeighborList


class SearchController(object):
    def __init__(self, ip: str, port: int, repository: Repository, neighbors: NeighborList):
        self.__r = repository
        self.__n = neighbors

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__socket.bind((ip, port))
        self.__ip = ip
        self.__port = port

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
                    self.__socket.sendto(f'hit: {result.__dict__}'.encode(), tuple(buff['sentry_address']))
                    continue

            # miss
            search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            for neighbor in self.__n.as_list():
                search_socket.sendto(json.dumps(buff).encode(), tuple(neighbor))


if __name__ == '__main__':
    search_controller = SearchController('127.0.0.1', 10000, Repository('repository'), NeighborList('neighbors'))
    search_controller()
