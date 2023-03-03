"""
calibrate_load_cell.py
Created by Colton Wright on 3/3/2023

Run this program to recieve prompts on what weights to hang from the load
cell for calibration, tell the computer when the weights are hung, and
automatically sample the load cell for a certain period of time, saving the
files together in the correct format so that calibration_curve.py can generate
the curves for you right after calibration.
"""

import numpy as np
import pandas as pd
import datetime
import nidaqmx
import time

import modules.m2 as m2

# Change this when you actually measure the weights
values = {"40aF": 40.001,
          "40bF": 39.999,
          "35aF": 35.001,
          "40aR": -40.001,
          "40bR": -39.999,
          "35aR": -35.001
          }
now = datetime.datetime.today()
now = now.strftime("%Y-%m-%d")
weight_order = ("40aF", "40aR", "40aR_40bF", "40bF_35aF", "40bF")
frames = []
for i in range(len(weight_order)):
    is_ready = m2.prompt_weight(weight_order[i])
    if is_ready == 'y':
        print("Collecting samples...")
        frames.append(m2.collect_samples())
        m2.save_frame(frames[i])
    else:
        break
    print(i)

