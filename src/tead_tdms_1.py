import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime

from nptdms import TdmsFile
from nptdms import tdms

# Program is to be ran in project root directory, JetCat_Comms


# Input the location of your TDMS file:
data_filename = input("Paste in FULL path to TDMS file... :\n")

test_descrip = input("Enter brief descrip of this test: \n")

# Create a folder and file name to store results
now = datetime.datetime.today()
now = now.strftime("%Y-%m-%d")
now_more = datetime.datetime.today()
now_more = now_more.strftime("%Y-%m-%d_%H:%M:%S")
FILE_PATH = os.path.join(".", "decoded_data", now+"_TDMS_Reading", test_descrip )
os.makedirs(FILE_PATH, exist_ok=True)
filename = os.path.join(FILE_PATH, (now_more + "_read_port"))

tdms_data = TdmsFile.read(data_filename)

for group in tdms_data.groups():
    # Determine if this is a thermocouple (MCCDAQ) or Load Cell (NI DAQ) TDMS
    if group.name == "Analog":
        file_type = "MCC"
    else:
        file_type = "NI"

if file_type == "MCC":
    print("MCCDAQ TDMS file found...")
    mcc_groups = tdms_data.groups()
    mcc_group1 = tdms_data["Analog"]
    mcc_allchannels = mcc_group1.channels()
    mcc_timechannel = mcc_group1["TimeStamps"]
    mcc_tempchannel1 = mcc_group1["AI0"]
    mcc_tempchannel2 = mcc_group1["AI1"]
    # These are numpy ndarrays
    mcc_time = mcc_timechannel[:]
    mcc_temp1 = mcc_tempchannel1[:]
    mcc_temp2 = mcc_tempchannel2[:]

    # Data pulled from file, just plot it now:

    # Plot MCC data
    FILE_PATH = os.path.join(FILE_PATH, "MCCDAQ")
    os.makedirs(FILE_PATH, exist_ok=True)
    plt.figure()
    plt.plot(mcc_time, mcc_temp1, 'blue', mcc_time, mcc_temp2, 'orange')
    plt.title('DAQami E-TC')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [degC]')
    plt.tight_layout()
    fig_path = os.path.join(FILE_PATH, "temps_v_time.png")
    plt.savefig(fig_path, dpi=600)

    plt.figure()
    plt.plot(mcc_time, mcc_temp1, 'blue')
    plt.title('DAQami E-TC')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [degC]')
    plt.tight_layout()
    fig_path = os.path.join(FILE_PATH, "temp1_v_time.png")
    plt.savefig(fig_path, dpi=600)

    plt.figure()
    plt.plot(mcc_time, mcc_temp2, 'orange')
    plt.title('DAQami E-TC')
    plt.xlabel('Time [s]')
    plt.ylabel('Temperature [degC]')
    plt.tight_layout()
    fig_path = os.path.join(FILE_PATH, "temp2_v_time.png")
    plt.savefig(fig_path, dpi=600)


    fig, ax1 = plt.subplots()
    ax1.plot(mcc_time, mcc_temp1, 'blue')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Temperature 1 [degC]', color='blue')
    ax2 = ax1.twinx()
    ax2.plot(mcc_time, mcc_temp2, 'orange')
    ax2.set_xlabel('Time [s]')
    ax2.set_ylabel('Temperature 2 [degC]', color='orange')

    fig_path = os.path.join(FILE_PATH, "temps_v_time_twin.png")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=600)
    plt.show()


if file_type == "NI":
    print("NI TDMS file found...")
    
    ni_groups = tdms_data.groups()
    i = 0
    group_names = []
    for group in ni_groups:
        group_names.append(group.name)
    print("NI group names: ")
    print(group_names, "\n")


    ni_group1 = tdms_data[group_names[0]]
    ni_g1_allchannels = ni_group1.channels()
    channel_names = []
    for channel in ni_g1_allchannels:
        channel_names.append(channel.name)
    print("NI channel names: ")
    print(channel_names, "\n")
    ni_g1_chan1 = ni_group1[channel_names[0]]

    # These are numpy ndarrays
    ni_g1_ai0_time = ni_g1_chan1.time_track()
    ni_g1_ai0_v = ni_g1_chan1[:]

    # Plot NI data
    FILE_PATH = os.path.join(FILE_PATH, "NI")
    os.makedirs(FILE_PATH, exist_ok=True)
    plt.figure()
    plt.plot(ni_g1_ai0_time, ni_g1_ai0_v, 'blue')
    plt.title('Load Cell Data')
    plt.xlabel('Time [s]')
    plt.ylabel('Voltage [V]')
    plt.tight_layout()
    fig_path = os.path.join(FILE_PATH, "load_v_time.png")
    plt.savefig(fig_path, dpi=600)
    plt.show()
