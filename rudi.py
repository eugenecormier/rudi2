#!/usr/bin/env python3

###################################################
# Imports
###################################################
from tkinter import *  # main gui library
from tkinter import ttk  # extended gui widgets
from tkinter import filedialog  # for save folder
import time  # for default filenames with date
from os import path  # for working cross platform with files/folders
import configparser  # for working with settings files (.ini)
# my data files
import headers

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
        config['SETTINGS'] = {'DefaultSaveFolder': defaultfolder,
                              'DeleteTempFiles': 0,
                              'DefaultFont': '',
                              'RightJustify': 1,
                              'BottomJustify': 1,
                              'LastBottomJustify': 1,
                              'PaperSize': 'Letter',
                              'PaperOrientation': 'Portrait'}
        config.write(configfile)
        # close file
        configfile.close()
    # if file exists read settings in
    else:
        # read in configuration
        config = configparser.ConfigParser()
        config.read(path.join(path.dirname(path.realpath(__file__)), 'config.ini'))
        defaultfolder = config['SETTINGS']['defaultsavefolder']
        deletefilesVar.set(config['SETTINGS']['deletetempfiles'])
        fontEntry.insert(END, config['SETTINGS']['defaultfont'])
        rightjustVar.set(config['SETTINGS']['rightjustify'])
        bottomjustifyVar.set(config['SETTINGS']['bottomjustify'])
        lastbottomjustifyVar.set(config['SETTINGS']['lastbottomjustify'])
        papersizeVar.set(config['SETTINGS']['papersize'])
        paperorientationVar.set(config['SETTINGS']['paperorientation'])
        # update button text
        defaultworkingfolderButton.config(text=defaultfolder)


def savesettings():
    configfile = open(path.join(path.dirname(path.realpath(__file__)), 'config.ini'),"w")
    config = configparser.ConfigParser()
    config['SETTINGS'] = {'DefaultSaveFolder': defaultfolder,
                          'DeleteTempFiles': deletefilesVar.get(),
                          'DefaultFont': fontEntry.get(),
                          'RightJustify': rightjustVar.get(),
                          'BottomJustify': bottomjustifyVar.get(),
                          'LastBottomJustify': lastbottomjustifyVar.get(),
                          'PaperSize': papersizeVar.get(),
                          'PaperOrientation': paperorientationVar.get()}
    config.write(configfile)
    configfile.close()

# main program ########################################
def create():
    docfont,docboldfont = initcustomfonts()
    worksheetfile,keysheetfile = start_ly_file(docfont,docboldfont)
    # scales()
    endfile(worksheetfile,keysheetfile)
#######################################################

def initcustomfonts():
    if fontEntry.get() != '':
        return '\override #\'(font-name . "' + fontEntry.get() + '") ','\override #\'(font-name . "' + fontEntry.get() + ' Bold") '
    else:
        return '','\\bold'

def start_ly_file(docfont,docboldfont):
    # setup filenames
    if filenameEntry.get():
        worksheetfilename = path.join(defaultfolder, filenameEntry.get() + '-worksheet.ly')
        keysheetfilename = path.join(defaultfolder, filenameEntry.get() + '-keysheet.ly')
    else:
        worksheetfilename = path.join(defaultfolder, 'theory-worksheet-' + time.strftime("%Y-%m-%d")  + '.ly')
        keysheetfilename = path.join(defaultfolder, 'theory-keysheet-' + time.strftime("%Y-%m-%d")  + '.ly')
    # open files for writing
    worksheetfile = open(worksheetfilename, 'w')
    keysheetfile = open(keysheetfilename, 'w')
    # set up header variables
    # titles
    if titleEntry.get() != '':
        doctitle = titleEntry.get()
    else:
        doctitle = 'Preliminary Rudiments Worksheet'
    # copyright
    if copyrightEntry.get() !='':
        doctag = copyrightEntry.get()
    else:
        doctag = 'Created by rudi v2.0'
    # right justify section
    #if rightjustVar.get() ='':



    # write the header to file
    worksheetfile.writelines(headers.lilypondheader.format(title=doctitle,font=docfont,boldfont=docboldfont,tag=doctag,keytitle=''))
    keysheetfile.writelines(headers.lilypondheader.format(title=doctitle,font=docfont,boldfont=docboldfont,tag=doctag,keytitle='\with-color #red Key'))
    # return the sheet filenames for subsequent writes
    return worksheetfile,keysheetfile

# scales
def scales():
    if majorScaleVar.get() == 1:
        print("you asked for major scales")
    if minorScaleVar.get() == 1:
        print("you asked for minor scales")
    if modesScaleVar.get() == 1:
        print("you asked for modes")

def endfile(worksheetfile,keysheetfile):
    worksheetfile.close()
    keysheetfile.close()



# settings
def selectsavefolder():
    global defaultfolder
    defaultfolder = filedialog.askdirectory(initialdir=defaultfolder)
    defaultworkingfolderButton.config(text=defaultfolder)

###################################################
###################################################

###################################################
# Main Window
###################################################
root = Tk()
root.title("Rudi 2")
# the following block hides hidden folders in the folder picker
try:
    # call a dummy dialog with an impossible option to initialize the file
    # dialog without really getting a dialog window; this will throw a
    # TclError, so we need a try...except :
    try:
        root.tk.call('tk_getOpenFile', '-foobarbaz')
    except TclError:
        pass
    # now set the magic variables accordingly
    root.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    root.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
except:
    pass

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
tab_parent = ttk.Notebook(mainframe, padding="2 5 2 5")
tab_parent.grid(row=0, column=0, sticky=(N, W, E))
# these are the tabs
welcometab = ttk.Frame(tab_parent)
basicstab = ttk.Frame(tab_parent)
scalestab = ttk.Frame(tab_parent)
intervalstab = ttk.Frame(tab_parent)
chordstab = ttk.Frame(tab_parent)
cadencestab = ttk.Frame(tab_parent)
settingstab = ttk.Frame(tab_parent)
settingstab.grid(column=0, row=0, sticky=(W, E))
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
# document settings frame
docframe = ttk.LabelFrame(settingstab, text='Document Settings', relief=GROOVE, borderwidth=2)
docframe.grid(row=0, column=0, sticky=(N, W, S, E), padx=xpadding, pady=ypadding)
rowvar = 0

# font
fontLabel = Label(docframe, text="Font:")
fontLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
fontEntry = Entry(docframe, width=50)
fontEntry.grid(row=rowvar, column=1, sticky=(W), padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

# paper size
papersizeLabel = Label(docframe, text="Page Size:")
papersizeLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
papersizeVar = StringVar(root)
papersizeVar.set('Letter')
papersizeMenu = OptionMenu(docframe, papersizeVar, *{'Letter', 'Legal', 'A4'})
papersizeMenu.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# paper orientation
paperorientationLabel = Label(docframe, text="Orientation:")
paperorientationLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
paperorientationVar = StringVar(root)
paperorientationVar.set('Portrait')
paperorientationMenu = OptionMenu(docframe, paperorientationVar, *{'Portrait', 'Landscape'})
paperorientationMenu.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1






# right justify
rightjustVar = IntVar(value=1)
rightjustCheckBox = Checkbutton(docframe, text = "Right Justify", variable = rightjustVar, onvalue = 1, offvalue = 0, height=1)
rightjustCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

# bottom justify
bottomjustifyVar = IntVar(value=1)
bottomjustifyCheckBox = Checkbutton(docframe, text = "Bottom Justify", variable = bottomjustifyVar, onvalue = 1, offvalue = 0, height=1)
bottomjustifyCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

# last bottom justify
lastbottomjustifyVar = IntVar(value=1)
lastbottomjustifyCheckBox = Checkbutton(docframe, text = "Last Bottom Justify", variable = lastbottomjustifyVar, onvalue = 1, offvalue = 0, height=1)
lastbottomjustifyCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

# program settings frame
progframe = ttk.LabelFrame(settingstab, text='Program Settings', relief=GROOVE, borderwidth=2)
progframe.grid(row=1, column=0, sticky=(W, E, N), padx=xpadding, pady=ypadding)
rowvar = 0

# delete temp files
deletefilesVar = IntVar()
deletefilesCheckBox = Checkbutton(progframe, text = "Delete intermediate files", variable = deletefilesVar, onvalue = 1, offvalue = 0, height=1)
deletefilesCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

# default output folder
defaultworkingfolderLabel = Label(progframe, text="Default Save Folder:")
defaultworkingfolderLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
defaultworkingfolderButton = ttk.Button(progframe, text=defaultfolder, command=selectsavefolder)
defaultworkingfolderButton.grid(row=rowvar, column=1, sticky=(W) ,padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

# save button
# this must be the last entry
savebuttonButton = ttk.Button(settingstab, text='Save Settings', command=savesettings)
# not sure about the South sticky, but it looks ok for now
savebuttonButton.grid(row=2, column=0, sticky=(S) ,padx=xpadding, pady=ypadding)

###################################################
# this starts the main program
###################################################
preguiinit()
root.mainloop()
