"""
Created by Colton Wright on 1/8/2023

Log all the data from the JetCat PRO_Interface, while also sending throttle
commands to control the RPM of the engine. No live serial plotting. This 
program will save the times as a better format and calculate everything
before starting the engine. Should also work as throttle percent or
throttle RPM in the same program.

FFI is required to send CRC16 to the PRO-Interface. You need the c .o files
compiled in order to run this program.


"""

import numpy as np
import pandas as pd
import serial
import time
import shutil

import modules.throttle_help as throttle_help

# Create log filename
data_filename = throttle_help.make_filename("data")
# Create 
log_filename = throttle_help.make_filename("log.txt")

# Ask if you're using a external ssd to backup data
is_using_external_disk = input("Is the T7 plugged in to backup your data? [y/n]: ")

# Open throttle curve request file.
cmd_file_path = input("Input command file path: ")

cmd_array = throttle_help.read_throttle_rpm_cmds(cmd_file_path)
cmd_length = cmd_array.shape[0]
time_to_kill = cmd_array[(cmd_length-1),0] # Seconds after start to kill engine
print("Test will last", time_to_kill, "seconds")

print("Connecting to port...")
with serial.Serial('/dev/pts/7', baudrate=115200, timeout=.25) as ser, \
    open(data_filename, 'ab') as dat_file, \
    open(log_filename, 'a') as log_file:

    throttle_help.write_curve_to_log(log_file, cmd_file_path)
    start_input = input("Connected to port. Are you ready to start the engine? [y/n] ")

    if start_input == "y":
        throttle_help.start_countdown()
        throttle_help.start_engine(ser)

        start_time = time.time()
        end_time = start_time + time_to_kill # now + length of the test
        cmd_counter = 1 # Increment when a RPM command is sent. Start at [1,0]
        now = start_time
        throttle_help.print_and_log(log_file, ("Starting time: " + str(start_time)))
        while now < end_time:

            # Write data to log file

            serial_port_data = ser.read(ser.in_waiting)
            dat_file.write(serial_port_data)

            # If enough time has elapsed, send a throttle command
            if now > (start_time + cmd_array[cmd_counter, 0]):

                throttle_help.print_and_log(log_file, ("Sent cmd at:" + str(now)))
                throttle_help.print_and_log(log_file, ("Time:" + str(cmd_array[cmd_counter, 0])))
                throttle_help.print_and_log(log_file, ("Throttle_RPM:" + str(cmd_array[cmd_counter, 1])))
                throttle_help.send_throttle_rpm(ser, log_file, cmd_array[cmd_counter, 1], cmd_counter)
                throttle_help.print_and_log(log_file, "\n")
                cmd_counter = cmd_counter + 1

            now = time.time()
        throttle_help.print_and_log(log_file, ("Stop time:" + str(time.time())))
        throttle_help.stop_engine(ser)

    else:
        throttle_help.print_and_log(log_file, "Not starting engine. Bye.")

if is_using_external_disk=='y':
    throttle_help.save_to_t7(data_filename, log_filename)
