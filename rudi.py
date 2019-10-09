#!/usr/bin/env python3

###################################################
# Imports
###################################################
from tkinter import * # main gui library
from tkinter import ttk # extended gui widgets
from tkinter import filedialog # for save folder
import time # for default filenames with date
from os import path # for working cross platform with files/folders
import configparser # for working with settings files (.ini)

###################################################
# Initial Variables
###################################################
xpadding=5
ypadding=5
defaultfolder = path.expanduser('~')

###################################################
###################################################
# Definitions
###################################################
# startup
def preguiinit():
    initconfigfile()

def initconfigfile():
    global defaultfolder
    # if file does not exist, create it, populate it with defaults, and save it
    if not path.exists(path.join(path.dirname(path.realpath(__file__)), 'config.ini')):
        configfile = open(path.join(path.dirname(path.realpath(__file__)), 'config.ini'),"w+")
        # config parser stuff
        config = configparser.ConfigParser()
        config['SETTINGS'] = {'DefaultSaveFolder': defaultfolder}
        config.write(configfile)
        # close file
        configfile.close()
    # if file exists read settings in
    else:
        # read in configuration
        config = configparser.ConfigParser()
        config.read(path.join(path.dirname(path.realpath(__file__)), 'config.ini'))
        defaultfolder = config['SETTINGS']['defaultsavefolder']
        # update button text
        defaultworkingfolderButton.config(text=defaultfolder)

def savesettings():
    configfile = open(path.join(path.dirname(path.realpath(__file__)), 'config.ini'),"w")
    config = configparser.ConfigParser()
    config['SETTINGS'] = {'DefaultSaveFolder': defaultfolder}
    config.write(configfile)
    configfile.close()

# main program
def create():
    print(defaultfolder)
    start_ly_file()
    # scales()
    # endfile()

def start_ly_file():
    if filenameEntry.get():
        fillinsheet = path.join(defaultfolder, filenameEntry.get() + '.ly')
        keysheet = path.join(defaultfolder, filenameEntry.get() + '-key.ly')
    else:
        fillinsheet = path.join(defaultfolder, 'theory-sheet-' + time.strftime("%Y-%m-%d")  + '.ly')
        keysheet = path.join(defaultfolder, 'theory-sheet-key-' + time.strftime("%Y-%m-%d")  + '.ly')
    print(fillinsheet)
    print(keysheet)

# scales
def scales():
    if majorScaleVar.get() == 1:
        print("you asked for major scales")
    if minorScaleVar.get() == 1:
        print("you asked for minor scales")
    if modesScaleVar.get() == 1:
        print("you asked for modes")

# settings
def selectsavefolder():
    global defaultfolder
    print(defaultfolder)
    defaultfolder = filedialog.askdirectory(initialdir=defaultfolder)
    defaultworkingfolderButton.config(text=defaultfolder)

###################################################
###################################################

###################################################
# Main Window
###################################################
root = Tk()
root.title("Rudi 2")

###################################################
# Themeing
###################################################
style = ttk.Style()
# tabs
style.theme_create( "MyStyle", parent="alt", settings={
                                #    Left, Top, Right, Bottom
    "TNotebook": {"configure": {"tabmargins": [7, 0, 0, 0] }},
                                #      Sides, Height
    "TNotebook.Tab": {"configure": {"padding": [15, 3] }}})
style.theme_use("MyStyle")
# button
ttk.Style().configure("TButton", padding=6, background="#aaa")
# fonts
# this doesn't apple to tabs or buttons (ttk)
#root.option_add("*Font", "courier 20")

###################################################
# Frames
###################################################
mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
subframe = ttk.Frame(root)
subframe.grid(column=0, row=1, sticky=(E, S))
# expand frame with window resize
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

###################################################
# Tabs
###################################################
tab_parent = ttk.Notebook(mainframe)
tab_parent.grid(column=1, row=1, sticky=(W, E))
# these are the tabs
welcometab = ttk.Frame(tab_parent)
basicstab = ttk.Frame(tab_parent)
scalestab = ttk.Frame(tab_parent)
intervalstab = ttk.Frame(tab_parent)
chordstab = ttk.Frame(tab_parent)
cadencestab = ttk.Frame(tab_parent)
settingstab = ttk.Frame(tab_parent)
# add the previous tabs to the window with titles
tab_parent.add(welcometab, text="Start")
tab_parent.add(basicstab, text="Basics")
tab_parent.add(scalestab, text="Scales")
tab_parent.add(intervalstab, text="Intervals")
tab_parent.add(chordstab, text="Chords")
tab_parent.add(cadencestab, text="Cadences")
tab_parent.add(settingstab, text="Settings")
# expand tab frame to size of window?
tab_parent.pack(expand=1, fill='both')

###################################################
# button
###################################################
button_parent = ttk.Button(subframe, text='Create', command=create)
button_parent.grid(column=2, row=0)
# output filename
filenameLabel = Label(subframe, text="Filename:")
filenameLabel.grid(row=0, column=0)
filenameEntry = Entry(subframe, width=50)
filenameEntry.grid(row=0, column=1, padx=5)

###################################################
# Start tab widgets
###################################################
titleLabel = Label(welcometab, text="Title:")
titleLabel.grid(row=0, column=0, padx=xpadding, pady=ypadding)
titleEntry = Entry(welcometab, width=50)
titleEntry.grid(row=0, column=1, padx=xpadding, pady=ypadding)

copyrightLabel = Label(welcometab, text="Copyright:")
copyrightLabel.grid(row=1, column=0, padx=xpadding, pady=ypadding)
copyrightEntry = Entry(welcometab, width=50)
copyrightEntry.grid(row=1, column=1, padx=xpadding, pady=ypadding)

###################################################
# Scales tab widgets
###################################################
majorScaleVar = IntVar()
majorScaleCheckBox = Checkbutton(scalestab, text = "Major Scales", variable = majorScaleVar, onvalue = 1, offvalue = 0, height=1)
majorScaleCheckBox.grid(row=0, column=0, sticky=W)

minorScaleVar = IntVar()
minorScaleCheckBox = Checkbutton(scalestab, text = "Minor Scales", variable = minorScaleVar, onvalue = 1, offvalue = 0, height=1)
minorScaleCheckBox.grid(row=1, column=0, sticky=W)

modesScaleVar = IntVar()
modesScaleCheckBox = Checkbutton(scalestab, text = "Modes", variable = modesScaleVar, onvalue = 1, offvalue = 0, height=1)
modesScaleCheckBox.grid(row=2, column=0, sticky=W)

###################################################
# Settings tab widgets
###################################################
fontLabel = Label(settingstab, text="Font:")
fontLabel.grid(row=0, column=0, padx=xpadding, pady=ypadding)
fontEntry = Entry(settingstab, width=50)
fontEntry.grid(row=0, column=1, padx=xpadding, pady=ypadding)

deletefilesVar = IntVar()
deletefilesCheckBox = Checkbutton(settingstab, text = "Delete intermediate files", variable = deletefilesVar, onvalue = 1, offvalue = 0, height=1)
deletefilesCheckBox.grid(row=1, column=0, sticky=W)

defaultworkingfolderLabel = Label(settingstab, text="Default Save Folder:")
defaultworkingfolderLabel.grid(row=2, column=0, padx=xpadding, pady=ypadding)
defaultworkingfolderButton = ttk.Button(settingstab, text=defaultfolder, command=selectsavefolder)
defaultworkingfolderButton.grid(row=2, column=1, padx=xpadding, pady=ypadding)

# this must be the last entry
savebuttonButton = ttk.Button(settingstab, text='Save Settings', command=savesettings)
savebuttonButton.grid(row=3, column=0, padx=xpadding, pady=ypadding)

###################################################
# this starts the main program
###################################################
preguiinit()
root.mainloop()