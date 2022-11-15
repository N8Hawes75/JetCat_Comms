import serial
import datetime
import os

import help_cw

print("Reading serial port...")
time_to_read = 2 # Time to read the port [min]
print("Test will take ", time_to_read, " minutes...")
# Create file and timing
filename = help_cw.make_txt_file()
time_to_end = datetime.datetime.today().timestamp() + 60*time_to_read

with serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=2) as ser, \
    open(filename, 'ab') as file:

    while datetime.datetime.today().timestamp() < time_to_end:

        a_data_packet = ser.read(100)
        # Do something with this data packet
        file.write(a_data_packet)
