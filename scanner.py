from pathlib import Path
import re
class Scanner:

    ignored_directories = []

    def __init__(self, p):
        self.p = Path(p)

    def directory_file_iteration(self):
        self.readInDirectories()
        filesFound = []
        for i in self.p.rglob("*"):
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
            'finance','purchase','mastercard',
            'visa','passport','identification',
            'username','login','ssn','secur',
            'confidential','discover','secret','personal',
            'secure','registration','doctor','taxes',
            'financial','pin ','receipt','vin ','tax','resume',
            'doctor','medic','money','contact','sensitive']

        if i.match("*.txt"): # Finding and reading in text files for keywords
            try:
                d = i.read_text(encoding='utf-8')
                for word in wordList:
                    if word in d.lower():
                        pass
                        #print("Found:",word," In:",i,"Contents:",d)
                self.ssnSearch(d)
            except UnicodeDecodeError as e:
                print("Error:",e,"Can't read file:",i)
        
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
        f = open("ignored_dir.txt","r")
        for x in f:
            self.ignored_directories.append(x)
        f.close()

        for i in self.ignored_directories:
            print("Ignored dir:",i)
    
    def ignoreThisDirectory(self,i):
        f = open("ignore_dir.txt","w")
        f.write(i)
        f.close()


    def get_scanning(self):
        return self.directory_file_iteration()
        
    