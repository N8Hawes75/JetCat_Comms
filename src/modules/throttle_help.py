import os
import datetime
import time

import pandas as pd
import numpy as np



def make_filename():
    # Create directory & filename for the log file
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d")
    FILE_PATH = os.path.join(".", "data", now )
    os.makedirs(FILE_PATH, exist_ok=True)
    now = datetime.datetime.today()
    now = now.strftime("%Y-%m-%d_T%H%M%S")
    filename = os.path.join(FILE_PATH, (now + "_log"))
    return filename

def read_throttle_cmds(file_path):
    # Read the throttle commands out of a text file.
    # Column 1 is time, column 2 is throttle %.
    print("Reading Command file...")
    frame = pd.read_csv(file_path)
    cmd_array = frame.to_numpy()
    return cmd_array

def start_countdown():
    print("STARTING ENGINE IN 10...")
    time.sleep(1)
    print("STARTING ENGINE IN 9...")
    time.sleep(1)
    print("STARTING ENGINE IN 8...")
    time.sleep(1)
    print("STARTING ENGINE IN 7...")
    time.sleep(1)
    print("STARTING ENGINE IN 6...")
    time.sleep(1)
    print("STARTING ENGINE IN 5...")
    time.sleep(1)
    print("STARTING ENGINE IN 4...")
    time.sleep(1)
    print("STARTING ENGINE IN 3...")
    time.sleep(1)
    print("STARTING ENGINE IN 2...")
    time.sleep(1)
    print("STARTING ENGINE IN 1...")
    time.sleep(1)
    print("STARTING ENGINE!")
