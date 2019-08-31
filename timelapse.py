#!/usr/bin/env python
import os
import math
from picamera import PiCamera
from time import sleep
from fractions import Fraction

# Setup
width = 1920;
height = 1080;
amount = 1440;
hold = 4;
current_pic = 0;
folder_path = "/media/exfat/timelapse";

if not os.path.isdir(folder_path):
    os.mkdir(folder_path);

while current_pic < amount:
    camera = PiCamera();
    camera.resolution = (width, height);
    sleep(hold);
    camera.capture(folder_path + "/" + '{0:0>4d}'.format(current_pic) + ".jpg");
    camera.close();
    current_pic += 1;
    print("Captured picture " + str(current_pic) + "/" + str(amount));
    sleep(60 - hold);

print("Time lapse done!");
