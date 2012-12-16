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

import optparse, logging, sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cctv.detect")
import cctv, cctv.image

def main():
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-V", "--version", dest="version", action="store_true",
                      help="print version of the program and quit", metavar="FILE", default=False)
#        parser.add_option("-o", "--out", dest="outfile",
#                          help="Filename where processed image is saved", metavar="FILE", default="merged.edf")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="debug", default=False,
                      help="switch to debug/verbose mode")
    (options, args) = parser.parse_args()
    if options.version:
        print("python cctv detect version %s" % cctv.version)
        sys.exit(0)
    if options.debug:
        logger.setLevel(logging.DEBUG)


    cctv.image.loop_delta()

if __name__ == "__main__":
    main()
