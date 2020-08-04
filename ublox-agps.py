#!/bin/env /usr/bin/python3

import requests
import serial
import sys

# You can hard-code the token and device below
token = ""
device = ""

if token == "" or device == "":
    print("Error: no token or device specified", file=sys.stderr)
    sys.exit(1)

url = f"http://online-live1.services.u-blox.com/GetOnlineData.ashx?token={token};gnss=gps;datatype=eph,alm,aux,pos;filteronpos;format=aid"
print("Downloading A-GPS data")
r = requests.get(url)

ser = serial.Serial(device, 9600)
print("Waiting for GPS to be free")
drainer = True
while drainer:
    drainer = ser.inWaiting()
    ser.read(drainer)

print(f"Writing AGPS data to {device}")
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
