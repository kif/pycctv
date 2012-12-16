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
__date__ = "16/12/2012"
__status__ = "devel"


import cctv, cctv.image

def main():

    cctv.image.loop_delta()

if __name__ == "__main__":
    main()
