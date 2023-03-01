"""
plot_csv.py

Created by Colton Wright on 2/27/2023

Takes a csv from E-TC, USB-6210, or PRO-Interface data and plot
"""

import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

import modules.data_analysis_m1 as m1

file_path = sys.argv[1] # Full path to file

frame = pd.read_csv(file_path)
base_path, extension = os.path.splitext(file_path)
# print(base_path)
parent_directory = os.path.dirname(file_path)


# Determine if the data is PRO-Interface, E-TC, or USB-6210
if frame.columns[0] == "Engine_Address":
    # print("Interface Data")
    for col in frame.columns:
        plt.figure()
        if col == "CRC16_Given" or col == "CRC16_Calculated":
            frame.plot(y=col, use_index=True, style='bo')
            plt.grid(True)
        else:
            frame.plot(y=col, use_index=True, style='b-')
            plt.grid(True)
        m1.save_fig2(base_path, col) # Want the name of data file in folder
        plt.close('all')

elif frame.columns[1] == "Voltage":
    # print("USB-6210 Data")
    plt.figure()
    frame.plot(x="Time [s]", y="Voltage", style='b-')
    plt.grid(True)
    m1.save_fig2(parent_directory, frame.columns[1])
    plt.close('all')

