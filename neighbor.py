import os
import sys
import json

import fcntl


class NeighborList(object):
    class Entry(object):
        def __init__(self, ip, port):
            self.ip = ip
            self.port = port

        def as_dict(self):
            return {
                'ip': self.ip,
                'port': self.port,
            }

        def __str__(self):
            return json.dumps(self.as_dict())

        def __getitem__(self, key):
            if key == 'ip':
                return self.ip
            elif key == 'port':
                return self.port
            else:
                raise KeyError()

        def __getattr__(self, key):
            return self.__getitem__(key)

        def __setattr__(self, key, value):
            if key == 'ip':
                self.ip = value
            elif key == 'port':
                self.port = value
            else:
                raise KeyError()

    def __init__(self, neighbor_list_path: str):
        if not os.path.isfile(neighbor_list_path):
            raise FileNotFoundError()
        self.__path = neighbor_list_path

    def __write(self, neighbors: list):
        content = json.dumps(neighbors)
        fd = open(self.__path, 'w')
        fcntl.lockf(fd, fcntl.LOCK_EX)
        fd.write(content)
        fcntl.lockf(fd, fcntl.LOCK_UN)
        fd.close()

    def __read(self):
        fd = open(self.__path, 'r')
        fcntl.lockf(fd, fcntl.LOCK_EX)
        content = fd.read()
        fcntl.lockf(fd, fcntl.LOCK_UN)
        fd.close()
        return json.loads(content)

    def as_list(self):
        return self.__read()

    def add_entry(self, ip: str, port: int):
        neighbors = self.__read()
        if [ip, port] in neighbors:
            return
        neighbors.append([ip, port])
        self.__write(neighbors)

    def __str__(self):
        return json.dumps(self.as_list())

    def __getitem__(self, key: int):
        return key


if __name__ == '__main__':
    neighbor_list = NeighborList(sys.argv[1])
    neighbor_list.add_entry('127.0.0.1', 1024)
    neighbor_list.add_entry('127.0.0.1', 1998)
    neighbor_list.add_entry('127.0.0.1', 1111)
