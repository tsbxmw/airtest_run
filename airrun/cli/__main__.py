# -*- coding: utf-8 -*-
import sys

from airrun.cli.parser import get_parser, check_runner_args


def main(argv=None):
    ap = get_parser()
    args = ap.parse_args(argv)
    if args.action == "info":
        from airrun.cli.info import infos
        print(infos)
    elif args.action == "report":
        from airrun.report.report import main as report_main
        report_main(args)
    elif args.action == "run":
        from airrun.main import main as runner
        if not check_runner_args(args):
            ap.print_help()
            sys.exit(-1)
        runner(args)
    elif args.action == "version":
        from airrun.utils.version import show_version
        show_version()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
