import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import datetime
from cffi import FFI
import os

import help_cw
import cw_helper2
from _crc.lib import pi_approx, get_crc16z

ffibuilder = FFI()

file_name = r"/home/colton/Documents/Python_Projects/JetCat_Comms/data/2022-11-22/2022-11-22_16:34:08_read_port"
folder_input = input("Enter description for image folder: ")

with open(file_name, 'rb',) as file:
    my_bytes = file.read()

printfirst = 1
list_of_list = []
data_packet = bytearray(80) # initialize byte array with 40 values
clipped_unstuffed_line = bytearray()
count = 0
for i in range(200, len(my_bytes)-100): # Skip putty header and last bytes
    if (my_bytes[i] == 0x7E and my_bytes[i+1] == 0x7E):
        # Two 7E in a row, new data packet starts at i+1
        j = 0
        i = i + 2
        while(my_bytes[i+j] != 0x7E ):
            data_packet[j] = my_bytes[i+j] # No framing bytes included
            j = j+1

        # CRC16 calculation:
        clipped_data = bytearray(j-2)
        for i in range(j-2):
            clipped_data[i] = data_packet[i]
        datastring = bytes(clipped_data)
        data = ffibuilder.new("char[]", datastring)
        length_line = j-2
        crc16_calculation = get_crc16z(data, length_line)

        # Unstuff the data packet for processing
        unstuffed_line = help_cw.byte_unstuffing(data_packet)
        decoded_numbers = help_cw.decode_line(unstuffed_line)
        decoded_numbers.append(crc16_calculation)

        print("\nData packet read this loop: ")
        print(data_packet)
        print("Unsuffed line: ")
        print(unstuffed_line)
        print("Data sent to crc16: ", datastring)
        print("Length of data sent to crc16: ", length_line)
        
        
        list_of_list.append(decoded_numbers)
        print("CRC given: ", decoded_numbers[len(decoded_numbers)-2])
        print("CRC calculated: ", decoded_numbers[len(decoded_numbers)-1])

        help_cw.check_crcs(decoded_numbers)

        # Reset data packet to all zero's
        for i in range(len(data_packet)):
            data_packet[i] = 0
        
        datastring=0
        count = count + 1
        print("Count: ", count)

# We have now looped through all bytes in putty log, and have a list of all
# the data. Save interpreted data into a data frame.
data_columns = ["Engine Address", "Message Descriptor", "Sequence Number",
"Data byte count", "RPM (setpoint)", "RPM (setpoint %)", "RPM (actual)", 
"RPM (actual %)", "EGT", "Pump Volts (setpoint)", "Pump Volts (actual)", 
"State", "Battery Volts", "Battery Volt Level %", "Battery Current", 
"Airspeed", "PWM-THR", "PWM-AUX","CRC16_Given","CRC16_Calculated"]
frame = pd.DataFrame(list_of_list, columns=data_columns)

# Check if the given CRC == calculated CRC
is_crc_equal = np.zeros((len(frame),1))
for i in range(len(frame)):
    if frame.iloc[i]["CRC16_Given"] == frame.iloc[i]["CRC16_Calculated"]:
        is_crc_equal[i] = True
    else:
        is_crc_equal[i] = False


# Plots
frame.plot()
help_cw.save_fig("all_data", folder_input)
for col in frame.columns:
    frame.plot(y=col, use_index=True, style='o')
    help_cw.save_fig(col, folder_input)


plt.figure()
plt.plot(frame.index, is_crc_equal)
help_cw.save_fig("is_equal", folder_input)

# Save the data frame to a text file
now = datetime.datetime.today()
now = now.strftime("%Y-%m-%d")
now_more = datetime.datetime.today()
now_more = now_more.strftime("%Y-%m-%d_%H:%M:%S")
FILE_PATH = os.path.join(".", "decoded_data", now )

os.makedirs(FILE_PATH, exist_ok=True)
frame.to_csv(os.path.join(FILE_PATH, now_more+"_decoded_data.csv"))



plt.show()

