# Authors David Ehevich & Dvir Biton
import subprocess
import csv
from tkinter import messagebox
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from pandas import *
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import platform
from time import sleep
from datetime import datetime
import os
import json
# from GUI import Gui
from tkinter import *
from threading import Thread



#################################################################################################
def runWindows():
    command = "Get-Service | Export-Csv -Path ./service.csv"
    completed = subprocess.run(["powershell", "-Command", command], capture_output=True)
    if completed.returncode != 0:
        print("An error occured: %s", completed.stderr)
    else:
        print("Hello command executed successfully!")


#################################################################################################

def ReadCSVUbuntu():
    serviceData = read_csv("service.csv")
    NameColumn = serviceData['UNIT'].tolist()
    StatusColumn = serviceData['SUB'].tolist()
    nameStat = {}
    for i in range(len(NameColumn)):
        nameStat[str(NameColumn[i])] = str(StatusColumn[i])
    return nameStat


#################################################################################################

def runUbuntu():
    os.system("systemctl list-units --type=service |awk '{print $1,$4}' | sed -E 's/ +/,/g' > service.csv")


#################################################################################################

def formatTime(time_data):
    date, time = time_data.split('~')
    day, month, year = date.split('/')
    hour, minute, seconds = time.split(':')
    time_tuple = (year, month, day, hour, minute)
    return time_tuple


#################################################################################################

def formatJSON(service):
    service_data = {}
    split = service.split(",")
    for i in split:
        try:
            key, value = i.split(":")
            service_data[key] = value
        except:
            continue
    return service_data


#################################################################################################

def checkRange(date_data, date_range, range_index):
    for i in range(5):
        if (int(date_data[i]) >= int(min(date_range[range_index][i], date_range[range_index + 1][i])) and int(
                date_data[i]) <= int(max(date_range[range_index][i], date_range[range_index + 1][i]))):
            if i == 4:
                return True
        else:
            return False


#################################################################################################

def checkNew(date1, date2):
    if date1[0] > date2[0]: return 1
    if date1[0] < date2[0]: return 2
    # same year
    if date1[1] > date2[1]: return 1
    if date1[1] < date2[1]: return 2
    # same month
    if date1[2] > date2[2]: return 1
    if date1[2] < date2[2]: return 2
    # same day
    if date1[3] > date2[3]: return 1
    if date1[3] < date2[3]: return 2
    # same hour
    if date1[4] > date2[4]: return 1
    if date1[4] < date2[4]: return 2


#################################################################################################

def manualMode(range,p):
    # GUI will send 4 strings ,2 time ranges , [(year,month,day,hour,minute),(year,month,day,hour,minute),....] each pair is time range
    service_log = open('serviceList.txt', 'r')
    log_lines = service_log.readlines()
    line_data = []
    time_data = []  # format (year,month,day,hour,minute)
    serviceData = {}
    check0, check1, currentCheck, range1, range2 = 0, 0, 0, 0, 0
    service_json1, service_json2 = {}, {}
    for i in log_lines:
        currentCheck = 0
        line_data = i.split("~!~")
        date_data = formatTime(line_data[0])
        # first range
        if checkRange(date_data, range, 0) and not check0:
            service_json1 = formatJSON(line_data[1])
            check0 = 1
            currentCheck = 1
            range1 = date_data
        if not currentCheck:
            if checkRange(date_data, range, 2):
                service_json2 = formatJSON(line_data[1])
                check1 = 1
                range2 = date_data
        if check1 and check0:
            break
    if not check1 or not check0:
        p.PrintOutPut("Manual Mode: No LOGS in given time range!\n")
    else:
        newestLog = checkNew(range1, range2)
        service_json = (service_json1, service_json2) if newestLog == 1 else (service_json2, service_json1)
        statusLog(service_json[0], service_json[1], 0, 0,p)
        # (new,old,time ,mode)


#################################################################################################

def ReadCSVWindows():
    serviceData = read_csv("service.csv", skiprows=1)
    NameColumn = serviceData['DisplayName'].tolist()
    StatusColumn = serviceData['Status'].tolist()
    nameStat = {}
    for i in range(len(NameColumn)):
        nameStat[NameColumn[i]] = StatusColumn[i]
    return nameStat


#################################################################################################


def CheckOS():
    my_os = platform.system()
    if my_os == "Windows":
        os = 0
    else:
        os = 1
    return os


# Press the green button in the gutter to run the script.

#################################################################################################

def monitorMode(delay_time,p):  # enter your time in seconds, 0=windows | 1=linux
    run = 1  # run is 1 until the user stops the monitoring by leaving the interface(GUI) or presses the stop button.
    # In the GUI the user will enter the time in seconds(x) and then he presses start.
    os = CheckOS()
    # dd/mm/YY H:M:S
    serviceData_old = {}
    while (run):
        runOS(os)
        sleep(int(delay_time))
        serviceData_new = ReadCSVUbuntu() if os else ReadCSVWindows()
        # Here check for changes in the services:
        now = datetime.now()
        current_time = now.strftime("%d/%m/%Y~%H:%M:%S")
        temp = serviceData_old
        serviceData_old = serviceData_new
        serviceList(serviceData_new, current_time)
        statusLog(serviceData_new, temp, current_time, 1,p)


#################################################################################################

def serviceList(serviceData, current_time):
    f = open("serviceList.txt", "a")
    f.write(current_time + "~!~")
    for i in serviceData:
        f.write("" + i + ": " + serviceData[i] + " ,")
    f.write("\n")
    f.close()
    # format: 26/06/2022~07:58:25 name_service:running,


#################################################################################################

def statusLog(serviceData_new: dict, serviceData_old: dict, current_time, mode, p):
    # mode=1 Monitor mode, mode =0  manual mode.
    f = open("Status_Log.txt", "a")
    change = 0
    # Stopped working and status change
    for i in serviceData_old:
        old_state = serviceData_old[i]
        try:
            new_state = serviceData_new[i]
            if old_state != new_state:
                if old_state == 'Running' and new_state == 'Stopped':
                    string = current_time + ": "
                    if mode:
                        f.write(current_time + ": " + i + " Stopped running but still exist.\n")
                        p.PrintOutPut(current_time + ": " + i + " Stopped running but still exist.\n")
                        change = 1
                    else:
                        p.PrintOutPut("Manual Mode: " + i + " Stopped running but still exist.\n")
                        change = 1
                else:
                    if mode:
                        f.write(current_time + ": " + i + " Started running , not new service.\n")
                        p.PrintOutPut(current_time + ": " + i + " Started running , not new service.\n")
                        change = 1
                    else:
                        p.PrintOutPut("Manual Mode: " + i + " Started running , not new service.\n")
                        change = 1
        except:
            if mode:
                f.write(current_time + ": " + i + " Completely Not working anymore.\n")
                p.PrintOutPut(current_time + ": " + i + " Completely Not working anymore.\n")
                change = 1
            else:
                p.PrintOutPut("Manual Mode: " + i + " Completely Not working anymore.\n")
                change = 1
    # New service
    for i in serviceData_new:
        try:
            old_state = serviceData_old[i]
        except:
            if mode:
                f.write(current_time + ": " + i + " Completely new Service.\n")
                output = current_time + ": " + i + " Completely new Service.\n"
                p.PrintOutPut(output)
                change = 1
            else:
                p.PrintOutPut(i + " Completely new Service.\n")
                change = 1
    if change:
        f.write("\n")
    f.close()


#################################################################################################

def runOS(os):
    if not os:
        runWindows()
    else:
        runUbuntu()

#################################################################################################
