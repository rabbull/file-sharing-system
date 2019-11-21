import socket
import argparse as ap

from daemon_config import DaemonConfig

BUFSIZE = 1024

class Daemon(object):
    def __init__(self, cfg: DaemonConfig):
        self.__ip = cfg.ip
        self.__port = cfg.port
        self.__repo = cfg.repository_path
        self.__neig = cfg.neighbor_list_path
    
    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.__ip, self.__port))
        while True:
            message, (client_ip, client_port) = sock.recvfrom(BUFSIZE)
            print(message, client_ip, client_port)
