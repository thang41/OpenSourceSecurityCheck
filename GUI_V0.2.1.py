import tkinter as tk
from tkinter import ttk, filedialog, END
import time, string, timer, scanner

class Application(tk.Frame):
    #directory = tk.StringVar()
    foundFiles = []
    folder_selected = ''
    
    def __init__(self, root):
        self.root = root
        self.initialize_user_interface()

    def initialize_user_interface(self):
        #Configuring root object of the application
        self.root.title("Open Source Security Check")
        self.windowWidth = 1460
        self.windowHeight = 840
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        self.xCordinate = int((self.screenWidth/2) - (self.windowWidth/2))
        self.yCordinate = int((self.screenHeight/2) - (self.windowHeight/2))
        self.root.geometry("{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, self.xCordinate, self.yCordinate))

        # Create a style
        self.style = ttk.Style(self.root)

        # Import the tcl file then Set the theme with the theme_use method
        self.root.tk.call('source', 'azure-dark.tcl')
        self.style.theme_use('azure-dark')

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

        # Frame for the Radiobuttons and entry 
        self.radioframe = ttk.LabelFrame(self.root, text='Scan Type', width=410, height=200)
        self.radioframe.place(x=10, y=10)

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
        self.entry.insert(0,"C:/")

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
        self.tempButton = ttk.Button(self.root, text='TEMP', command=self.insert_data)
        self.tempButton.place(x=190,y=220)

        # Notebook
        self.notebook = ttk.Notebook(self.root, width=1000, height=780)
        self.notebook.place(x=440,y=19)

        #Notebook tabs
        self.notebookTab1 = ttk.Frame(self.notebook,width=1000, height=780)
        self.notebook.add(self.notebookTab1, text='  Files  ')

        self.notebookTab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab2, text='  Treeview  ')

        self.notebookTab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.notebookTab3, text='  Other  ')

        # Treeview
        self.treeview = ttk.Treeview(self.notebookTab2,height=30)
        self.treeview.pack()

        self.treeview.column("#0",width=1000)
        
        self.treeview.heading("#0", text="File Categories", anchor='w')

        self.treeview.insert(parent='', index='end', iid=1, text="Text Files")
        self.treeview.insert(parent='', index='end', iid=2, text="Unknown Type")
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
        if self.checkRadiobutton() == 3:
            self.text.delete('1.0',END) # Remove what's currently in entry widget
            scan = scanner.Scanner(self.entry.get()) # creating scan object
            timer1 = timer.Timer()
            timer1.startTimer()

            foundFiles = scan.get_scanning()

            timer1.stopTimer()

            self.text.insert(tk.END,str(timer1.getTime()) + ' Seconds\n\n')
            
            for x in foundFiles:
                if x.match("*.txt"):
                    self.insert_data(x,1)
                else:
                    self.insert_data(x,2)

                self.text.insert(tk.END, str(x) +'\n')

    # Browse button function call           
    def browseButtonActions(self):
        folder_selected = filedialog.askdirectory()

        if len(folder_selected) > 0:
            self.entry.delete('0',END)
            self.entry.insert('0',folder_selected)

    # Inserting data into treeview
    def insert_data(self,file, parentNumber):         
        self.treeview.insert(parent=parentNumber, index='end', text=str(file))

app = Application(tk.Tk())
app.root.mainloop()        
