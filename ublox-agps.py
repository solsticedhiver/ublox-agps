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
print("Connecting to u-blox")
r = requests.get(url)
print("Downloading A-GPS data")

ser = serial.Serial(device, 9600)
print("Waiting to GPS be free")
drainer = True
while drainer:
    drainer = ser.inWaiting()
    ser.read(drainer)

print("Writing AGPS data")
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
