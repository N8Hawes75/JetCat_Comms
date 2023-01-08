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

import throttle_help as throttle_help
from cffi import FFI
from _crc.lib import get_crc16z


# Create log filename
filename = throttle_help.make_filename()

# Open throttle curve request file.
cmd_file_path = input("Input command file path: ")
cmd_array = throttle_help.read_throttle_rpm_cmds(cmd_file_path)
cmd_length = cmd_array.shape[0]
time_to_kill = cmd_array[(cmd_length-1),0] # Seconds after start to kill engine
print("Test will last", time_to_kill, "seconds")

print("Connecting to port...")
with serial.Serial('/dev/pts/3', baudrate=115200, timeout=.25) as ser, \
    open(filename, 'ab') as file:

    start_input = input("Connected to port. Are you ready to start the engine? [y/n] ")

    if start_input == "y":
        throttle_help.start_countdown()
        throttle_help.start_engine(ser)

        start_time = time.time()
        end_time = start_time + time_to_kill # now + length of the test
        cmd_counter = 1 # Increment when a RPM command is sent. Start at [1,0]
        now = start_time
        print("Starting time: ", start_time)
        while now < end_time:

            # Write data to log file

            serial_port_data = ser.read(ser.in_waiting)
            file.write(serial_port_data)

            # If enough time has elapsed, send a throttle command
            if now > (start_time + cmd_array[cmd_counter, 0]):

                print("Sent cmd at:", now)
                print("Time:", cmd_array[cmd_counter, 0])
                print("Throttle_RPM:", cmd_array[cmd_counter, 1])
                throttle_help.send_throttle_rpm(ser, cmd_array[cmd_counter, 1], cmd_counter)
                print()
                cmd_counter = cmd_counter + 1

            now = time.time()
        throttle_help.stop_engine()

    else:
        print("Not starting engine. Bye.")

