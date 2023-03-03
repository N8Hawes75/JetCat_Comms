def byte_array_to_string(byte_array):
    # Convert byte array to a string so it can go into crc16 calculation
    """
    """


def get_crc16(byte_array):
    # Cut off the extra zeros in the byte_array, as well as the n-2 bytes sent
    # The CRC calculation does not use the last two bytes, those contain the 
    # CRC value!
    #new_array = byte_array[:31]

    length = len(byte_array)
    crc_16_data = 0
    print("Length of byte_array: ", length)
    i = 0

    while(length):

        data = byte_array[i]
        print("i: ", i, "data: ", data)
        crc_16_data = crc16_update(crc_16_data, data)
        print("crc_16_data: ", crc_16_data)
        i = i + 1
        length = length - 1
    return crc_16_data

def crc16_update(crc, data):
    b8_crc = crc & 0xFF

    data = data ^ (b8_crc & 0xFF)
    print("data1: ", data)
    data = data ^ (data << 4)
    print("data2: ", data)
    ret_val = ((data<<8) | ((crc&0xFF00)>>8)) ^ (data>>4) ^ (data<<3)
    print("ret_val: ", ret_val)
    return ret_val