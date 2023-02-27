"""
tdms_to_csv.py

Created by Colton Wright on 2/27/2023

Takes binary data file from NI USB-6210 and MCCDaq E-TC and converts to a CSV
"""

import pandas as pd
import os
import pickle
import sys
import modules.data_analysis_m1 as m1


file_path = sys.argv[1] # Full path to file
# file_path = r"/media/colton/T7/JetCat_Data/2023-02-22_JetCat_Test/signal_express/02222023_011948_PM/Voltage.tdms"

frame = m1.tdms_to_frame(file_path)

base_path, extension = os.path.splitext(file_path)
frame.to_csv(base_path + ".csv") # Write csv to same location


with open (base_path+'.pickle', 'wb') as handle:
    pickle.dump(frame, handle, protocol=pickle.HIGHEST_PROTOCOL)