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

import os
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
    font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 8)
    cv.NamedWindow('Camera', cv.CV_WINDOW_AUTOSIZE)
    cascade = cv.Load('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
    last = "last.jpg"
    def __init__(self, filename=None):
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
        if filename and os.path.isfile(filename):
            self.frame = cv.LoadImage(filename, cv.CV_LOAD_IMAGE_COLOR)
            self.timestamp = time.time()
    def __repr__(self):
        if self.frame:
            return "Image with shape %s taken at %s" % (self.raw_array.shape, time.asctime(time.gmtime(self.timestamp)))
        else:
            return "empty Image"
#    @timeit
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

#    @timeit
    def binning(self, factor=None):
        if factor is None:
            factor = self.binning_factor
        if self.grey_array is None:
            self.grab()
        npa = self.grey_array.copy()
        npa.shape = self.shape[0] // factor, factor, self.shape[1] // factor, factor
        self.thumb = npa.sum(axis= -1).sum(axis=1) / (factor * factor)
        self.mean = self.thumb.mean()
        self.std = numpy.sqrt(((self.thumb - self.mean) ** 2).mean())
        self.thumb /= self.std
        self.thumb -= self.mean / self.std - 1

    def delta(self, other, threshold=0.1):
        if self.mean is None:
            self.binning()
        if other.mean is None:
            other.binning()
        if self.mean <= 1 and other.mean < 1:
            # if the signal is very low ...
            return 0
        return (abs(other.thumb - self.thumb) > threshold).sum()

    def tag(self):
        """
        Put date/time on image
        """
        cv.PutText(self.frame, time.asctime(time.localtime(self.timestamp)), (self.shape[1] // 2 , self.shape[0] - 50), self.font, 255)

    def save(self, filename=None):
        if filename is None:
            # millisec precision
            filename = time.strftime("%Y%m%d-%Hh%Mm%S", time.localtime(self.timestamp)) + str(self.timestamp % 1)[1:5] + ".jpg"
        cv.SaveImage(filename, self.frame)
        if os.path.islink(self.last):
            os.unlink(self.last)
        os.symlink(filename, self.last)

    @timeit
    def detect_face(self):
        if self.frame is None:
            self.grab()
        # create grayscale version
        if self.frame.nChannels == 3:
            grayscale = cv.CreateImage(cv.GetSize(self.frame), 8, 1)
            cv.CvtColor(self.frame, grayscale, cv.CV_BGR2GRAY)
        else:
            grayscale = self.frame
        cv.EqualizeHist(grayscale, grayscale)

        faces = cv.HaarDetectObjects(grayscale, self.cascade, cv.CreateMemStorage(), 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (50, 50))

        if faces:
            logger.warning('%i faces detected!' % len(faces))
#        for i, j in faces:
#            print i, j
#            cv.Rectangle(image, (int(i[0]), int(i[1])),
#                         (int(i[0] + i[2]), int(i[1] + i[3])),
#                         (0, 255, 0), 3, 8, 0)
        return faces

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

def loop_face():
    print("Face detection from camera loop")
    while 1:
        t0 = time.time()
        i = Image()
        i.grab()
        if i.detect_face():
            i.tag()
            i.save()
            print("Frame rate: %.1f" % (1 / (time.time() - t0)))

def loop_delta(count=3, thres=0.1):
    print("Image variation detection from camera loop")
    last = Image()
    last.grab()
    while 1:
        t0 = time.time()
        i = Image()
        i.grab()
        if last.delta(i, thres) > count:
            i.tag()
            i.save()
            print("Frame rate: %.1f" % (1 / (time.time() - t0)))
        last = i


