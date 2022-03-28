# ServiceMonitor

*All files in this repo must be under the same directory.

written in python.

This service monitor tool has 2 states:

1.Monitor Mode: 

In monitor mode , the program will automatically write all states of the  current services running on the computer, to the ServiceList.txt file, every given x seconds. the output format in this file is: day/month/year,hour:minute:second~!~service states.                                                                                  Monitor mode will also compare each x given seconds , the 2 last samples taken and compare them, if a difference is found , the user will be notified in the GUI window.
Taking input: in the GUI window , the user can enter the number of seconds he wants to wait between every sample, then he has to press monitor mode to activate the program.

2.Manual Mode:

In manual mode , the user has two enter 2 time ranges, each range consists the following input: year/month/day & hour:minute, totally entering 4 dates , and then the user has pressed the "manual" button the program will take one sample from each time range and compare them , if a difference is found the user will be notified in the GUI window.

Safety Measurements:

1.Encrypting our code: we have encrypted our code using python with a given key , the EncDec.py program allows you to encrypt and decrypt the MonitorModes.py program using the provided key which is in the key.key file(text file).

2.Using python's watchdog: since all the important files are located in the python current working directory , we use watchdog to watch for suspicious activity , meaning whenever a file is being modified in the directory or a file is being moved into the or outside the directory, the user will be notified in the "warning" tab.

Running the code:

After you have entered the directory in which you kept the files , type: python3 (or python) GUI.py

Or just double click the GUI.py since .py files are .exe and a GUI window will appear.

The GUI window: 

![Monitor](https://user-images.githubusercontent.com/54214707/160246332-ee1e78fb-4f5e-4ef6-87d3-731164aecce0.PNG)

# ServiceMonitor
