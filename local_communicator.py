import os
import sys
import socket
import uuid
import json
from multiprocessing import Pool

from repository import Repository
from neighbor import NeighborList


class LocalCommunicator(object):
    def __init__(self, socket_path: str, repository: Repository, neighbors: NeighborList, search_ip: str, search_port: int):
        self.__local_socket = socket.socket(
            socket.AF_UNIX, socket.SOCK_SEQPACKET)
        try:
            self.__local_socket.bind(socket_path)
        except OSError as e:
            if e.errno == 98:
                os.remove(socket_path)
                self.__local_socket.bind(socket_path)
        self.__local_socket.listen(1024)

        self.__search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__search_ip = search_ip
        self.__search_port = search_port

        self.__r = repository
        self.__n = neighbors

    def __call__(self):
        self.run()

    def run(self):
        while True:
            ctl_socket, _ = self.__local_socket.accept()
            buff: list = ctl_socket.recv(1024).decode('utf8').split()
            print(buff)
            if buff[0] == '$Search':
                filename = str(buff[1])
                timeout = float(buff[2])

            import autoport
            sentry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            port = autoport.get_available_port(
                ip=self.__search_ip, protocol='udp', start_from=self.__search_port)
            sentry_address = (self.__search_ip, port)
            print(sentry_address)
            sentry_socket.bind(sentry_address)
            sentry_socket.settimeout(timeout)

            data = json.dumps({
                'filename': filename,
                'timeout': timeout,
                'query_id': uuid.uuid4().hex,
                'sentry_address': sentry_address,
            }).encode()
            address = (self.__search_ip, self.__search_port)
            self.__search_socket.sendto(data, address)
            try:
                result, _ = sentry_socket.recvfrom(1024)
            except socket.timeout:
                ctl_socket.send(b'timeout')
                continue
            ctl_socket.send(result)


if __name__ == '__main__':
    search_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    communicator = LocalCommunicator(
        'test/communicator.socket', Repository('repository'),
        NeighborList('neighbors'), '127.0.0.1', 10000
    )
    communicator()
    pass
