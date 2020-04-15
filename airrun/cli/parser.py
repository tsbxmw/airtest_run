# -*- coding: utf-8 -*-
import argparse
from airrun.report.report import get_parger as report_parser


def get_parser():
    ap = argparse.ArgumentParser()
    subparsers = ap.add_subparsers(dest="action", help="version/run/info/report")
    # subparser version
    subparsers.add_parser("version", help="show version and exit")
    # subparser run
    ap_run = subparsers.add_parser("run", help="run script")
    runner_parser(ap_run)
    # subparser info
    ap_info = subparsers.add_parser("info", help="get & print author/title/desc info of script")
    ap_info.add_argument("script", help="script filename")
    # subparser report
    ap_report = subparsers.add_parser("report", help="generate report of script")
    report_parser(ap_report)
    return ap


def runner_parser(ap=None):
    if not ap:
        ap = argparse.ArgumentParser()
    ap.add_argument("--package", help="package name", default="com.**.*****", nargs="?")
    ap.add_argument("--apk", help="apk package path", default="./apk/**.apk", nargs="?")
    ap.add_argument("--install", help="install apk from file or not", default=False, nargs="?")
    ap.add_argument("--uninstall", help="uninstall apk or not", default=False, nargs="?")
    ap.add_argument("--device", help="Android Device", default="", nargs="?")
    return ap
