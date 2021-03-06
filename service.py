import os
import xbmc, xbmcgui,  xbmcaddon
import re
import mk4
import time
from lib import repo


MK4Notifications   =  xbmc.translatePath(os.path.join('special://home/addons/' , 'plugin.program.mkiv.notifications'))
addon_id = 'plugin.program.mkiv'
ADDON = xbmcaddon.Addon(id=addon_id)
Title = "[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
my_addon = xbmcaddon.Addon()
dp = xbmcgui.DialogProgress()
dialog = xbmcgui.Dialog()
Addons20 = xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons20.db'))
ART = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
phoenix = xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.phstreams'))
Installer=xbmc.translatePath('special://home/addons/plugin.program.mkiv-installer')
AresTracker = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/script.areswizard/','buildinstall'))
RequestPatch=xbmc.translatePath(os.path.join('special://home/addons/script.module.requests/lib/requests/','packages'))
skin=xbmc.getSkinDir()
myplatform = mk4.platform()
dp           =  xbmcgui.DialogProgress()
GoogleOne = "http://www.google.com"
GoogleTwo = "http://www.google.co.uk"
BASEURL = "http://mk-iv.github.io" 


mk4.SetSetting('NewSession','true')


xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
version=float(xbmc_version[:4])
if version >= 16.0 and version <= 16.9:
    mk4.SetSetting('KodiVersion','Jarvis')
    pass
    # if ADDON.getSetting('FreshStart') == 'false':
    #     try:
    #         mk4.ShowPic('https://raw.githubusercontent.com/MK-IV/Dependencies/master/ProgramSplash/fanart.jpg')
    #        pass
    #    except: pass
    #else: pass
elif version >= 17.0 and version <= 17.9:
    mk4.SetSetting('KodiVersion','Krypton')
    if ADDON.getSetting('BuildName') == "MK-IV" or ADDON.getSetting('BuildName') == "MK-IV (UK Server)":
        mk4.RequiredUpdate()
        pass
    else: pass
    #if ADDON.getSetting('FreshStart') == 'false':
    #    try:
    #         mk4.ShowPic('https://raw.githubusercontent.com/MK-IV/Dependencies/master/ProgramSplash/fanart.jpg')
    #         pass
    #    except: pass
    #else: pass
    if os.path.exists(Addons20):
        mk4.RemoveTrigger()
        pass
else: pass
#if ADDON.getSetting('KodiVersion')=='Krypton' and os.path.exists(RequestPatch):
   # mk4.InstallRequests()

if ADDON.getSetting('FreshStart') == 'true':
    mk4.SetSetting('FreshStart','false')
    pass
else: pass

if not os.path.exists(MK4Notifications):
    mk4.SetSetting('MK4Build', 'false')
    pass
else:
    mk4.SetSetting('MK4Build', 'true')
    pass

if ADDON.getSetting('InstallRepo') == 'true':
    repo.InstallRepo
    pass
else: pass
 
if os.path.exists(Installer):
    mk4.RemoveInstaller()
    pass

if os.path.exists(AresTracker):
    a=open(AresTracker).read()	
    b=a.replace('\n','').replace('\r','').replace('{"canupdate": ','canupdate=').replace(', "guisettingssize": ',' guisettingssize=').replace(', "wizardname": ',' wizardname=').replace(', "installedversion": ',' installedversion=').replace(', "buildurl": ',' buildurl=').replace(', "buildname": ',' buildname=').replace('}','')
    AresName = re.compile('buildname="(.+?)"').findall(b)
    AresURL = re.compile('buildurl="(.+?)"').findall(b)
    AresVersion = re.compile('installedversion="(.+?)"').findall(b)
    xbmc.log('Ares Tracker Info: '+b)
    for buildname in AresName:
        if buildname != ADDON.getSetting('AresName'):
            mk4.SetSetting('AresName', buildname)
            pass
        else: pass  
    for installedversion in AresVersion:
        if installedversion != ADDON.getSetting('AresVersion'):
            mk4.SetSetting('AresVersion', installedversion)  
            pass
        else: pass
else: pass
if ADDON.getSetting('AresName') == "":
    pass
elif ADDON.getSetting('BuildName') == "" and ADDON.getSetting('AresName') != "":
    mk4.SetSetting('BuildName', ADDON.getSetting('AresName'))
    mk4.SetSetting('BuildVersion', ADDON.getSetting('AresVersion'))
    pass
elif ADDON.getSetting('BuildName') == ADDON.getSetting('AresName'):
    if ADDON.getSetting('AresVersion') > ADDON.getSetting('BuildVersion'):
        mk4.SetSetting('BuildVersion', ADDON.getSetting('AresVersion'))
        pass
    elif ADDON.getSetting('AresVersion') < ADDON.getSetting('BuildVersion'):
        os.remove(AresTracker)
        mk4.SetSetting('AresVersion', ADDON.getSetting('BuildVersion'))
        pass
else: pass
        
if ADDON.getSetting('UpdateAddons') == 'true':
    #Update all repos and packages.
    xbmc.executebuiltin("UpdateAddonRepos")
    xbmc.executebuiltin("UpdateLocalAddons")
    pass
else: pass

#if not os.path.exists(RequestPatch) and ADDON.getSetting('KodiVersion') == 'Krypton':
#    if skin != 'skin.estuary' and skin != 'skin.estouchy':
#        time.sleep(30)
#        if xbmcgui.Dialog().yesno(Title,'[COLOR red]A patch is available to fix errors you might be having...[/COLOR]','','Would you like to apply a patch?'):
#            mk4.ADDONWIZ('Python Requests Module','http://mkiv.netne.net/Admin/Addon%20Packs/script.module.requests-2.9.1.zip','script.module.requests')
#            time.sleep(2)
#            mk4.EnableAll()
#            time.sleep(2)
#            xbmc.executebuiltin('UpdateLocalAddons')
#            pass
#        else: pass
#    else: pass
#else: pass

# Sleeper added due to the updating of addons.
time.sleep(60)

if ADDON.getSetting('MK4Build') == 'true' and ADDON.getSetting('FirstMK4Startup') == 'true':
    mk4.SetSetting('FirstMK4Startup','false')
    if myplatform == 'android':
        dialog = xbmcgui.Dialog()
        if dialog.yesno(Title, 'The AceStream Engine is required to play some sports section content.', 'After its installed sign into the app and thats it.','Would you like to download and install now?', nolabel='SKIP',yeslabel='Yes'):
            if dialog.yesno(Title, 'Is your Android device x86 or ARM based', '','(If your not sure try ARM first)', nolabel='ARM',yeslabel='x86'):
                mk4.INSTALLAPK('acestreamsx86','https://archive.org/download/aappkk/AceStream-3.1.6.0-x86.apk','')
                #mk4.INSTALLAPK('acestreams','http://dl.acestream.org/products/acestream-engine/android/latest','')
                pass
            else:
                mk4.INSTALLAPK('acestreamsARM','https://archive.org/download/aappkk/AceStream-3.1.6.0-armv7.apk','')
                pass
        else:
            dialog.ok(Title,'This message will not be shown again','To download AceStreams later go to the MK-IV Wizard','and look in the MK-IV Build Menu.')
            pass
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno(Title, 'The AceStream Engine is required to play some sports section content.', 'After its installed sign into the app and thats it.','Would you like to download and install now?', nolabel='SKIP',yeslabel='Yes'):
            dialog.ok(Title,'Press OK to launch your browser to the download page','You only need the engine.','')
            mk4.OpenWebpage('http://wiki.acestream.org/wiki/index.php/AceStream_3.0/en')
            pass
        else:
            dialog.ok(Title,'This message will not be shown again','To download AceStreams later go to the MK-IV Wizard','and look in the MK-IV Build Menu.')
            pass
else: pass


if ADDON.getSetting('AutoClean') == 'true':
    mk4.CleanOnStart()
    pass
else: pass

time.sleep(10)

if ADDON.getSetting('BuildName') != '' and ADDON.getSetting('BuildVersion') != '':
    if ADDON.getSetting('Update') == 'true':
        mk4.Check4Update()
        pass
    else: pass
else: pass
