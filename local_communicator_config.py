from neighbor import NeighborList
from repository import Repository


class LocalCommunicatorConfig(object):
    def __init__(self, socket_path: str, repository: Repository, neighbors: NeighborList, search_ip: str,
                 search_port: int):
        self.__socket_path = socket_path
        self.__repository = repository
        self.__neighbors = neighbors
        self.__search_addr = (search_ip, search_port)

    @property
    def socket_path(self):
        return self.__socket_path

    @property
    def repository(self):
        return self.__repository

    @property
    def neighbors(self):
        return self.__repository

    @property
    def search_ip(self):
        return self.__search_addr[0]

    @property
    def search_port(self):
        return self.__search_addr[1]

    @property
    def search_address(self):
        return self.__search_addr
