import json
import os
import socket

from repository import Repository


class FileHost(object):
    BUFFER_SIZE = 16

    def __init__(self, ip: str, port: int, repo_entry: Repository.Entry, timeout: int = 1200):
        super(FileHost, self).__init__()
        self.__host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__host.bind((ip, port))
        self.__host.listen(1)
        self.__host.settimeout(timeout)
        self.__entry = repo_entry
        self.__timeout = timeout

    def __call__(self, *args, **kwargs):
        self.run()

    def run(self):
        try:
            client, client_addr = self.__host.accept()
        except socket.timeout:
            return 1

        meta = {
            'name': self.__entry.basename,
            'size': self.__entry.size,
            'buffer_size': self.BUFFER_SIZE,
        }
        print(meta)
        client.send(json.dumps(meta).encode())
        try:
            print(client.recv(1024))
        except socket.timeout:
            return 1

        f = open(self.__entry.path, 'rb+')
        remain = self.__entry.size
        while remain > 0:
            data = f.read(self.BUFFER_SIZE)
            n = client.send(data)
            remain -= n
        f.close()

    def __del__(self):
        self.__host.close()


class FileClient(object):
    def __init__(self, host_ip: str, host_port: int, save_path: str):
        self.__host_addr = (host_ip, host_port)
        self.__save_path = save_path
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __call__(self, *args, **kwargs):
        self.run()

    def run(self):
        print(type(self.__host_addr), self.__host_addr)
        self.__client.connect(self.__host_addr)

        meta = json.loads(self.__client.recv(102400))
        self.__client.send(b'meta received!')
        size = meta['size']
        name = meta['name']
        buffer_size = meta['buffer_size']
        if os.path.isdir(self.__save_path):
            path = os.path.join(self.__save_path, name)
        else:
            path = self.__save_path
        downloaded = 0
        f = open(path, 'wb')
        while downloaded < size:
            data = self.__client.recv(buffer_size)
            n = f.write(data)
            downloaded += n
            print(f'{downloaded}/{size} downloaded.')
        f.close()


if __name__ == '__main__':
    repo = Repository('/home/karl/Documents/file-sharing-system/repository')
    port = 11111
    import sys
    if sys.argv[1] == 'host':
        host = FileHost(ip='127.0.0.1', port=port, repo_entry=repo.as_list()[0])
        host.run()
    elif sys.argv[1] == 'client':
        client = FileClient(host_ip='127.0.0.1', host_port=port, save_path='..')
        client.run()
