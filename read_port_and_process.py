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
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

import help_cw
import cw_helper2

time_to_read = 0.5 # Time to read the port [min]
print("Begin...")
print("Test will run for ", time_to_read, " minutes...")

# Create file and timing
filename = cw_helper2.make_txt_file()
time_to_end = datetime.datetime.today().timestamp() + 60*time_to_read
fig, ax = plt.subplots()
ln, = ax.plot([], [], 'ro')
count = 0
ticks = np.zeros((1,1))
rpm = np.zeros((1,1))

# Open serial port and .bin file. with will close both of them at the end of
# the program for us automatically.
with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    ser.read_until(b'\x7E\x7E') # Get to framing bytes
    #After file is opened, read & process data until time has elapsed
    while datetime.datetime.today().timestamp() < time_to_end:

        
        ser.read(2) # Get to start of packet

        a_data_packet = ser.read_until(b'\x7E\x7E') # Read packet
        print("Number of bytes read: ", len(a_data_packet))

        # Do something with this data
        file.write(a_data_packet)
        count = count+1
        # Add functions here that will process the data and plot
        # Decode that data into a numpy array...
        print("Decoding the read bytes...")
        # TODO: Destuff the data packet before unpack
        unstuffed = cw_helper2.byte_unstuffing(a_data_packet)
        # Unpack the bytes into a tuple
        unpacked_data = cw_helper2.unpack_bytes(a_data_packet)
        ticks=np.append(ticks, count)
        rpm=np.append(rpm, unstuffed[7])
        # Set up plot to call animate() function periodically
        ani = animation.FuncAnimation(fig,\
            partial(cw_helper2.animate),frames=ticks, interval=10)
        plt.show()





print("Done")