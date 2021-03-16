from pathlib import Path
import re
import pickle

class Scanner:

    # word list. I might make this editable so someone can edit/add ones they want
    wordList = ['important','password','private','bank',
            'hidden','phone','credit card','paypal',
            'email','backup','nude','hidden','porn',
            'finance','purchase','mastercard','passport','identification',
            'username','login',
            'confidential','secret','personal',
            'secure','registration','doctor','taxes',
            'financial','receipt','taxes','resume',
            'doctor','medical','money','contact','sensitive']
    
    # this will store all of the file dictionsaries
    files = []


    p = ''


    def directory_file_iteration(self):
        ignored_directories = self.getIgnoredDirectories()
        
        for i in Path(self.p).rglob("*"):
            if str(i.parents[0]) in ignored_directories: # allow you to ignore certain directories
                pass
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
                    

                except UnicodeDecodeError:
                    pass            

    # searching for SSNs
    def ssnSearch(self,file_,fileContents):

        #ssn format: xxxxxxxxx or xxx-xx-xxxx      
        ssnFound = re.findall(r'(?<!\d)(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})(?!\d)', fileContents)

        strSSNFOUND = ""

        for ssn in ssnFound:
            strSSNFOUND = strSSNFOUND + " " + ssn
        
        if len(ssnFound) < 1:
            return file_
        else:
            file_["flag"] = True
            file_["data"]["ssn"] = file_["data"]["ssn"] + strSSNFOUND

            return file_
        
                
    
    # Ignore_dir.txt which will hold directories you want to ignore
    def getIgnoredDirectories(self):
        ignored_directories = []
        f = open("ignored directories.txt","r")
        for x in f:
            ignored_directories.append(x)
        f.close()

        return ignored_directories
    
    def ignoreThisDirectory(self,i):
        f = open("ignore_dir.txt","w")

        j = Path(i)
        
        
        f.write(str(j.parents[0]))
        f.close()
    
    # Setting path to scan
    def setPath(self,i):
        self.p = i

    def get_scanning(self):
        self.files = [] # removing all data in the files list
        self.directory_file_iteration()
        self.checkFileNames()
        self.readInTextFile()
        
        return self.files