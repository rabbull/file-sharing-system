from neighbor import NeighborList
from repository import Repository


class SearchControllerConfig(object):
    def __init__(self, ip: str, port: int, repository: Repository, neighbors: NeighborList):
        super(SearchControllerConfig, self).__init__()
        self.__ip = ip
        self.__port = port
        self.__repo = repository
        self.__neig = neighbors

    @property
    def ip(self):
        return self.__ip

    @property
    def port(self):
        return self.__port

    @property
    def repository(self):
        return self.__repo

    @property
    def neighbors(self):
        return self.__neig

