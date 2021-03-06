import tkinter as tk
from tkinter import ttk, filedialog, END, BOTH
import time, string, timer, scanner, os, pickle
from random import seed, random, choice
from scanner import Scanner



class Application(tk.Frame):
    #directory = tk.StringVar()
    foundFiles = []
    folder_selected = ''
    full_scan = False # for the popup message, but I commeneted out so no use atm
    files_Global = []
    keyWords_Global = []
    isAdmin = False

    def __init__(self, root):
        self.root = root
        self.initialize_user_interface()

    def initialize_user_interface(self):
        #Configuring root object of the application
        self.root.title("Open-Source Security Check")
        self.windowWidth = 1465
        self.windowHeight = 840
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        self.xCordinate = int((self.screenWidth/2) - (self.windowWidth/2))
        self.yCordinate = int((self.screenHeight/2) - (self.windowHeight/2))
        self.root.geometry("{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, self.xCordinate, self.yCordinate))

        # Create a style
        #self.style = ttk.Style(self.root)
        #self.root.configure(bg="gray26")

        # Import the tcl file then Set the theme with the theme_use method
        # self.root.tk.call('source', 'azure-dark.tcl')
        # self.style.theme_use('azure-dark')

        # Create control variables
        self.a = tk.IntVar()
        self.b = tk.IntVar(value=1)
        self.c = tk.IntVar()
        self.d = tk.IntVar(value=1)

        # Control Variables specifically for radiobuttons
        self.r0 = tk.IntVar()
        self.r1 = tk.IntVar()
        self.r2 = tk.IntVar(value=3)

        #e = tk.StringVar(value=option_list[1])
        self.f = tk.IntVar()
        self.g = tk.IntVar(value=75)
        self.h = tk.IntVar()

        #checkbox variable
        self.var1 = tk.IntVar()

        # Frame for the Radiobuttons and entry 
        self.radioframe = tk.LabelFrame(self.root, text='Scan Type', width=410, height=200)
        self.radioframe.place(x=10, y=10)
        #self.radioframe.configure(bg="gray26",)

        # Radiobuttons
        self.radio0 = ttk.Radiobutton(self.radioframe, text='Quick Scan', variable=self.d, value=1)
        self.radio0.place(x=20, y=20)
        self.radio1 = ttk.Radiobutton(self.radioframe, text='Deep Scan', variable=self.d, value=2)
        self.radio1.place(x=20, y=60)
        # self.radio2 = ttk.Radiobutton(self.radioframe, text='Partial Scan', variable=self.d, value=3)
        # self.radio2.place(x=20, y=100)

        # Entry
        self.entry = ttk.Entry(self.root, width=43)
        self.entry.place(x=132, y=166)
        self.entry.insert(0,"")

        # Browse Button
        self.browseButton = ttk.Button(self.root, text='Browse..', command=lambda: self.browseButtonActions()) # 
        self.browseButton.place(x=40,y=165)

        # Scan Button
        self.scanButton = ttk.Button(self.root, text='Scan',command=lambda:  self.scanButtonActions()) # lambda was needed to stop command from running automatically     
        self.scanButton.place(x=10,y=220)

        # export Button
        # self.exportButton = ttk.Button(self.root, text='Export',state=tk.DISABLED)
        # self.exportButton.place(x=170,y=220)

        # Exit Button
        self.exitButton = ttk.Button(self.root, text='Exit', command=self.root.destroy)
        self.exitButton.place(x=335,y=220)

        # Options BUTTON
        self.optionsButton = ttk.Button(self.root, text='Options', command=lambda: self.optionsMenu())
        self.optionsButton.place(x=90,y=220)

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=440,y=19)

        #Notebook tabs
        # self.notebookTab1 = ttk.Frame(self.notebook)
        # self.notebook.add(self.notebookTab1, text='  Data  ')

        self.notebookTab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab2, text='    Files    ')

        self.notebookTab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab3, text='  Report  ')

        # Scrollbar
        self.treeScroll = ttk.Scrollbar(self.notebookTab2)
        self.treeScroll.pack(side='right', fill='y')

        # Tree
        self.treeview = ttk.Treeview(self.notebookTab2,height=38, yscrollcommand=self.treeScroll.set)
        self.treeview.pack(side='left',fill='y')

        self.treeview.column("#0",width=1000)
        
        self.treeview.heading("#0", text="File Categories", anchor='w')

        self.treeScroll.config(command=self.treeview.yview)

        self.treeview.insert(parent='', index='end', iid=1, text="Documents" )
        self.treeview.insert(parent='', index='end', iid=2, text="Graphics")
        self.treeview.insert(parent='', index='end', iid=3, text="Multimedia")
        self.treeview.insert(parent='', index='end', iid=4, text="Archive")
        self.treeview.insert(parent='', index='end', iid=5, text="Executable")
        self.treeview.insert(parent='', index='end', iid=6, text="Other")
        self.treeview.insert(parent='', index='end', iid=7, text="Unknown")
        #self.treeview.item(1, open=True)

        self.iid = 3

        # Text Output Box
        self.textReportBox = tk.Text(self.notebookTab3, width=1000, height=780)
        self.textReportBox.place(x=0,y=0)

        self.treeScroll = ttk.Scrollbar(self.notebookTab3)
        self.treeScroll.pack(side='right', fill='y')

        #Information Frame
        self.infoframe = ttk.LabelFrame(self.root, text='Information', width=410, height=570)
        self.infoframe.place(x=10,y=260)

        self.lbl_1 = ttk.Label(self.infoframe, text=" ??? Quick scan will scan just filenames for keywords.  ")
        self.lbl_1.place(x=7,y=10)

        self.lbl_2 = ttk.Label(self.infoframe, text=" ??? Deep scan checks filenames and filedata for keywords and sensitive info.\n     ??? Time Consuming\n     ??? Checks file data for phone numbers, cc info, ssn, and emails")
        self.lbl_2.place(x=7,y=35)

        #self.lbl_3 = ttk.Label(self.infoframe, text=" ??? Partial scan allows you to define the directory.")
        #self.lbl_3.place(x=7, y=60)

        self.lbl_4 = ttk.Label(self.infoframe, text="Scan time: ")
        self.lbl_4.place(x=7, y=110)

        self.lbl_5 = ttk.Label(self.infoframe, text="Total Files: ")
        self.lbl_5.place(x=7, y=135)

        self.lbl_6 = ttk.Label(self.infoframe, text="Flagged files: ")
        self.lbl_6.place(x=7, y=160)
        # Bind our functions to the Treeview.
        self.treeview.bind("<Button-3>", self.preClick)
        self.treeview.bind("<Button-1>", self.onLeft)

        # Checkbox for flagged files
        self.flaggedCheckBox = ttk.Checkbutton(self.root, text="Flagged Files", variable=self.var1, onvalue=1, offvalue=0, command=lambda: self.checkboxActions())
        self.flaggedCheckBox.place(x=560,y=20)

    # Right Click menu
    def onRight(self, *args):
        # Here we fetch our X and Y coordinates of the cursor RELATIVE to the window
        cursorx = int(self.root.winfo_pointerx() - self.root.winfo_rootx())
        cursory = int(self.root.winfo_pointery() - self.root.winfo_rooty())

        # Now we define our right click menu canvas
        self.onRight_menu = tk.Canvas(self.root, width=150, height=50, highlightbackground="gray", highlightthickness=1)
        # And here is where we use our X and Y variables, to place the menu where our cursor is,
        # That's how right click menus should be placed.
        self.onRight_menu.place(x=cursorx, y=cursory)
        # This is for packing our options onto the canvas, to prevent the canvas from resizing.
        # This is extremely useful if you split your program into multiple canvases or frames
        # and the pack method is forcing them to resize.
        self.onRight_menu.pack_propagate(0)
        # Here is our label on the right click menu for deleting a row, notice the cursor
        # value, which will give us a pointy finger when you hover over the option.
        delLabel = tk.Label(self.onRight_menu, text="Ignore Directory", cursor="hand2", anchor="w")
        delLabel.pack(side="top", padx=1, pady=1, fill="x")

        # This function is for removing the canvas when an option is clicked.
        def destroy(self):
            self.onRight_menu.place_forget()

        # This is the function that removes the selected item when the label is clicked.
        def removeFromDir(*args):
            selection = self.treeview.focus()
            tempDict = self.treeview.item(selection)
            scan1 = scanner.Scanner()
            #scan1.ignoreThisDirectory(tempDict['pathParent'])
            
            try:
                self.onRight_menu.destroy()
            except Exception:
                pass    

        delLabel.bind("<Button-1>", removeFromDir)


    # This is to prevent infinite right click menus; it sees if there is an existing menu
    # and removes it, bringing it out in a new position.
    def preClick(self,*args):
        try:
            self.onRight_menu.place_forget()
            self.onRight()
        except Exception:
            self.onRight()

    # Hide menu when left clicking
    def onLeft(self, *args):
        try:
            self.onRight_menu.place_forget()
        except Exception:
            pass

    # Check Radiobutton selection
    def checkRadiobutton(self):
        if self.d.get() == 1:
            return 1
        elif self.d.get() == 2:
            return 2
        elif self.d.get() == 3:
            return 3
    
    # Scan button function call
    def scanButtonActions(self):
        self.clear_tree()
        scan = scanner.Scanner() 

        if self.checkRadiobutton() == 1:

            scan.setPath(self.entry.get())
            timer1 = timer.Timer()
            timer1.startTimer()
            files = scan.get_scanning("quick")
            self.files_Global = files

            timer1.stopTimer()

            self.lbl_4.config(text="Scan time: " + str(timer1.getTime()) + ' Seconds\n\n')

            # Inserting into tree
            self.writingToTree()
            
            # setting the total files scanned and flagged files labels in info box
            self.setfileCountLabels()

        if self.checkRadiobutton() == 2:
            
            #self.popupmsg("    This could take a very long time, continue?")
            #self.text.delete('1.0',END) # Remove what's currently in entry widget
            # creating scan object
            timer1 = timer.Timer()
            timer1.startTimer()

            scan.setPath(self.entry.get())
            files = scan.get_scanning("deep")
            self.files_Global = files

            timer1.stopTimer()

            self.lbl_4.config(text="Scan time: " + str(timer1.getTime()) + ' Seconds\n\n')

            # Inserting into tree
            self.writingToTree()
            
            # setting the total files scanned and flagged files labels in info box
            self.setfileCountLabels()
                
        if self.checkRadiobutton() == 3:
            files = scan.get_scanning("quick")
            #self.text.delete('1.0',END) # Remove what's currently in entry widget
            # creating scan object
            timer1 = timer.Timer()
            timer1.startTimer()

            scan.setPath(self.entry.get())
            files = scan.get_scanning()
            self.files_Global = files

            timer1.stopTimer()

            self.lbl_4.config(text="Scan time: " + str(timer1.getTime()) + ' Seconds\n\n')

            # Inserting into tree
            self.writingToTree()
            
            # setting the total files scanned and flagged files labels in info box
            self.setfileCountLabels()
      
        self.setTreeviewCounts()
        #self.setExportEnableOrDisable()
        
        # checks if user is on admin account or not
        self.checkIfAdmin()

        #this goes at bottom always
        self.writeToReport()

    # this is the main code for writing data to the treeview
    def writingToTree(self):
        self.clear_tree()
        
        if self.var1.get() == False:
            for file_ in self.files_Global:
                self.writingToTreeCall(file_)

        if self.var1.get() == True:
            for file_ in self.files_Global:
                if file_["flag"] == True:
                    self.writingToTreeCall(file_)
                else:
                    pass
        else:
            pass

        self.setTreeviewCounts()

    # this was necesarry to break up the code for the function above. Just made it look better
    def writingToTreeCall(self,file_):
        if file_["filetype"].lower() in (".doc", ".rtf", ".txt",".docx", ".pdf"):
            self.insert_data(file_,1)
            return
        if file_["filetype"].lower() in {".jpg",".png",".jpeg",".gif"}:
            self.insert_data(file_, 2)
            return
        if file_["filetype"].lower() in {".mp4",".mpeg", ".mov", ".mkv",".flv",".avi", ".webm", ".mp3", ".flav",".flak",".wmv"}:
            self.insert_data(file_, 3)
            return
        if file_["filetype"].lower() in {".zip", ".7z", ".gz", ".zipx", ".zz", ".s7z", ".rar"}:
            self.insert_data(file_, 4)
            return
        if file_["filetype"].lower() in {".exe", ".bat", ".bin", ".cmd"}:
            self.insert_data(file_, 5)
            return
        else:
            if file_["filetype"] != '': 
                
                self.insert_data(file_,6)
                return
            else:
                self.insert_data(file_,7)
                return

    # Inserting data into treeview
    def insert_data(self,file_, parentNumber):
        
        # if file_["flag"] == False:
        #     self.treeview.insert(parent=parentNumber, index='end', text=str(file_["filename"]))
        # else:
        ranNum = random()
        ranNum2 = random()
        
        self.treeview.insert(parent=parentNumber, iid=ranNum, index='end', text=str(file_["filename"]))
        for item in file_.items():
            if item[0] != "data":
                self.treeview.insert(parent=ranNum, index='end', text=str(item))
            if item[0] == "data":
                self.treeview.insert(parent=ranNum, id=ranNum2 , index='end', text="File Data", open=True)
                for key in file_["data"]:
                    if len(file_["data"][key]) < 1:
                        pass
                    else:
                        self.treeview.insert(parent=ranNum2, index='end', text= str(key) + ":   " + str(file_["data"][key]))                 

    # This will clear the tree so when you scan again, the items in the tree will disappear
    def clear_tree(self):
        children_count = 1
        try:
            while True:
                for x in self.treeview.get_children(children_count):
                    self.treeview.delete(x)
                children_count += 1
        except Exception:
            pass

    # checkbox so that you can filter all files by flagged
    def checkboxActions(self):
        self.writingToTree()

    # Write data to the text box widget
    # def writeToTextBox(self, files):
    #     for file_ in files:
    #         if file_["flag"] == True:
    #             self.text.insert(tk.END, str(file_["data"])+"\n")

    # This will add how many of a particular item was found and at it after the name such as "Text Files (4)" if it found 4 text files.
    def setTreeviewCounts(self):
        
        num1 = len(self.treeview.get_children(1))
        num2 = len(self.treeview.get_children(2))
        num3 = len(self.treeview.get_children(3))
        num4 = len(self.treeview.get_children(4))
        num5 = len(self.treeview.get_children(5))
        num6 = len(self.treeview.get_children(6))
        num7 = len(self.treeview.get_children(7))
        if num1 + num2 + num3 + num4 + num5 + num6 != 0:
            self.treeview.item(1, text='Documents ( ' + str("{:,}".format(num1)) +' )')
            self.treeview.item(2, text='Graphics ( ' + str("{:,}".format(num2)) +' )')
            self.treeview.item(3, text='Multimedia ( ' + str("{:,}".format(num3)) +' )')
            self.treeview.item(4, text='Archive ( ' + str("{:,}".format(num4)) +' )')
            self.treeview.item(5, text='Executable ( ' + str("{:,}".format(num5)) +' )')
            self.treeview.item(6, text='Other ( ' + str("{:,}".format(num6)) +' )')
            self.treeview.item(7, text='Unknown ( ' + str("{:,}".format(num7)) +' )')
        else:
            pass
    # Sets how many files have been found and how many were flagged
    def setfileCountLabels(self):
        totalFiles = 0
        flaggedFiles = 0
        totalFilesByLen = len(self.files_Global)
        for file_ in self.files_Global:
            totalFiles+=1
            if file_["flag"] == True:
                flaggedFiles+=1

        self.lbl_5.config(text="Total Files: "+ str("{:,}".format(totalFilesByLen)))
        self.lbl_6.config(text="Flagged Files: "+ str("{:,}".format(flaggedFiles)))

    # Browse button function call           
    def browseButtonActions(self):
        folder_selected = filedialog.askdirectory()

        if len(folder_selected) > 0:
            self.entry.delete('0',END)
            self.entry.insert('0',folder_selected)

    # Options Menu popup
    def optionsMenu(self):
        popup = tk.Tk()
        popup.title("Options")
        popupWidth = 800
        popupHeight = 600
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        xCordinate = int((screenWidth/2) - (popupWidth/2))
        yCordinate = int((screenHeight/2) - (popupHeight/2))
        popup.geometry("{}x{}+{}+{}".format(popupWidth, popupHeight, xCordinate, yCordinate))

        flag = False

        # Creating notebook widget
        notebook = ttk.Notebook(popup)
        notebook.pack(fill='x')

        #Notebook tabs
        notebookTab1 = ttk.Frame(notebook)
        notebook.add(notebookTab1, text='  Keywords  ')

        notebookTab2 = ttk.Frame(notebook)
        notebook.add(notebookTab2, text='    Ignored Directories    ')

        notebookTab3 = ttk.Frame(notebook)
        notebook.add(notebookTab3, text='  Ignored Filetypes  ')

        textBox = tk.Text(notebookTab1, height=600, width=800, borderwidth=2)
        textBox.pack(pady=(0,50))

        textBox2 = tk.Text(notebookTab2, height=600, width=800, borderwidth=2)
        textBox2.pack(pady=(0,50))

        textBox3 = tk.Text(notebookTab3, height=600, width=800, borderwidth=2)
        textBox3.pack(pady=(0,50))
        
        B1 = ttk.Button(popup, text="    Apply    ",state=tk.DISABLED, command=lambda: [writeToWordListFile(), writeToIgnoredDirFile(), writeToFileType(), setModifiedFalse(), popup.destroy()])
        B1.place(x=710,y=560)

        B2 = ttk.Button(popup, text="    Cancel    ", command=lambda: popup.destroy())
        B2.place(x=630,y=560) 

        try:
            wordList = pickle.load(open("word list.p", "rb"))
            #wordList = sorted(wordList)
        except EOFError:
            wordList = []
    
        try:
            ignoredDir = pickle.load(open("ignored directories.p", "rb"))
            #ignoredDir = sorted(ignoredDir)
        except EOFError:
            ignoredDir = []
        
        try:
            ignoredType = pickle.load(open("ignored filetypes.p", "rb"))
            #ignoredType = sorted(ignoredType)
        except EOFError:
            ignoredType = []

        if len(wordList) > 0:
            for word in wordList:
                textBox.insert(END, word + "\n")

        if len(ignoredDir) > 0:
            for directory in ignoredDir:
                textBox2.insert(END, directory + "\n")
        
        if len(ignoredType) > 0:
            for directory in ignoredType:
                textBox3.insert(END, directory + "\n")
        
        textBox.edit_modified(False)
        textBox2.edit_modified(False)
        textBox3.edit_modified(False)

        def setModifiedFalse():
            textBox.edit_modified(False)
            textBox2.edit_modified(False)
            textBox3.edit_modified(False)

        def writeToTextBox(self):
            pass

        def on_click(event):         
            if textBox.edit_modified():
                B1.config(state=tk.NORMAL)

            elif textBox2.edit_modified():
                B1.config(state=tk.NORMAL)
            
            elif textBox3.edit_modified():
                B1.config(state=tk.NORMAL)

        textBox.bind("<<Modified>>", on_click)
        textBox2.bind("<<Modified>>", on_click)
        textBox3.bind("<<Modified>>", on_click)

        def writeToWordListFile():
            try:
                keyword_contents = textBox.get(1.0, END)
                contents = keyword_contents.split('\n')
                contents = list(filter(len, contents))
                pickle.dump(contents, open("word list.p", "wb"))
            except:
                pass
        
        def writeToIgnoredDirFile():
            directory_contents = textBox2.get(1.0, END)
            contents = directory_contents.split('\n')
            contents = list(filter(len, contents))
            # try:
            #     for dir in contents:                
            #         index = contents.index(dir)
            #         contents[index] = os.path.normpath(dir)
            # except:
            #     pass

            pickle.dump(contents, open("ignored directories.p", "wb"))

        
        def writeToFileType():
            try:
                ignored_filetypes = textBox3.get(1.0, END)
                contents = ignored_filetypes.split('\n')
                contents = list(filter(len, contents))
            except:
                pass
           
            pickle.dump(contents, open("ignored filetypes.p", "wb"))

        popup.mainloop()

    # Pop up message for warning
    def popupmsg(self,msg):
        popup = tk.Tk()
        popup.title("Info")
        popupWidth = 250
        popupHeight = 100
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        xCordinate = int((screenWidth/2) - (popupWidth/2))
        yCordinate = int((screenHeight/2) - (popupHeight/2))
        popup.geometry("{}x{}+{}+{}".format(popupWidth, popupHeight, xCordinate, yCordinate))
        label = ttk.Label(popup, text=msg)
        label.pack()
        B1 = ttk.Button(popup, text=" Scan ", command=lambda: [self.popupmsgButtonActions(), popup.destroy()])
        B1.place(x=20,y=50)
        B2 = ttk.Button(popup, text=" Quit ", command=lambda: [popup.destroy()])
        B2.place(x=120,y=50)
        popup.mainloop()
    
    def popupmsgButtonActions(self):
        full_scan = True

    def optionsButtonActions(self):
        pass
    
    # def setExportEnableOrDisable(self):
    #     self.exportButton.config(state=tk.NORMAL)
    
    def getIfAdmin(self):
        scan = scanner.Scanner()
        scan.checkIfAdmin()
    
    def writeToReport(self):
        self.textReportBox.config(state=tk.NORMAL)
        self.textReportBox.delete("1.0","end")
        flagFile1 = ''
        flagFile2 = ''

        self.textReportBox.insert(tk.END, "We found files like '" + str(self.getFlaggedFile()) + "' and '" + str(self.getFlaggedFile())+"'")
        self.textReportBox.insert(tk.END, "\nThese are going to be typical files that a bad actor could search for and easily find.")
        
        try:
            email_data = self.getEmailsFromFlaggedFiles()
            self.textReportBox.insert(tk.END, "\n\nWe even found " + str(email_data[0]) + " email(s) some of which include " + str(email_data[1]))
        except:
            self.textReportBox.insert(tk.END, "\n\nLuckily, there were no emails found.")

        if self.isAdmin == True:
            self.textReportBox.insert(tk.END, "\n\nYou are using an admin account. This is not good security practice because if someone were to get on your machine, \nthey would have higher privalage access to more information and abilities.\nTry creating a regular account and only using admin account when necessary!")
        else:
            self.textReportBox.insert(tk.END, "\n\nYou are not using an admin account, which is great!")
        
        self.textReportBox.insert(tk.END, "\n\nSo, information was found. What can you do to help mitigate this? The top things you can do to make sure you are secure\non your own machine is the use of encryption software and password managers.")
        self.textReportBox.insert(tk.END, "\nEncryption software is software that will encrypt folders, files and drives. It takes the data and creates cipher text \nthat makes it unreadable unless you can decrypt it using a password. This is where a password manager comes into play.")
        self.textReportBox.insert(tk.END, "\n\nUsing a strong password is your first defense to security with most applications. Since humans aren't that great at \nremembering complex sudo random passwords so we tend to go with things that can be easily guesssed.\nThis is bad and opens you up to getting exploited, whether it's on your own personal\nmachine or on a website.")
        self.textReportBox.insert(tk.END, "\n\nEncryption: If you are using Windows, to keep things simple, try using Bitlocker to encrypt your drive. \nFind more information here: \n\thttps://en.wikipedia.org/wiki/BitLocker")
        self.textReportBox.insert(tk.END, "\n\nThis does not stop someone from gathering information once they are on your machine though. If you are logged in\nand you forget to lock your computer, anyone can access all of your data. What can you do about that?")
        self.textReportBox.insert(tk.END, "\nFor this, use a third-party software such as veracrypt. It's open-source so the code has been vetted, and you can\nuse it to encrypt individuale files and folders. Find more information here:\n\thttps://www.veracrypt.fr/en/Home.html")
        self.textReportBox.insert(tk.END, "\n\nNext, we have password managers. A password manager is an application that will provide you with an extremely\nhard to guess password, and has the ability to store those passwords for you. You then would only\nneed to remember the password to access the password manager, and let the rest of the passwords be handled by\nthe password manager. The use of a password manager allows you to easily manage and store mutliple passwords for different\nlogins/sites so that you aren't using the same one or similar ones for multiple logins.")
        self.textReportBox.insert(tk.END, "\n\nYou have mutliple options here, but the two most recommended and vetted are Bitwarden and LastPass.\nThere are also built in ones such as icloud Keychain for apple devices. Find more information here:\n\thttps://bitwarden.com/\n\thttps://www.lastpass.com/\n\thttps://en.wikipedia.org/wiki/Password_manager")
        self.textReportBox.insert(tk.END, "\n\nIn combination with all of these, try using a VPN when connecting to an unfamiliar network like McDonalds or Starbucks wifi.")
        self.textReportBox.insert(tk.END, "\n\nMore tips:\n\tWifi is less secure than a wired network\n\tKnow what you're installing. Don't agree to all terms and conditions when installing something.\n\tRemmember, don't use Admin as your main account.\n\tDon't respond to unknown emails.\n\tIf your browswer warns you a website isn't secure, be aware that it could be comprimised.\n\t")
        #self.textReportBox.config(state=tk.DISABLED)

    def getFlaggedFile(self):

        flagged_files = []

        for file_ in self.files_Global:
            if file_['flag'] == True and file_["data"]["filename"] != "":
                flagged_files.append(file_)
        
        try:
            flagFile = choice(flagged_files)
            return flagFile["filename"]
        except:
            return "NONE"
    
    def getEmailsFromFlaggedFiles(self):
        emails_found = []
        email_count = 0

        for file_ in self.files_Global:
            if file_["flag"] == True and len(file_["data"]["email"]) > 0:
                for email in file_["data"]["email"]:
                    emails_found.append(email)
            else:
                pass
                
        email_count = len(emails_found)
        if email_count > 0:
            email_data = [email_count, str(choice(emails_found))]
            return email_data
    

    def checkIfAdmin(self):
        self.isAdmin = Scanner.checkIfAdmin(self)

app = Application(tk.Tk())
app.root.mainloop()        