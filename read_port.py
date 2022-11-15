import serial
import numpy as np
import serial
import time
import pandas as pd
import csv
import help_cw
import os
import datetime


buffer = []
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
x = ser.read_until()
print(x)
buffer.append(x)
print("Buffer: ", buffer)
ser.close()
print("\n\n\n\nBuffer: ", buffer)
print(x)
print(datetime.datetime.today().timestamp())


# Create file and timing
filename = help_cw.make_txt_file()
time_to_end = datetime.datetime.today().timestamp() + 60*1
with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:
    while datetime.datetime.today().timestamp() < time_to_end:

        a_data_packet = ser.read(100)
        # Do something with this data packet
        file.write(a_data_packet)

ser.close()
