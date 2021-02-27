import tkinter as tk
from tkinter import ttk
import keyWordSearch
import time
from tkinter import *
import string

root = tk.Tk()
root.title('Scan Parameters')


# Declaring variables
# for storing directory and other things
directory=tk.StringVar()
foundFiles = []


# Check Radiobutton selection
def checkRadiobutton():
    if d.get() == 1:
        return 1
    elif d.get() == 2:
        return 2
    elif d.get() == 3:
        return 3
        
# scan button function call
def multipleActions():

    testint = 1

    if checkRadiobutton() == 3:

        text.delete('1.0', END)
        #time_start = time.clock()
        foundFiles = keyWordSearch.main(entry.get())
        #time_end = time.clock()

        #text.insert(tk.END,str(time_end-time_start) + ' Seconds\n\n')
        
        for x in foundFiles:
            text.insert(tk.END, x +'\n')
        
   
        


# Place the window in the center of the screen
windowWidth = 1600
windowHeight = 900
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
xCordinate = int((screenWidth/2) - (windowWidth/2))
yCordinate = int((screenHeight/2) - (windowHeight/2))
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, xCordinate, yCordinate))

# Create a style
style = ttk.Style(root)

# Import the tcl file
root.tk.call('source', 'azure-dark.tcl')

# Set the theme with the theme_use method
style.theme_use('azure-dark')

# Create control variables
a = tk.IntVar()
b = tk.IntVar(value=1)
c = tk.IntVar()
d = tk.IntVar(value=1)

# Control Variables specifically for radiobuttons
r0 = tk.IntVar()
r1 = tk.IntVar()
r2 = tk.IntVar(value=3)

#e = tk.StringVar(value=option_list[1])
f = tk.IntVar()
g = tk.IntVar(value=75)
h = tk.IntVar()

# Create a Frame for the Radiobuttons and entry 
radioframe = ttk.LabelFrame(root, text='Scan Type', width=410, height=160)
radioframe.place(x=10, y=10)

# Radiobuttons
radio0 = ttk.Radiobutton(radioframe, text='Quick Scan', variable=d, value=1)
radio0.place(x=20, y=20)
radio1 = ttk.Radiobutton(radioframe, text='Full Scan', variable=d, value=2)
radio1.place(x=20, y=60)
radio2 = ttk.Radiobutton(radioframe, text='Partial Scan', variable=d, value=3)
radio2.place(x=20, y=100)

# Entry
entry = ttk.Entry(root, width=35, textvariable = directory)
entry.place(x=150, y=123)
entry.insert(0,"C:\\example\\")

# Scan Button
scanButton = ttk.Button(root, text='Scan',command=lambda:  multipleActions()) # lambda was needed to stop command from running automatically
scanButton.place(x=10,y=180)

# Quit Button
quitButton = ttk.Button(root, text='Quit', command=root.destroy)
quitButton.place(x=100,y=180)

### Text Output Frame
##textFrame = ttk.LabelFrame(root, text='Scan Output', height=755, width=1000)
##textFrame.place(x=550, y=10)
##
### Text Output Box
##text = tk.Text(textFrame, height=48, width=164)
##text.place(x=5,y=3)

# Notebook
notebook = ttk.Notebook(root, width=900, height=780)


notebookTab1 = ttk.Frame(notebook, width=350, height=150)
notebook.add(notebookTab1, text='  Files  ')
notebookTab2 = ttk.Frame(notebook, width=350, height=150)
notebook.add(notebookTab2, text='Passwords')
notebookTab3 = ttk.Frame(notebook, width=350, height=150)
notebook.add(notebookTab3, text='  Other  ')
notebook.place(x=440,y=19)

# Text Output Box
text = tk.Text(notebookTab1, height=100, width=700)
text.place(x=0,y=0)


#Information Frame
infoframe = ttk.LabelFrame(root, text='Information', width=410, height=600)
infoframe.place(x=10,y=230)

# Information Labels
radiolbl = ttk.Label(infoframe, text="Scan Type", font=('',10))
radiolbl.place(x=4,y=5)

lbl_1 = ttk.Label(infoframe, text=" • Full scan scans all drives and folders.\n  ", font=('',10))
lbl_1.place(x=5,y=30)

lbl_2 = ttk.Label(infoframe, text=" • Quick scan will scan most used folders/files.  ", font=('',10))
lbl_2.place(x=5,y=55)

lbl_3 = ttk.Label(infoframe, text=" • Partial scan allows you to define the directory.", font=('',10))
lbl_3.place(x=5, y=80)






root.mainloop()
