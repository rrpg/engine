# -*- coding: utf-8 -*-
from tests.commands import *
import unittest

if __name__ == "__main__":
	testsuite = unittest.TestLoader().discover('.')
	unittest.TextTestRunner(verbosity=1).run(testsuite)
