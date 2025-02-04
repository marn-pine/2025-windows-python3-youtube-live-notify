# Latest update: 21-Jan-25, for Windows 11 and from Python 3.1.2 
# Ready-compiled stand-alone .exe file used with .ini file
# This app will continuously notify you when a YouTube channel goes live. 
# Right-click the tray icon and choose Exit to exit the app.                                                  

# built-in packages
from time import *
from configparser import ConfigParser
import threading
import os
import winsound

# external packages
# pip install youtube-lv
# pip install pystray 
from ytlv import youtube
import pystray
from PIL import Image

# compile .py to .exe
# pip install pyinstaller 
# pyinstaller --onefile --noconsole youtube-live-notify.py --distpath .\

# check and delay 1 second
def timer_event():
    global live_channel, sound_notify, tray_notify
    global stop_threads, sound_played

    # check and wait 1 second
    while True:
        sleep(1)
        if stop_threads == False: 
            if sound_played == False:
                live = youtube(live_channel) 
                if live.islive == True:
                    # winsound.SND_ASYNC can stop while playing    
                    winsound.PlaySound(sound_notify, winsound.SND_ASYNC + winsound.SND_LOOP)
                    sound_played = True
                    icon.notify(tray_notify, title=None)
                    
        if stop_threads == True:
            if sound_played == True:
                # stop playing
                winsound.PlaySound(None, 0)
            break
                 
# right click tray menu     
def after_click(icon, query):
    global stop_threads

    if str(query) == "Exit":
        icon.stop()
        stop_threads = True       
                
# read .ini file // same as .exe file name
app_name = os.path.splitext(os.path.basename(__file__))[0]
ini_name = app_name + ".ini"
config = ConfigParser() 
config.read(ini_name)
live_channel = config.get('Live Channel','Live')
sound_notify = config.get('Sound Notify','Wav')
tray_icon = config.get('Tray Icon','Png')
tray_notify = config.get('Tray Notify','Message')

# prepare thread // timing event
sound_played = False
stop_threads = False
timer_thread = threading.Thread(target=timer_event)
timer_thread.start() 

# windows system tray
image = Image.open(tray_icon) 
icon = pystray.Icon(app_name, image, app_name, menu=pystray.Menu(
       pystray.MenuItem("Exit", after_click)))
icon.run()