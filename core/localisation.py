# -*- coding: utf-8 -*-
import gettext
import core.config

def _(s):
	try:
		s = gettext.translation('message', core.config.localesDir).gettext(s)
	except IOError:
		s = gettext.translation('message', core.config.localesDir, languages=['en_GB']).gettext(s)

	return s
