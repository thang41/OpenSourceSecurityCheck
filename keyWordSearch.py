import os
import re # needed to test keywords in each string
import string

    
def iterateThroughFilesFolders(directory): # This will iterate through a chosen directory to get filenames
    fileListWithDirectory = []
    
 
    for root, path, file in os.walk(directory):
        for filename in file:
            if root[-2:-1] == '/':
                fileListWithDirectory.append(root+filename)
            else:
                fileListWithDirectory.append(root+"\\"+filename)
                
    return fileListWithDirectory
                

def keyWordSearch(x):
    foundFiles = []
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
                
                foundFiles.append(file)
                break 
            else:
                continue # Continues
    return foundFiles

def main(directory):
    filesFound = keyWordSearch(iterateThroughFilesFolders(directory))
    return filesFound

if __name__ == "__main__":
    main()
