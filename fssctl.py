import os
import sys
import argparse as ap

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
    elif args.daemon:
        daemon.main()
    else:
        command_parser.print_usage()
        exit(1)


if __name__ == '__main__':
    fssctl_main()
