#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys, getopt
from Rpg import Rpg
from argparse import ArgumentParser

def main(argv):
    # shortOptions = 'v:i:'
    shortOptions = 'l:'
    longOptions = ('login=', 'password=')

    parser = ArgumentParser()

    parser.add_argument(
        "-l", "--login",
        dest="login", help="Player login",metavar="LOGIN"
    )
    parser.add_argument(
        "-p", "--password",
        dest="password", help="Player password", metavar="PASSWORD"
    )
    parser.add_argument(
        "action",
        metavar="A", nargs='*', help="Action to execute"
    )

    args = parser.parse_args()

    rpg = Rpg(args.login, args.password, args.action)

if __name__ == "__main__":
    main(sys.argv[1:])
