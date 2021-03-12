from pathlib import Path
import re
class Scanner:

    
    ignored_directories = []

    p = ''

    def __init__(self):
        pass

    def directory_file_iteration(self):
        self.readInDirectories()
        filesFound = []
        for i in Path(self.p).rglob("*"):
            if str(i.parents[0]) in self.ignored_directories: # allow you to ignore certain directories
                print("Ignored", i)
                pass
            else:
                if i.is_file():
                    if self.keywordSearch(i):
                        filesFound.append(i)
        return filesFound
    
    def keywordSearch(self,i):

        #file_and_contents = {} # Dictionary decleration

        wordList = ['important','password','private','bank',
            'hidden','phone','credit card','paypal',
            'email','backup','nude','hidden','porn',
            'finance','purchase','mastercard','passport','identification',
            'username','login',
            'confidential','secret','personal',
            'secure','registration','doctor','taxes',
            'financial','receipt','taxes','resume',
            'doctor','medical','money','contact','sensitive']

        if i.match("*.txt"): # Finding and reading in text files for keywords
            try:
                d = i.read_text(encoding='utf-8')
                for word in wordList:
                    if word in d.lower():
                        pass
                        #print("Found:",word," In:",i,"Contents:",d)
                self.ssnSearch(d)
            except UnicodeDecodeError as e:
                print(i.name,"couldn't be read.")
                # for word in wordList:
                #     if word in line:
                #         print("Found word", word,"in",i.name)
                
        
        for word in wordList:
            if word in str(i.name).lower(): # checking filename
                if i:
                    return True
            else:
                return True
    
    

    
    # searching for SSNs
    def ssnSearch(self,d):

        #ssn format: xxxxxxxxx or xxx-xx-xxxx      
        ssnFound = re.findall(r'(?<!\d)(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})(?!\d)', d)
        for i in ssnFound:
            if len(ssnFound) < 1:
                pass
            else:
                print("Possible SSN:",i)
    
    # Ignore_dir.txt which will hold directories you want to ignore
    def readInDirectories(self):
        f = open("ignore_dir.txt","r")
        print("IN read in directories:",f)
        for x in f:
            self.ignored_directories.append(x)
        f.close()

        for i in self.ignored_directories:
            print("Ignored dir:",i)
    
    def ignoreThisDirectory(self,i):
        f = open("ignore_dir.txt","w")

        j = Path(i)
        
        
        f.write(str(j.parents[0]))
        f.close()
    
    # Setting path to scan
    def setPath(self,i):
        self.p = i

    def get_scanning(self):
        return self.directory_file_iteration()
        
    