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

def byte_unstuffing(bytes1):
    """
    byte_unstuffing takes the byte_array and decodes any stuffing that might
    have happened. 
    """
    # TODO: Test this function. If it does not work, engine data will become
    # corrupted.

    for i in range(len(bytes1)-2):

        # "If 0x7D should be transmitted, transmit two bytes: 0x7D and 0x5D"
        # This is from JetCat documentation
        byte_array = bytearray(bytes1)
        if(byte_array[i]==0x7D and byte_array[i+1]==0x5D):
            # Delete the extra byte
            del byte_array[i+1]

        # "If 0x7E should be transmitted, transmit two bytes: 0x7D and 0x5E"
        # This is from JetCat documentation
        if(byte_array[i]==0x7D and byte_array[i+1]==0x5E):
            # Replace two bytes with 0x7E
            byte_array[i] = 0x7E
            del byte_array[i+1]
    
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
    now_more = datetime.datetime.today()
    now_more = now_more.strftime("%Y-%m-%d_%H:%M:%S")
    FILE_PATH = os.path.join(".", "data", now )
    os.makedirs(FILE_PATH, exist_ok=True)
    filename = os.path.join(FILE_PATH, (now_more + "_read_port"))
    f = open(filename, 'w')
    return filename




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
