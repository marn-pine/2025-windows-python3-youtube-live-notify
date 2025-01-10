# Latest update: 10-Jan-25, for Windows 11 and from Python 3.1.2 
# Ready-compiled stand-alone .exe file used with .ini file
# This app will loop notify you when a YouTube channel goes live. 
# Right-click the tray icon and choose Exit to exit the app.                                                  

# built-in packages
from time import *
from PIL import Image
from configparser import ConfigParser
import threading
import os
import pystray
import winsound

# external packages
# pip install youtube-lv
# pip install pystray 
# pip install pyinstaller // compile to .exe file // pyinstaller --onefile --noconsole youtube-live-notify.py
from ytlv import youtube
import pystray

# check and delay 1 second
def timer_event():
    global stop_threads, live_channel, notify_sound 

    while True:
        sleep(1)  
        live = youtube(live_channel) 
        if live.status == "LIVE" and live.islive == True:
            winsound.PlaySound(notify_sound, winsound.SND_FILENAME)      
        if stop_threads:
            break

# right click tray menu     
def after_click(icon, query):
    global stop_threads

    if str(query) == "Exit":
        stop_threads = True       
        icon.stop()
        
# read ini file
app_name = os.path.splitext(os.path.basename(__file__))[0]
ini_name = app_name + ".ini"
configur = ConfigParser() 
configur.read(ini_name)

live_channel = configur.get('Live Channel','Live')
notify_sound = configur.get('Notify Sound','Wav')
tray_icon = configur.get('Tray Icon','Png')

# prepare thread
stop_threads = False
timer_thread = threading.Thread(target=timer_event)
timer_thread.start() 

# windows system tray
image = Image.open(tray_icon) 
icon = pystray.Icon(app_name, image, app_name, menu=pystray.Menu(
       pystray.MenuItem("Exit", after_click)))
icon.run()