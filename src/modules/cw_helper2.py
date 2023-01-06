import numpy as np
import struct
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
from cffi import FFI

def byte_unstuffing(bytes1):
    """
    byte_unstuffing takes the byte_array and decodes any stuffing that might
    have happened. 
    """
    # TODO: Test this function. If it does not work, engine data will become
    # corrupted.
    byte_array = bytearray(bytes1)
    for i in range(len(bytes1)-2):

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
        if(byte_array[i]==0x7D
            and byte_array[i+1]==0x5E):
            # Replace two bytes with 0x7E
            byte_array[i] = 0x7E
            del byte_array[i+1]
            byte_array.append(0x00)

    # Bytes are unstuffed, but there is extra length from the appends. Appends
    # cannot be removed or it will break the for loop, so now that we are
    # done unstuffing lets just shorten the bytearray to the correct length
    byte_array = byte_array[0:33]
    return byte_array

def unpack_bytes(bytes):
    unpack_format = ">BHBB HHHHHHHBHBHHHH H"
    unpackaged1 = struct.unpack(unpack_format, bytes)
    return(unpackaged1)

def save_fig(fig_id, folder_descrip , tight_layout=True,\
    fig_extension="png", resolution=600):

    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    IMAGES_PATH = os.path.join(".", "images", now, folder_descrip)
    os.makedirs(IMAGES_PATH, exist_ok=True)
    fig_id = now + " " + fig_id
    path = os.path.join(IMAGES_PATH, fig_id + " " +\
            folder_descrip + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)

def make_txt_file():
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    FILE_PATH = os.path.join(".", "data", now )
    os.makedirs(FILE_PATH, exist_ok=True)
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d_T%H%M%S")
    filename = os.path.join(FILE_PATH, (now + "_log"))
    return filename

def get_command_message(main_bytes):
    """
    Get the data packet to send for a particular command message.
    Give a bytes value that is:
    slave address, high byte of command, low byte of command, sequence number,
    number of data bytes, data byte 1, data byte 2,...
    checksum is calculated and bytes are unstuffed, framing bytes are added
    """
    ffibuilder = FFI()

    main_bytes_c = ffibuilder.new("char[]", main_bytes)


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] #store relative frequency here
rs = [] #for theoretical probability

# This function is called periodically from FuncAnimation
def animate(frame, tick, data):

    # Draw x and y lists
    ax.clear()
    ax.plot(tick, data, label="Actual RPM")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Animating a variable...')
    plt.ylabel('RPM')
    plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
