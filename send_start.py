"""
Created 11/23/2022

Send a command to the PRO-Interface and tell it to start.
"Whenever the engine is off/not running, the control mode is automatically
set to 'PWM control mode'. This basically allows all control sources to take
engine control by starting the engine."

So send a start command and then see if it will allow us to change some of the
data settings afterwards.
"""

import serial
import datetime
import os

import cw_helper2
from cffi import FFI
from _crc.lib import pi_approx, get_crc16z
ffibuilder = FFI()

print("Reading serial port...")
time_to_read = .5 # Time to read the port [min]
print("Test will take ", time_to_read, " minutes...")
# Create file and timing
filename = cw_helper2.make_txt_file()
time_to_end = datetime.datetime.today().timestamp() + 60*time_to_read

# Process a data packet to send over the serial port. For now. following the
# example of thrust % in the documentation. 

# Note: "Typically, the host would increment the sequence number with every
# message sent. The ECU would copy this number into its own messages sent
# back on a frequent basis. By this the host can easily verify that messages
# are decoded and passing through the ECU"

header_data = b'\x01\x01\x01\x01\x02\x00\x01'
header_data_c = ffibuilder.new("char[]", header_data)
print(len(header_data))
crc16_calculation = get_crc16z(header_data_c, len(header_data_c)-1)
crc16_calc_hex = crc16_calculation.to_bytes(2, 'big')
print("crc: ", crc16_calculation)
print(type(crc16_calculation))
print("crc hex: ", crc16_calc_hex)
packet = b'\x7E'+header_data+crc16_calc_hex+b'\x7E'
print(packet)

header_data2 = b'\x01\x01\x0D\x02\x02\x03\x01'
header_data2_c = ffibuilder.new("char[]", header_data2)
print(len(header_data2))
crc16_calculation2 = get_crc16z(header_data2_c, len(header_data2_c)-1)
crc16_calc_hex2 = crc16_calculation2.to_bytes(2, 'big')
print("crc2: ", crc16_calculation2)
print(type(crc16_calculation2))
print("crc2 hex: ", crc16_calc_hex2)
packet2 = b'\x7E'+header_data2+crc16_calc_hex2+b'\x7E'
print(packet2)

with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    ser.write(packet)
    a_data_packet = ser.read(100)
    file.write(a_data_packet)
    ser.write(packet2)


    time_to_end = datetime.datetime.today().timestamp() + 60*time_to_read

    while datetime.datetime.today().timestamp() < time_to_end:

        a_data_packet = ser.read(100)
        # Do something with this data packet
        file.write(a_data_packet)
