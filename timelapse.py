#!/usr/bin/env python3
import os
import time
from datetime import datetime, timezone
from suntime import Sun, SunTimeException

# Setup Camera
quality = 100
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
    start_time = time.perf_counter()
    command = f'raspistill -w {width} -h {height} -q {quality} -awb greyworld '
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
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    if current_pic < amount:
        time.sleep(delay - elapsed_time)

print('Time lapse done!')
