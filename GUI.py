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
import ServiceMonitor as service
from FileGuard import WatchDog
#################################################################################################

class Gui:
    def PrintOutPut(self, output):
        self.t.insert(END, output)

    #################################################################################################

    def ok(self):
        date1 = (self.date1_1.get("1.0", "end-1c"), self.date1_2.get("1.0", "end-1c"),
                 self.date1_3.get("1.0", "end-1c"), self.date1_4.get("1.0", "end-1c"),
                 self.date1_5.get("1.0", "end-1c"))
        date2 = (self.date2_1.get("1.0", "end-1c"), self.date2_2.get("1.0", "end-1c"),
                 self.date2_3.get("1.0", "end-1c"), self.date2_4.get("1.0", "end-1c"),
                 self.date2_5.get("1.0", "end-1c"))
        date3 = (self.date3_1.get("1.0", "end-1c"), self.date3_2.get("1.0", "end-1c"),
                 self.date3_3.get("1.0", "end-1c"), self.date3_4.get("1.0", "end-1c"),
                 self.date3_5.get("1.0", "end-1c"))
        date4 = (self.date4_1.get("1.0", "end-1c"), self.date4_2.get("1.0", "end-1c"),
                 self.date4_3.get("1.0", "end-1c"), self.date4_4.get("1.0", "end-1c"),
                 self.date4_5.get("1.0", "end-1c"))
        dates = [date1, date2, date3, date4]
        for d in dates:
            for t in d:
                if t == '':
                    messagebox.showwarning(title="warning", message="all the fields must be filled")
                    return False
        thread = Thread(target=service.manualMode, args=(dates,p))
        thread.start()

    #################################################################################################

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            os._exit(0)

    #################################################################################################

    def secToWait(self):
        sec = self.timeForMonitor.get("1.0", "end-1c")
        if sec == '':
            messagebox.showwarning(title="warning", message="you must enter a number")
        else:
            thread = Thread(target=service.monitorMode, args=(int(sec),p))
            thread.start()

    #################################################################################################

    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x500")

        #################################################################################################

        #################Output#################
        self.t = Text(self.root, height=15, width=70)
        self.t.grid(row=11, column=0, columnspan=9, rowspan=10)
        self.warning = Text(self.root, height=5, width=30)
        self.warning.grid(row=10, column=12, columnspan=2, rowspan=4)
        self.l = Label(self.root, text="Warnnings!")
        self.l.config(font=("Courier", 14))
        self.l.grid(row=9, column=12, columnspan=2, rowspan=4)
        self.l = Label(self.root, text="Log Output")
        self.l.config(font=("Courier", 14))
        self.l.grid(row=10, column=0, columnspan=9)
        # self.dateList = Button(self.root, text="dates", padx=10, pady=10, command=self.showList)
        # self.dateList.grid(row=1, column=1)

        #################################################################################################

        ################Buttoms####################
        self.okb = Button(self.root, text="manual", padx=20, pady=10, command=self.ok)
        self.okb.grid(row=9, column=3, columnspan=3)
        # self.manual = Button(self.root, text="manual", padx=15, pady=15, command=self.ok)
        # self.manual.grid(row=11, column=9, rowspan=1)
        self.monitor = Button(self.root, text="monitor", padx=15, pady=15, command=self.secToWait)
        self.monitor.grid(row=13, column=9, rowspan=1)
        ##############second to wait###############
        self.timeForMonitor = Text(self.root, height=1, width=10, bg="light yellow")
        self.timeForMonitor.grid(row=14, column=10)
        self.year = Label(self.root, text="second to wait:").grid(row=14, column=9)

        #################################################################################################

        #############start first date#################
        #####Text#####
        self.date1_1 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date1_2 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date1_3 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date1_4 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date1_5 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")

        #################################################################################################

        #####Label######
        self.year = Label(self.root, text="Enter start for first date:", bg="red", font=('Ariel', 9)).grid(row=1,
                                                                                                           column=3,
                                                                                                           columnspan=3)
        self.year = Label(self.root, text="Year").grid(row=2, column=0)
        self.year = Label(self.root, text="Month").grid(row=2, column=2)
        self.year = Label(self.root, text="Day").grid(row=2, column=4)
        self.year = Label(self.root, text="Hour").grid(row=2, column=6)
        self.year = Label(self.root, text="Minute").grid(row=2, column=8)

        #################################################################################################

        #####Location####
        self.date1_1.grid(row=2, column=1)
        self.date1_2.grid(row=2, column=3)
        self.date1_3.grid(row=2, column=5)
        self.date1_4.grid(row=2, column=7)
        self.date1_5.grid(row=2, column=9)
        #############end first date#################
        #####Text#####
        self.date2_1 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date2_2 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date2_3 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date2_4 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date2_5 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")

        #################################################################################################

        #####Label######
        self.year = Label(self.root, text="Enter end for first date:", bg="red", font=('Ariel', 9)).grid(row=3,
                                                                                                         column=3,
                                                                                                         columnspan=3)
        self.year = Label(self.root, text="Year").grid(row=4, column=0)
        self.year = Label(self.root, text="Month").grid(row=4, column=2)
        self.year = Label(self.root, text="Day").grid(row=4, column=4)
        self.year = Label(self.root, text="Hour").grid(row=4, column=6)
        self.year = Label(self.root, text="Minute").grid(row=4, column=8)
        #####Location####
        self.date2_1.grid(row=4, column=1)
        self.date2_2.grid(row=4, column=3)
        self.date2_3.grid(row=4, column=5)
        self.date2_4.grid(row=4, column=7)
        self.date2_5.grid(row=4, column=9)

        #################################################################################################

        #############start second date#################
        #####Text#####
        self.date3_1 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date3_2 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date3_3 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date3_4 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date3_5 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")

        #################################################################################################

        #####Label######
        self.year = Label(self.root, text="Enter start for the second date:", bg="red", font=('Ariel', 9)).grid(row=5,
                                                                                                                column=3,
                                                                                                                columnspan=3)
        self.year = Label(self.root, text="Year").grid(row=6, column=0)
        self.year = Label(self.root, text="Month").grid(row=6, column=2)
        self.year = Label(self.root, text="Day").grid(row=6, column=4)
        self.year = Label(self.root, text="Hour").grid(row=6, column=6)
        self.year = Label(self.root, text="Minute").grid(row=6, column=8)
        #####Location####
        self.date3_1.grid(row=6, column=1)
        self.date3_2.grid(row=6, column=3)
        self.date3_3.grid(row=6, column=5)
        self.date3_4.grid(row=6, column=7)
        self.date3_5.grid(row=6, column=9)

        #################################################################################################

        #############end second date#################
        #####Text#####
        self.date4_1 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date4_2 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date4_3 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date4_4 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        self.date4_5 = Text(self.root, height=1,
                            width=10,
                            bg="light yellow")
        #################################################################################################

        #####Label######
        self.year = Label(self.root, text="Enter end for the second date:", bg="red", font=('Ariel', 9)).grid(row=7,
                                                                                                              column=3,
                                                                                                              columnspan=3)
        self.year = Label(self.root, text="Year").grid(row=8, column=0)
        self.year = Label(self.root, text="Month").grid(row=8, column=2)
        self.year = Label(self.root, text="Day").grid(row=8, column=4)
        self.year = Label(self.root, text="Hour").grid(row=8, column=6)
        self.year = Label(self.root, text="Minute").grid(row=8, column=8)
        #####Location####
        self.date4_1.grid(row=8, column=1)
        self.date4_2.grid(row=8, column=3)
        self.date4_3.grid(row=8, column=5)
        self.date4_4.grid(row=8, column=7)
        self.date4_5.grid(row=8, column=9)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


#################################################################################################


if __name__ == '__main__':
    # print("cwd= ", os.getcwd())
    p = Gui()
    thread = Thread(target=WatchDog, args=(p,))
    thread.start()
    p.root.mainloop()
