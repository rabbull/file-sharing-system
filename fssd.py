import argparse as ap
from daemon import Daemon
from daemon_config import DaemonConfig


def main():
    parser = ap.ArgumentParser()
    parser.add_argument('-d', '--daemon', action='store_true', help='run in daemon mode')
    parser.add_argument('-c', '--config', metavar='PATH', type=str)
    parser.add_argument('-s', '--server-ip', metavar='IP', type=str)
    parser.add_argument('-p', '--server-port', metavar='PORT', type=int)
    parser.add_argument('--neighbor-list', metavar='PATH', type=str)
    parser.add_argument('--repository', metavar='PATH', type=str)

    args = parser.parse_args()
    print(args)

if __name__ == '__main__':
    main()
