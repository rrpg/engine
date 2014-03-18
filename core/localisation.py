import gettext
import core.config

_ = gettext.translation('message', core.config.localesDir).gettext
