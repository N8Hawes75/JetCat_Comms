#!/bin/bash

# Start timer
start=$(date +%s.%N)

# activate virtual environment
source /home/colton/Documents/GitHub/JetCat_Comms/.venv/bin/activate

# change directory to the folder with the files
cd "$1"

# iterate over all .bin files in the folder and its subdirectories
find . -type f -name "*.csv" | while read file; do
  # run the Python script with the .bin file as the argument
  echo "Processing file: $file"
  /home/colton/Documents/GitHub/JetCat_Comms/.venv/bin/python /home/colton/Documents/GitHub/JetCat_Comms/src/plot_csv.py "$file"
done


# deactivate virtual environment
deactivate

# End timer
end=$(date +%s.%N)
runtime=$(echo "$end - $start" | bc)

# Print the runtime
echo "Runtime: $runtime seconds"
