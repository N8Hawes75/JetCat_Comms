#!/bin/bash

# Start timer
start=$(date +%s.%N)

# activate virtual environment
source /home/colton/Documents/GitHub/JetCat_Comms/.venv/bin/activate

# change directory to the folder with the files
cd "$1"

/home/colton/Documents/GitHub/JetCat_Comms/.venv/bin/python /home/colton/Documents/GitHub/JetCat_Comms/src/calibration_curve.py "$1"
# deactivate virtual environment
deactivate

# End timer
end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc)

# Print the runtime
echo "Runtime: $runtime seconds"