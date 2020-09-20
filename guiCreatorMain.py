from tkinter import *
from tkinter import messagebox
from spotipy.exceptions import SpotifyException
from requests.exceptions import ReadTimeout
from intershuffle import *
from traceback import format_exc
from datetime import date, datetime
import os
import requests

HEIGHT = 600
WIDTH = 960

NAMESIZE = 103

# Seaweed Color Palette
COLOR1 = '#023859' #Darkest
COLOR2 = '#D9A404' #Secondary
COLOR3 = '#F2CB07' #Main
COLOR4 = '#03738C' #Selection
COLOR5 = '#49AFBB' #Brigthest

COLORTEXTLABEL = 'black'
COLORTEXTBOX = 'black'
COLORTEXTBUTTON = 'black'
COLORTEXTSEL = 'white'
COLORTEXTSEC = 'white'

COLORBUTTON = COLOR3
COLORBUTTONSEC = COLOR2

COLORLABEL = COLOR5
COLORLABELSEC = COLOR4
COLORBOX = COLOR2
COLORBOXSEL = COLOR4

COLORBG = COLOR2
COLORBGSEC = COLOR1

# -------------------------------------------------------------------------------
def run():
    o = optMeth.get().strip()

    try:
        if o == 'Intershuffle':
            runMain()
        elif o == 'Chaotic':
            runChaotic()
        
        saveToPlay.place(relx=0.78, rely=0.895, relwidth=0.2)

    except SpotifyException as se:
        if "No active device found" in se.msg:
            messagebox.showerror("Oh Shit", "No active devices were found!\nPlease make sure you have Spotify open somewhere")
        elif "Premium required" in se.msg:
            messagebox.showerror("Oh Shit", "I'm so sorry you're poor\nThis app was made by the rich gang\n(You need Spotify Premium)")
        else:
            path = "errors"

            try:
                os.mkdir(path)
            except OSError:
                print ("Folder already created")

            fileDir = os.path.dirname(os.path.realpath('__file__'))
            ts = str(datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')[0:16]
            ts = f"Exception_{ts}.log"
            filename = os.path.join(path, ts)
            filename = os.path.join(fileDir, filename)

            messagebox.showerror("Oh Shit", 'Something wrong happened\nEither you are stupid or I am (please read the README)\nPossible logs with the error(s) was created in the "errors" subfolder')

            with open(filename, 'w') as f:
                f.write(str(se))
                f.write(format_exc())
    
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        messagebox.showerror("Oh Shit", 'The Internet just went down\nTry to not cry and avoid having a mental breakdown')

    except Exception as e:
        print("Exception caught!")
        if "No device selected" in str(e):
            messagebox.showerror("Oh Shit", 'No device detected or selected\nPlease make sure you have Spotify open somewhere')
        elif "No playlist selected" in str(e):
            messagebox.showerror("Oh Shit", 'No playlist selected\nSelect at least one playlist')
        else:        
            path = "errors"

            try:
                os.mkdir(path)
            except OSError:
                print ("Folder already created")

            fileDir = os.path.dirname(os.path.realpath('__file__'))
            ts = str(datetime.now()).replace('-', '').replace(' ', '').replace(':', '').replace('.', '')[0:16]
            ts = f"Exception_{ts}.log"
            filename = os.path.join(path, ts)
            filename = os.path.join(fileDir, filename)

            messagebox.showerror("Oh Shit", 'Something wrong happened\nEither you are stupid or I am (please read the README)\nPossible logs with the error(s) was created in the "errors" subfolder')

            with open(filename, 'w') as f:
                f.write(str(e))
                f.write(format_exc())
    
    # Restart everything for next execution
    Restart()
    GetPlaylistsCached()
    # on_select(None)
    pass

def runMain():
    print("Run Main...")
    d = optDevice.get().strip()
    if d == "":
        raise Exception("No device selected")

    SetDevice(d)
    vPlay = optPlay.get().strip()

    opts = list(chpls.curselection())
    names = []

    if len(opts) <= 0:
        pass

    for i in opts:
        names.append(playlistNames[i].strip())

    if checkVar.get() == 0 and vPlay in names:
        startingPlaylist[0] = vPlay

    print(vPlay)
    main(names)
    pass

def runChaotic():
    print("Run Chaotic...")
    SetDevice(optDevice.get().strip())
    
    opts = list(chpls.curselection())
    names = []

    if len(opts) <= 0:
        pass

    for i in opts:
        names.append(playlistNames[i].strip())
    
    print(names)
    
    chaoticMain(names)
    pass

def refresh():
    dropDownOptions.clear()
    try:
        for d in GetDevices():
            dropDownOptions.append(f"{d['name']} ({d['type']})")
    except Exception:
        dropDownOptions.clear()
        dropDownOptions.append("")

    for i, s in enumerate(dropDownOptions):
        dropDownOptions[i] = s.ljust(NAMESIZE)

    menu = drop['menu']
    menu.delete(0, 'end')
    for name in dropDownOptions:
        menu.add_command(label=name, command=lambda name=name: optDevice.set(name))
    
    optDevice.set(dropDownOptions[0])

    refreshPlaylists()

def refreshPlaylists():
    playlistNames.clear()
    
    try:
        GetSpotPlaylists()
        
        for d in GetPlaylists():
            playlistNames.append(d)

    except requests.exceptions.ConnectionError:
        messagebox.showerror("Oh Shit", 'The Internet just went down\nTry to not cry and avoid having a mental breakdown')

    for i, s in enumerate(playlistNames):
        playlistNames[i] = s.ljust(NAMESIZE)

    menu = pls['menu']
    menu.delete(0, 'end')
    for name in playlistNames:
        menu.add_command(label=name, command=lambda name=name: optPlay.set(name))
    
    subFrame.place_forget()
    chpls.pack_forget()
    scrollbar.pack_forget()

    if len(playlistNames) > 10:
        scrollbar.config(command=chpls.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        chpls.config(width=NAMESIZE+3)
    else:
        scrollbar.pack_forget()
        chpls.config(width=NAMESIZE+5)

    subFrame.place(relx=0.02, rely=0.565)
    chpls.config(height=min(len(playlistNames), 10))
    chpls.pack()

    chpls.delete(0, END)
    for s in playlistNames:
        chpls.insert(END, s.strip())
    
    optPlay.set(" "*NAMESIZE)

def show_hide():
    if checkVar.get() == 1:
        pls.place_forget()
    else:
        pls.place(relx=0.02, rely=0.405, relheight=0.06)

def switch_meth(event):
    if event.strip() == "Chaotic":
        cb.place_forget()
        pls.place_forget()
        label3.place_forget()
    else:
        cb.place(relx=0.7175, rely=0.34, relheight=0.06)
        show_hide()
        label3.place(relx=0.02, rely=0.34, relheight=0.06)

def on_select(event):
    opts = list(chpls.curselection())
    curPlaylistNames.clear()

    for i in opts:
        curPlaylistNames.append(playlistNames[i])

    for i, s in enumerate(curPlaylistNames):
        curPlaylistNames[i] = s.ljust(NAMESIZE)

    menu = pls['menu']
    menu.delete(0, 'end')
    for name in curPlaylistNames:
        menu.add_command(label=name, command=lambda name=name: optPlay.set(name))
    
    if optPlay.get() not in curPlaylistNames:
        if len(curPlaylistNames) > 0:
            optPlay.set(curPlaylistNames[0])
        else:
            optPlay.set(' '*NAMESIZE)

def select_all():
    if len(chpls.curselection()) == len(playlistNames):
        chpls.select_clear(0, END)
    else:
        chpls.selection_set(0, END)
    on_select(None)

def savePlaylist():
    savePlaybackToPlaylist(optMeth.get().strip())

def key(event):
    if event.keycode == 17:
        testVersion[0] = True
        testLabel.pack()

# -------------------------------------------------------------------------------

print("Creating GUI...")

root = Tk()
root.title('Laminaria')
root.resizable(width=False, height=False)


imgName = 'icon.ico'
if not os.path.exists(imgName):
    print("Icon doesn't exist, downloading...")
    with open(imgName, 'wb') as handle:
        response = requests.get('https://i.imgur.com/Whladjr.png', stream=True)

        if not response.ok:
            print(response.status_code)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

try:
    root.iconbitmap(imgName)
except:
    try:
        img = PhotoImage(file=imgName)
        root.tk.call('wm', 'iconphoto', root._w, img)
    except:
        print("Icon Error, not putting any icon then")

# -------------------------------------------------------------------------------

Init()

playlistNames = [""]
curPlaylistNames = [""]

# -------------------------------------------------------------------------------

root.bind("<Key>", key)

dropDownOptions = []

methods = ['Intershuffle', 'Chaotic']

canvas = Canvas(root, height=HEIGHT, width=WIDTH, bg=COLORBG)
canvas.pack()

frame = Frame(root, bg=COLORBGSEC, bd=5)
frame.place(relx=0.5, rely=0.025, relwidth=0.95, relheight=0.95, anchor='n')

testLabel = Label(frame, text="Test Mode", font='Courier 10', foreground=COLORTEXTLABEL)

Label(frame, background=COLORBUTTONSEC).place(relx=0.41, rely=0.89, relwidth=0.18, relheight=0.09)

buttonRun = Button(frame, text="RUN", bg=COLORBUTTON, fg=COLORTEXTBUTTON, font=40, command=run)
buttonRun.config(font='Courier 16 bold')
buttonRun.place(relx=0.42, rely=0.9, relwidth=0.16)

# -------------------------------------------------------------------------------

for i, s in enumerate(methods):
    methods[i] = s.ljust(NAMESIZE)

# -------------------------------------------------------------------------------

optDevice = StringVar()
optPlay = StringVar()
optMeth = StringVar()
optMeth.set(methods[0])

# -------------------------------------------------------------------------------

label1 = Label(frame, text="Device where the music will be played: ", font='Courier 10', background=COLORLABEL, foreground=COLORTEXTLABEL).place(relx=0.02, rely=0.02, relheight=0.06)

drop = OptionMenu(frame, optDevice, None, *dropDownOptions)
drop.config(font='Courier 10', background=COLORBOX, foreground=COLORTEXTBOX, activebackground=COLORBOXSEL, activeforeground=COLORTEXTSEL)
drop['menu'].config(font=('Courier',(10)), background=COLORBOX, foreground=COLORTEXTBOX, activebackground=COLORBOXSEL, activeforeground=COLORTEXTSEL)

buttonRefresh = Button(frame, text="Refresh", bg=COLORBUTTON, fg=COLORTEXTBUTTON, command=refresh)
buttonRefresh.config(font='Courier 10')

drop.         place(relx=0.02, rely=0.085, relheight=0.06)
buttonRefresh.place(relx=0.78, rely=0.02, relheight=0.06, relwidth=0.2)

# -------------------------------------------------------------------------------

label2 = Label(frame, text="Shuffling Mode: ", font='Courier 10', background=COLORLABEL, foreground=COLORTEXTLABEL).place(relx=0.02, rely=0.18, relheight=0.06)

checkVar = IntVar()
checkVar.set(0)
cb = Checkbutton(frame, text="Start on a Random Playlist", variable=checkVar, command=show_hide)
cb.config(font='Courier 10', background=COLORLABELSEC, foreground=COLORTEXTSEC)
cb.place(relx=0.7175, rely=0.34, relheight=0.06)

# -------------------------------------------------------------------------------

label3 = Label(frame, text="Choose starting playlist: ", font='Courier 10', background=COLORLABEL, foreground=COLORTEXTLABEL)
label3.place(relx=0.02, rely=0.34, relheight=0.06)

pls = OptionMenu(frame, optPlay, *curPlaylistNames)
pls.config(font='Courier 10', background=COLORBOX, foreground=COLORTEXTBOX, activebackground=COLORBOXSEL, activeforeground=COLORTEXTSEL)
pls['menu'].config(font=('Courier',(10)), background=COLORBOX, foreground=COLORTEXTBOX, activebackground=COLORBOXSEL, activeforeground=COLORTEXTSEL)
pls.place(relx=0.02, rely=0.405, relheight=0.06)

# -------------------------------------------------------------------------------

method = OptionMenu(frame, optMeth, *methods, command=switch_meth)
method.config(font='Courier 10', background=COLORBOX, foreground=COLORTEXTBOX, activebackground=COLORBOXSEL, activeforeground=COLORTEXTSEL)
method['menu'].config(font=('Courier',(10)), background=COLORBOX, foreground=COLORTEXTBOX, activebackground=COLORBOXSEL, activeforeground=COLORTEXTSEL)
method.place(relx=0.02, rely=0.245, relheight=0.06)

# -------------------------------------------------------------------------------

label4 = Label(frame, text="Select playlists that will be used as source: ", font='Courier 10', background=COLORLABEL, foreground=COLORTEXTLABEL).place(relx=0.02, rely=0.5, relheight=0.06)

subFrame = Frame(frame)
scrollbar = Scrollbar(subFrame, orient=VERTICAL)
chpls = Listbox(subFrame, width=NAMESIZE+3, background=COLORBOX, selectbackground=COLORBOXSEL, selectforeground=COLORTEXTSEL, foreground=COLORTEXTBOX, selectmode=MULTIPLE, yscrollcommand=scrollbar.set)

if len(playlistNames) > 10:
    scrollbar.config(command=chpls.yview)
    # scrollbar.pack(side=RIGHT, fill=Y)

# subFrame.place(relx=0.02, rely=0.565)
chpls.pack()

chpls.bind('<<ListboxSelect>>', on_select)
chpls.config(font='Courier 10')
chpls.config(height=min(len(playlistNames), 10))

for s in playlistNames:
    chpls.insert(END, s.strip())

# -------------------------------------------------------------------------------

selAll = Button(frame, text="Select All", bg=COLORBUTTON, fg=COLORTEXTBOX, command=select_all)
selAll.config(font='Courier 10')
selAll.place(relx=0.78, rely=0.5, relheight=0.06, relwidth=0.2)

saveToPlay = Button(frame, text="Save Playback\nas new Playlist", bg=COLORBOX, fg=COLORTEXTBOX, command=savePlaylist)
saveToPlay.config(font='Courier 10')
#saveToPlay.place(relx=0.78, rely=0.895, relwidth=0.2)

# -------------------------------------------------------------------------------

while True:
    try:
        refresh()
        on_select(None)
        break
    except ReadTimeout:
        print("Timed out")

root.mainloop()


# The MIT License (MIT)
#
# Copyright (c) 2014 Paul Lamere
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.