"""
Created by Colton Wright on 1/6/2023

Log all the data from the JetCat PRO_Interface, while also sending throttle
commands to control the RPM of the engine. No live serial plotting.

FFI is required to send CRC16 to the PRO-Interface. You need the c .o files
compiled in order to run this program.


"""

import numpy as np
import pandas as pd
import serial
import time

import src.modules.throttle_help as throttle_help
from cffi import FFI
from _crc.lib import get_crc16z


# Create log filename
filename = throttle_help.make_filename()

# Open throttle curve request file.
cmd_file_path = input("Input command file path: ")
cmd_array = throttle_help.read_throttle_cmds(cmd_file_path)
cmd_length = cmd_array.shape[0]
time_to_kill = cmd_array[(cmd_length-1),0] # Seconds after start to kill engine
print("Test will last", time_to_kill, "seconds")

print("Connecting to port...")
with serial.Serial('/dev/pts/7', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    start = input("Connected to port. Are you ready to start the engine? [y/n]")

    if start == "y":
        throttle_help.start_countdown()
        throttle_help.start_engine(ser)

        starting_time = time.time()
        end_time = starting_time + time_to_kill
        while starting_time < end_time:

            a_data_packet = ser.read(100)
            # Do something with this data packet
            file.write(a_data_packet)
    else:
        print("Not starting engine. Bye.")



