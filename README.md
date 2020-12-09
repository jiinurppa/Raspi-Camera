# Raspi-Camera
Notes for Raspbian &amp; Raspberry Pi Camera Module. Tested on **Raspberry Pi 3 B+**.
- [Setup](https://www.raspberrypi.org/documentation/configuration/camera.md)
- [Tech Specs](https://www.raspberrypi.org/documentation/hardware/camera/README.md)
- [Commands](https://www.raspberrypi.org/documentation/raspbian/applications/camera.md)

## Watch Live Feed
Requirements: `mplayer` or `mpv` (for desktop)

1. From **desktop** run either
   1. `nc -l 8111 | mpv --no-correct-pts --fps=30 --no-audio -` or
   2. `nc -l 8111 | mplayer -fps 30 -vf scale=1920:1080 -nosound -cache 4096 -`
2. From **Raspberry Pi** run either
   1. `pi_camera_server.py` (instructions in file) or
   2. `raspivid -t 0 -w 1920 -h 1080 -fps 30 -o - | nc desktop-ip-here 8111` (replace `desktop-ip-here` with correct IP)

❗ Get desktop IP with:
* Linux: `hostname -I`
* macOS: `ipconfig getifaddr en0` (ethernet) or `ipconfig getifaddr en1` (wifi)


## Record Time Lapse Using `raspistill`
Requirements: External drive for pictures, `screen`, `ffmpeg`

These notes are for the **NoIR** module. If you're using a regular camera, remove the `-awb greyworld` option.

❗ I suggest disabling leds on the Raspberry Pi so you don't accidentally get reflections of them on camera:
* Disable **red** PWR led by running `sudo sh -c 'echo 0 > /sys/class/leds/led1/brightness'`
* Disable **green** ACT led by running `sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'`


1. Install [SunTime](https://github.com/SatAgro/suntime) by running `pip3 install suntime`
2. Create mount point for external drive with `sudo mkdir /media/exfat`
3. Mount your external drive by running `sudo mount -t auto /dev/sda1 /media/exfat`
4. Save the following script as `timelapse.py` or download it with `wget https://raw.githubusercontent.com/jiinurppa/Raspi-Camera/master/timelapse.py`:
```python
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
```
5. Change `latitude` and `longitude` to match your location
6. Make script executable by running `chmod u+x timelapse.py`
7. Start screen by running `screen -S timelapse`
8. Run script with `./timelapse.py`
9. Detach from screen with `Ctrl-a` + `d` and let the script run in the background
10. Check the progress by running `screen -r timelapse`, when it's done you should see `Time lapse done!`
11. Exit screen with `exit` and run `cd /media/exfat/timelapse`
12. Create a video by running `ffmpeg -r 24 -f image2 -i %08d.jpg -r 24 -s 1920x1080 -c:v libx264 -preset slow -crf 20 timelapse.mkv`


## Record Time Lapse Using PiCamera (old)
Requirements: External drive for pictures, `screen`, `ffmpeg`

You'll get better results (and `greyworld` support) using the `raspistill` version above. 

❗ I suggest disabling leds on the Raspberry Pi so you don't accidentally get reflections of them on camera:
* Disable **red** PWR led by running `sudo sh -c 'echo 0 > /sys/class/leds/led1/brightness'`
* Disable **green** ACT led by running `sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'`


1. Create mount point for external drive with `sudo mkdir /media/exfat`
2. Mount your external drive by running `sudo mount -t auto /dev/sda1 /media/exfat`
3. Save the following script as `timelapse.py`:
```python
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
folder_path = '/media/exfat/timelapse';

if not os.path.isdir(folder_path):
    os.mkdir(folder_path);

while current_pic < amount:
    camera = PiCamera();
    camera.resolution = (width, height);
    sleep(hold);
    camera.capture(folder_path + '/' + '{0:0>8d}'.format(current_pic) + '.jpg');
    camera.close();
    current_pic += 1;
    print('Captured picture ' + str(current_pic) + '/' + str(amount));
    sleep(60 - hold);

print('Time lapse done!');
```
4. Make script executable by running `chmod u+x timelapse.py`
5. Start screen by running `screen -S timelapse`
6. Run script with `./timelapse.py`
7. Detach from screen with `Ctrl-a` + `d` and let the script run in the background
8. Check the progress by running `screen -r timelapse`, when it's done you should see `Time lapse done!`
9. Exit screen with `exit` and run `cd /media/exfat/timelapse`
10. Create a video by running `ffmpeg -r 24 -f image2 -i %08d.jpg -r 24 -s 1920x1080 -c:v libx264 -preset slow -crf 20 timelapse.mkv`
