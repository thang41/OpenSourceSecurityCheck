import tkinter as tk
from tkinter import ttk, filedialog, END
import time, string, timer, scanner

class Application(tk.Frame):
    #directory = tk.StringVar()
    foundFiles = []
    folder_selected = ''
    full_scan = False # for the popup message, but I commeneted out so no use atm
    files_Global = []

    def __init__(self, root):
        self.root = root
        self.initialize_user_interface()

    def initialize_user_interface(self):
        #Configuring root object of the application
        self.root.title("Open-Source Security Check")
        self.windowWidth = 1460
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
        self.radio1 = ttk.Radiobutton(self.radioframe, text='Full Scan', variable=self.d, value=2)
        self.radio1.place(x=20, y=60)
        self.radio2 = ttk.Radiobutton(self.radioframe, text='Partial Scan', variable=self.d, value=3)
        self.radio2.place(x=20, y=100)

        # Entry
        self.entry = ttk.Entry(self.root, width=43)
        self.entry.place(x=132, y=165)
        self.entry.insert(0,"")

        # Browse Button
        self.browseButton = ttk.Button(self.root, text='Browse..', command=lambda: self.browseButtonActions()) # 
        self.browseButton.place(x=40,y=165)

        # Scan Button
        self.scanButton = ttk.Button(self.root, text='Scan',command=lambda:  self.scanButtonActions()) # lambda was needed to stop command from running automatically     
        self.scanButton.place(x=10,y=220)

        # export Button
        self.exportButton = ttk.Button(self.root, text='Export',state=tk.DISABLED)
        self.exportButton.place(x=100,y=220)

        # Exit Button
        self.exitButton = ttk.Button(self.root, text='Exit', command=self.root.destroy)
        self.exitButton.place(x=335,y=220)

        # TEMP BUTTON
        self.tempButton = ttk.Button(self.root, text='Options', state=tk.DISABLED)
        self.tempButton.place(x=190,y=220)

        # Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.place(x=440,y=19)

        #Notebook tabs
        self.notebookTab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab1, text='  Data  ')

        self.notebookTab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab2, text='  File Types  ')

        self.notebookTab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab3, text='  Other  ')

        # Treeview
        self.treeview = ttk.Treeview(self.notebookTab2,height=38)
        self.treeview.pack()

        self.treeview.column("#0",width=1000)
        
        self.treeview.heading("#0", text="File Categories", anchor='w')

        self.treeview.insert(parent='', index='end', iid=1, text="Documents" )
        self.treeview.insert(parent='', index='end', iid=2, text="Graphics")
        self.treeview.insert(parent='', index='end', iid=3, text="Unknown")
        #self.treeview.item(1, open=True)

        self.iid = 3

        # Text Output Box
        self.text = tk.Text(self.notebookTab1, width=1000, height=780)
        self.text.place(x=0,y=0)

        #Information Frame
        self.infoframe = ttk.LabelFrame(self.root, text='Information', width=410, height=570)
        self.infoframe.place(x=10,y=260)

        self.lbl_1 = ttk.Label(self.infoframe, text=" • Quick scan will scan most used directories  ")
        self.lbl_1.place(x=7,y=10)

        self.lbl_2 = ttk.Label(self.infoframe, text=" • Full scan scans all drives and folders. - (Time Consuming)  ")
        self.lbl_2.place(x=7,y=35)

        self.lbl_3 = ttk.Label(self.infoframe, text=" • Partial scan allows you to define the directory.")
        self.lbl_3.place(x=7, y=60)

        self.lbl_4 = ttk.Label(self.infoframe, text="Scan time: ")
        self.lbl_4.place(x=7, y=100)

        self.lbl_5 = ttk.Label(self.infoframe, text="Files Scanned: ")
        self.lbl_5.place(x=7, y=125)
        # Bind our functions to the Treeview.
        self.treeview.bind("<Button-3>", self.preClick)
        self.treeview.bind("<Button-1>", self.onLeft)

        # Checkbox for flagged files
        self.flaggedCheckBox = ttk.Checkbutton(self.root, text="Flagged Files", variable=self.var1, onvalue=1, offvalue=0, command=lambda: self.checkboxActions())
        self.flaggedCheckBox.place(x=630,y=20)

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
            scan1.ignoreThisDirectory(tempDict['text'])
            
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
        if self.checkRadiobutton() == 1:
            self.popupmsg("    This could take a very long time, continue?")
            if full_scan:
                full_scan = False
            pass
        
        if self.checkRadiobutton() == 2:
            pass
                
        if self.checkRadiobutton() == 3:
            self.text.delete('1.0',END) # Remove what's currently in entry widget
            scan = scanner.Scanner() # creating scan object
            timer1 = timer.Timer()
            timer1.startTimer()

            scan.setPath(self.entry.get())
            files = scan.get_scanning()
            self.files_Global = files

            timer1.stopTimer()

            self.lbl_4.config(text="Scan time: " + str(timer1.getTime()) + ' Seconds\n\n')

            # Inserting into tree
            self.writingToTree()

            # Writing data to the textbox
            self.writeToTextBox(files)

            
            
            
        self.setTreeviewCounts()
    
    # This will only send the right files based on the checkbox 
    # def sendToTreeFuncForWriting(self):
       
    #     for file_ in self.files_Global:
    #         if self.checkboxActions():
    #             if file_["flag"]:
    #                 self.writingToTree(file_)
    #         if self.checkboxActions() == False:
    #             self.writingToTree(file_)
    #         else:
    #             pass

    # writing data to the tree
    def writingToTree(self):
        self.clear_tree()
        if self.var1.get() == True:
            for file_ in self.files_Global:
                if file_["filetype"] in (".doc", "rtf", ".txt"):
                    self.insert_data(file_["filename"],1)
                    continue

                if file_["filetype"] in {".jpg",".png",".jpeg",".gif"}:
                    self.insert_data(file_["filename"], 2)
                    continue

                else:
                    self.insert_data(file_["filename"],3)
                    continue

        if self.var1.get() == False:
            for file_ in self.files_Global:  
                if file_["filetype"] in (".doc", ".rtf", ".txt"):
                    self.insert_data(file_["filename"],1)
                    continue

                if file_["filetype"] in {".jpg",".png",".jpeg",".gif"}:
                    self.insert_data(file_["filename"], 2)
                    continue

                else:
                    self.insert_data(file_["filename"],3)
                    continue
        else:
            pass

        self.setTreeviewCounts()

    # checkbox so that you can filter all files by flagged
    def checkboxActions(self):
        self.writingToTree()

    # Write data to the text box widget
    def writeToTextBox(self, files):
        for file_ in files:
            if file_["flag"] == True:
                self.text.insert(tk.END, str(file_["data"])+"\n")
                

        

    # This will add how many of a particular item was found and at it after the name such as "Text Files (4)" if it found 4 text files.
    def setTreeviewCounts(self):
        
        num1 = len(self.treeview.get_children(1))
        num2 = len(self.treeview.get_children(2))
        num3 = len(self.treeview.get_children(3))
        totalFilesFound = num1 + num2 + num3
        self.treeview.item(1, text='Documents ( ' + str(num1) +' )')
        self.treeview.item(2, text='Graphics ( ' + str(num2) +' )')
        self.treeview.item(3, text='Unknown ( ' + str(num3) +' )')
        self.lbl_5.config(text="Files Scanned: "+ str(totalFilesFound))
        # self.treeview.insert("", index='end',iid=1,text="Test"+num)

    # Browse button function call           
    def browseButtonActions(self):
        folder_selected = filedialog.askdirectory()

        if len(folder_selected) > 0:
            self.entry.delete('0',END)
            self.entry.insert('0',folder_selected)

    # Inserting data into treeview
    def insert_data(self,file, parentNumber):         
        self.treeview.insert(parent=parentNumber, index='end', text=str(file))
    
    # This will clear the tree so when you scan again, the items in the tree will disappear
    def clear_tree(self):
        children_count = 1
        try:
            while True:
                for x in self.treeview.get_children(children_count):
                    self.treeview.delete(x)
                children_count += 1
        except Exception as e:
            pass
            
    # Pop up message
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
    
    # def popupmsgButtonActions(self):
    #     full_scan = True

    def optionsButtonActions(self):
        pass
    

        

app = Application(tk.Tk())
app.root.mainloop()        
