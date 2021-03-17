import pickle


wordList = pickle.load(open("word list.p", "rb"))


print("Word list:",wordList)


for word in wordList:
    print(word)