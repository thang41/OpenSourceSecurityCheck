from pathlib import Path
import re, pickle, os
import pickle

class Scanner:
   
    wordList = ""
    ignored_type = ""
    ignored_dir = ""
    
    # this will store all of the file dictionsaries
    files = []

    # This is the path that will be scanned
    p = ''

    # The code that iterates through the path from above
    def directory_file_iteration(self):
        ignored_directories = self.getIgnoredDirectories()
        ignored_filetypes = self.getIgnoredFileTypes()
        
        for i in Path(self.p).rglob("*"):

            # If there are directories in the "ignored directories.p" file, then it will iterate through them to see if file should be ignored
            if len(ignored_directories) > 0:            
        
                # If the path of the file is in the ignored directories file, it will move to the next file
                if os.path.normpath(i.parents[0]) in ignored_directories:
                    continue
                # if the file type of the file is in the ignored filetypes, it will move to the next file
                if Path(i).suffix.lower() in ignored_filetypes or len(Path(i).suffix) == 0 and "none" in ignored_filetypes:
                    continue

                # if it passes both, it will check if it's actually a file
                else: 
                    if i.is_file():
                        # creating a file dictionary of attributes
                        fileDict = {"filename":i.name,"pathParent":i.parents[0],"fullPath":i, "filetype":Path(i).suffix, "flag":False, "data":{"filename":"","filecontents":"","ssn":"","phone":"","email":"", "cc":""}}
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
                print(file_["filename"])
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

                    # searching for emails
       
                    file_ = self.emailSearch(file_, fileContents)

                    # searching for credit cards
                  
                    file_ = self.ccSearch(file_, fileContents)
                    

                except UnicodeDecodeError:
                    pass
    def ccSearch(self, file_, fileContents):
        
        ccAmexFound = re.findall(r'(?<!\d)3[47][0-9]{13}$(?!\d)', fileContents)
        ccVisaFound = re.findall(r'(?<!\d)4[0-9]{12}(?:[0-9]{3})?(?!\d)', fileContents)
        ccMasterCardFound = re.findall(r'(?<!\d)(5[1-5][0-9]{14}|2(22[1-9][0-9]{12}|2[3-9][0-9]{13}|[3-6][0-9]{14}|7[0-1][0-9]{13}|720[0-9]{12}))(?!\d)', fileContents)

        strAmex = ''
        strVisa = ''
        strMaster = ''

        for card in ccAmexFound:
            strAmex = strAmex + " , Amex " + str(card)
        
        for card in ccVisaFound:
            strVisa = strVisa + " , Visa " + str(card)
        
        for card in ccMasterCardFound:
            strMaster = strMaster + " , Master " + str(card)
        
        if len(strAmex) + len(strVisa) + len(strMaster) < 1:
            return file_
        
        else:
            ccFound = str(strAmex) + str(strVisa) + str(strMaster)
            try:
                file_["flag"] = True
            except:
                pass
            
            file_["data"]["cc"] = file_["data"]["cc"] + ccFound
            return file_

    def emailSearch(self, file_, fileContents):
        emailFound = re.findall(r'[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+', fileContents)

        strEmailFound = ""

        for email in emailFound:
            strEmailFound = strEmailFound + " , " + email
        
        if len(emailFound) < 1:
            return file_
        
        else:
            try:
                file_["flag"] = True
            except:
                pass
            file_["data"]["email"] = file_["data"]["email"] + strEmailFound
           
            return file_

    def phoneNumberSearch(self, file_, fileContents):  
        phoneFound = re.findall(r'(?<!\d)(?!000|.+0{4})(?:\d{10}|\d{3}-\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4}|\d{3}\s\d{3}\s\d{4}|\(\d{3}\)\s\d{3}\s\d{4})(?!\d)', fileContents)

        strPhoneFound = ""
        
        for phone in phoneFound:
            strPhoneFound = strPhoneFound + " , " + phone
        
        if len(phoneFound) < 1:
            return file_
        else:
            try:
                file_["flag"] = True
            except:
                pass
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
            try:
                file_["flag"] = True
            except:
                pass
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
    
    def checkIfAdmin(self):
        if 'logonserver' in os.environ:
            server = os.environ['logonserver'][2:]
        else:
            server = None

        def if_user_is_admin(Server):
            groups = win32net.NetUserGetLocalGroups(Server, os.getlogin())
            isadmin = False
            for group in groups:
                if group.lower().startswith('admin'):
                    isadmin = True
            return isadmin, groups


        # Function usage
        is_admin, groups = if_user_is_admin(server)

        # Result handeling
        if is_admin == True:
            print('You are an admin user!')
        else:
            print('You are not an admin user.')
        print('You are in the following groups:')
        for group in groups:
            print(group)

        sleep(10)
        #if error: no module named win32api, run these lines in cmd
        #pip uninstall pipywin32
        #pip uninstall pywin32
        #pip install pywin32

    def get_scanning(self, scan_type):

        if scan_type == "quick":
         
            self.getWordList()
            self.files = [] # removing all data in the files list
            self.directory_file_iteration()
            self.checkFileNames()
        else:
            self.getWordList()
            self.files = [] # removing all data in the files list
            self.directory_file_iteration()
            self.checkFileNames()
            self.readInTextFile()
        
        return self.files
    
  

