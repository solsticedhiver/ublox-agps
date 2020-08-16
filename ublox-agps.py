#!/bin/env /usr/bin/python3

import requests
import serial
import sys
import argparse
import os
import struct

def checksum(data):
    a = b = 0
    for d in data:
        a += d
        a = a & 0xFF
        b += a
        b = b & 0xFF
    return (a,b)

def is_checksum_ok(ck_a, ck_b, data):
    return checksum(data) == (ck_a, ck_b)

parser = argparse.ArgumentParser(description='Retrieve aiding data and update GPS module')
parser.add_argument('--debug', action='store_true', help='add more verbose message')
parser.add_argument('--lat', type=float, help='your longitude')
parser.add_argument('--lon', type=float, help='your latitude')
parser.add_argument('--format', choices=['mga', 'aid'], default='aid', help='format of the downloaded data: mga for M8 onwards, aid for u7 or earlier')
parser.add_argument('-t', '--token', required=True, help='your token to access AssistNow data site')
parser.add_argument('-d', '--device', required=True, help='the device/port where to reach the GPS device')

args = parser.parse_args()

if not os.path.exists(args.device):
    print(f'Error: device {args.device} does not exist', file=sys.stderr)
    sys.exit(1)
if not os.access(args.device, os.W_OK):
    print(f'Error: device {args.device} is not writable', file=sys.stderr)
    sys.exit(1)

if (args.lat and not args.lon) or (args.lat and not args.lon):
    print('Error: you need to use both latitude and longitude', file=sys.stderr)
    sys.exit(1)

url = f'https://online-live1.services.u-blox.com/GetOnlineData.ashx?token={args.token};gnss=gps;datatype=eph,alm,aux,pos;filteronpos;format={args.format}'
if args.lat and args.lon:
    if args.lat > 90 or args.lat < -90 or args.lon > 180 or args.lon < -180:
        print('Error: latitude or longitude not in expected range', file=sys.stderr)
        sys.exit(1)
    # add pacc field based on number of decimal of lat and lon
    nd = min(len(str(args.lat).split('.')[1]), len(str(args.lon).split('.')[1]))
    pacc = int(111000/10**nd)
    url += f';lon={args.lon};lat={args.lat};pacc={pacc}'

print('Downloading A-GPS data from u-blox server')
r = requests.get(url)
if r.status_code != 200:
    print(f'Error {r.status_code} {r.content.decode()}', file=sys.stderr)
    sys.exit(1)
data = r.content

# check the checksum of the downloaded data
is_valid = data[0] == 0xb5 and data[1] == 0x62 # first header
indx = 0
while is_valid and indx < len(data):
    if data[indx] == 0xb5 and data[indx+1] == 0x62:
        length = struct.unpack('<H', bytes(data[indx+4:indx+6]))[0]
        payload = data[indx+2:indx+5+length+1]
        check = is_checksum_ok(data[indx+5+length+1], data[indx+5+length+2], payload)
        if args.debug:
            ok = "OK" if check else "NOT OK"
            print(f'Found header {hex(data[indx+2])}/{hex(data[indx+3])} at {indx}, {length} bytes, checksum {ok}')
        indx += 5+length+3
        is_valid = is_valid and check

if is_valid:
    print('Checksums are OK')
else:
    print('Error: checksums are NOT OK', file=sys.stderr)
    sys.exit(1)

ser = serial.Serial(args.device, 9600)
print('Waiting for GPS to be free')
drainer = True
while drainer:
    drainer = ser.inWaiting()
    ser.read(drainer)

print(f'Writing AGPS data to {args.device}')
ser.write(r.content)
print('Done')
print(':: Warning: we have not checked that the dongle acknowledged the data sent')
