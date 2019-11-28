import socket


def get_available_port(ip: str = '127.0.0.1', start_from: int = 1024, end_at: int = 65535, protocol: str = 'tcp'):
    assert start_from > 0
    assert end_at < 65536
    assert protocol in {'tcp', 'udp'}
    socket_type = socket.SOCK_DGRAM if protocol == 'udp' else socket.SOCK_STREAM
    s = socket.socket(socket.AF_INET, socket_type)
    for port in range(start_from, end_at + 1):
        try:
            s.bind((ip, port))
        except:
            continue
        s.close()
        return port
    return None


if __name__ == '__main__':
    port = get_available_port('192.168.3.36', 1080, 1200)
    print(port)
    port = 1080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.3.36', port))
    while True:
        print(s.recv(1024))
        input()
