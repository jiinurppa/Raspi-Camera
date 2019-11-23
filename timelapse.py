#!/usr/bin/env python3
import os
import math
from datetime import datetime, timezone
from suntime import Sun
from time import sleep

# Setup Camera
width = 1920;
height = 1080;
amount = 1440;
delay = 60;
current_pic = 0;
folder_path = '/media/exfat/first';
# Setup Night Exposure
latitude = 61.49;
longitude = 23.76;
sun = Sun(latitude, longitude);

if not os.path.isdir(folder_path):
    os.mkdir(folder_path);

while current_pic < amount:
    sunrise = sun.get_sunrise_time();
    sunset = sun.get_sunset_time();
    now = datetime.now(timezone.utc);
    command = 'raspistill -w ' + str(width) + ' -h ' + str(height) + ' -awb greyworld ';
    night = False;
    if now < sunrise or now > sunset:
        command += '-ex night ';
        night = True;
    filename = folder_path + '/' + '{0:0>8d}'.format(current_pic) + '.jpg';
    command += '-o ' + filename;
    os.system(command);
    current_pic += 1;
    timestamp = datetime.now().strftime('[%H:%M:%S %d.%m.%Y]');
    print(timestamp + ' Captured picture ' + str(current_pic) + '/' + str(amount) + ' Night Exposure: ' + str(night));
    sleep(delay);

print('Time lapse done!');
