#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import sys
import getopt

def main(argv):
    # shortOptions = 'v:i:'
    shortOptions = 'l:'
    longOptions = ('login=', 'password=')

    # handle command-line parameters
    try:
        options, action = getopt.getopt(argv, shortOptions, longOptions)
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    login = ''
    password = ''

    for opt, arg in options:
        if opt == '--login':
            login = arg
        if opt == '--password':
            password = arg

    print login
    print password
    print action

if __name__ == "__main__":
    main(sys.argv[1:])
