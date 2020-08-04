#!/bin/env /usr/bin/python3

import requests
import serial
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Retrieve aiding data and update GPS module')
parser.add_argument('-t', '--token', required=True, help='your token to access AssistNow data site')
parser.add_argument('-d', '--device', required=True, help='the device/port where the GPS device is')

args = parser.parse_args()

if not os.path.exists(args.device):
    print(f'Error: device {args.device} does not exist', file=sys.stderr)
    sys.exit(1)
if not os.access(args.device, os.W_OK):
    print(f'Error: device {args.device} is not writable', file=sys.stderr)
    sys.exit(1)

url = f"http://online-live1.services.u-blox.com/GetOnlineData.ashx?token={args.token};gnss=gps;datatype=eph,alm,aux,pos;filteronpos;format=aid"
print("Downloading A-GPS data")
r = requests.get(url)

ser = serial.Serial(args.device, 9600)
print("Waiting for GPS to be free")
drainer = True
while drainer:
    drainer = ser.inWaiting()
    ser.read(drainer)

print(f"Writing AGPS data to {args.device}")
ser.write(r.content)
print("Done")

print("Reading GPS data: hit CTRL-C to quit")
buffer = True
message = b""
try:
    while buffer:
        buffer = ser.read()
        if buffer == b"$":
            if message.startswith(b"$GPGGA"):
                print(message.strip().decode())
            message = b""
        message = message + buffer
except KeyboardInterrupt:
    ser.close()
