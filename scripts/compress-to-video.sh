#!/bin/sh
video=$(date +"%Y%m%d-%Hh%Mm%S.avi")
mencoder -ovc x264 -o $video mf://*.jpg