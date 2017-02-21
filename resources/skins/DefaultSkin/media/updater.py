import xbmc, xbmcgui, xbmcaddon
import shutil
import os
import re
import downloader
import extract
import time
import urllib2

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def UpdateCheck(AddonTitle, addon_id):
    try:
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle,'Checking for updates...','', 'Please Wait')
        link = OPEN_URL('https://raw.githubusercontent.com/MK-IV/BuildAWizard/master/addon.xml').replace('\n','').replace('\r','')
        match = re.compile('BAWversion="(.+?)"').findall(link)
        for BAWversion in match:
            ADDON=xbmcaddon.Addon(id=addon_id)
            xbmc.log(AddonTitle+' is checking for core updates...')
            xbmc.log(addon_id+' Latest version='+BAWversion+' Installed version='+ADDON.getAddonInfo("version")+'')
            if BAWversion > ADDON.getAddonInfo('version'):
                xbmc.log(AddonTitle+' Update files found... Attempting update...')
                #try:
                ADDONS = xbmc.translatePath(os.path.join('special://home','addons',''))
                path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                dp = xbmcgui.DialogProgress()
                dp.create(AddonTitle,'Downloading '+AddonTitle+' update...','', 'Please Wait')
                lib=os.path.join(path, 'BuildAWizard-master.zip')
                try:
                    os.remove(lib)
                except:
                    pass
                downloader.download('https://github.com/MK-IV/BuildAWizard/archive/master.zip', lib, dp)
                dp.update(0,'Downloading '+AddonTitle+' update... [COLOR lime]Finished[/COLOR]', 'Installing...')
                extract.all(lib,ADDONS,dp)
                time.sleep(.5)
                try:
                    os.remove(lib)
                except:
                    pass
                Addons = xbmc.translatePath('special://home/addons/')
                addontmp = xbmc.translatePath(os.path.join(Addons+'BuildAWizard-master/','addon.xml'))
                defaulttmp = xbmc.translatePath(os.path.join(Addons+'BuildAWizard-master/','default.py'))
                updatetmp = xbmc.translatePath(os.path.join(Addons+'BuildAWizard-master/','updater.py'))
                defaultpy = xbmc.translatePath(os.path.join(Addons+addon_id,'default.py'))
                updatepy = xbmc.translatePath(os.path.join(Addons+addon_id,'updater.py'))
                addonxml = xbmc.translatePath(os.path.join(Addons+addon_id,'addon.xml'))
                local = xbmc.translatePath(os.path.join(Addons,addon_id))
                localtmp = xbmc.translatePath(os.path.join(Addons,addon_id+'-tmp'))
                master = xbmc.translatePath(os.path.join(Addons,'BuildAWizard-master'))
                fanart = xbmc.translatePath(os.path.join(local,'fanart.jpg'))
                icon = xbmc.translatePath(os.path.join(local,'icon.png'))
                fanart1 = xbmc.translatePath(os.path.join(localtmp,'fanart.jpg'))
                icon1 = xbmc.translatePath(os.path.join(localtmp,'icon.png'))
                link = open(os.path.join(local, 'default.py'))
                match = re.compile('addonname="(.+?)"wizardname="(.+?)"providername="(.+?)"zipurl="(.+?)"').findall(link)
                for addonname,wizardname,providername,zipurl in match:
                    a=open(addontmp).read()
                    b=a.replace('addonname',addonname).replace('wizardname',wizardname).replace('providername',providername)
                    f = open(addontmp, mode='w')
                    f.write(str(b))
                    f.close()
                    time.sleep(2)
                    a=open(defaulttmp).read()
                    b=a.replace('addonname',addonname).replace('wizardname',wizardname).replace('providername',providername).replace('zipurl',zipurl)
                    f = open(defaulttmp, mode='w')
                    f.write(str(b))
                    f.close()
                    pass
                try:
                    os.rename(local,localtmp)
                    os.rename(master,local)
                    if os.path.exists(icon1):
                        shutil.copy(icon1,icon)
                    if os.path.exists(fanart1):
                        shutil.copy(fanart1,fanart)
                    shutil.rmtree(localtmp)
                except: pass
                dp.close
                xbmc.executebuiltin("Container.Refresh")
                #except: pass
            else: pass
    except: pass
