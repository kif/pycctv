#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Project: Closed Circuit TeleVision for Python
#             https://github.com/kif/pycctv
#
__author__ = "Jérôme Kieffer"
__contact__ = "Jerome.Kieffer@terre-adelie.org"
__license__ = "GPLv3+"
__copyright__ = "Jérôme Kieffer"
__date__ = "15/12/2012"
__status__ = "devel"

import logging
import time
import sys
logger = logging.getLogger("cctv.utils")
timelog = logging.getLogger("cctv.timeit")

if sys.platform != "win32":
    WindowsError = RuntimeError

def timeit(func):
    def wrapper(*arg, **kw):
        '''This is the docstring of timeit:
        a decorator that logs the execution time'''
        t1 = time.time()
        res = func(*arg, **kw)
        timelog.warning("%s took %.3fs" % (func.func_name, time.time() - t1))
        return res
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper
