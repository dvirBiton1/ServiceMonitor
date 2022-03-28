# Authors David Ehevich & Dvir Biton
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import os
from tkinter import *


#################################################################################################
class WatchDog():
    #################################################################################################
    p=None
    def __init__(self,p):
        self.p=p
        patterns = ["*"]
        ignore_patterns = None
        ignore_directories = False
        case_sensitive = True
        my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        my_event_handler.on_modified = self.modified
        my_event_handler.on_moved = self.moved
        path = os.getcwd()
        go_recursively = True
        my_observer = Observer()
        my_observer.schedule(my_event_handler, path, recursive=go_recursively)
        my_observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()

    # Watch dog event handler
    #################################################################################################

    def slicePath(self, path):
        retPath = ""
        for i in range(len(path) - 1, 0, -1):
            if path[i] == '\\':
                break
            else:
                retPath = retPath + path[i]
        return retPath[::-1]

    #################################################################################################

    def modified(self, event):
      #if self.slicePath(event.src_path)=="service.csv" or "FileGuard.py" or "GUI.py" or "ServiceList.py" or "key.key" or  "EncDec.py" or "Status_Log.txt" or "ServiceMonitor.py":
        self.p.warning.insert(END, f"{self.slicePath(event.src_path)} has been modified\n")

    #################################################################################################

    def moved(self, event):

        self.p.warning.insert(END, f"file moved {event.src_path} to {event.dest_path}")

    #################################################################################################
