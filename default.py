"""
    Copyright (C) 2016 MK-IV Wizard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import xbmc, xbmcaddon, xbmcgui, xbmcplugin  
import mk4
from lib import mk4video as mv
import urllib
import re
import os
import time
import sys
import uploadlog
import plugintools

addon_id = 'plugin.program.mkiv'
ADDON = xbmcaddon.Addon(id=addon_id)
PATH = "MK-IV"
Title = "[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
Master   =  xbmc.translatePath(os.path.join('special://home/addons/' , 'plugin.program.mkiv-master'))
AddonFolder   =  xbmc.translatePath(os.path.join('special://home/addons/' , 'plugin.program.mkiv'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons',''))
dp           =  xbmcgui.DialogProgress()
repo = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/', 'repo.zip'))
repo1 = xbmc.translatePath(os.path.join('special://home/addons/' , 'repository.mkiv-1.0'))
MK4Build   =  xbmc.translatePath(os.path.join('special://home/addons/' , 'plugin.program.mkiv.notifications'))
Slave = xbmc.translatePath(os.path.join('special://home/addons/' , 'script.mkiv-2.0'))
InstallRepo          =  ADDON.getSetting('InstallRepo')
AutoUpdate  =  ADDON.getSetting('AutoUpdate')
BackupPath   =  ADDON.getSetting('backup')
WorkPath     =  ADDON.getSetting('MK4WorkFolder')


'''#Get params and clean up into string or integer
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param'''


params=plugintools.get_params()
url=None
name=None
buildname=None
updated=None
author=None
version=None
mode=None
iconimage=None
description=None
video=None
link=None
skins=None
videoaddons=None
audioaddons=None
programaddons=None
audioaddons=None
sources=None
local=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        guisettingslink=urllib.unquote_plus(params["guisettingslink"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        mode=str(params["mode"])
except:
        pass
try:
        link=urllib.unquote_plus(params["link"])
except:
        pass
try:
        skins=urllib.unquote_plus(params["skins"])
except:
        pass
try:
        videoaddons=urllib.unquote_plus(params["videoaddons"])
except:
        pass
try:
        audioaddons=urllib.unquote_plus(params["audioaddons"])
except:
        pass
try:
        programaddons=urllib.unquote_plus(params["programaddons"])
except:
        pass
try:
        pictureaddons=urllib.unquote_plus(params["pictureaddons"])
except:
        pass
try:
        local=urllib.unquote_plus(params["local"])
except:
        pass
try:
        sources=urllib.unquote_plus(params["sources"])
except:
        pass
try:
        adult=urllib.unquote_plus(params["adult"])
except:
        pass
try:
        buildname=urllib.unquote_plus(params["buildname"])
except:
        pass
try:
        updated=urllib.unquote_plus(params["updated"])
except:
        pass
try:
        version=urllib.unquote_plus(params["version"])
except:
        pass
try:
        author=urllib.unquote_plus(params["author"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        video=urllib.unquote_plus(params["video"])
except:
        pass

        

                      
params=plugintools.get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None
fav_mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:
    fav_mode=int(params["fav_mode"])
except:
    pass
        
        
print str(PATH)+': '+str(ADDON.getAddonInfo('version'))
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


        
        
if mode==None or url==None or len(url)<1:
        mk4.NewSession()
        mk4.INDEX()
elif mode==2: mk4.HelpVideos()
elif mode==3: mk4.WebsitesMenu()
elif mode==4: mk4.deletecachefiles(url)
elif mode==5: mk4.YouTube(url)
elif mode==6: mk4.FRESHSTART(params)
elif mode==7: mk4.DeletePackages(url)
elif mode==8: mk4.EndUser()
elif mode==9: mk4.Restore(url)
elif mode==10: mk4.ADDONWIZ(name,url,description)
elif mode==11: mk4.DeleteThumbnails(url)
elif mode==12: mk4.UNIVERSAL_BACKUP()
elif mode==13: mk4.TESTWIZARDMENU()
elif mode==14: mk4.CANADABUILDS()
#elif mode==15: USABUILDS()
elif mode==16: mk4.SUBMITREQUEST()
#elif mode==17: UKBUILDS()
elif mode==18: mk4.ADULTCONTENT()
elif mode==19: mk4.OpenWebpage(url)
elif mode==20: mk4.BUILDMENU()
elif mode==21: mk4.THEMES()
elif mode==22: mk4.AddonMenu()
elif mode==23:
        mk4.INSTALLAPK(name, url, description)
        if name=='Snes9x': 
            dialog = xbmcgui.Dialog()
            if dialog.yesno(Title, 'Additional files are available for this app.', 'Would you like to download them?','(480.7M)', nolabel='SKIP',yeslabel='Yes'):
                mk4.APKDOWNWIZ('AlphaTest','https://archive.org/download/MarkFourG/ALPHA.zip')
        elif name=='Md.Emu':
            dialog = xbmcgui.Dialog() 
            if dialog.yesno(Title, 'Additional files are available for this app.', 'Would you like to download them?','(342.8M)', nolabel='SKIP',yeslabel='Yes'):
                mk4.APKDOWNWIZ('BetaTest','https://archive.org/download/MarkFourG/BETA.zip')
elif mode==24: mk4.APKDOWNWIZ(name,url)
elif mode==25: mk4.BUILDERS()
elif mode==26: mk4.MAINTENANCE()
elif mode==27: mk4.WIZARD(name,url,version)
elif mode==28: mk4.killxbmc()
elif mode==29: 
        mk4.FIX_SPECIAL(url)
        dialog = xbmcgui.Dialog()
        dialog.ok("Paths successfully changed.", "This process requires a restart \nPress OK to force close the MC.")
        mk4.killxbmc()
elif mode==30:
        mk4.Addon_Settings()
        mk4.BackupMenu()
elif mode==31: mk4.BackupMenu()
elif mode==32: mk4.MKIVWIZARD()
elif mode==33: mk4.FireFox()
elif mode==34: mk4.GetAceStream()
elif mode==35: mk4.RunConsole()
elif mode==36: mk4.RepoMenu()
elif mode==37:
        mk4.BuildAWizardTextBox()
        mk4.BuildAWizardMenu()
elif mode==38: mk4.APKDOWNWIZ('Firefox','http://mkiv.netne.net/Admin/APKs/Firefox.zip','Firefox')
elif mode==39:
        mk4.PlayStore(name, url, description)
        if name=='Snes9x': 
            dialog = xbmcgui.Dialog()
            if dialog.yesno(Title, 'Additional files are available for this app.', 'Would you like to download them?','(480.7M)', nolabel='SKIP',yeslabel='Yes'):
                mk4.APKDOWNWIZ('AlphaTest','https://archive.org/download/MarkFourG/ALPHA.zip')
        elif name=='Md.Emu':
            dialog = xbmcgui.Dialog() 
            if dialog.yesno(Title, 'Additional files are available for this app.', 'Would you like to download them?','(342.8M)', nolabel='SKIP',yeslabel='Yes'):
                mk4.APKDOWNWIZ('BetaTest','https://archive.org/download/MarkFourG/BETA.zip')
elif mode==40: mk4.PlayStoreMenu()
elif mode==41: mk4.SPEEDTEST()
elif mode==42: mk4.RepoAction(name,url)
elif mode==43: mk4.MakePointerFile()
elif mode==44: mk4.MakeRssFile()
elif mode==45: mk4.BuildAWizard()
elif mode==46: mk4.LogMenu()
elif mode==47: mk4.viewErrors()
elif mode==48: mk4.view_LastError()
elif mode==49: mk4.viewLogFile()
elif mode==50: mk4.CHECK_BROKEN_SOURCES()
elif mode==51: mk4.GET_ADDON_STATS()
elif mode==52: mk4.DeleteBackup(url)
elif mode==53: mk4.ListBackDel()
elif mode==54: mk4.ClearLog()
elif mode==55: uploadlog.main(argv=None)
elif mode==56: mk4.INSTALL_FANRIFFIC(name,url, description)
elif mode==57:
        choice = xbmcgui.Dialog().yesno('There are two ways to add your build','Method 1 has more steps but allows Ares to look for updates.','Method 2 has less steps but you need to let Ares know when you update.','',  nolabel='Method 1',yeslabel='Method 2')
        if choice == 0:
            mk4.AddToAres1()
            pass
        elif choice == 1:
            mk4.AddToAres2()
            pass
elif mode==58: mk4.ViewChangelog()
elif mode==59: mk4.BackupSkinSettings()
elif mode==60: mk4.RestoreSkinSettings()
elif mode==61: mk4.DeleteSkinBackup()
elif mode==62: mk4.ThemeMenu()
elif mode==63: mk4.JarvisThemes()
elif mode==64: mk4.KryptonThemes()
elif mode==65: mk4.OldThemes()
elif mode==66: mk4.NewThemes()
elif mode==67: mk4.GuideThemes()
elif mode==68: mk4.ThemeUpdates()
elif mode==69: mk4.SkyThemesGui()
elif mode==70: mk4.EnableAll()
elif mode==71: mk4.ListBackRes()
elif mode==72: mk4.DeleteBackup(url)
elif mode==73: mk4.DeleteAllBackups()
elif mode==74: mk4.RestoreOther()
elif mode==75: mk4.MK4Backgrounds()
elif mode==76: mk4.RestoreMK4Backgrounds()
elif mode==77: mk4.DeleteMK4BackgroundsBackup()
elif mode==78: mk4.Contact()
elif mode==79: mk4.MK4WizUpdate()
elif mode==80: mk4.AddonInstallWindow()
elif mode==81: mk4.UpdateSwitch()
elif mode==82:
    Passcode=xbmcgui.Dialog().input('Type 1234', type=xbmcgui.INPUT_NUMERIC)
    try:
        if PasscodeAttempt == '1234':
            mk4.ResetMK4Settings()
        else: sys.exit(0)
    except: sys.exit(0)
elif mode==83: mk4.RepoFiles()
elif mode==84: mk4.md5File()
elif mode==85:
    #if xbmcgui.Dialog().yesno('[COLOR red]WARNING!!![/COLOR]','Sorry,this section is for approved testers only.','','','Turn Back','Enter'):
        import hashlib
        passcode = ADDON.getSetting('Test')
        PasscodeAttempt=xbmcgui.Dialog().input('Enter Passcode', type=xbmcgui.INPUT_NUMERIC)
        PasscodeAttempt=hashlib.md5(PasscodeAttempt).hexdigest()
        if PasscodeAttempt == passcode:
            mk4.Toast('[COLOR lime]Welcome to the Testing Area[/COLOR]')
            mk4.TestMenu()
        else:
            #if xbmc.getCondVisibility('System.HasAddon(plugin.video.youtube)'):
             #   mk4.YouTube('tgj3nZWtOfA')
            #else:
            #xbmc.executebuiltin("ShowPicture('http://www.cutestpaw.com/wp-content/uploads/2013/09/White-Bunny.jpg')")
            sys.exit(0)
    #else: sys.exit(0)
elif mode==86: mk4.BuildARepo()
elif mode==87: mv.MK4Video()
elif mode==88: mv.GetTvImdb(url)
elif mode==89: mv.GetGenres(url)
elif mode==90: mv.GetYears(url)
elif mode==91: mv.GetContent(url)
elif mode==92: mv.Search()
elif mode==93: mv.GetImdb(url)
elif mode==94: mv.GetTV(url)
elif mode==95: mv.GetShowContent(url)
elif mode==96: mv.resolve(name,url,iconimage, description)
elif mode==97: mk4.RepoAddon()
elif mode==98: mk4.RepoUpdater()
elif mode==99: mk4.BuildARepoMenu()
elif mode==100: mk4.MKIVMENU() 
elif mode==101: mk4.B64Encode()
elif mode==102: mk4.B64Decode()
elif mode==103: mk4.ToolsMenu()
elif mode==104: mk4.B64View()
elif mode==105: mv.QueueItem()
elif mode==106:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    mv.addFavorite(name,url,iconimage,fanart,fav_mode)
elif mode==107:
    try:
        name = name.split('\\ ')[1]
    except:
        pass
    try:
        name = name.split('  - ')[0]
    except:
        pass
    mv.rmFavorite(name)
elif mode==108: xbmc.executebuiltin('ActivateWindow(10134,return)')#mv.GetFavourites()
elif mode==109: mv.Movies()
elif mode==110: mv.TV()

    
    
		
xbmcplugin.endOfDirectory(int(sys.argv[1]))
