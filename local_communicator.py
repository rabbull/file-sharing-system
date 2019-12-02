import os
import socket
import uuid
import json

from local_communicator_config import LocalCommunicatorConfig
from repository import Repository
from neighbor import NeighborList


class LocalCommunicator(object):
    def __init__(self, cfg: LocalCommunicatorConfig):
        self.__local_socket = socket.socket(
            socket.AF_UNIX, socket.SOCK_SEQPACKET)
        try:
            self.__local_socket.bind(cfg.socket_path)
        except OSError as e:
            if e.errno == 98:
                os.remove(cfg.socket_path)
                self.__local_socket.bind(cfg.socket_path)
        self.__local_socket.listen(1024)

        self.__search_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__search_ip = cfg.search_ip
        self.__search_port = cfg.search_port

        self.__r = cfg.repository
        self.__n = cfg.neighbors

    def __call__(self):
        self.run()

    def run(self):
        while True:
            ctl_socket, _ = self.__local_socket.accept()
            buff: list = ctl_socket.recv(1024).decode('utf8').split()
            if buff[0] == '$Search':
                self.search(ctl_socket, buff)
            elif buff[0] == '$Repository':
                self.repository(ctl_socket, buff)
            elif buff[0] == '$Neighbor':
                self.neighbor(ctl_socket, buff)

    def neighbor(self, ctl_socket: socket.socket, buff: list):
        if buff[1] == 'List':
            neighbors = self.__n.as_list()
            ctl_socket.send(json.dumps([f'{n[0]}:{n[1]}' for n in neighbors]).encode())
        elif buff[1] == 'Add':
            try:
                ip, port = buff[2].split(':')
                self.__n.add_entry(ip, port)
            except Exception as e:
                ctl_socket.send(f'failed: {e}'.encode())
                return
            ctl_socket.send(b'done.')
        else:
            raise NotImplementedError()

    def repository(self, ctl_socket: socket.socket, buff: list):
        if buff[1] == 'List':
            entries = self.__r.as_list()
            ctl_socket.send(json.dumps([e.__dict__ for e in entries]).encode())
        elif buff[1] == 'Add':
            try:
                self.__r.add_entry(buff[2])
            except Exception as e:
                ctl_socket.send(f'failed: {str(e)}'.encode())
                return -1
            ctl_socket.send(b'done.')
        elif buff[0] == 'Remove':
            raise NotImplementedError()
        else:
            raise SyntaxError()

    def search(self, ctl_socket: socket.socket, buff: list):
        filename = str(buff[1])
        timeout = float(buff[2])

        import autoport
        sentry_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        port = autoport.get_available_port(ip=self.__search_ip, protocol='udp', start_from=self.__search_port)
        sentry_address = (self.__search_ip, port)
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
            sentry_socket.close()
            return
        sentry_socket.close()
        ctl_socket.send(result)


if __name__ == '__main__':
    search_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    communicator_cfg = LocalCommunicatorConfig('/tmp/fss.socket', Repository('repository'),
                                               NeighborList('neighbors'), '127.0.0.1', 10000)
    communicator = LocalCommunicator(communicator_cfg)
    communicator()
    pass
