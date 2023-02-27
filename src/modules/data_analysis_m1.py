"""
data_analysis_m1.py

Created by Colton Wright on 2/26/2023
Helper functions for main script
"""

import pandas as pd
from cffi import FFI
from _crc.lib import pi_approx, get_crc16z
import struct
import os
import matplotlib.pyplot as plt
import datetime

ffibuilder = FFI()




def bin_to_frame(data_file_path):

    with open(data_file_path, 'rb',) as file:
        my_bytes = file.read()

        list_of_list = []
        data_packet = bytearray() # initialize byte array
        i = 0
        while i < len(my_bytes)-1:

            if (my_bytes[i] == 0x7E and my_bytes[i+1] == 0x7E):
                # Two 7E in a row, new data packet starts at i+1
                j = my_bytes.find(bytes([0x7E]), i+2)
                if (j == -1): # Break if it cannot find 0x7E anywhere
                    print("Break")
                    break
                data_packet = my_bytes[i+2:j] # This is a data packet with no framing bytes
                data_packet = bytearray(data_packet)

                # CRC16 calculation:
                datastring = bytes(data_packet)
                # print("Datastring: ", datastring)
                # print("len(datastring)", len(datastring))
                data = ffibuilder.new("char[]", datastring)
                crc16_calculation = get_crc16z(data, len(datastring)-2)

                # Unstuff the data packet for processing
                # print(i)

                unstuffed_line = byte_unstuffing(data_packet)

                # print("unstuffed_line: ", unstuffed_line)
                # print("len(unstuffed_line): ", len(unstuffed_line))

                if len(unstuffed_line) == 33:
                    decoded_numbers = decode_line(unstuffed_line)
                    decoded_numbers.append(crc16_calculation)
                    list_of_list.append(decoded_numbers)
                else:
                    print("Error, wrong length at i =", i)
                    print("Broken packet: ", unstuffed_line)
                i=j

            else:
                i = i+1

        # We have now looped through all bytes in putty log, and have a list of all
        # the data. Save interpreted data into a data frame.
        data_columns = ["Engine Address", "Message Descriptor", "Sequence Number",
        "Data byte count", "RPM (setpoint)", "RPM (setpoint %)", "RPM (actual)", 
        "RPM (actual %)", "EGT", "Pump Volts (setpoint)", "Pump Volts (actual)", 
        "State", "Battery Volts", "Battery Volt Level %", "Battery Current", 
        "Airspeed", "PWM-THR", "PWM-AUX","CRC16_Given","CRC16_Calculated"]
        frame = pd.DataFrame(list_of_list, columns=data_columns)

    return frame

def byte_unstuffing(byte_array):
    """
    byte_unstuffing takes the byte_array and decodes any stuffing that might
    have happened. 
    """
    # TODO: Test this function. If it does not work, engine data will become
    # corrupted.

    i = 0
    while i < len(byte_array)-1:

        # "If 0x7D should be transmitted, transmit two bytes: 0x7D and 0x5D"
        # This is from JetCat documentation
        if(byte_array[i]==0x7D and byte_array[i+1]==0x5D):
            # print("Unstuff!")
            # Delete the extra byte if not at the end of the array
            if i+2 < len(byte_array):
                byte_array.pop(i+1)
            else:
                byte_array.pop(i+1)
                break
            i -= 1  # decrement i to re-check the current byte

        # "If 0x7E should be transmitted, transmit two bytes: 0x7D and 0x5E"
        # This is from JetCat documentation
        elif(byte_array[i]==0x7D and byte_array[i+1]==0x5E):
            # print("Unstuff")
            # Replace two bytes with 0x7E
            byte_array[i] = 0x7E
            # Delete the extra byte if not at the end of the array
            if i+2 < len(byte_array):
                byte_array.pop(i+1)
            else:
                byte_array.pop(i+1)
                break
            i -= 1  # decrement i to re-check the current byte

        i += 1

    return byte_array

def decode_line(byte_array):
    """
    decode_line Decodes a line of bytes with the framing bytes included. Has
    nothing built in for byte stuffing or checksum yet.

    :param byte_array: byte_array is <class 'bytearray'>. Has no framing
    bytes included
    :return: Returns a Series of the processed data in order of JetCat
    documentation
    """

    # Old worse way of doing things
    # engine_address = byte_array[0] # Address of engine to be accessed
    # message_description = byte_array[1] << 8 | byte_array[2]
    # sequence_number = byte_array[3]
    # data_byte_count = byte_array[4]

    # setpoint_rpm = (byte_array[5] << 8 | byte_array[6])*10
    # setpoint_rpm_percent = (byte_array[7] << 8 | byte_array[8])*.01
    # actual_rpm = (byte_array[9] << 8 | byte_array[10])*10
    # actual_rpm_percent = (byte_array[11] << 8 | byte_array[12])*.01
    # exhaust_gas_temp = (byte_array[13] << 8 | byte_array[14])*.1
    # setpoint_pump_volts = (byte_array[15] << 8 | byte_array[16])*.01
    # actual_pump_volts = (byte_array[17] << 8 | byte_array[18])*.01
    # state = (byte_array[19])
    # battery_volts = (byte_array[20] << 8 | byte_array[21])*.01
    # battery_volts_percent = (byte_array[22])*.5
    # battery_current = (byte_array[23] << 8 | byte_array[24])*.01
    # airspeed = (byte_array[25] << 8 | byte_array[26])*.1
    # pwm_thr = (byte_array[27] << 8 | byte_array[28])*.1
    # pwm_aux = (byte_array[29] << 8 | byte_array[30])*.1
    # crc16 = (byte_array[31] << 8 | byte_array[32])

    # decoded_packet = [engine_address, message_description, sequence_number,
    # data_byte_count, setpoint_rpm, setpoint_rpm_percent, actual_rpm,
    # actual_rpm_percent, exhaust_gas_temp, setpoint_pump_volts,
    # actual_pump_volts, state, battery_volts, battery_volts_percent,
    # battery_current, airspeed, pwm_thr, pwm_aux, crc16]

    byte_format = ">BHBB HHHHHHHBHBHHHH H"
    values = struct.unpack(byte_format, byte_array)
    values = list(values)


    # Apply scaling factors to the appropriate fields
    values[4] *= 10  # setpoint_rpm
    values[5] *= 0.01  # setpoint_rpm_percent
    values[6] *= 10  # actual_rpm
    values[7] *= 0.01  # actual_rpm_percent
    values[8] *= 0.1  # exhaust_gas_temp
    values[9] *= 0.01  # setpoint_pump_volts
    values[10] *= 0.01  # actual_pump_volts
    values[12] *= 0.01 # Battery Volts
    values[13] *= 0.5 # Battery avolt level %
    values[14] *= 0.01 # Battery current
    values[15] *= 0.1 # Airspeed
    values[16] *= 0.1 # PWM-THR Channel
    values[17] *= 0.1 # PWM-AUX Channel

    # print("decoded_packet: ", decoded_packet)
    # print("values        : ", values)

    return values

def save_fig(fig_id, folder_descrip , tight_layout=True,\
    fig_extension="png", resolution=600):

    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    IMAGES_PATH = os.path.join(".", "images", now, folder_descrip)
    os.makedirs(IMAGES_PATH, exist_ok=True)
    fig_id = now + "_" + fig_id
    path = os.path.join(IMAGES_PATH, fig_id + " " +\
            folder_descrip + "." + fig_extension)
    # print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)