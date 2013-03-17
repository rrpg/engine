# -*- coding: utf8 -*-


def read(prompt):
    try:
        s = raw_input(prompt)
    except NameError:
        s = input(prompt)

    return s
