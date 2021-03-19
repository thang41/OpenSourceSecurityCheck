from pathlib import Path
import re, pickle, os
import pickle

class Scanner:

    # word list. I might make this editable so someone can edit/add ones they want
    # wordList = ['important','password','private','bank',
    #         'hidden','phone','credit card','paypal',
    #         'email','backup','nude','hidden','porn',
    #         'finance','purchase','mastercard','passport','identification',
    #         'username','login',
    #         'confidential','secret','personal',
    #         'secure','registration','doctor','taxes',
    #         'financial','receipt','taxes',
    #         'doctor','medical','money','contact','sensitive']
    
    wordList = ""
    ignored_type = ""
    ignored_dir = ""
    
    # this will store all of the file dictionsaries
    files = []


    p = ''


    def directory_file_iteration(self):
        ignored_directories = self.getIgnoredDirectories()
        ignored_filetypes = self.getIgnoredFileTypes()
        
        for i in Path(self.p).rglob("*"):

            # If there are directories in the "ignored directories.p" file, then it will iterate through them to see if file should be ignored
            if len(ignored_directories) > 0:
               
                #for directory in ignored_directories:
                    #if directory in os.path.normpath(i.parents[0]):
                

                
                

                if os.path.normpath(i.parents[0]) in ignored_directories:
                    continue
                if Path(i).suffix in ignored_filetypes:
                    continue
                else: 
                    if i.is_file():
                        
                        fileDict = {"filename":i.name,"pathParent":i.parents[0],"fullPath":i, "filetype":Path(i).suffix, "flag":False, "data":{"filename":"","filecontents":"","ssn":"","phone":"","email":""}}
                        self.files.append(fileDict)
                    else:
                        continue
                            

            # if there are none in ignored directories.p it will run this  
            elif Path(i).suffix in ignored_filetypes:
                continue
            else:
                if i.is_file():
                    
                    fileDict = {"filename":i.name,"pathParent":i.parents[0],"fullPath":i, "filetype":Path(i).suffix, "flag":False, "data":{"filename":"","filecontents":"","ssn":"","phone":"","email":""}}
                    self.files.append(fileDict)  


    # checking to see if a keyword is in a filename
    def checkFileNames(self):
        for file_ in self.files:
            for word in self.wordList:
                if word.lower() in str(file_["filename"].lower()):
                    file_["flag"] = True
                    file_["data"]["filename"] = word


    # reading in .txt files and checking for keywords
    def readInTextFile(self):
        for file_ in self.files:
            if file_["filetype"] == ".txt":
                try: # trying to open the file, sometimes it won't read because it isn't always ascii characters. 
                    f = open(file_["fullPath"], "r")
                    fileContents = f.read()
                    f.close()
                    
                    # searching the contents of the file for keyword
                    for word in self.wordList:
                        if word in fileContents.lower():
                            file_["flag"] = True
                            file_["data"]["filecontents"] = file_["data"]["filecontents"] + " " + word
                    
                    # searching contents of file for SSN
                    file_ = self.ssnSearch(file_, fileContents)

                    # searching for phone numbers
                    file_ = self.phoneNumberSearch(file_, fileContents)

                    file_ = self.emailSearch(file_, fileContents)
                    

                except UnicodeDecodeError:
                    pass

    def emailSearch(self, file_, fileContents):
        emailFound = re.findall(r'[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+', fileContents)

        strEmailFound = ""

        for email in emailFound:
            strEmailFound = strEmailFound + " , " + email
        
        if len(emailFound) < 1:
            return file_
        
        else:
            file_["flag"] = True
            file_["data"]["email"] = file_["data"]["email"] + strEmailFound

    def phoneNumberSearch(self, file_, fileContents):  
        phoneFound = re.findall(r'(?<!\d)(?!000|.+0{4})(?:\d{10}|\d{3}-\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4}|\d{3}\s\d{3}\s\d{4}|\(\d{3}\)\s\d{3}\s\d{4})(?!\d)', fileContents)

        strPhoneFound = ""
        
        for phone in phoneFound:
            strPhoneFound = strPhoneFound + " , " + phone
        
        if len(phoneFound) < 1:
            return file_
        else:
            file_["flag"] = True
            file_["data"]["phone"] = file_["data"]["phone"] + strPhoneFound

            return file_

    # searching for SSNs
    def ssnSearch(self,file_,fileContents):

        #ssn format: xxxxxxxxx or xxx-xx-xxxx      
        ssnFound = re.findall(r'(?<!\d)(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})(?!\d)', fileContents)

        strSSNFOUND = ""

        for ssn in ssnFound:
            strSSNFOUND = strSSNFOUND + " , " + ssn
        
        if len(ssnFound) < 1:
            return file_
        else:
            file_["flag"] = True
            file_["data"]["ssn"] = file_["data"]["ssn"] + strSSNFOUND

            return file_
        
                
    
    # Ignore_dir.txt which will hold directories you want to ignore
    def getIgnoredDirectories(self):
        ignored_directories = pickle.load(open("ignored directories.p","rb"))
        return ignored_directories
    
    # Ignore the file types in this file such as .torrent, .txt
    def getIgnoredFileTypes(self):
        ignored_filetypes = pickle.load(open("ignored filetypes.p", "rb"))
        return ignored_filetypes
    
    # Setting path to scan
    def setPath(self,i):
        self.p = i
    
    def getWordList(self):
        self.wordList = pickle.load(open("word list.p", "rb"))

    def get_scanning(self):
        self.getWordList()
        self.files = [] # removing all data in the files list
        self.directory_file_iteration()
        self.checkFileNames()
        self.readInTextFile()
        
        return self.files
    
  

