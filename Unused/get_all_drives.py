import pathlib

def findDrives():
    driveList = ['a','b','c','d','e','f','g','h','i','j','k','l',
    'm','n','o','p','q','r','s','t','u','v','w','x','y','z']

    for drive in driveList:
        if pathlib.Path(drive + ":/").exists():
            print("Found drive:",drive)

findDrives()
