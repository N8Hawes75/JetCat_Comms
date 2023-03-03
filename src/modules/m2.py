"""
m2.py

Created by Colton Wright on 2/26/2023
Helper functions for calibrating the load cell. No cffi.
"""

import numpy as np
import pandas as pd
import nidaqmx
import datetime
import os

def collect_samples():
    """
    Collect the samples for the current weight that is hanging off of the cell.
    Returns a data frame
    """

    n_samples = 100000 # Take 100k samples for each weight hanging
    sampling_rate = 10000 # USB-6210 peaks at 250000 kS/s
    data = np.array([])
    sample_times = np.linspace(0,n_samples/sampling_rate,n_samples)
    with nidaqmx.Task() as task:

        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
        task.timing.cfg_samp_clk_timing(sampling_rate, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)

        n_samples_per_loop = 5000 # You cannot just shove 100k samples into a list
        n_loops = int(n_samples/n_samples_per_loop)
        for i in range(n_loops):
            reading = task.read(n_samples_per_loop, timeout=nidaqmx.constants.WAIT_INFINITELY)
            data = np.append(data, reading)
        full_data = np.vstack((sample_times, data)).transpose()
        frame = pd.DataFrame(full_data, columns=["Time [s]", "Voltage [V]"])
    print("Done")
    return frame


def prompt_weight(input_string):
    """
    Prompt the user to hang the appropriate weights off of the load cell
    """
    substrings = input_string.split("_")
    weights_to_hang = []
    which_side = []
    for sub in substrings:
        # print(sub)
        weights_to_hang.append(sub[:-1])
        which_side.append(sub[-1])

    which_side_long = []
    for el in which_side:
        if el == 'R':
            which_side_long.append("Rear")
        elif el == 'F':
            which_side_long.append("Front")
    
    # print(weights_to_hang)
    # print(which_side_long)

    for i in range(len(weights_to_hang)):
        if i == 0:
            print("Please hang weight " + weights_to_hang[i] + " off the " + which_side_long[i] + " side of the load cell")
        else:
            print("Also hang " +  weights_to_hang[i] + " off the " + which_side_long[i])
    is_ready = input("Are you ready to collect samples? [y/n]: ")

    return is_ready


def save_frame(frame):
    csv_path = os.path.join(parent_directory, "data", now)
    os.makedirs(IMAGES_PATH, exist_ok=True)
    path = os.path.join(IMAGES_PATH, file_name+"."+fig_extension)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)
    print("Saving plots to ", path)