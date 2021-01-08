#!/usr/bin/env python3

###################################################
# Imports
###################################################
from tkinter import *  # main gui library
from tkinter import ttk  # extended gui widgets
from tkinter import filedialog  # for save folder
import time  # for default filenames with date
from os import path  # for working cross platform with files/folders
from os import system # for running lilypond externally
import configparser  # for working with settings files (.ini)
import random

# my data files
import headers
import auralintervalsdata
import drawclefsdata
import identwritenotesdata

import footers

###################################################
# Initial Variables
###################################################
xpadding = 20
ypadding = 8
defaultfolder = path.expanduser('~')


###################################################
# Definitions
###################################################

### CONFIG FILE STUFF ###
def initconfigfile():
    global defaultfolder
    # if file does not exist, create it, populate it with defaults, and save it
    if not path.exists(path.join(path.dirname(path.realpath(__file__)), 'config.ini')):
        configfile = open(path.join(path.dirname(path.realpath(__file__)), 'config.ini'), "w+")
        # config parser stuff
        config = configparser.ConfigParser()
        config['SETTINGS'] = {'DefaultSaveFolder': defaultfolder,
                              'DeleteTempFiles': 0,
                              'DefaultFont': 'Sans',
                              'RightJustify': 1,
                              'BottomJustify': 1,
                              'LastBottomJustify': 1,
                              'PaperSize': 'Letter',
                              'PaperOrientation': 'Portrait',
                              'Scaling': '22',
                              'TrebleWeight': '10',
                              'AltoWeight': '2',
                              'TenorWeight': '1',
                              'BassWeight': '8'}
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
        fontVar.set(config['SETTINGS']['defaultfont'])
        rightjustVar.set(config['SETTINGS']['rightjustify'])
        bottomjustifyVar.set(config['SETTINGS']['bottomjustify'])
        lastbottomjustifyVar.set(config['SETTINGS']['lastbottomjustify'])
        papersizeVar.set(config['SETTINGS']['papersize'])
        paperorientationVar.set(config['SETTINGS']['paperorientation'])
        scalingVar.set(config['SETTINGS']['scaling'])
        trebleVar.set(config['SETTINGS']['trebleweight'])
        altoVar.set(config['SETTINGS']['altoweight'])
        tenorVar.set(config['SETTINGS']['tenorweight'])
        bassVar.set(config['SETTINGS']['bassweight'])
        # update button text
        defaultworkingfolderButton.config(text=defaultfolder)


def savesettings():
    configfile = open(path.join(path.dirname(path.realpath(__file__)), 'config.ini'), "w")
    config = configparser.ConfigParser()
    config['SETTINGS'] = {'DefaultSaveFolder': defaultfolder,
                          'DeleteTempFiles': deletefilesVar.get(),
                          'DefaultFont': fontVar.get(),
                          'RightJustify': rightjustVar.get(),
                          'BottomJustify': bottomjustifyVar.get(),
                          'LastBottomJustify': lastbottomjustifyVar.get(),
                          'PaperSize': papersizeVar.get(),
                          'PaperOrientation': paperorientationVar.get(),
                          'Scaling': scalingVar.get(),
                          'TrebleWeight': trebleVar.get(),
                          'AltoWeight': altoVar.get(),
                          'TenorWeight': tenorVar.get(),
                          'BassWeight': bassVar.get()}
    config.write(configfile)
    configfile.close()

# main program ########################################


def createButton():
    docfont, docboldfont = initcustomfonts()
    worksheetfile, keysheetfile, worksheetfilename, keysheetfilename = start_ly_file(docfont, docboldfont)
    auralintervals(worksheetfile, keysheetfile, docfont, docboldfont)
    drawclefs(worksheetfile, keysheetfile, docfont, docboldfont)
    identwritenotes(worksheetfile, keysheetfile, docfont, docboldfont)
    endfile(worksheetfile, keysheetfile)
    callLilypond(worksheetfilename, keysheetfilename)

#######################################################

# definitions


def initcustomfonts():
    if fontEntry.get() != '':
        return '\override #\'(font-name . "' + fontEntry.get() + '")', '\override #\'(font-name . "' + fontEntry.get() + ' Bold") '
    else:
        return '', '\\bold'


def start_ly_file(docfont,docboldfont):
    # setup filenames
    if filenameEntry.get():
        worksheetfilename = path.join(defaultfolder, filenameEntry.get() + '-worksheet.ly')
        keysheetfilename = path.join(defaultfolder, filenameEntry.get() + '-keysheet.ly')
    else:
        worksheetfilename = path.join(defaultfolder, 'theory-worksheet-' + time.strftime("%Y-%m-%d") + '.ly')
        keysheetfilename = path.join(defaultfolder, 'theory-keysheet-' + time.strftime("%Y-%m-%d") + '.ly')
    # open files for writing
    worksheetfile = open(worksheetfilename, 'w')
    keysheetfile = open(keysheetfilename, 'w')
    # set up header variables/options
    # titles
    if titleEntry.get() != '':
        doctitle = titleEntry.get()
    else:
        doctitle = 'Preliminary Rudiments Worksheet'
    # copyright
    if copyrightEntry.get() != '':
        doctag = copyrightEntry.get()
    else:
        doctag = 'Created by rudi v2.0'
    # right justify
    if rightjustVar.get() == 1:
        raggedrightvar = 'ragged-right = ##f'
    else:
        raggedrightvar = 'ragged-right = ##t'
    # bottom justify
    if bottomjustifyVar.get() == 1:
        raggedbottomvar = 'ragged-bottom = ##f'
    else:
        raggedbottomvar = 'ragged-bottom = ##t'
    # last bottom justify
    if lastbottomjustifyVar.get() == 1:
        raggedlastbottomvar = 'ragged-last-bottom = ##f'
    else:
        raggedlastbottomvar = 'ragged-last-bottom = ##t'
    # paper size is in the header write block directly
    # paper orientation
    if paperorientationVar.get() == 'Landscape':
        orientationvar = " 'landscape"
    else:
        orientationvar = ''
    # scaling is in the header write block directly


    # write the header to file
    worksheetfile.writelines(headers.lilypondheader.format(title=doctitle, font=docfont, boldfont=docboldfont,
                                                           tag=doctag, keytitle='',
                                                           raggedright=raggedrightvar, raggedbottom=raggedbottomvar,
                                                           raggedlastbottom=raggedlastbottomvar,
                                                           papersize=papersizeVar.get().lower(), orientation=orientationvar,
                                                           scaling=scalingVar.get()))
    keysheetfile.writelines(headers.lilypondheader.format(title=doctitle, font=docfont, boldfont=docboldfont,
                                                          tag=doctag, keytitle='\with-color #red Key',
                                                          raggedright=raggedrightvar, raggedbottom=raggedbottomvar,
                                                          raggedlastbottom=raggedlastbottomvar,
                                                          papersize=papersizeVar.get().lower(), orientation=orientationvar,
                                                          scaling=scalingVar.get()))

    # return the sheet filenames for subsequent writes
    return worksheetfile, keysheetfile, worksheetfilename, keysheetfilename


def listifyClefs(treble, alto, tenor, bass):
    cleflist = []
    if treble.get() == 1:
        cleflist.append('treble')
    if alto.get() == 1:
        cleflist.append('alto')
    if tenor.get() == 1:
        cleflist.append('tenor')
    if bass.get() == 1:
        cleflist.append('bass')
    return cleflist


def auralintervals(worksheetfile, keysheetfile, docfont, docboldfont):
    if auralintervalsVar.get() == 1:
        # init variables
        intervals = []
        worksheetdata = ''
        keydata = ''

        # poll for user chosen intervals and add to the 'intervals' list above
        if PPVar.get() == 1:
            intervals.append('PP')
        if m2Var.get() == 1:
            intervals.append('m2')
        if M2Var.get() == 1:
            intervals.append('M2')
        if m3Var.get() == 1:
            intervals.append('m3')
        if M3Var.get() == 1:
            intervals.append('M3')
        if P4Var.get() == 1:
            intervals.append('P4')
        if TTVar.get() == 1:
            intervals.append('TT')
        if P5Var.get() == 1:
            intervals.append('P5')
        if m6Var.get() == 1:
            intervals.append('m6')
        if M6Var.get() == 1:
            intervals.append('M6')
        if m7Var.get() == 1:
            intervals.append('m7')
        if M7Var.get() == 1:
            intervals.append('M7')
        if P8Var.get() == 1:
            intervals.append('P8')

        # create the questions variable
        for i in range(10):
            if i in range(int(auralintervalsnumberVar.get())):
                worksheetdata += str(auralintervalsdata.columnstart.format())
                keydata += str(auralintervalsdata.columnstart.format())
                count = i + 1
                while count - 1 in range(int(auralintervalsnumberVar.get())):
                    worksheetdata += str(auralintervalsdata.loop.format(number=count, answer='\hspace # 4'))
                    keydata += str(auralintervalsdata.loop.format(number=count, answer='\with-color #red ' + random.choice(intervals)))
                    count += 10
                worksheetdata += ' } '
                keydata += ' } '

        # write out results
        worksheetfile.writelines(auralintervalsdata.header.format(font=docfont, boldfont=docboldfont, masterloop=worksheetdata))
        keysheetfile.writelines(auralintervalsdata.header.format(font=docfont, boldfont=docboldfont, masterloop=keydata))


def drawclefs(worksheetfile, keysheetfile, docfont, docboldfont):
    if drawclefsVar.get() == 1:
        worksheetfile.writelines(drawclefsdata.header.format(font=docfont, boldfont=docboldfont, number=drawclefsnumberVar.get()))
        keysheetfile.writelines(drawclefsdata.header.format(font=docfont, boldfont=docboldfont, number=drawclefsnumberVar.get()))

        # set up clef list variable
        cleflist = listifyClefs(drawcleftrebleVar, drawclefaltoVar, drawcleftenorVar, drawclefbassVar)

        if len(cleflist) == 1:
            worksheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[0], key='\once \override Staff.Clef.transparent = ##t'))
            worksheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[0], startstaff='', key='\once \override Staff.Clef.transparent = ##t', hideclef='\once \override Staff.Clef.transparent = ##t'))
            keysheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[0], key=''))
            keysheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[0], startstaff='', key='\once \override Staff.Clef.transparent = ##t', hideclef='\once \override Staff.Clef.transparent = ##t'))
        if len(cleflist) >= 2:
            worksheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[0], key='\once \override Staff.Clef.transparent = ##t'))
            worksheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[1], startstaff='\startStaff', key='\once \override Staff.Clef.transparent = ##t', hideclef=''))
            keysheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[0], key=''))
            keysheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[1], startstaff='\startStaff', key='', hideclef=''))
        if len(cleflist) == 3:
            worksheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[2], key='\once \override Staff.Clef.transparent = ##t'))
            worksheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[2], startstaff='', key='\once \override Staff.Clef.transparent = ##t', hideclef='\once \override Staff.Clef.transparent = ##t'))
            keysheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[2], key=''))
            keysheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[2], startstaff='', key='\once \override Staff.Clef.transparent = ##t', hideclef='\once \override Staff.Clef.transparent = ##t'))
        if len(cleflist) == 4:
            worksheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[2], key='\once \override Staff.Clef.transparent = ##t'))
            worksheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[3], startstaff='\startStaff', key='\once \override Staff.Clef.transparent = ##t', hideclef=''))
            keysheetfile.writelines(drawclefsdata.clefone.format(clef=cleflist[2], key=''))
            keysheetfile.writelines(drawclefsdata.cleftwo.format(clef=cleflist[3], startstaff='\startStaff', key='', hideclef=''))

def identNotesPopulateList(notes, ledgernotes, key, ledgerkey):
    if ledgerLinesVar.get() == 1:
        noteslist = notes + ledgernotes
        keylist = key + ledgerkey
    else:
        noteslist = notes.copy()
        keylist = key.copy()
    return noteslist, keylist

def writeNotesPopulateList(notes, key):
    return notes.copy(), key.copy()


def identwritenotes(worksheetfile,keysheetfile,docfont,docboldfont):
    # headers
    if identnotesVar.get() == 1 or writenotesVar.get() == 1:
        worksheetfile.writelines(identwritenotesdata.header.format(boldfont=docboldfont))
        keysheetfile.writelines(identwritenotesdata.header.format(boldfont=docboldfont))
    # variables setup
    identcleflist = listifyClefs(identnotestrebleVar, identnotesaltoVar, identnotestenorVar, identnotesbassVar)
    writecleflist = listifyClefs(writenotestrebleVar, writenotesaltoVar, writenotestenorVar, writenotesbassVar)
    trebleNotes = []
    altoNotes = []
    tenorNotes = []
    bassNotes = []

    # identify notes
    if identnotesVar.get() == 1:
        worksheetfile.writelines(identwritenotesdata.identText.format(font=docfont))
        keysheetfile.writelines(identwritenotesdata.identText.format(font=docfont))
        # TREBLE
        if 'treble' in identcleflist:
            worksheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='treble'))
            keysheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='treble'))
            for i in range(int(identnotesnumberVar.get())):
                if len(trebleNotes) == 0:
                    trebleNotes, trebleKey = identNotesPopulateList(identwritenotesdata.trebleNotes, identwritenotesdata.trebleLedgerNotes, identwritenotesdata.trebleKey, identwritenotesdata.trebleLedgerKey)
                selection = random.choice(range(len(trebleNotes)))
                note = trebleNotes.pop(selection)
                key = trebleKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='__'))
                keysheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='\with-color #red ' + key))
            worksheetfile.writelines(identwritenotesdata.identSectionEnd)
            keysheetfile.writelines(identwritenotesdata.identSectionEnd)
        # ALTO
        if 'alto' in identcleflist:
            worksheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='alto'))
            keysheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='alto'))
            for i in range(int(identnotesnumberVar.get())):
                if len(altoNotes) == 0:
                    altoNotes, altoKey = identNotesPopulateList(identwritenotesdata.altoNotes, identwritenotesdata.altoLedgerNotes, identwritenotesdata.altoKey, identwritenotesdata.altoLedgerKey)
                selection = random.choice(range(len(altoNotes)))
                note = altoNotes.pop(selection)
                key = altoKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='__'))
                keysheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='\with-color #red ' + key))
            worksheetfile.writelines(identwritenotesdata.identSectionEnd)
            keysheetfile.writelines(identwritenotesdata.identSectionEnd)
        # TENOR
        if 'tenor' in identcleflist:
            worksheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='tenor'))
            keysheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='tenor'))
            for i in range(int(identnotesnumberVar.get())):
                if len(tenorNotes) == 0:
                    tenorNotes, tenorKey = identNotesPopulateList(identwritenotesdata.tenorNotes, identwritenotesdata.tenorLedgerNotes, identwritenotesdata.tenorKey, identwritenotesdata.tenorLedgerKey)
                selection = random.choice(range(len(tenorNotes)))
                note = tenorNotes.pop(selection)
                key = tenorKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='__'))
                keysheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='\with-color #red ' + key))
            worksheetfile.writelines(identwritenotesdata.identSectionEnd)
            keysheetfile.writelines(identwritenotesdata.identSectionEnd)
        # BASS
        if 'bass' in identcleflist:
            worksheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='bass'))
            keysheetfile.writelines(identwritenotesdata.identSectionStart.format(clef='bass'))
            for i in range(int(identnotesnumberVar.get())):
                if len(bassNotes) == 0:
                    bassNotes, bassKey = identNotesPopulateList(identwritenotesdata.bassNotes, identwritenotesdata.bassLedgerNotes, identwritenotesdata.bassKey, identwritenotesdata.bassLedgerKey)
                selection = random.choice(range(len(bassNotes)))
                note = bassNotes.pop(selection)
                key = bassKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='__'))
                keysheetfile.writelines(identwritenotesdata.identLoop.format(note=note, key='\with-color #red ' + key))
            worksheetfile.writelines(identwritenotesdata.identSectionEnd)
            keysheetfile.writelines(identwritenotesdata.identSectionEnd)


    # write notes
    if writenotesVar.get() == 1:
        worksheetfile.writelines(identwritenotesdata.writeText.format(font=docfont))
        keysheetfile.writelines(identwritenotesdata.writeText.format(font=docfont))
        # TREBLE
        if 'treble' in writecleflist:
            worksheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='treble'))
            keysheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='treble'))
            for i in range(int(writenotesnumberVar.get())):
                if len(trebleNotes) == 0:
                    trebleNotes, trebleKey = writeNotesPopulateList(identwritenotesdata.trebleNotes, identwritenotesdata.trebleKey)
                selection = random.choice(range(len(trebleNotes)))
                note = trebleNotes.pop(selection)
                key = trebleKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.writeLoop.format(note='s', key=key))
                keysheetfile.writelines(identwritenotesdata.writeLoop.format(note="\override NoteHead.color = #red \override Stem.color = #red " + note, key=key))
            worksheetfile.writelines(identwritenotesdata.writeSectionEnd)
            keysheetfile.writelines(identwritenotesdata.writeSectionEnd)
        # ALTO
        if 'alto' in writecleflist:
            worksheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='alto'))
            keysheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='alto'))
            for i in range(int(writenotesnumberVar.get())):
                if len(altoNotes) == 0:
                    altoNotes, altoKey = writeNotesPopulateList(identwritenotesdata.altoNotes, identwritenotesdata.altoKey)
                selection = random.choice(range(len(altoNotes)))
                note = altoNotes.pop(selection)
                key = altoKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.writeLoop.format(note='s', key=key))
                keysheetfile.writelines(identwritenotesdata.writeLoop.format(note="\override NoteHead.color = #red \override Stem.color = #red " + note, key=key))
            worksheetfile.writelines(identwritenotesdata.writeSectionEnd)
            keysheetfile.writelines(identwritenotesdata.writeSectionEnd)
        # TENOR
        if 'tenor' in writecleflist:
            worksheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='tenor'))
            keysheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='tenor'))
            for i in range(int(writenotesnumberVar.get())):
                if len(tenorNotes) == 0:
                    tenorNotes, tenorKey = writeNotesPopulateList(identwritenotesdata.tenorNotes, identwritenotesdata.tenorKey)
                selection = random.choice(range(len(tenorNotes)))
                note = tenorNotes.pop(selection)
                key = tenorKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.writeLoop.format(note='s', key=key))
                keysheetfile.writelines(identwritenotesdata.writeLoop.format(note="\override NoteHead.color = #red \override Stem.color = #red " + note, key=key))
            worksheetfile.writelines(identwritenotesdata.writeSectionEnd)
            keysheetfile.writelines(identwritenotesdata.writeSectionEnd)
        # BASS
        if 'bass' in writecleflist:
            worksheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='bass'))
            keysheetfile.writelines(identwritenotesdata.writeSectionStart.format(clef='bass'))
            for i in range(int(writenotesnumberVar.get())):
                if len(bassNotes) == 0:
                    bassNotes, bassKey = writeNotesPopulateList(identwritenotesdata.bassNotes, identwritenotesdata.bassKey)
                selection = random.choice(range(len(bassNotes)))
                note = bassNotes.pop(selection)
                key = bassKey.pop(selection)
                worksheetfile.writelines(identwritenotesdata.writeLoop.format(note='s', key=key))
                keysheetfile.writelines(identwritenotesdata.writeLoop.format(note="\override NoteHead.color = #red \override Stem.color = #red " + note, key=key))
            worksheetfile.writelines(identwritenotesdata.writeSectionEnd)
            keysheetfile.writelines(identwritenotesdata.writeSectionEnd)







def endfile(worksheetfile,keysheetfile):
    worksheetfile.writelines(footers.lilypondfooter)
    keysheetfile.writelines(footers.lilypondfooter)
    worksheetfile.close()
    keysheetfile.close()

# settings
def selectsavefolder():
    global defaultfolder
    defaultfolder = filedialog.askdirectory(initialdir=defaultfolder)
    defaultworkingfolderButton.config(text=defaultfolder)


# enable widgets function
def enableWidgets(checkbox,widgets):
    if checkbox.get():
        for i in widgets:
            i.config(state=NORMAL)
    else:
        for i in widgets:
            i.config(state=DISABLED)

def enableauralintervalswidgets():
    enableWidgets(auralintervalsVar, [PPCheckBox, m2CheckBox, M2CheckBox, m3CheckBox, M3CheckBox, P4CheckBox, TTCheckBox, P5CheckBox, m6CheckBox, M6CheckBox, m7CheckBox, M7CheckBox, P8CheckBox])

def enabledrawclefswidgets():
    enableWidgets(drawclefsVar, [drawcleftrebleCheckBox, drawclefbassCheckBox, drawclefaltoCheckBox, drawcleftenorCheckBox])

def enableidentnoteswidgets():
    enableWidgets(identnotesVar, [identnotestrebleCheckBox, identnotesbassCheckBox, identnotesaltoCheckBox, identnotestenorCheckBox, ledgerLinesCheckBox])

def enablewritenoteswidgets():
    enableWidgets(writenotesVar, [writenotestrebleCheckBox, writenotesbassCheckBox, writenotesaltoCheckBox, writenotestenorCheckBox])


def callLilypond(worksheet,key):
    #pass
    # I'm doing the call this way due to a lilypond bug in Gentoo in which it doesn't accept the -o argument
    system('cd ' + path.dirname(worksheet) + ' && lilypond ' + path.basename(worksheet))
    system('cd ' + path.dirname(key) + ' && lilypond ' + path.basename(key))









###################################################
###################################################

###################################################
# Main Window
###################################################
root = Tk()
root.title("Rudi 1.9.1")
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
starttab = ttk.Frame(tab_parent)
basicstab = ttk.Frame(tab_parent)
scalestab = ttk.Frame(tab_parent)
intervalstab = ttk.Frame(tab_parent)
chordstab = ttk.Frame(tab_parent)
cadencestab = ttk.Frame(tab_parent)
settingstab = ttk.Frame(tab_parent)
settingstab.grid(column=0, row=0, sticky=(W, E))
# add the previous tabs to the window with titles
tab_parent.add(starttab, text="Start")
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
button_parent = ttk.Button(subframe, text='Create', command=createButton)
button_parent.grid(column=2, row=0)
# output filename
filenameLabel = Label(subframe, text="Filename:")
filenameLabel.grid(row=0, column=0)
filenameEntry = Entry(subframe, width=50)
filenameEntry.grid(row=0, column=1, padx=5)

###################################################
# Start tab widgets
###################################################
# titles frame
framerow = 0
titlesframe = ttk.LabelFrame(starttab, text='Titles', relief=GROOVE, borderwidth=2)
titlesframe.grid(row=framerow, column=0, sticky=(W, E, N), padx=xpadding, pady=ypadding)
framerow = framerow + 1
rowvar = 0

# title
titleLabel = Label(titlesframe, text="Title:")
titleLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
titleEntry = Entry(titlesframe, width=50)
titleEntry.grid(row=rowvar, column=1, padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

# copyright
copyrightLabel = Label(titlesframe, text="Copyright:")
copyrightLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
copyrightEntry = Entry(titlesframe, width=50)
copyrightEntry.grid(row=rowvar, column=1, padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

###################################################
# basics tab widgets
###################################################

###################################################
# auralintervals frame
auralintervalsframe = ttk.LabelFrame(basicstab, text='Aural Intervals', relief=GROOVE, borderwidth=2)
auralintervalsframe.grid(row=0, column=0, sticky=(W, E, N), padx=xpadding, pady=ypadding)
rowvar = 0

# intervals selection
auralintervalsVar = IntVar(value=0)
auralintervalsCheckBox = Checkbutton(auralintervalsframe, text = "Interval fill in boxes", variable = auralintervalsVar, onvalue = 1, offvalue = 0, height=1, command=enableauralintervalswidgets)
auralintervalsCheckBox.grid(row=rowvar, column=0, sticky=W)

# intervals number of questions
auralintervalsnumberVar = StringVar()
auralintervalsnumberVar.set("10")
auralintervalsnumberBox = Spinbox(auralintervalsframe, from_=0, to=100, width=3, textvariable=auralintervalsnumberVar)
auralintervalsnumberBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# interval types to include in questions
intervalTypeLabel = Label(auralintervalsframe, text="Interval Types:")
intervalTypeLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

PPVar = IntVar(value=1)
PPCheckBox = Checkbutton(auralintervalsframe, text = "PP", variable = PPVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
PPCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

m2Var = IntVar(value=1)
m2CheckBox = Checkbutton(auralintervalsframe, text = "m2", variable = m2Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
m2CheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

M2Var = IntVar(value=1)
M2CheckBox = Checkbutton(auralintervalsframe, text = "M2", variable = M2Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
M2CheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

m3Var = IntVar(value=1)
m3CheckBox = Checkbutton(auralintervalsframe, text = "m3", variable = m3Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
m3CheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

M3Var = IntVar(value=1)
M3CheckBox = Checkbutton(auralintervalsframe, text = "M3", variable = M3Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
M3CheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

P4Var = IntVar(value=1)
P4CheckBox = Checkbutton(auralintervalsframe, text = "P4", variable = P4Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
P4CheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

TTVar = IntVar(value=1)
TTCheckBox = Checkbutton(auralintervalsframe, text = "TT", variable = TTVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
TTCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

# column split
rowvar = 2
P5Var = IntVar(value=1)
P5CheckBox = Checkbutton(auralintervalsframe, text = "P5", variable = P5Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
P5CheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

m6Var = IntVar(value=1)
m6CheckBox = Checkbutton(auralintervalsframe, text = "m6", variable = m6Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
m6CheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

M6Var = IntVar(value=1)
M6CheckBox = Checkbutton(auralintervalsframe, text = "M6", variable = M6Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
M6CheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

m7Var = IntVar(value=1)
m7CheckBox = Checkbutton(auralintervalsframe, text = "m7", variable = m7Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
m7CheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

M7Var = IntVar(value=1)
M7CheckBox = Checkbutton(auralintervalsframe, text = "M7", variable = M7Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
M7CheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

P8Var = IntVar(value=1)
P8CheckBox = Checkbutton(auralintervalsframe, text = "P8", variable = P8Var, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
P8CheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1


###################################################
### Draw Clefs frame
drawclefsframe = ttk.LabelFrame(basicstab, text='Clefs', relief=GROOVE, borderwidth=2)
drawclefsframe.grid(row=0, column=1, sticky=(W, E, N), padx=xpadding, pady=ypadding)
rowvar = 0

drawclefsVar = IntVar(value=0)
drawclefsCheckBox = Checkbutton(drawclefsframe, text = "Draw Clefs", variable = drawclefsVar, onvalue = 1, offvalue = 0, height=1, command=enabledrawclefswidgets)
drawclefsCheckBox.grid(row=rowvar, column=0, sticky=W)

# number of questions
drawclefsnumberVar = StringVar()
drawclefsnumberVar.set("5")
drawclefsnumberBox = Spinbox(drawclefsframe, from_=0, to=100, width=3, textvariable=drawclefsnumberVar)
drawclefsnumberBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# clef selection
drawclefsclefselectionLabel = Label(drawclefsframe, text="Clefs:")
drawclefsclefselectionLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

drawcleftrebleVar = IntVar(value=1)
drawcleftrebleCheckBox = Checkbutton(drawclefsframe, text = "Treble", variable = drawcleftrebleVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
drawcleftrebleCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

drawclefaltoVar = IntVar(value=1)
drawclefaltoCheckBox = Checkbutton(drawclefsframe, text = "Alto", variable = drawclefaltoVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
drawclefaltoCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

drawcleftenorVar = IntVar(value=1)
drawcleftenorCheckBox = Checkbutton(drawclefsframe, text = "Tenor", variable = drawcleftenorVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
drawcleftenorCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

drawclefbassVar = IntVar(value=1)
drawclefbassCheckBox = Checkbutton(drawclefsframe, text = "Bass", variable = drawclefbassVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
drawclefbassCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

###################################################
### ident/write notes frame
identwritenotesframe = ttk.LabelFrame(basicstab, text='Identify/Write Notes', relief=GROOVE, borderwidth=2)
identwritenotesframe.grid(row=0, column=2, sticky=(W, E, N), padx=xpadding, pady=ypadding)
rowvar = 0

# ident notes
identnotesVar = IntVar(value=0)
identnotesCheckBox = Checkbutton(identwritenotesframe, text = "Identify Notes", variable = identnotesVar, onvalue = 1, offvalue = 0, height=1, command=enableidentnoteswidgets)
identnotesCheckBox.grid(row=rowvar, column=0, sticky=W)

# number of questions
identnotesnumberVar = StringVar()
identnotesnumberVar.set("10")
identnotesnumberBox = Spinbox(identwritenotesframe, from_=0, to=100, width=3, textvariable=identnotesnumberVar)
identnotesnumberBox.grid(row=rowvar, column=0, sticky=E)
rowvar = rowvar + 1

identnotesclefselectionLabel = Label(identwritenotesframe, text="Clefs:")
identnotesclefselectionLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

identnotestrebleVar = IntVar(value=1)
identnotestrebleCheckBox = Checkbutton(identwritenotesframe, text = "Treble", variable = identnotestrebleVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
identnotestrebleCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

identnotesaltoVar = IntVar(value=1)
identnotesaltoCheckBox = Checkbutton(identwritenotesframe, text = "Alto", variable = identnotesaltoVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
identnotesaltoCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

identnotestenorVar = IntVar(value=1)
identnotestenorCheckBox = Checkbutton(identwritenotesframe, text = "Tenor", variable = identnotestenorVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
identnotestenorCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

identnotesbassVar = IntVar(value=1)
identnotesbassCheckBox = Checkbutton(identwritenotesframe, text = "Bass", variable = identnotesbassVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
identnotesbassCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1

# ledger lines settings
ledgerLinesVar = IntVar(value=0)
ledgerLinesCheckBox = Checkbutton(identwritenotesframe, text = "Ledger Lines", variable = ledgerLinesVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
ledgerLinesCheckBox.grid(row=rowvar, column=0, sticky=W)
rowvar = rowvar + 1



# write notes
rowvar = 0
writenotesVar = IntVar(value=0)
writenotesCheckBox = Checkbutton(identwritenotesframe, text = "Write Notes", variable = writenotesVar, onvalue = 1, offvalue = 0, height=1, command=enablewritenoteswidgets)
writenotesCheckBox.grid(row=rowvar, column=1, sticky=W)

# number of questions
writenotesnumberVar = StringVar()
writenotesnumberVar.set("10")
writenotesnumberBox = Spinbox(identwritenotesframe, from_=0, to=100, width=3, textvariable=writenotesnumberVar)
writenotesnumberBox.grid(row=rowvar, column=1, sticky=E)
rowvar = rowvar + 1

writenotesclefselectionLabel = Label(identwritenotesframe, text="Clefs:")
writenotesclefselectionLabel.grid(row=rowvar, column=1, padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

writenotestrebleVar = IntVar(value=1)
writenotestrebleCheckBox = Checkbutton(identwritenotesframe, text = "Treble", variable = writenotestrebleVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
writenotestrebleCheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

writenotesaltoVar = IntVar(value=1)
writenotesaltoCheckBox = Checkbutton(identwritenotesframe, text = "Alto", variable = writenotesaltoVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
writenotesaltoCheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

writenotestenorVar = IntVar(value=1)
writenotestenorCheckBox = Checkbutton(identwritenotesframe, text = "Tenor", variable = writenotestenorVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
writenotestenorCheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

writenotesbassVar = IntVar(value=1)
writenotesbassCheckBox = Checkbutton(identwritenotesframe, text = "Bass", variable = writenotesbassVar, onvalue = 1, offvalue = 0, height=1,state=DISABLED)
writenotesbassCheckBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

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

####### document settings frame #######
framerow = 0
docframe = ttk.LabelFrame(settingstab, text='Document Settings', relief=GROOVE, borderwidth=2)
docframe.grid(row=framerow, column=0, sticky=(N, W, S, E), padx=xpadding, pady=ypadding)
framerow = framerow + 1
rowvar = 0

# font
fontLabel = Label(docframe, text="Font:")
fontLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
fontVar = StringVar()
fontVar.set('Sans')
fontEntry = Entry(docframe, textvariable=fontVar, width=50)
fontEntry.grid(row=rowvar, column=1, sticky=(W), padx=xpadding, pady=ypadding)
rowvar = rowvar + 1

# paper size
papersizeLabel = Label(docframe, text="Page Size:")
papersizeLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
papersizeVar = StringVar()
papersizeVar.set('Letter')
papersizeMenu = OptionMenu(docframe, papersizeVar, 'Letter', 'Legal', 'A4')
papersizeMenu.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# paper orientation
paperorientationLabel = Label(docframe, text="Orientation:")
paperorientationLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
paperorientationVar = StringVar()
paperorientationVar.set('Portrait')
paperorientationMenu = OptionMenu(docframe, paperorientationVar, 'Portrait', 'Landscape')
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

# notation scaling
scalingLabel = Label(docframe, text="Scaling:")
scalingLabel.grid(row=rowvar, column=0, sticky=(W) ,padx=xpadding, pady=ypadding)
scalingVar = StringVar()
scalingVar.set("22")
scalingBox = Spinbox(docframe, from_=5, to=30, width=3, textvariable=scalingVar)
scalingBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

####### random clef frame #######
clefsframe = ttk.LabelFrame(settingstab, text='Random Clef Selection Weights', relief=GROOVE, borderwidth=2)
clefsframe.grid(row=framerow, column=0, sticky=(W, E), padx=xpadding, pady=ypadding)
framerow = framerow + 1
rowvar = 0

# treble clef
trebleLabel = Label(clefsframe, text="Treble:")
trebleLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
trebleVar = StringVar()
trebleVar.set("10")
trebleBox = Spinbox(clefsframe, from_=0, to=100, width=3, textvariable=trebleVar)
trebleBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# alto clef
altoLabel = Label(clefsframe, text="Alto:")
altoLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
altoVar = StringVar()
altoVar.set("2")
altoBox = Spinbox(clefsframe, from_=0, to=100, width=3, textvariable=altoVar)
altoBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# tenor clef
tenorLabel = Label(clefsframe, text="Tenor:")
tenorLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
tenorVar = StringVar()
tenorVar.set("1")
tenorBox = Spinbox(clefsframe, from_=0, to=100, width=3, textvariable=tenorVar)
tenorBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1

# bass clef
bassLabel = Label(clefsframe, text="Bass:")
bassLabel.grid(row=rowvar, column=0, padx=xpadding, pady=ypadding)
bassVar = StringVar()
bassVar.set("8")
bassBox = Spinbox(clefsframe, from_=0, to=100, width=3, textvariable=bassVar)
bassBox.grid(row=rowvar, column=1, sticky=W)
rowvar = rowvar + 1


####### program settings frame #######
progframe = ttk.LabelFrame(settingstab, text='Program Settings', relief=GROOVE, borderwidth=2)
progframe.grid(row=framerow, column=0, sticky=(W, E, N), padx=xpadding, pady=ypadding)
framerow = framerow + 1
rowvar = 0

# delete temp files
deletefilesVar = IntVar()
deletefilesCheckBox = Checkbutton(progframe, text = "Delete intermediate files **need to fix this**", variable = deletefilesVar, onvalue = 1, offvalue = 0, height=1)
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
savebuttonButton.grid(row=framerow, column=0, sticky=(S) ,padx=xpadding, pady=ypadding)

###################################################
# this starts the main program
###################################################
initconfigfile()
root.mainloop()
