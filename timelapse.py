#!/usr/bin/env python3
import os
from datetime import datetime, timezone
from suntime import Sun, SunTimeException
from time import sleep

# Setup Camera
width = 1920
height = 1080
amount = 1440
delay = 60
current_pic = 0
folder_path = '/media/extusb/timelapse'
# Setup Night Exposure
latitude = 61.49
longitude = 23.76
sun = Sun(latitude, longitude)

if not os.path.isdir(folder_path):
    os.mkdir(folder_path)

while current_pic < amount:
    command = f'raspistill -w {width} -h {height} -awb greyworld '
    night = False
    try:
        sunrise = sun.get_sunrise_time()
        sunset = sun.get_sunset_time()
        now = datetime.now(timezone.utc)
        if now < sunrise or now > sunset:
            command += '-ex night '
            night = True
    except SunTimeException as e:
        print('Can\'t determine sunrise or sunset')
    filename = f'{folder_path}/{current_pic:08}.jpg'
    command += f'-o {filename}'
    os.system(command)
    current_pic += 1
    timestamp = f'{datetime.now():[%H:%M:%S %d.%m.%Y]}'
    print(f'{timestamp} Captured picture {current_pic}/{amount} Night exposure: {night}')
    if current_pic < amount:
        sleep(delay)

print('Time lapse done!')
