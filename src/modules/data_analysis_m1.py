"""
data_analysis_m1.py

Created by Colton Wright on 2/26/2023
Helper functions for main script
"""

import pandas as pd
from cffi import FFI
from _crc.lib import pi_approx, get_crc16z
import struct


ffibuilder = FFI()




def bin_to_frame(data_file_path):
    print("Hello!")

    with open(data_file_path, 'rb',) as file:
        my_bytes = file.read()

        printfirst = 1
        list_of_list = []
        data_packet = bytearray(80) # initialize byte array with 80 values
        clipped_unstuffed_line = bytearray()
        count = 0
        for i in range(0, len(my_bytes)-100): # Skip putty header and last bytes
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
                unstuffed_line = byte_unstuffing(data_packet)
                print(data_packet)
                decoded_numbers = decode_line(unstuffed_line)
                decoded_numbers.append(crc16_calculation)

                # print("\nData packet read this loop: ")
                # print(data_packet)
                # print("Unsuffed line: ")
                # print(unstuffed_line)
                # print("Data sent to crc16: ", datastring)
                # print("Length of data sent to crc16: ", length_line)
                
                
                list_of_list.append(decoded_numbers)
                # print("CRC given: ", decoded_numbers[len(decoded_numbers)-2])
                # print("CRC calculated: ", decoded_numbers[len(decoded_numbers)-1])

                # help_cw.check_crcs(decoded_numbers)

                # Reset data packet to all zero's
                for i in range(len(data_packet)):
                    data_packet[i] = 0
                
                datastring=0
                count = count + 1
                # print("Count: ", count)

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

    for i in range(len(byte_array)-1):

        # "If 0x7D should be transmitted, transmit two bytes: 0x7D and 0x5D"
        # This is from JetCat documentation
        if(byte_array[i]==0x7D and byte_array[i+1]==0x5D):
            # Delete the extra byte
            del byte_array[i+1]
            # Append so that byte_array does not lose length. Code will
            # fail if this is not done.
            byte_array.append(0x00)


        # "If 0x7E should be transmitted, transmit two bytes: 0x7D and 0x5E"
        # This is from JetCat documentation
        if(byte_array[i]==0x7D and byte_array[i+1]==0x5E):
            # Replace two bytes with 0x7E
            byte_array[i] = 0x7E
            del byte_array[i+1]
            byte_array.append(0x00)


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

    engine_address = byte_array[0] # Address of engine to be accessed
    message_description = byte_array[1] << 8 | byte_array[2]
    sequence_number = byte_array[3]
    data_byte_count = byte_array[4]

    setpoint_rpm = (byte_array[5] << 8 | byte_array[6])*10
    setpoint_rpm_percent = (byte_array[7] << 8 | byte_array[8])*.01
    actual_rpm = (byte_array[9] << 8 | byte_array[10])*10
    actual_rpm_percent = (byte_array[11] << 8 | byte_array[12])*.01
    exhaust_gas_temp = (byte_array[13] << 8 | byte_array[14])*.1
    setpoint_pump_volts = (byte_array[15] << 8 | byte_array[16])*.01
    actual_pump_volts = (byte_array[17] << 8 | byte_array[18])*.01
    state = (byte_array[19])
    battery_volts = (byte_array[20] << 8 | byte_array[21])*.01
    battery_volts_percent = (byte_array[22])*.5
    battery_current = (byte_array[23] << 8 | byte_array[24])*.01
    airspeed = (byte_array[25] << 8 | byte_array[26])*.1
    pwm_thr = (byte_array[27] << 8 | byte_array[28])*.1
    pwm_aux = (byte_array[29] << 8 | byte_array[30])*.1
    crc16 = (byte_array[31] << 8 | byte_array[32])

    decoded_packet = [engine_address, message_description, sequence_number,
    data_byte_count, setpoint_rpm, setpoint_rpm_percent, actual_rpm,
    actual_rpm_percent, exhaust_gas_temp, setpoint_pump_volts,
    actual_pump_volts, state, battery_volts, battery_volts_percent,
    battery_current, airspeed, pwm_thr, pwm_aux, crc16]

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
    values[14] *= 0.5  # battery_volts_percent
    values[15] *= 0.01  # battery_current
    values[16] *= 0.1  # airspeed
    values[17] *= 0.1  # pwm_thr
    values[18] *= 0.1  # pwm_aux

    print(decoded_packet)
    print(values)

    return decoded_packet