import argparse as ap
import json
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
    if args.daemon:
        raise NotImplementedError()

    cfg = DaemonConfig()
    if args.config:
        path = args.config
        with open(path, 'r') as fp:
            cfg.__dict__ = json.load(fp)
    if args.server_ip:
        cfg.set_ip(args.server_ip)
    if args.server_port:
        cfg.set_port(args.server_port)
    if args.neighbor_list:
        cfg.set_neig(args.neighbor_list)
    if args.repository:
        cfg.set_repo(args.repository)

    daemon = Daemon(cfg)
    daemon()


if __name__ == '__main__':
    main()
