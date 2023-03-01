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
from nptdms import TdmsFile
from nptdms import tdms


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
                # else:
                    # print("Error, wrong length at i =", i)
                    # print("Broken packet: ", unstuffed_line)
                i=j

            else:
                i = i+1

        # We have now looped through all bytes in putty log, and have a list of all
        # the data. Save interpreted data into a data frame.
        data_columns = ["Engine_Address", "Message_Descriptor", "Sequence_Number",
        "Data_Byte_Count", "RPM_(setpoint)", "RPM_(setpoint%)", "RPM_(actual)", 
        "RPM_(actual%)", "EGT", "Pump_Volts_(setpoint)", "Pump_Volts_(actual)", 
        "State", "Battery_Volts", "Battery_Volt_Level%", "Battery_Current", 
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

def tdms_to_frame(file_path):
    tdms_data = TdmsFile.read(file_path)

    for group in tdms_data.groups():
        # Determine if this is a thermocouple (MCCDAQ) or Load Cell (NI DAQ) TDMSVoltage.tdms
        if group.name == "Analog":
            file_type = "MCC"
        else:
            file_type = "NI"

    if file_type == "MCC":
        # print("MCCDAQ TDMS file found...")
        mcc_group1 = tdms_data["Analog"]
        mcc_timechannel = mcc_group1["TimeStamps"]
        mcc_tempchannel1 = mcc_group1["AI0"]
        mcc_tempchannel2 = mcc_group1["AI1"]
        mcc_tempchannel3 = mcc_group1["AI2"]
        # These are numpy ndarrays
        mcc_time = mcc_timechannel[:]
        mcc_temp1 = mcc_tempchannel1[:]
        mcc_temp2 = mcc_tempchannel2[:]
        mcc_temp3 = mcc_tempchannel3[:]
        frame = pd.DataFrame({'Time [s]': mcc_time,
                              'AI0': mcc_temp1,
                              'AI1': mcc_temp2,
                              'AI2': mcc_temp3})
        return frame

    elif file_type == "NI":
        # print("NI TDMS file found...")
        
        ni_groups = tdms_data.groups()
        group_names = []
        for group in ni_groups:
            group_names.append(group.name)
        # print("NI group names: ")
        # print(group_names, "\n")

        ni_group1 = tdms_data[group_names[0]]
        ni_g1_allchannels = ni_group1.channels()
        channel_names = []
        for channel in ni_g1_allchannels:
            channel_names.append(channel.name)
        # print("NI channel names: ")
        # print(channel_names, "\n")
        ni_g1_chan1 = ni_group1[channel_names[0]]

        # These are numpy ndarrays
        ni_g1_ai0_time = ni_g1_chan1.time_track()
        ni_g1_ai0_v = ni_g1_chan1[:]
        frame = pd.DataFrame({'Time [s]': ni_g1_ai0_time,
                              'Voltage': ni_g1_ai0_v})
        return frame

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

def save_fig2(parent_directory, file_name, tight_layout=True,\
    fig_extension="png", resolution=600):
    """
    Saves the figure inside a folder where the .csv file was found
    """
    IMAGES_PATH = os.path.join(parent_directory, "images")
    os.makedirs(IMAGES_PATH, exist_ok=True)
    path = os.path.join(IMAGES_PATH, file_name+"."+fig_extension)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    print("Saving plots to ", path)