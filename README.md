# JetCat Comms Project

Created Repo on 11/11/2022


## Setup Help

```
sudo apt-get install python-dev libxml2-dev libxslt-dev
```

Ubuntu also required dev tools for c to be installed for FCCI to work. Run
```
sudo apt-get update && sudo apt-get install build-essential
```

To save Matplotlib animations you must install ffmpeg in ubuntu terminal
```
sudo apt install ffmpeg
```
Other modules included in `requirements.txt`

## CFFI

To run cffi, you need to run `main.py` inside the main `JetCat_Comms` directory for some reason. This will compile the library you need to include inside of any program that requires crc16 calcs.

This is a bit of a mess right now. Run `main.py` to create the python .so library, then put that library in the same folder as the source code you're going to run, `import _crc.lib`

## throttle_cmd_1.py

This program is for sending throttle commands to the PRO-Interface while also logging all the data from the serial port. The commands are received through a .txt file that follows this format:
```
Time, Throttle_RPM
0,0
45,34000
100,100000
120,33000
180,0
```
The first RPM command needs a significant amount of time from start to allow the engine to start. The engine should be primed with the GSU 

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
Python can then connect to /dev/pts/5 and any commands sent over this port will be received on your terminal. You can also not run the cat command above, run the python program so that the serial write data is saved into the buffer, and then use the command:
```
cat < /dev/pts/4 | hexdump -C
```
To see the serial data in binary.

These instructions come from [stack overflow](https://stackoverflow.com/questions/52187/virtual-serial-port-for-linux)

#### throttle_cmd_1.py Run Tips

You need at least ~40-45 seconds between your START command and the first set engine RPM command. I tested the program with the simulate engine mode and it works. If you change the RPM on the GSU, the next RPM command just overwrites your change. If you shut the engine down on the GSU, it will remain off while new RPM commands are being sent. 

#### throttle_cmd_1.py Notes

This program should work with the engine now.

Byte stuffing should be totally done. Timing used to be bad because I had `ser.read(100)` set, with a timeout of 2 seconds, so the program would just halt at the read statement and wait for 100 bytes for 2 seconds. Fixed this with `ser.read(ser.in_waiting)`.

## TODO:

- `throttle_cmd_1.py` and `read_port.py` Timestamps with the processed data somehow? Save to another file while also saving the PRO-Interface data to a file? There should be a time column in the `/decoded_data/XXXX-XX-XX/XXXX.csv` data files
- `throttle_cmd_1.py` There really is no reason to figure out what the engine control commands are while the engine is running. This should really all be calculated before the engine is started and then pulled from storage to send. But probably fast enough so that it does not matter.
- Organize the code