import os
import win32api # Used for the 'findDrives()' function. Not used though, but could be implemented here or somewhere else later
import re # needed to test keywords in each string

def findDrives():
    #make sure to import win32api at the top
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    print(drives)
    
def iterateThroughFilesFolders(): # This will iterate through a chosen directory to get filenames
    fileListWithDirectory = []
 
    for root, path, file in os.walk("C://"):
        for filename in file:
            if root[-2:-1] == '/':
                fileListWithDirectory.append(root+filename)
            else:
                fileListWithDirectory.append(root+'//'+filename)
                
    return fileListWithDirectory
                

def keyWordSearch(x):
    wordList = ['important','password','private','bank',
                'hidden','phone','credit','card','paypal',
                'email','backup','nude','hidden','porn',
                'finance','purchase','delete','mastercard',
                'visa','passport','identification',
                'username','login','ssn','security',
                'confidential','discover','secret','personal',
                'secure','registration','doctor','taxes',
                'financial','pin','receipt','vin','final']
   
    for file in x:
        base = os.path.basename(file) #removing the directory
        temp1 = os.path.splitext(base) # this takes the file name 'example.jpg' and splits it into a list ['example','.jpg']

        cleanFilename = re.sub('\W+',' ',temp1[0]) #using regex to remove special characters

        for word in wordList:
            if word in cleanFilename.lower():
                print('Possible Sensitive Files Found: '+ file)
                break 
            else:
                continue # Continues

def main():
    #findDrives()
    keyWordSearch(iterateThroughFilesFolders())


main()
