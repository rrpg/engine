# -*- coding: utf-8 -*-

values = dict()


def get(key):
	if key in values.keys():
		return values[key]

	return None

def set(key, value):
	values[key] = value
