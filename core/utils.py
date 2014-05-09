# -*- coding: utf-8 -*-


def read(prompt): # pragma: no cover
	try:
		s = raw_input(prompt)
	except NameError:
		s = input(prompt)

	return s
