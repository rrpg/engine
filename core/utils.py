# -*- coding: utf-8 -*-


def read(prompt):
	try:
		s = raw_input(prompt)
	except NameError:
		s = input(prompt)

	return unicode(s, "utf-8")
