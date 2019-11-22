import socket
import argparse as ap

from daemon_config import DaemonConfig
from neighbor import NeighborList
from repository import Repository

BUFSIZE = 1024

class Daemon(object):
    def __init__(self, cfg: DaemonConfig):
        self.__ip = cfg.ip
        self.__port = cfg.port
        self.__addr = (self.__ip, self.__port)
        self.__neighbor_list = NeighborList(cfg.neighbor_list_path)
        self.__repository = Repository(cfg.repository_path)
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(self.__addr)
        while True:
            message, (client_ip, client_port) = sock.recvfrom(BUFSIZE)
            print(message, client_ip, client_port)
