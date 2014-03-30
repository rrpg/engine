# -*- coding: utf-8 -*-
import gettext
import core.config

try:
    _ = gettext.translation('message', core.config.localesDir).ugettext
except IOError:
    _ = gettext.translation('message', core.config.localesDir, languages=['en_GB']).ugettext
