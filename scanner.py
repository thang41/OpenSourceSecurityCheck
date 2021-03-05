from pathlib import Path

class Scanner:

    def __init__(self, p):
        self.p = Path(p)

    def directory_file_iteration(self):
        filesFound = []
        for i in self.p.rglob("*"):
            if i.is_file():
                if self.keywordSearch(i):
                    filesFound.append(i)
        return filesFound
    
    def keywordSearch(self,i):

        #file_and_contents = {} # Dictionary decleration

        wordList = ['important','password','private','bank',
            'hidden','phone','credit','card','paypal',
            'email','backup','nude','hidden','porn',
            'finance','purchase','delete','mastercard',
            'visa','passport','identification',
            'username','login','ssn','security',
            'confidential','discover','secret','personal',
            'secure','registration','doctor','taxes',
            'financial','pin ','receipt','vin ','tax','resume',
            'doctor','medic','money','key']

        # if i.match("*.txt"): # Finding and reading in text files for keywords
        #     d = i.read_text()
        #     for word in wordList:
        #         if word in d.lower():
        #             print("Found:",word," In:",i,"Contents:",d)
        
        for word in wordList:
            if word in str(i.name).lower(): # checking filename
                if i:
                    return True

    def get_scanning(self):
        return self.directory_file_iteration()
        