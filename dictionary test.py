# dictionary test
from pathlib import Path

def ignore():
    fileList = {1:{"Name":"Brian","Age": "28","Sex":"Male"},
                2:{"Name":"Sabelyz","Age":"30", "Sex":"Female"}}

#    key = int,   filename = "test.jpg",   directory = c:/test.jpg"


    for key in fileList:
        print(key)


    print(fileList)



    for i, d in fileList.items():
        print("THis is the key", i)

        for key in d:
            print(key + ":", d[key])


def dictTest():
        p = "C:/Users/brian/Desktop/"
        
        tempDict = {}
        

        filesFound = []
        count = 1
        for i in Path(p).rglob("*"):           
            if i.is_file():
                tempDict = {"filename":i.name,"path":i.parents[0], "filetype":Path(i).suffix, "flag":False, "reason":"NA"}
                filesFound.append(tempDict)

                
                
        
        
        for fileDict in filesFound:
            if "bank" in fileDict["filename"]:
                fileDict["flag"] = True
                fileDict["reason"] = "bank"
        
        for i in filesFound:
            if i["flag"] == True:
                print(i["path"])


dictTest()