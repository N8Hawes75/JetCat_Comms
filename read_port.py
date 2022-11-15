import serial
import numpy as np
import serial
import time
import pandas as pd
import csv
from help_cw import *
import os
import datetime

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
x = ser.read_until()
print(x)

now = datetime.datetime.today()
now = now.strftime("%Y-%m-%d")
now_more = datetime.datetime.today()
now_more = now_more.strftime("%Y-%m-%d %H:%M:%S")
FILE_PATH = os.path.join(".", "data", now )
print(FILE_PATH)
os.makedirs(FILE_PATH, exist_ok=True)
filename = os.path.join(FILE_PATH, (now_more + " read_port"))


f = open(filename, 'w')
f.write(str(x))
f.close()


ser.close()
