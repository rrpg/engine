import gettext
import config

_ = gettext.translation('message', config.localesDir).gettext
