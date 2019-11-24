import os
import sys
import json
import argparse as ap

from daemon_config import DaemonConfig

def fssctl_main():
    command_parser = ap.ArgumentParser()
    group = command_parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--config', action='store_true')
    group.add_argument('-s', '--search', action='store_true')

    args = command_parser.parse_args()
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[:2])
        sys.argv.remove(sys.argv[1])
    if args.config:
        config_main()
    elif args.search:
        search_main()
    else:
        command_parser.print_usage()
        exit(-1)


def config_main():
    raise NotImplementedError()

def search_main():
    argparser = ap.ArgumentParser()
    argparser.add_argument('-c', '--config', metavar='PATH')
    argparser.add_argument('--neighbor-list', metavar='PATH')
    argparser.add_argument('-n', '--name', metavar='FILENAME')

    args = argparser.parse_args()
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[1])
        sys.argv.remove(sys.argv[1])
    
    cfg = DaemonConfig()
    if args.config:
        with open(args.config, 'r') as fp:
            cfg.__dict__ = json.load(fp)


if __name__ == '__main__':
    fssctl_main()
