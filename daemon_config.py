import json
import os

DEFAULT_ROOT=os.path.join(os.environ['HOME'], '.fss')
DEFAULT_REPOSITORY=os.path.join(DEFAULT_ROOT, 'repo')
DEFAULT_NEIGHBOR_LIST=os.path.join(DEFAULT_ROOT, 'neighbor')


class DaemonConfig(object):
    def self_check(self):
        def __is_valid_ip(ip: str):
            address = ip.strip().split('.')
            if not len(address) == 4:
                return False
            for i in range(4):
                field = address[i]
                try:
                    field = int(field)
                except:
                    return False
                return 256 > field > int(i == 0)
        
        def __is_valid_port(port: int):
            return 65536 > port > 0
        
        if not __is_valid_ip(self.ip):
            raise SyntaxError('ip')
        if not __is_valid_port(self.port):
            raise SyntaxError('port')

    def __init__(self, ip='127.0.0.1', port=11000, repository_path=DEFAULT_REPOSITORY, neighbor_list_path=DEFAULT_NEIGHBOR_LIST):
        self.__ip = ip
        self.__port = port
        self.__repo_path = repository_path
        self.__neig_path = neighbor_list_path
        self.self_check()
    
    def load(self, path: str):
        with open(path, 'r') as f:
            res = json.load(f)
        self.__ip = res['ip']
        self.__port = int(res['port'])
        self.__repo_path = res['repository']
        self.__neig_path = res['neighbor']
        self.self_check()

    def as_dict(self):
        return {
            'ip': self.__ip,
            'port': self.__port,
            'repository': self.repository_path,
            'neighbor': self.neighbor_list_path,
        }

    def set_ip(self, ip: str):
        self.__ip = ip
        self.self_check()
    
    def set_port(self, port: int):
        self.__port = port
        self.self_check()

    @property
    def ip(self):
        return self.__ip
    
    @property
    def port(self):
        return self.__port
    
    @property
    def repository_path(self):
        return self.repository_path
    
    @property
    def neighbor_list_path(self):
        return self.neighbor_list_path


if __name__ == '__main__':
    config = DaemonConfig()
    config.load('/mnt/c/Users/Karl/Documents/file-sharing-system/daemon/daemon.conf')
    print(config.as_dict())
