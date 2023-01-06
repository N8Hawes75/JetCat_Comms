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

import modules.throttle_help as throttle_help


# Create log filename
filename = throttle_help.make_filename()

# Open throttle curve request file.
cmd_file_path = input("Input command file path: ")
cmd_array = throttle_help.read_throttle_cmds(cmd_file_path)


print("Connecting to port...")
with serial.Serial('/dev/pts/5', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    start = input("Connected to port. Are you ready to start the engine? [y/n]")

    if start == "y":

        ser.write(b"test_from_python")
        a_data_packet = ser.read(100)
        # Do something with this data packet
        file.write(a_data_packet)
    else:
        print("Bye")


