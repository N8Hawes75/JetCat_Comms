import os
import datetime
import time

import pandas as pd
import numpy as np



def make_filename():
    # Create directory & filename for the log file
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    FILE_PATH = os.path.join(".", "data", now )
    os.makedirs(FILE_PATH, exist_ok=True)
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d_T%H%M%S")
    filename = os.path.join(FILE_PATH, (now + "_log"))
    return filename

def read_throttle_rpm_cmds(file_path):
    # Read the throttle commands out of a text file.
    # Column 1 is time, column 2 is throttle %.
    print("Reading Command file...")
    frame = pd.read_csv(file_path)
    cmd_array = frame.to_numpy()
    return cmd_array

def start_countdown():
    print("STARTING ENGINE IN 10...")
    time.sleep(1)
    print("STARTING ENGINE IN 9...")
    time.sleep(1)
    print("STARTING ENGINE IN 8...")
    time.sleep(1)
    print("STARTING ENGINE IN 7...")
    time.sleep(1)
    print("STARTING ENGINE IN 6...")
    time.sleep(1)
    print("STARTING ENGINE IN 5...")
    time.sleep(1)
    print("STARTING ENGINE IN 4...")
    time.sleep(1)
    print("STARTING ENGINE IN 3...")
    time.sleep(1)
    print("STARTING ENGINE IN 2...")
    time.sleep(1)
    print("STARTING ENGINE IN 1...")
    time.sleep(1)
    print("STARTING ENGINE!")

def start_engine(ser):
    # I am just going to hard code this message, even though I have to make 
    # a function that calculates it anyways. This message is the same every
    # time. The sequence number will be 1 after this command is sent.

    # Command to start the P300-PRO with binary serial interface:
    ser.write(b"\x7E\x01\x01\x01\x01\x02\x00\x01\x28\x30\x7E")

def send_throttle_rpm(ser, throttle_rpm):
    # Send the P300-PRO any throttle command.


    # Jetcat documentation:
    """
    Command Message for engine Rpm control/demand
    Message Descriptor: 0x0102
    No of data bytes in message: 2
    Data interpretation: uint16_t
    Scale: 10x RPM
    Range: 0-300000 RPM

    If demanded RPM should be out of allowed range of engine, value would
    be automatically limited to possible/allowed range!
    """

    # If you want to send the throttle 100000 to the engine, you actually
    # send the integer 10000, because uint16_t's maximum decimal value is
    # 65535.
    rpm_to_send = throttle_rpm // 10 # Truncate off decimal place
    header_data = bytes(rpm_to_send)







    # For now, just write the integer to serial port:
    ser.write(header_data)