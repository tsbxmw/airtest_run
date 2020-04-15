# -*- coding: utf-8 -*-
from airrun.cli.parser import get_parser


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
        runner(args)
    elif args.action == "version":
        from airrun.utils.version import show_version
        show_version()
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
