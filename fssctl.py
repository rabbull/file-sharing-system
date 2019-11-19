import argparse as ap


def fssctl():
    command_parser = ap.ArgumentParser()
    group = command_parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--config', action='store_true')
    group.add_argument('-s', '--search', action='store_true')
    group.add_argument('-d', '--daemon', action='store_true')

    args = command_parser.parse_args()
    if args.config:
        raise NotImplementedError()
    elif args.search:
        raise NotImplementedError()
    elif args.daemon:
        raise NotImplementedError()
    else:
        command_parser.print_usage()
        return 1


if __name__ == '__main__':
    exit(fssctl())
