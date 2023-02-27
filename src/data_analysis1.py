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

interface_data1_frame = m1.bin_to_frame(interface_data1_path)
print(interface_data1_frame)
