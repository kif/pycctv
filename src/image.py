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
logger = logging.getLogger("cctv.image")
import cv
import numpy
from utils import timeit
import pylab
import time

class Image(object):
    """
    Main methods are:
    -grab()
    -normalize
    """
    binning_factor = 8
    shape = (768, 1024)
    camera = cv.CaptureFromCAM(0)
    cv.SetCaptureProperty(camera, cv.CV_CAP_PROP_FRAME_WIDTH, shape[1])
    cv.SetCaptureProperty(camera, cv.CV_CAP_PROP_FRAME_HEIGHT, shape[0])
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8)
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
    def __init__(self):
        """
        """
        self.timestamp = None
        self.time_tuple = None
        self.raw_array = None
        self.frame = None
        self.normalized = None
        self.grey_array = None
        self.mean = None
        self.std = None
        self.thumb = None
    def __repr__(self):
        if self.frame:
            return "Image with shape %s taken at %s"(self.raw_array.shape, time.asctime(time.gmtime(self.timestamp)))
        else:
            return "empty Image"
    @timeit
    def grab(self):
        self.frame = cv.QueryFrame(self.camera)
        size = cv.GetSize(self.frame)
        self.shape = size[1], size[0]  # self.shape != self.__class__.shape
        self.timestamp = time.time()
        self.raw_array = numpy.fromstring(self.frame.tostring(), dtype="uint8")
        self.raw_array.shape = self.shape[0], self.shape[1], -1
        if self.raw_array.shape[-1] == 1:
            self.grey_array = self.raw_array[:, :, 0].astype(numpy.float32)
        elif self.raw_array.shape[-1] == 3:
            self.grey_array = numpy.float32(0.2126) * self.raw_array[:, :, 0] + \
                              numpy.float32(0.7152) * self.raw_array[:, :, 1] + \
                              numpy.float32(0.0722) * self.raw_array[:, :, 2]

    @timeit
    def binning(self, factor=None):
        if factor is None:
            factor = self.binning_factor
        if self.grey_array is None:
            self.grab()
        npa = self.grey_array.copy()
        npa.shape = self.shape[0] // factor, factor, self.shape[1] // factor, factor
        self.thumb = npa.sum(axis= -1).sum(axis=1) / (factor * factor)
        self.mean = self.thumb.mean()
        self.std = self.thumb.std()

    def delta(self, other):
        if self.mean is None:
            self.binning()
        return


    def show(self, what="RGB"):


        pylab.ion()
        if self.raw_array.shape[-1] not in [3, 4]:
            what = "L"
        if what == "RGB":
            pylab.imshow(self.raw_array)
        elif what == "L":
            # show grey image
            pylab.imshow(self.grey_array, cmap="gray")
        else:
            cv.ShowImage('Camera', self.frame)
