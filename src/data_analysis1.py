"""
data_analysis1.py

Created by Colton Wright on 2/26/2023
Program looks at some data taken from the 2/22/2023 P300-PRO engine testing and
looks at sample rate, exports to CSV, etc.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os

import modules.data_analysis_m1 as m1


# Let's first look at the PRO-Interface data from the longest run of 2/22/2023
interface_data1_path = r"/home/colton/Documents/GitHub/JetCat_Comms/data/2023-02-22/2023-02-22_T121427_data"

d1 = m1.bin_to_frame(interface_data1_path)
print(d1.head())

plt.figure()
plt.plot(d1['Sequence Number'])
plt.figure()
plt.plot(d1['RPM (actual)'])
plt.figure()
plt.plot(d1['Battery Volts'])
plt.figure()
plt.plot(d1['RPM (actual)'].diff())
plt.figure()
plt.plot(d1['CRC16_Given'], 'o')
plt.figure()
plt.plot(d1['CRC16_Calculated'], 'o')


# From log files and sequence plot, find the sampling rate:
print("Sampling rate: ", end="")
print(("{0:.3f}".format((10243-2624)/(1677087474.0343964-1677086374.0343955))))


# Get smallest change in RPM measured over the entire frame:
d1_rpm_diff = d1['RPM (actual)'].diff()
d1_rpm_resolution = d1_rpm_diff[d1_rpm_diff>0].min()
print("Smallest RPM difference: ", end="")
print("{0:.8f}".format(d1_rpm_resolution))

# Get smallest change in EGT measured over the entire frame:
d1_egt_diff = d1['EGT'].diff()
d1_egt_resolution = d1_egt_diff[d1_egt_diff>0].min()
print("Smallest EGT difference: ", end="")
print("{0:.8f}".format(d1_egt_resolution))








plt.show()