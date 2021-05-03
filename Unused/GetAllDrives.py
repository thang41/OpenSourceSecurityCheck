def findDrives():
    #make sure to import win32api at the top
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    print(drives)

