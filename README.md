# Raspi-Camera
Notes for Rasbian &amp; Raspberry Pi Camera Module. Tested on **Raspberry Pi 3 B+**.

## Watch Live Feed
Requirements: mplayer
1. From **desktop** run `nc -l 8111 | mplayer -fps 30 -vf scale=1920:1080 -nosound -cache 4096 -`
2. From **Raspberry Pi** replace `desktop-ip-here` with correct IP and run `raspivid -t 0 -w 1920 -h 1080 -fps 30 -o - | nc desktop-ip-here 8111`

**TIP** Get desktop IP with:
* Linux: `hostname -I`
* macOS: `ipconfig getifaddr en0` (ethernet) or `ipconfig getifaddr en1` (wifi)

___

## Record Time Lapse
Requirements: External drive for pictures, screen, ffmpeg

**TIP** I suggest disabling leds on the Raspberry Pi so you don't accidentally get reflections of them on camera:
* Disable red PWR led by running `sudo sh -c 'echo 0 > /sys/class/leds/led1/brightness'`
* Disable green ACT led by running `sudo sh -c 'echo 0 > /sys/class/leds/led0/brightness'`


1. Mount your external drive by running `sudo mount -t auto /dev/sda1 /media/exfat`
2. Save the following script as `timelapse.py`:
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
    print("Captured picture " + str(current_pic));
    sleep(60 - hold);

print("Time lapse done!");
```
3. Run `chmod u+x timelapse.py`
4. Run `screen -S timelapse`
5. Run `./timelapse.py`
6. Detach from screen with `Ctrl-a` + `d` and let the script run in the background
7. Check the progress by running `screen -r timelapse`, when it's done you should see `Time lapse done!`
8. Exit screen with `exit` and run `cd /media/exfat/timelapse`
9. Create a video with `ffmpeg -f image2 -i %04d.jpg -r 3 -s 1920x1080 -b 2097152 timelapse.avi`
