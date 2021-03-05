import os
import win32api


def findDrives():
    #requires win23api import
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    print(drives)

findDrives()