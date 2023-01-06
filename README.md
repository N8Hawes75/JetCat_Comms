# JetCat Comms Project
Created Repo on 11/11/2022


## Setup Help
```
sudo apt-get install python-dev libxml2-dev libxslt-dev
```

Ubuntu also required dev tools for c to be installed for fcci to work. Run
```
sudo apt-get update && sudo apt-get install build-essential
```

To save matplotlib animations you must install ffmpeg in ubuntu terminal
```
sudo apt install ffmpeg
```

## throttle_cmd_1.py

This program is for sending throttle commands to the PRO-Interface while also logging all the data from the serial port. The commands are received through a .txt file that follows this format:
```
Time, Throtttle%
0,0
10,33000
30,100000
120,33000
180,0
```
#### throttle_cmd_1.py virtual serial port for testing

To test the program, you should open a virtual serial port to make sure the proper commands are being sent. To create a virtual serial port, open a terminal and enter
```
socat -d -d pty,raw,echo=0 pty,raw,echo=0
```
This will return something like:
```
2023/01/06 16:09:03 socat[40084] N PTY is /dev/pts/4
2023/01/06 16:09:03 socat[40084] N PTY is /dev/pts/5
2023/01/06 16:09:03 socat[40084] N starting data transfer loop with FDs [5,5] and [7,7]
```

Then open a new terminal and type
```
cat < /dev/pts/4
```
Python can then connect to /dev/pts/5 and any commands sent over this port will be received on your terminal.

#### throttle_cmd_1.py CFFI

To run cffi, you need to run `main.py` inside the main `JetCat_Comms` directory for some reason. This will compile the library you need to include inside of `throttle_cmd_1.py`.

This is a bit of a mess right now. Run `main.py` to create the python .so library, then run `throttle_cmd_1.py` in the root directory as well so that it can view the .so c extension.