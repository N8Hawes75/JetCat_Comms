"""
calibration_curve.py

Created by Colton Wright on 3/1/2023

Point to the YYY-MM-DD_Calibration_Data directory and get the calibration curve
"""

import numpy as np
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt


folder_path = sys.argv[1] # Full path to file
files = []
frames = []
weights_used = []
val_weights = []
values = {"40aF": 40.001,
          "40bF": 39.999,
          "35aF": 35.001,
          "40aR": -40.001,
          "40bR": -39.999,
          "35aR": -35.001
          }


for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        files.append(file_path)

# Sort files according to the first number of their name
sorted_files = sorted(files, key=lambda x: int(x.split('/')[-1].split('_')[0]))

for file in sorted_files:
    frames.append(pd.read_csv(file))
    name = file.split('/')[-1].split('.')[0]
    w = name.split('_')[1:]
    w = '_'.join(w)
    w = w.replace('_', '+')
    weights_used.append(w)


for expr in weights_used:
    for var, val in values.items():
        expr = expr.replace(var, str(val))
        print(expr)
    value = eval(expr)
    val_weights.append(value)
print(val_weights)


x = np.zeros((len(val_weights)))
y = np.zeros((len(val_weights)))
for i in range(len(val_weights)):
    x[i] = val_weights[i]
    y[i] = frames[i]["Voltage"].mean()

labels = range(1, len(val_weights)+1)
fig, ax = plt.subplots()
ax.plot(x, y)
for i, txt in enumerate(labels):
    ax.annotate(txt, (x[i], y[i]))
plt.xlabel("Weight [lb]")
plt.ylabel("Voltage [V]")
plt.title("Calibration Curve")
plt.grid(True)
plt.show()



