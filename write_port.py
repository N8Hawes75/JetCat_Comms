import serial
import datetime
import os

import cw_helper2
from cffi import FFI
from _crc.lib import pi_approx, get_crc16z
ffibuilder = FFI()

print("Reading serial port...")
time_to_read = .1 # Time to read the port [min]
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

header_data = b'\x01\x01\x0D\x04\x02\x03\x01'
header_data_c = ffibuilder.new("char[]", header_data)
print(len(header_data))
crc16_calculation = get_crc16z(header_data_c, len(header_data_c)-1)
crc16_calc_hex = crc16_calculation.to_bytes(2, 'big')
print("crc: ", crc16_calculation)
print(type(crc16_calculation))
print("crc hex: ", crc16_calc_hex)
packet = b'\x7E'+header_data+crc16_calc_hex+b'\x7E'
print(packet)

with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    ser.write(packet)
    time_to_end = datetime.datetime.today().timestamp() + 60*time_to_read

    while datetime.datetime.today().timestamp() < time_to_end:

        a_data_packet = ser.read(100)
        # Do something with this data packet
        file.write(a_data_packet)
