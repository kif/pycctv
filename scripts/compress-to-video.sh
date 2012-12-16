#!/bin/sh
video=$(date +"%Y%m%d-%Hh%Mm%S.avi")
mencoder -ovc lavc -o $video mf://*.jpg