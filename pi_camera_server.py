#!/usr/bin/env python3
# From: https://github.com/jiinurppa/Raspi-Camera
# Watch live feed from your Raspberry Pi
# Example: http://192.168.0.2:8080/stream?ip=192.168.0.3&width=1280&height=720
# Parameters:
#   ip              = video client IP address
#   port            = video client port (default: 8111)
#   width           = video width (default: 1920)
#   height          = video height (default: 1080)
#   fps             = video Frames Per Second (default: 30)
#   awb             = camera Automatic White Balance mode (default: auto)
#   vertical_flip   = flip video vertically (default: false)
#   horizontal_flip = flip video horizontally (default: false)
#
# Requires Bottle: pip3 install bottle
# Bottle docs: https://bottlepy.org/docs/dev/
from bottle import route, run, request
import subprocess
import ipaddress
import re


@route('/stream')
def stream():
    awb_modes = ['off', 'auto', 'sun', 'cloud', 'shade',
                 'tungsten', 'fluorescent', 'incandescent',
                 'flash', 'horizon', 'greyworld']
    num_regex = re.compile('[^0-9]')
    awb = ''
    vertical_flip = ''
    horizontal_flip = ''
    ip = request.query.ip
    port = num_regex.sub('', request.query.port)
    width = num_regex.sub('', request.query.width)
    height = num_regex.sub('', request.query.height)
    fps = num_regex.sub('', request.query.fps)
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return 'Bad IP'
    if not port:
        port = '8111'
    if not width:
        width = '1920'
    if not height:
        height = '1080'
    if not fps:
        fps = '30'
    if request.query.awb:
        regex = re.compile('[^a-zA-Z]')
        awb = regex.sub('', request.query.awb)
        if awb not in awb_modes:
            awb = 'auto'
        awb = f'-awb {awb}'
    if request.query.vf is 'true':
        vertical_flip = '-vf'
    if request.query.hf is 'true':
        horizontal_flip = '-hf'
    subprocess.run(f'raspivid -t 0 -w {width} -h {height} -fps {fps} {awb} {vertical_flip} {horizontal_flip} -o - '
                   f'| nc {ip} {port}')
    return 'OK'


run(host='localhost', port=8080, debug=True)
