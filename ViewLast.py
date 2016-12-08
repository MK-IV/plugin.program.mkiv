import xbmc, xbmcgui
import os
import time
import sys
import re


Title = "[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
dialog = xbmcgui.Dialog()
tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
WindowsCache = xbmc.translatePath('special://home')
found = 0
    
def TextBoxes(heading,announce):
  class TextBox():
    WINDOW=10147
    CONTROL_LABEL=1
    CONTROL_TEXTBOX=5
    def __init__(self,*args,**kwargs):
      xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
      self.win=xbmcgui.Window(self.WINDOW) # get window
      xbmc.sleep(500) # give window time to initialize
      self.setControls()
    def setControls(self):
      self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
      try: f=open(announce); text=f.read()
      except: text=announce
      self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
      return
  TextBox()
  while xbmc.getCondVisibility('Window.IsVisible(10147)'):  
    time.sleep(.5)
    
    

        
if os.path.exists(tempPath):
    for root, dirs, files in os.walk(tempPath,topdown=True):
        dirs[:] = [d for d in dirs]
        for name in files:
            if ".old.log" not in name.lower():
                if ".log" in name.lower():
                    got_log = 1
                    a=open((os.path.join(root, name))).read()	
                    b=a.replace('\n','NEW_L').replace('\r','NEW_R')
                    match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
                    for checker in match:
                        found = 1
                        THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
                    if found == 0:
                        dialog.ok(Title,'Great news! We did not find any errors in your log.')
                        sys.exit()
                    else:
                        c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
                        TextBoxes(Title,"%s" % c)
                        sys.exit(0)

if os.path.exists(WindowsCache):
    for root, dirs, files in os.walk(WindowsCache,topdown=True):
        dirs[:] = [d for d in dirs]
        for name in files:
            if ".old.log" not in name.lower():
                if ".log" in name.lower():
                    got_log = 1
                    a=open((os.path.join(root, name))).read()	
                    b=a.replace('\n','NEW_L').replace('\r','NEW_R')
                    match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(b)
                    for checker in match:
                        found = 1
                        THE_ERROR = "[B][COLOR red]THE LAST ERROR YOU ENCOUNTERED WAS:[/B][/COLOR]\n\n" + checker + '\n'
                    if found == 0:
                        dialog.ok(Title,'Great news! We did not find any errors in your log.')
                        sys.exit(0)
                    else:
                        c=THE_ERROR.replace('NEW_L','\n').replace('NEW_R','\r')
                        TextBoxes(Title,"%s" % c)
                        sys.exit(0)
if got_log == 0:
    dialog.ok(Title,'Sorry we could not find a log file on your system')
