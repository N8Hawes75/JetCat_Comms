"""
read_port_and_process.py
Created by Colton Wright on 11/15/2022

NOTE: This file does NOT support any multiprocessing, this is a test to show
how many bytes I am losing by processing and reading data from the port at the
same time.
"""


import serial
import datetime
import os

import help_cw

time_to_read = 0.1 # Time to read the port [min]
print("Begin...")
print("Test will run for ", time_to_read, " minutes...")

# Create file and timing
filename = help_cw.make_txt_file()
time_to_end = datetime.datetime.today().timestamp() + 60*time_to_read

# Open serial port and .bin file. with will close both of them at the end of
# the program for us automatically.
with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    #After file is opened, read & process data until time has elapsed
    while datetime.datetime.today().timestamp() < time_to_end:

        read_bytes = ser.read(100) # type(a_data_packet) = <class 'bytes'>
        read_bytes2 = read_bytes + ser.read_until(b'\x7E\x7E')
        read_bytes3 = read_bytes2 + ser.read_until(b'\x7E\x7E')
        print(len(read_bytes3))

        # Do something with this data
        file.write(read_bytes)
        # Add functions here that will process the data and plot
        # Decode that data into a numpy array...
        print("Decoding the read bytes...")

        help_cw.decode_bytes(read_bytes3)







print("Done")