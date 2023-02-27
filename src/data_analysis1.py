"""
data_analysis1.py

Created by Colton Wright on 2/26/2023
Program looks at some data taken from the 2/22/2023 P300-PRO engine testing and
looks at sample rate, exports to CSV, etc.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import modules.data_analysis_m1 as m1


# Open PRO-Interface data
interface_data0_path = r"/home/colton/Documents/GitHub/JetCat_Comms/data/2023-02-22/2023-02-22_T114204_data"
interface_data1_path = r"/home/colton/Documents/GitHub/JetCat_Comms/data/2023-02-22/2023-02-22_T121427_data"
interface_data2_path = r"/home/colton/Documents/GitHub/JetCat_Comms/data/2023-02-22/2023-02-22_T131809_data"
interface_data3_path = r"/home/colton/Documents/GitHub/JetCat_Comms/data/2023-02-22/2023-02-22_T131842_data"
interface_data4_path = r"/home/colton/Documents/GitHub/JetCat_Comms/data/2023-02-22/2023-02-22_T132715_data"

d0 = m1.bin_to_frame(interface_data0_path)
d1 = m1.bin_to_frame(interface_data1_path)
d2 = m1.bin_to_frame(interface_data2_path)
d3 = m1.bin_to_frame(interface_data3_path)
d4 = m1.bin_to_frame(interface_data4_path)
frame_list = [d0,d1,d2,d3,d4]

for i, frame in zip(range(len(frame_list)), frame_list):
    for col in frame.columns:
        plt.figure()
        if col == "CRC16_Given" or col == "CRC16_Calculated":
            frame.plot(y=col, use_index=True, style='bo')
        else:
            frame.plot(y=col, use_index=True, style='b-')
        m1.save_fig(col, "test_"+str(i))
        plt.close('all')

# From log files and sequence plot, find the sampling rate:
print("d0 Sampling rate: ", end="")
print(("{0:.3f}".format((5400-116)/(1677085795.6710713-1677085225.6710684))))
print("d1 Sampling rate: ", end="")
print(("{0:.3f}".format((14640-2624)/(1677087654.034397-1677085315.6710699))))
# print("d2 Sampling rate: ", end="")
# print(("{0:.3f}".format((10243-2624)/(1677090266.2674663-1677086374.0343955))))
print("d3 Sampling rate: ", end="")
print(("{0:.3f}".format((3155-2600)/(1677090266.2674663-1677090206.2674649))))
print("d4 Sampling rate: ", end="")
print(("{0:.3f}".format((1503-106)/(1677090780.3121603-1677090540.312161))))

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

d0.to_csv("2023-02-22_T114204_data.csv")
d1.to_csv("2023-02-22_T121427_data.csv")
d2.to_csv("2023-02-22_T131809_data.csv")
d3.to_csv("2023-02-22_T131842_data.csv")
d4.to_csv("2023-02-22_T132715_data.csv")





plt.show()