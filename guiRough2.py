import tkinter as tk
from tkinter import filedialog, Text
import os
import keyWordSearch
root = tk.Tk()

## Frame that will be where the content is shown post scan
frame = tk.Frame(root, bg="White")
frame.place(relwidth=0.8, relheight=0.6, relx=0.1, rely=0.1)

## create code to allow keyWordSearch.py to run when clicking Scan Files button
ScanFile = tk.Button(root, text="Scan Files", width =7, command = keyWordSearch.main,
                        height =2, fg="white", bg="grey")


## GRIDS

## CANVAS GRID
canvas = tk.Canvas(root, height=550, width=800, bg="Black")
canvas.grid()

## FRAME GRID
ScanFile.grid(row = 1, column = 0)
frame.grid(row = 0, column = 0)

## EXIT GRID

exitApp = tk.Button(root, text="Exit", width=7,  command = exit,
                        height = 2, fg="white", bg="blue")
exitApp.grid(row = 2, column = 0)



## create close when button clicked
root.mainloop()