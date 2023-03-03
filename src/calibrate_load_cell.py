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
import nidaqmx
import time

import modules.m2 as m2

n_samples = 100000 # Take 100k samples for each weight hanging
sampling_rate = 10000 # USB-6210 peaks at 250000 kS/s
data = np.array([])
sample_times = np.linspace(0,n_samples/sampling_rate,n_samples)
with nidaqmx.Task() as task:

    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(sampling_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
    start = time.time()

    n_samples_per_loop = 5000 # You cannot just shove 100k samples into a list
    n_loop = int(n_samples/5000)
    for i in range(n_loop):
        reading = task.read(n_samples_per_loop, timeout=nidaqmx.constants.WAIT_INFINITELY)
        data = np.append(data, reading)

# print(data)
print("Runtime:", (time.time()-start))
print(len(data))

