import xbmc, xbmcgui
import os
import time


Title = "[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
dialog = xbmcgui.Dialog()
kodilog = xbmc.translatePath('special://logpath/kodi.log')
spmclog = xbmc.translatePath('special://logpath/spmc.log')
dbmclog = xbmc.translatePath('special://logpath/dbmc.log')
kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
spmcold = xbmc.translatePath('special://logpath/spmc.old.log')
dbmcold = xbmc.translatePath('special://logpath/dbmc.old.log')
    
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
    
if os.path.exists(dbmclog):
    if os.path.exists(dbmclog) and os.path.exists(dbmcold):
        choice = xbmcgui.Dialog().yesno(Title,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
        if choice == 0:
            f = open(dbmclog,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
            TextBoxes(Title+' - Log Viewer',"%s - dbmc.log" % "[COLOR white]" + msg + "[/COLOR]")
        else:
            f = open(dbmcold,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
            TextBoxes(Title+' - Log Viewer',"%s - dbmc.old.log" % "[COLOR white]" + msg + "[/COLOR]")
    else:
        f = open(dbmclog,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
        TextBoxes(Title+' - Log Viewer',"%s - dbmc.log" % "[COLOR white]" + msg + "[/COLOR]")

if os.path.exists(spmclog):
    if os.path.exists(spmclog) and os.path.exists(spmcold):
        choice = xbmcgui.Dialog().yesno(Title,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
        if choice == 0:
            f = open(spmclog,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
            TextBoxes(Title+' - Log Viewer',"%s - spmc.log" % "[COLOR white]" + msg + "[/COLOR]")
        else:
            f = open(spmcold,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
            TextBoxes(Title+' - Log Viewer',"%s - spmc.old.log" % "[COLOR white]" + msg + "[/COLOR]")
    else:
        f = open(spmclog,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
        TextBoxes(Title+' - Log Viewer',"%s - spmc.log" % "[COLOR white]" + msg + "[/COLOR]")
        
if os.path.exists(kodilog):
    if os.path.exists(kodilog) and os.path.exists(kodiold):
        choice = xbmcgui.Dialog().yesno(Title,"Current & Old Log Detected on your system.","Which log would you like to view?","", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
        if choice == 0:
            f = open(kodilog,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
            TextBoxes(Title+' - Log Viewer',"%s - kodi.log" % "[COLOR white]" + msg + "[/COLOR]")
        else:
            f = open(kodiold,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
            TextBoxes(Title+' - Log Viewer',"%s - kodi.old.log" % "[COLOR white]" + msg + "[/COLOR]")
    else:
        f = open(kodilog,mode='r'); rawmsg = f.read().replace(' ERROR: ',' [COLOR red]ERROR[/COLOR]: ').replace(' WARNING: ',' [COLOR gold]WARNING[/COLOR]: '); msg = '\n'.join(rawmsg.splitlines()[::-1]); f.close()
        TextBoxes(Title+' - Log Viewer',"%s - kodi.log" % "[COLOR white]" + msg + "[/COLOR]")

else:
    dialog.ok(Title,'Sorry, No log file was found.','','[COLOR smokewhite]Thank you for using MK-IV Wizard[/COLOR]')
