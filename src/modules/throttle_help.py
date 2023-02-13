import os
import datetime
import time

import pandas as pd
import numpy as np

from cffi import FFI
from _crc.lib import get_crc16z


ffibuilder = FFI()


def make_filename(descrip):
    # Create directory & filename for the log file
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    FILE_PATH = os.path.join(".", "data", now )
    os.makedirs(FILE_PATH, exist_ok=True)
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d_T%H%M%S")
    filename = os.path.join(FILE_PATH, (now + "_" + descrip ))
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

def stop_engine(ser):
    ser.write(b"\x7E\x01\x01\x01\x01\x02\x00\x00\x39\xB9\x7E")

def send_throttle_rpm(ser, log_file, throttle_rpm, sequence_no):
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
    rpm_bytes = (rpm_to_send.item()).to_bytes(2, 'big')

    sequence_no_bytes = sequence_no.to_bytes(1, 'big')

    # header without stuffing or crc16
    header_basic = b'\x01\x01\x02' + sequence_no_bytes + b'\x02' + rpm_bytes

    # Calculate the crc16 from the basic header
    header_basic_c = ffibuilder.new("char[]", header_basic)
    crc16_calc = get_crc16z(header_basic_c, len(header_basic_c)-1)
    crc16_bytes = crc16_calc.to_bytes(2, 'big')

    # Append the crc16 bytes to the end of the basic header
    header_unstuffed = header_basic + crc16_bytes

    print_and_log(log_file, ("RPM to send:" + str(rpm_bytes)))
    print_and_log(log_file, ("CRC16 decimal:" + str(crc16_calc)))
    print_and_log(log_file, ("CRC16 hex:" + str(crc16_bytes)))
    # Need to stuff the header data in case there are any 0x7E or 0x7D bytes
    header_stuffed = stuff_header(header_unstuffed)
    header_send = b'\x7E' + header_stuffed + b'\x7E'


    print("Full header_send:", header_send)
    ser.write(header_send)


def stuff_header(header_bytes):
    # Take a header and stuff to fix any 0x7D and 0x7E problems.
    # Using a while loop so that we can update the length of the byte array,
    # that way when the array grows we still index clear to the end of it.


    byte_array1 = bytearray(header_bytes)
    i = 0
    while i < len(byte_array1):

        # You have to check for 7D first. If you don't, it will replace the
        # 0x7D inserted from 0x7E check and break your program!
        if byte_array1[i] == 0x7D:
            # Need to stuff 0x7D 0x5D in its place
            del byte_array1[i]
            insert_this = bytearray(b'\x7D\x5D')
            byte_array1[i:i] = insert_this
            print("Stuffed the 7D:", byte_array1)

        if byte_array1[i] == 0x7E:
            # Need to stuff 0x7D 0x5E in its place
            del byte_array1[i]
            insert_this = bytearray(b'\x7D\x5E')
            byte_array1[i:i] = insert_this
            print("Stuffed the 7E:", byte_array1)

        i = i + 1


    stuffed_header = bytes(byte_array1)
    return(stuffed_header)




def calculate_throttle_cmds():
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
    rpm_bytes = (rpm_to_send.item()).to_bytes(2, 'big')

    sequence_no_bytes = sequence_no.to_bytes(1, 'big')

    # header without stuffing or crc16
    header_basic = b'\x01\x01\x02' + sequence_no_bytes + b'\x02' + rpm_bytes

    # Calculate the crc16 from the basic header
    header_basic_c = ffibuilder.new("char[]", header_basic)
    crc16_calc = get_crc16z(header_basic_c, len(header_basic_c)-1)
    crc16_bytes = crc16_calc.to_bytes(2, 'big')

    # Append the crc16 bytes to the end of the basic header
    header_unstuffed = header_basic + crc16_bytes

    print("RPM to send:", rpm_bytes)
    print("CRC16 decimal:", crc16_calc)
    print("CRC16 hex:", crc16_bytes)
    # Need to stuff the header data in case there are any 0x7E or 0x7D bytes
    header_stuffed = stuff_header(header_unstuffed)
    header_send = b'\x7E' + header_stuffed + b'\x7E'


    print("Full header_send:", header_send)

def write_curve_to_log(log_file, cmd_file_path):
    with open(cmd_file_path, 'r') as cmds:
        for line in cmds:
            log_file.write(line)
    log_file.write("\n\n")

def print_and_log(log_file, to_print):
    log_file.write(to_print + "\n")
    print(to_print)

