"""
    Copyright (C) 2017 MK-IV Wizard

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
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib
import sqlite3
import plugintools
#import errno
import re
import downloader, extract, webbrowser, plugintools
import time
from addon.common.addon import Addon
from addon.common.net import Net
#from xml.etree import ElementTree as et
import zipfile
#import ntpath
import glob
#import subprocess
import speedtest
#import uploadlog
from lib import smtplib
import hashlib
# Py2
try:
    from urlparse import urljoin
    from urllib import quote_plus, unquote_plus
    import urllib2
    from HTMLParser import HTMLParser

# Py3:
except ImportError:
    import urllib.request as urllib2
    from urllib.parse import urljoin, quote_plus, unquote_plus

from resources.libs import extract, downloader, notify, debridit, traktit, loginit, skinSwitch, uploadLog, yt, speedtest, wizard as wiz



USER_AGENT='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id='plugin.program.mkiv'
ADDON=xbmcaddon.Addon(id=addon_id)
version=ADDON.getAddonInfo('version')
AddonID='plugin.program.mkiv'
Title="[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
dialog=xbmcgui.Dialog()
net=Net()
HOME=xbmc.translatePath('special://home/')
dp=xbmcgui.DialogProgress()
FANART=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))            
BASEURL="http://mkiv.netne.net" 
phoenix=xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.phstreams'))
repo1=xbmc.translatePath(os.path.join('special://home/addons/' , 'repository.mkiv-1.0'))
H='http://'
Hs='https://'
skin=xbmc.getSkinDir()
EXCLUDES=['BackgroundsBackup.zip','kodi.log','script.areswizard','sources.xml','favourites.xml','plugin.program.mkiv','plugin.program.mkiv-master','script.module.addon.common','autoexec.py','service.xbmc.versioncheck','metadata.tvdb.com','metadata.common.imdb.com']
BackupPath=ADDON.getSetting('backup')
fullbackuppath=xbmc.translatePath(os.path.join(BackupPath,'KODI Backups'))
WorkPath=ADDON.getSetting('MK4WorkFolder')
fullworkpath=xbmc.translatePath(os.path.join(WorkPath,'KODI Work Folder'))
Downloader=xbmc.translatePath(os.path.join('special://home/addons/'+ addon_id , 'downloader.py'))
Extractor=xbmc.translatePath(os.path.join('special://home/addons/'+ addon_id , 'extract.py'))
Local=xbmc.translatePath(os.path.join('special://home/addons/',addon_id))
Localtmp=xbmc.translatePath(os.path.join('special://home/addons/',addon_id+'-tmp'))
Master=xbmc.translatePath(os.path.join('special://home/addons/',addon_id+'-master'))
ART=BASEURL+'/Admin/Pictures/'
PACKAGES=xbmc.translatePath(os.path.join('special://home/addons','packages'))
USERDATA=xbmc.translatePath(os.path.join('special://home/','userdata'))
MEDIA=xbmc.translatePath(os.path.join('special://home/media',''))
MAIN=xbmc.translatePath(os.path.join('special://home',''))
AUTOEXEC=xbmc.translatePath(os.path.join(USERDATA,'autoexec.py'))
ADDON_DATA=xbmc.translatePath(os.path.join('special://home/userdata/','addon_data/'))
SkinSettings=xbmc.translatePath(os.path.join('special://home/userdata/addon_data/','%s')) % skin
SkinSettingsXML=xbmc.translatePath(os.path.join('special://home/userdata/addon_data/%s/','settings.xml')) % skin
PLAYLISTS=xbmc.translatePath(os.path.join(USERDATA,'playlists'))
ADDONS=xbmc.translatePath(os.path.join('special://home','addons'))
GUISETTINGS=os.path.join(USERDATA,'guisettings.xml')
A='archive.org'
Media1=xbmc.translatePath(os.path.join('special://home/addons/'+addon_id+'/resources/skins/DefaultSkin/media/'))
GUI=xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
GuiBackup=xbmc.translatePath(os.path.join(USERDATA,'guisettingsbackup'))
_SkinSettings=xbmc.translatePath(os.path.join(USERDATA,'SkinSettingsBackup'))
SkinSettingsBackup=xbmc.translatePath(os.path.join('special://home/userdata/','SkinSettingsBackup.zip'))
Backgrounds=xbmc.translatePath(os.path.join(USERDATA,'Background_pics'))
BackgroundsBackup=xbmc.translatePath(os.path.join(USERDATA,'BackgroundsBackup'))
BackgroundsBackupZip=xbmc.translatePath(os.path.join(USERDATA,'BackgroundsBackup.zip'))
ScriptSkin=xbmc.translatePath(os.path.join('special://home/userdata/addon_data/','script.skinshortcuts'))
ScriptSkinBackup=xbmc.translatePath(os.path.join('special://home/userdata/','ScriptSkinShortcutsBackup.zip'))
addon_dataBackup=xbmc.translatePath(os.path.join('special://home/userdata/','addon_dataBackup.zip'))
Requests=xbmc.translatePath(os.path.join('special://home/addons/','script.module.requests'))
USB=xbmc.translatePath(os.path.join(BackupPath,'KODI Backups'))
INSTALL=xbmc.translatePath(os.path.join(USERDATA,'install.xml'))
FAVS=xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE=xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED=xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
PROFILES=xbmc.translatePath(os.path.join(USERDATA,'profiles.xml'))
RSS=xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS=xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
WorkFolder=xbmc.translatePath(os.path.join(WorkPath))
Resources=xbmc.translatePath(os.path.join(ADDONS,AddonID,'resources/'))
ChangeLog=xbmc.translatePath(os.path.join(ADDONS,AddonID,'changelog.txt'))
skin=xbmc.getSkinDir()
userdatafolder=xbmc.translatePath(os.path.join(ADDON_DATA,AddonID))
urlbase='None'
mk4g='MarkFourG/'
Installer=xbmc.translatePath('special://home/addons/plugin.program.mkiv-installer')
password=ADDON.getSetting('password')
InstallRepo=ADDON.getSetting('InstallRepo')
ShowAdult=ADDON.getSetting('ShowAdult')
AutoUpdate=ADDON.getSetting('AutoUpdate')
AutoUpdateClean=ADDON.getSetting('AutoUpdateClean')
SettingsFile=xbmc.translatePath(os.path.join(ADDON_DATA+addon_id,'settings.xml'))
JARVIS=xbmc.translatePath(os.path.join('special://home/','JARVIS.xml'))
KODI16=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons20.db'))
Addons20=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons20.db'))
Addons26=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons26.db'))
Addons27=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons27.db'))
Database=xbmc.translatePath(os.path.join('special://home/userdata/','Database/'))
FreshStart=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/', 'FreshStart.db'))
Textures13=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Textures13.db'))
log_path=xbmc.translatePath('special://logpath/')
AppPath="/storage/emulated/0/Download/"
P='/download/'
MK4Build=xbmc.translatePath(os.path.join('special://home/addons/' , 'plugin.program.mkiv.notifications'))
Slave=xbmc.translatePath(os.path.join('special://home/addons/' , 'script.mkiv-2.0'))
THE_TIME=time.strftime("%H:%M %p")
THE_DATE=time.strftime("%A %B %d %Y")
Build_A_Icon=xbmc.translatePath(os.path.join(Media1,'icon.png'))



def TestMenu():
        #Toast('Entering Testing Area')
        addItem('md5File',BASEURL,84,ICON,FANART,'')
        addItem('Repo Files',BASEURL,83,ICON,FANART,'')
        addItem('Build A Repo',BASEURL,86,ICON,FANART,'')
        addItem('Repo Addon',BASEURL,97,ICON,FANART,'')
        addItem('Repo updater',BASEURL,98,ICON,FANART,'')
        addDir('[B][COLOR red]MK-IV Video[/COLOR][/B]','JVtHtoiKYAE',87,ICON,FANART,'','')
        addItem('[B][COLOR red]Reduce image size[/COLOR][/B]','JVtHtoiKYAE',111,ICON,FANART,'')
       # time.sleep(3)
        #if xbmcgui.Dialog().yesno(Title,'Disable Password for Test Area?'):
            #SetSetting('Test','')
            #pass
        #else: pass

def INDEX(): #1
        xbmc.executebuiltin('SendClick(12005,Close)')
        PlayerWindow=xbmcgui.Window(12005)
        PlayerWindow.close()
        addDir('[B][COLOR red]MK-IV [/COLOR][COLOR deepskyblue]Build Menu[/COLOR][/B]','JVtHtoiKYAE',100,ICON,FANART,'','')
        #addDir('[B][COLOR red]BUILDS[/B]',BASEURL,20,ART+'builds.png',FANART,'','')
        myplatform = platform()            
        if myplatform == 'android':
            addDir('[COLOR lime][B]Android Apps[/B][/COLOR]',BASEURL,40,'http://www.technocrazed.com/wp-content/uploads/2015/01/Using-Arabic-Urdu-Persian-And-Other-Languages-Fonts-In-Android-App-Development-1.jpg',FANART,'','')       
        addDir('[B][COLOR red]MK-IV Video[/COLOR][/B]','JVtHtoiKYAE',87,ICON,FANART,'','')
	addDir('[B]Log Viewer[/B]',BASEURL,46,'http://www.iconshock.com/img_jpg/STROKE/communications/jpg/256/log_file_icon.jpg',FANART,'','')
        addDir('[B]Maintenance[/B]',BASEURL,26,'http://vignette3.wikia.nocookie.net/paw-patrol/images/8/89/Character_large-rocky.jpg/revision/latest?cb=20140112112749',FANART,'','')
        addDir('[B]Backup/Restore[/B]',BASEURL,31,'http://cdn1.itpro.co.uk/sites/itpro/files/styles/article_main_wide_image/public/2015/06/backup.jpg?itok=e3650P7m',FANART,'','')
        addDir('[B]Add Sources[/B]',BASEURL,36,'http://cdn.htpcbeginner.com/images/2015/09/03-Add-Video-Source-Browse-for-New-Share.jpg',FANART,'','')
        addDir('[B]Add-ons[/B]',BASEURL,22,'http://celticdroid.net/xbmc/tools/wizard/images/backgrounds/Addons.jpg',FANART,'','')
        addDir('[B]Developer Tools[/B]',BASEURL,25,'http://gonintendo.com/system/file_uploads/uploads/000/013/711/original/MnRlr66.jpg',FANART,'','')
        addDir('[B]System Info[/B]',BASEURL,51,ICON,FANART,'','')
        addItem('[B]End User Info[/B]',BASEURL,8,'http://appv2.asustor.com/uploadIcons/0020_999_1422510692_kodi256.png',FANART,'')
        if myplatform == 'android':
            addDir('[B]Download Firefox[/B]','org.mozilla.firefox',33,'http://orig13.deviantart.net/877f/f/2011/117/f/a/mozilla_firefox_by_dj_fahr-d3ezwg9.png',FANART,'','')
        if ShowAdult=='true':
            addDir('[B]Adult Content[/B]',BASEURL,18,'http://kodi.iptvaddon.com/wp-content/uploads/2015/03/xxx-ADULT-ADDON-FOR-KODI-XBMC-new-video-and-addon.jpg',FANART,'','')
        else: pass
        addItem('[B][/B]','service.xbmc.versioncheck',666,ICON,FANART,'')
        addItem('[B][COLOR yellow]Contact Form[/COLOR][/B]','http://www.mkiv.ca/contact.html',19,'http://downloadicons.net/sites/default/files/contacts-icon-14474.png',FANART,'')
        addItem('[B][COLOR deepskyblue]View Changelog[/COLOR][/B]',BASEURL,58,'http://www.workschedule.net/wp-content/uploads/2014/08/changelog1.png',FANART,'')
        addItem('[COLOR yellow][B]Settings[/B][/COLOR]',BASEURL,30,'https://s-media-cache-ak0.pinimg.com/564x/c7/d6/9a/c7d69ab67de8553c02c0555409267b90.jpg',FANART,'')
        addItem('[COLOR deepskyblue][B]Force update check[/B][/COLOR]  (Database Version: '+version+')',BASEURL,79,ICON,FANART,'')
        addItem('[B][COLOR yellow]Reset [/COLOR][/B]'+Title+'[B][COLOR yellow] Settings[/COLOR][/B]','service.xbmc.versioncheck',82,ICON,FANART,'')
        addItem('[B][/B]','service.xbmc.versioncheck',666,ICON,FANART,'')
        if myplatform == 'android':
            addDir('[B][COLOR blue]OPEN MK-IV ON YOUR PC TO UNLOCK EVEN MORE[/COLOR][/B]',BASEURL,666,ICON,FANART,'','')
        else:
            addDir('[B][COLOR blue]OPEN MK-IV ON YOUR ANDROID TO UNLOCK EVEN MORE[/COLOR][/B]',BASEURL,666,ICON,FANART,'','')

def BUILDMENU():
    addDir('[COLOR red][B]Canadian Builds[/B][/COLOR]',BASEURL,14,ART+'ca.jpg',FANART,'','')
    addDir('[COLOR blue][B]USA Builds[/B][/COLOR]',BASEURL,15,ART+'us.jpg',FANART,'','')
    addDir('[COLOR red][B]UK Builds[/B][/COLOR]',BASEURL,17,ART+'uk.jpg',FANART,'','')
    addDir('[COLOR yellow][B]ADD YOUR BUILD TO MK-IV[/B][/COLOR]',BASEURL,16,ART+'website.jpg',FANART,'','')

def MAINTENANCE():
        try:
            os.remove(Textures13)
            pass
        except: pass
        Toast('[COLOR lime]Populating sizes[/COLOR]')
        CacheSize = GETFOLDERSIZE(xbmc.translatePath('special://home/cache'))
        ThumbsSize = GETFOLDERSIZE(xbmc.translatePath('special://home/userdata/Thumbnails'))
        PackagesSize = GETFOLDERSIZE(xbmc.translatePath('special://home/addons/packages'))
        BuildSize = GETFOLDERSIZE(xbmc.translatePath('special://home/'))
        addItem('[B]Delete Cache[/B] ('+CacheSize+')','url',4,'http://a3.mzstatic.com/eu/r30/Purple20/v4/8a/d6/08/8ad6089c-37f1-6670-7aa1-069ba44de89e/icon128-2x.png',FANART,'')
        addItem('[B]Delete Thumbnails[/B] ('+ThumbsSize+')','url',11,'http://icons.iconarchive.com/icons/media-design/hydropro/512/HP-Pictures-Folder-icon.png',FANART,'')
        addItem('[B]Delete Packages[/B] ('+PackagesSize+')','url',7,'http://www.freeiconspng.com/uploads/packages-icon-21.png',FANART,'')
        if ADDON.getSetting('KodiVersion') == 'Krypton':
            addItem('[B]Enable All Addons[/B]','url',70,'http://clipartix.com/wp-content/uploads/2016/04/Thumbs-up-clipart-2.png',FANART,'')
            #addItem('[B]Check Sources[/B]',BASEURL,50,ART+'checksources.png',FANART,'')
            addItem('[B]     -----     [/B]','url',0,ICON,FANART,'')
            addItem('[COLOR red][B]Fresh Start[/B][/COLOR] ('+BuildSize+')','url',6,'http://www.southdecaturchurch.com/files/southdecatur/Pic%20and%20Sermons/FreshStart_preview.jpg',FANART,'')
        if ADDON.getSetting('KodiVersion') == 'Jarvis':
            #addItem('[B]Check Sources[/B]',BASEURL,50,ART+'checksources.png',FANART,'')
            addItem('[COLOR deepskyblue][B]     -----     [/B][/COLOR]','url',0,ICON,FANART,'')
            addItem('[COLOR red][B]Fresh Start[/B][/COLOR] ('+BuildSize+')','url',6,'http://www.southdecaturchurch.com/files/southdecatur/Pic%20and%20Sermons/FreshStart_preview.jpg',FANART,'')

def BUILDERS():
    addDir('[B]Add your build to Ares Wizard[/B]',BASEURL,57,'http://0716zip.ares8.seedr.io/ares_home.jpg',FANART,'','')
    addDir('[B]Build-A-Wizard Section[/B]',BASEURL,37,Build_A_Icon,FANART,'','')
    addItem('[B]Convert Physical Paths To \'special://home/\'[/B]',HOME,29,'http://www.magix.info/mcpool01/10/9B/A5/D2/30/95/7A/11/E1/94/24/AB/1C/59/9A/71/41/9BABC5A0957A11E1A739DD97599A7141.jpg',FANART,'')
    #addDir('[B]Test Wizard[/B]',BASEURL,13,ART+'testwizard.png',FANART,'','')
    addDir('[B]Websites[/B]',BASEURL,3,'http://www.finansovi-otcheti.com/wp-content/uploads/2015/06/business-intro.png',FANART,'','')
    addDir('[B]Download Themes[/B]',BASEURL,62,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')
    addDir('[B]Help Videos[/B]',BASEURL,2,'https://thinklivebepositive.files.wordpress.com/2014/05/helping-others-ws31.jpg',FANART,'','')
    addItem('[B]Speed Test[/B]',BASEURL,41,'http://lh3.ggpht.com/JHRfJdIQ91uybbg7vdqvSRGsii1BbTt8Pt_UXxIC1kZpLpAMfrIC_DETMEzc0Ek5tg=w300',FANART,'')
    addDir('[B]More Tools[/B]',BASEURL,103,'https://openclipart.org/image/2400px/svg_to_png/192629/gear-tools.png',FANART,'','')
    addItem('[B][/B]',BASEURL,0,ICON,FANART,'')
    addItem('[B]Force Close[/B]',BASEURL,28,'http://dreadpirate.info/images/jollyroger2.jpg',FANART,'')

def BackupMenu():
    addItem('[B]Universal Backup[/B]',BASEURL,12,'http://iconbug.com/data/5c/512/3acbd906e7b75eaf09e70d1d26c665f9.png',FANART,'')
    if os.path.exists(fullbackuppath):
        try:
            for file in os.listdir(fullbackuppath):
                path=os.path.join(fullbackuppath, file)
                if file.endswith('.zip'):    
                    addItem('[B]Restore '+file+'[/B]',path,9,'https://www.restoretools.com/icon/icon_zip_256.png',FANART,'')
                    pass
        except: pass

    addItem('[B]Choose Restore Location[/B]',BASEURL,74,'https://www.restoretools.com/icon/icon_zip_256.png',FANART,'')
    addItem('[B]Backup Skin Settings[/B]',BASEURL,59,'http://iconbug.com/data/5c/512/3acbd906e7b75eaf09e70d1d26c665f9.png',FANART,'')
    addItem('[B]Backup Add-on Settings[/B]',BASEURL,105,'http://iconbug.com/data/5c/512/3acbd906e7b75eaf09e70d1d26c665f9.png',FANART,'')
    if os.path.exists(SkinSettingsBackup):
        addDir('[B]Restore Skin Settings[/B]',BASEURL,60,'https://www.restoretools.com/icon/icon_zip_256.png',FANART,'','')
        addItem('[B][/B]',BASEURL,0,'',FANART,'')
        addItem('[B][COLOR white]Delete Skin Settings Backup[/COLOR][/B]',BASEURL,61,'https://premium.wpmudev.org/blog/wp-content/uploads/2012/08/delete-big.jpg',FANART,'')
    else: pass
    if os.path.exists(addon_dataBackup):
        addDir('[B]Restore Add-on Settings[/B]',BASEURL,106,'https://www.restoretools.com/icon/icon_zip_256.png',FANART,'','')
        addItem('[B][/B]',BASEURL,0,'',FANART,'')
        addItem('[B][COLOR white]Delete Add-on Settings Backup[/COLOR][/B]',BASEURL,107,'https://premium.wpmudev.org/blog/wp-content/uploads/2012/08/delete-big.jpg',FANART,'')
    else: pass
    if os.path.exists(fullbackuppath):
        try:
            for file in os.listdir(fullbackuppath):
                path=os.path.join(fullbackuppath, file)
                if file.endswith('.zip'):
                    addItem('[B][COLOR white]Delete '+file+'[/COLOR][/B]',path,53,'https://premium.wpmudev.org/blog/wp-content/uploads/2012/08/delete-big.jpg',FANART,'')
        except: pass
        addItem('[B][COLOR white]Delete all Backups[/COLOR][/B]',BASEURL,73,'https://premium.wpmudev.org/blog/wp-content/uploads/2012/08/delete-big.jpg',FANART,'')

def RepoMenu(): #36
    addItem('[COLOR yellow][B]Sources will appear on next start[/B][/COLOR]','http://get.mkiv.ca',42,ICON,FANART,'')
    addItem('MK-IV Repo','http://get.mkiv.ca',42,ICON,FANART,'')
    addItem('Ares Repo','http://areswizard.uk',42,'http://0716zip.ares8.seedr.io/ares_home.jpg',FANART,'')
    addItem('TVaddons Repo','http://fusion.tvaddons.ag',42,'https://pbs.twimg.com/profile_images/687462449457541124/6YhPlu-3.png',FANART,'')
    addItem('SuperRepo','http://srp.nu',42,'https://superrepo.org/wp-content/uploads/90x60xSuperRepo-Logo-transparent-141x100.png.pagespeed.ic.pSswIbNwLw.png',FANART,'')
    addItem('The Beast Repo','http://thebeastkodi.com/repo',42,'https://seo-michael.co.uk/content/images/2016/05/beastfeat.jpg',FANART,'')
    addItem('No Issue Repo','http://solved.no-issue.is/',42,'https://i.ytimg.com/vi/JEZOVXa8iGE/sddefault.jpg',FANART,'')
    addItem('Kaosbox Repo','http://install.kaosbox.tv/',42,'https://superrepo.org/static/images/icons/original/xplugin.program.kaosboxinstall.png.pagespeed.ic.06zwuc3b3_.png',FANART,'')
    addItem('Metal Kettle Repo','http://kodi.metalkettle.co/',42,'https://pbs.twimg.com/profile_images/720521598495813632/0k6os-YG.jpg',FANART,'')
    addItem('Taffy MC Repo','http://add.taffymc.com/',42,'http://taffymc.com/wp-content/uploads/2015/10/Slider_TMC_GNP.png',FANART,'')
    addItem('Montreal-in-a-box Repo','http://upgrades.montrealandroidtv.com/',42,'http://www.mtlfreetv.com/images/logo-0.png',FANART,'')
    addItem('Mega-Tron Repo','http://mega-tron.tv/transform/',42,'http://mega-tron.tv/wp-content/uploads/2016/09/megatron-logo.png',FANART,'')
    addItem('M3U Repo','http://www.tugafree.hostei.com/',42,'http://kodim3u.com/wp-content/uploads/2015/09/kodi_m3u_logo.png',FANART,'')
    addItem('Wookie Repo','http://wookiespmc.com/wiz/',42,'https://seo-michael.co.uk/content/images/2016/02/wookiefeat.jpeg',FANART,'')
    addItem('TDB Repo','http://tdbrepo.com/',42,'https://seo-michael.co.uk/content/images/2016/09/echofeat.png',FANART,'')
    addItem('My Supremacy Repo','http://www.mysupremacy.co.uk/',42,'https://seo-michael.co.uk/content/images/2016/11/supremacyfeat.jpg',FANART,'')
    addItem('[B][/B]',BASEURL,0,'',FANART,'')
    addItem('[B][COLOR yellow]Click here to Force Close[/COLOR][/B]',BASEURL,28,'http://dreadpirate.info/images/jollyroger2.jpg',FANART,'')

def FireFox():
        addItem('FireFox for x86 devices','https://archive.org/download/aappkk/org.mozilla.firefox_49.0.2-2015448644_minAPI15x86.apk',23,'http://orig13.deviantart.net/877f/f/2011/117/f/a/mozilla_firefox_by_dj_fahr-d3ezwg9.png',FANART,'')
        addItem('FireFox for ARM devices','https://archive.org/download/aappkk/org.mozilla.firefox_49.0.2-2015448641_minAPI15armeabi-v7a.apk',23,'http://orig13.deviantart.net/877f/f/2011/117/f/a/mozilla_firefox_by_dj_fahr-d3ezwg9.png',FANART,'')

def CANADABUILDS():
    addItem('[B][COLOR red]MK-IV[/COLOR][/B]',BASEURL,100,ICON,FANART,'')

def BuildAWizardMenu():
    addItem('[COLOR yellow][B]Add-on Settings[/B][/COLOR]',BASEURL,30,'https://s-media-cache-ak0.pinimg.com/564x/c7/d6/9a/c7d69ab67de8553c02c0555409267b90.jpg',FANART,'')
    addItem('[B]Build a Pointer File[/B]','https://ares-forum.uk',43,'http://codecondo.com/wp-content/uploads/2015/10/7-Good-Reasons-why-you-must-learn-Python-programming-in-2015_785.png?478983',FANART,'')
    addItem('[B]Build A Wizard[/B]','https://ares-forum.uk',45,'http://blog.stoneriverelearning.com/wp-content/uploads/2016/07/Programmer.jpg',FANART,'')
    addItem('[B]Build an RSS file[/B]','https://ares-forum.uk',44,'http://icons.iconarchive.com/icons/fasticon/social-bookmark/256/Feeds-icon.png',FANART,'')
    addDir('[B]Build a Repository[/B]','https://ares-forum.uk',99,'http://asiaglobaltechnology.my/images/equella%20digital%20repository.png',FANART,'','')

def BuildARepoMenu():
    Addonsxml = xbmc.translatePath(os.path.join(fullworkpath, 'Repository/addons.xml'))
    addItem('[B]Make a Repository[/B]',BASEURL,86,'http://asiaglobaltechnology.my/images/equella%20digital%20repository.png',FANART,'')
    addItem('[B]Make a Repo Add-on[/B]',BASEURL,97,'http://more-sky.com/data/out/8/IMG_258740.jpg',FANART,'')
    if os.path.exists(Addonsxml):
        addItem('[B]Update Repository[/B]',BASEURL,98,'http://www.komando.com/wp-content/uploads/2015/04/update2-970x546.jpg',FANART,'')
    else: pass
    
def ToolsMenu():
    myplatform = platform()
    if myplatform == 'android':
        addItem('[B][COLOR lime]Send Command to Terminal[/COLOR][/B]',BASEURL,35,'http://tr1.cbsistatic.com/hub/i/2016/07/05/2f15aab4-230a-4709-8e10-11d300e44ad5/termuxhero.jpg',FANART,'')
    addItem('[B]Create MD5 Hash from file[/B]',BASEURL,84,'https://lh6.ggpht.com/vz6k4Gx2DCF_0plmI5qgJ2pG1qdG3LbeKjjwm6j7v8UK36ZY8RCYxjPKHGDP3uOZ-YEV=w300',FANART,'')
    addItem('[B]Base64 Encode File[/B]',BASEURL,101,'https://2.bp.blogspot.com/-NE7kCIPrTDk/V9PCr9qnxlI/AAAAAAAAG-Y/127QBCZ8A1otHiA-p-vGMsIFTSslsPAhgCLcB/s1600/base64%2BEncoding%2Band%2BDecoding%2BExample%2Bin%2BJava.png',FANART,'')
    addItem('[B]Base64 Decode File[/B]',BASEURL,102,'https://2.bp.blogspot.com/-NE7kCIPrTDk/V9PCr9qnxlI/AAAAAAAAG-Y/127QBCZ8A1otHiA-p-vGMsIFTSslsPAhgCLcB/s1600/base64%2BEncoding%2Band%2BDecoding%2BExample%2Bin%2BJava.png',FANART,'')
    addItem('[B]Base64 Decode and View File[/B]',BASEURL,104,'https://2.bp.blogspot.com/-NE7kCIPrTDk/V9PCr9qnxlI/AAAAAAAAG-Y/127QBCZ8A1otHiA-p-vGMsIFTSslsPAhgCLcB/s1600/base64%2BEncoding%2Band%2BDecoding%2BExample%2Bin%2BJava.png',FANART,'')
    addDir('[B][COLOR yellow]Test Area[/COLOR][/B]',BASEURL,85,'http://vignette1.wikia.nocookie.net/fallout/images/3/32/X-8_terminal_to_test_area.jpg/revision/latest?cb=20130402140618',FANART,'','')

def AddToAres1():
    addItem('[COLOR yellow][B]Add-on Settings[/B][/COLOR]',BASEURL,30,'https://s-media-cache-ak0.pinimg.com/564x/c7/d6/9a/c7d69ab67de8553c02c0555409267b90.jpg',FANART,'')
    addItem('[COLOR lime]-----     Method 1     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[COLOR deepskyblue]-----     Step 1: Create a Universal Backup     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to Backup[/B]',BASEURL,12,'http://iconbug.com/data/5c/512/3acbd906e7b75eaf09e70d1d26c665f9.png',FANART,'')
    addItem('[COLOR deepskyblue]-----     Step 2: Upload the backup and get its link     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to go to Archive.org[/B]','https://archive.org/',19,'http://blog.archive.org/wp-content/uploads/2013/04/Internetlogo.jpg',FANART,'')
    addItem('[COLOR deepskyblue]----- Step 3:Make a pointer file with links to two pictures and your zip file -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to build a Pointer File[/B]','https://ares-forum.uk',43,'http://codecondo.com/wp-content/uploads/2015/10/7-Good-Reasons-why-you-must-learn-Python-programming-in-2015_785.png?478983',FANART,'')
    addItem('[COLOR deepskyblue]-----     Step 4:Upload your Pointer File and get its link     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to go to Archive.org[/B]','https://archive.org/',19,'http://blog.archive.org/wp-content/uploads/2013/04/Internetlogo.jpg',FANART,'')
    addItem('[COLOR deepskyblue]-----     Step 5: Give your Pointer File\'s link to Ares     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to add your build to Ares[/B]','https://ares-project.uk/pages/build_submission/',19,'http://0716zip.ares8.seedr.io/ares_home.jpg',FANART,'')

def AddToAres2():
    addItem('[COLOR yellow][B]Add-on Settings[/B][/COLOR]',BASEURL,30,'https://s-media-cache-ak0.pinimg.com/564x/c7/d6/9a/c7d69ab67de8553c02c0555409267b90.jpg',FANART,'')
    addItem('[COLOR lime]-----     Method 2     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[COLOR deepskyblue]-----     Step 1: Create a Universal Backup     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to Backup[/B]',BASEURL,12,'http://iconbug.com/data/5c/512/3acbd906e7b75eaf09e70d1d26c665f9.png',FANART,'')
    addItem('[COLOR deepskyblue]-----     Step 2: Upload the backup and get its link     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to go to Archive.org[/B]','https://archive.org/',19,'http://blog.archive.org/wp-content/uploads/2013/04/Internetlogo.jpg',FANART,'')
    addItem('[COLOR deepskyblue]-----     Step 3: Give your File\'s download link to Ares     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'Alpha')#Md.Emu
    addItem('[B]Click here to add your build to Ares[/B]','https://ares-project.uk/pages/build_submission/',19,'http://0716zip.ares8.seedr.io/ares_home.jpg',FANART,'')  

#def USABUILDS():

#def UKBUILDS():
#      addDir('[B][COLOR yellow]Coming Soon...[/COLOR][/B]',BASEURL,20,ART+'uk.jpg',FANART,'','')

def MKIVMENU(): 
            if ADDON.getSetting('Update') == 'true' and ADDON.getSetting('BuildName') != '':
                Updater='[COLOR lime]ON[/COLOR]'
                pass
            elif ADDON.getSetting('Update') == 'false' and ADDON.getSetting('BuildName') != '':
                Updater='[COLOR red]OFF[/COLOR]'
                pass
            else:
                Updater='[COLOR orangered]Not Available[/COLOR]'
                pass
            addDir('[B][COLOR red]Install MK-IV[/COLOR][/B]',BASEURL,32,ICON,FANART,'','')
            addItem('[B][COLOR blue]MK-IV Website[/COLOR][/B]','http://mkiv.ca',19,FANART,FANART,'')
            addItem('[B][COLOR red]Donate to MK-IV[/COLOR][/B]','https://paypal.me/mkiv',19,'http://www.fofrescue.org/wp-content/uploads/2013/09/paypal-logo-donate.png',FANART,'')
            addItem('[B][COLOR blue]MK-IV Auto-update[/COLOR] %s'% Updater+'[/B]',BASEURL,81,ICON,FANART,'')
            addItem('[B][COLOR white][/COLOR][/B]','http://mkiv.ca',666,FANART,FANART,'')
            addItem('[COLOR powderblue]Get AceStreams Engine[/COLOR]',BASEURL,34,'http://freeiptv.weightlosstoday.org/wp-content/uploads/2016/01/Ace-Stream-Media-Full-Free-Download.jpg',FANART,'')
            addItem('[COLOR deepskyblue]Edit Backgrounds[/COLOR]',BASEURL,75,ICON,FANART,'')
            if os.path.exists(BackgroundsBackupZip):
                addItem('[COLOR powderblue]Restore Backgrounds[/COLOR]','http://mkiv.ca',76,FANART,FANART,'')
                addItem('',BASEURL,32,ICON,FANART,'')
                addItem('[COLOR orangered]Delete Backgrounds Backup[/COLOR]','http://mkiv.ca',77,FANART,FANART,'')
            else: pass



def PlayStoreMenu():
    addItem('[COLOR deepskyblue]-----     PlayStore Apps     -----[/COLOR]','com.explusalpha.MdEmu',999,'https://cdn1.iconfinder.com/data/icons/app-stores-2/128/Google_Play_3.png',FANART,'Alpha')#Md.Emu
    addItem('Md.Emu','com.explusalpha.MdEmu',39,'https://raw.githubusercontent.com/MK-IV/Dependencies/master/Pictures/segaimage.jpg','https://raw.githubusercontent.com/MK-IV/Dependencies/master/Pictures/sonicfanart.png','Alpha')#Md.Emu
    addItem('Snes9x','com.explusalpha.Snes9xPlus',39,'https://raw.githubusercontent.com/MK-IV/Dependencies/master/Pictures/snesimage.jpg','https://raw.githubusercontent.com/MK-IV/Dependencies/master/Pictures/nintendofanart.png','Beta')#Snes9x
    addItem('Firefox','org.mozilla.firefox',39,'http://orig13.deviantart.net/877f/f/2011/117/f/a/mozilla_firefox_by_dj_fahr-d3ezwg9.png','http://cdn.neurogadget.net/wp-content/uploads/2015/11/Firefox-vs.-Chrome.jpg','')#Firefox    
    addItem('Netflix','com.netflix.mediaclient',39,'http://www.thetechloft.com/wp-content/uploads/2014/01/nexusae0_Netflix-Thumb.png','http://images2.fanpop.com/images/quiz/76382_1224169744552_413_310.jpg','')#Netflix      
    addItem('Disney Replay','com.disney.disneychannelreplay_goo',39,'https://cdn.d23.com/cdn2015/wp-content/uploads/2015/07/081514_disney-channel-stars-make-comeback-feat-1.jpg','http://cdn-image.travelandleisure.com/sites/default/files/styles/1600x1000/public/1450974650/disney-fireworks-castle-DISNEY1215_0_0.jpg','')#Disney Replay  
    addItem('Lena Desktop Launcher','de.m_lang.leena',39,'http://1.bp.blogspot.com/-p6HLi2bc_-w/ToyG0lObigI/AAAAAAAAAXM/lsUZCGCzlf0/s1600/android-skin-windows-desktop.jpg','https://lh3.googleusercontent.com/ge0YtiFPUnP3n4iZqHt4fkLrjCS4biOoUVoFQjhNiaARwrkKssPSBYkBX1HVEBNetDs=h900','')#Lena  
    addItem('ES File Manager','com.estrongs.android.pop',39,'http://droidforpc.com/wp-content/uploads/2015/05/droidforpc-0021.png','https://lh3.googleusercontent.com/I3qeHDSYyXPxkOTgKYpPoRP42XRs_KcFXGPr5YUxB9BydcELcERqVdQ8g0SOFI4b_9wi=h310','')#ES File Manager
    addItem('Kodi','org.xbmc.kodi',39,'http://sideloadfiretv.com/wp-content/uploads/2015/01/preview_84a70e233a1a6d1ac0d93d2e9f1f2de0e7c2d64d289f1e6f17434fe4c3752717.png','http://cdn.wallpapersafari.com/67/60/fEqKbm.jpg','')  
    addItem('SPMC','com.semperpac.spmc16',39,'http://s15.postimg.org/fu5jq82ff/1280_splash.png','http://dvxjmen5kgvfb.cloudfront.net/wp-content/uploads/2014/08/SPMC-Splash.jpg','')
    addItem('Team Viewer','com.teamviewer.teamviewer.market.mobile',39,'https://screenshots.en.sftcdn.net/en/scrn/60000/60958/teamviewer-09-535x535.png','https://lh3.googleusercontent.com/iba_vTCnUpAPv5DAcT_u_UMdmIQvCyE62AKGKnxD4m0NrWTf64lWn-JoAOx_mZIBLw=h900','')
    try:
        addItem('[COLOR deepskyblue]-----     MK Store Apps     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'')
        link = OPEN_URL('http://androidmenu.mkiv.ca').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,23,iconimage,fanart,description)
    except: pass
    try:
        addItem('[COLOR deepskyblue]-----     Kobra Apps     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'')
        link = OPEN_URL('http://kobracustombuilds.com/apks/wizard/wizard.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,23,iconimage,fanart,description)
    except: pass
    try:
        addItem('[COLOR deepskyblue]-----     Emulator Apps     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'')
        link = OPEN_URL('http://kobracustombuilds.com/emulators/wizard/wizard.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,23,iconimage,fanart,description)
    except: pass
    if ShowAdult=='true':
        try:
            addItem('[COLOR deepskyblue]-----     Adults Only Apps     -----[/COLOR]','com.explusalpha.MdEmu',999,ICON,FANART,'')
            link = OPEN_URL('http://kobracustombuilds.com/adult/wizard/wizard.txt').replace('\n','').replace('\r','')
            match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            for name,url,iconimage,fanart,description in match:
                addItem(name,url,23,iconimage,fanart,description)
        except: pass
    else: pass

def LogMenu():
    addItem('[B]View Last Error[/B]',BASEURL,48,'http://www.iconshock.com/img_jpg/STROKE/communications/jpg/256/log_file_icon.jpg',FANART,'')
    addItem('[B]View All Errors[/B]',BASEURL,47,'http://www.iconshock.com/img_jpg/STROKE/communications/jpg/256/log_file_icon.jpg',FANART,'')
    addItem('[B]View Full Log[/B]',BASEURL,49,'http://www.iconshock.com/img_jpg/STROKE/communications/jpg/256/log_file_icon.jpg',FANART,'')
    addItem('[B]Upload Log File[/B]',BASEURL,55,'http://netdna.webdesignerdepot.com/uploads/2012/09/cloud_1.png',FANART,'')

def WebsitesMenu(): #3
    addItem('[B]MK-IV Website[/B]','http://mkiv.ca',19,ICON,FANART,'')
    addItem('[B]Add your build to Ares[/B]','https://ares-project.uk/pages/build_submission/',19,'http://0716zip.ares8.seedr.io/ares_home.jpg',FANART,'')
    addItem('[B]ARES Forum[/B]','https://ares-forum.uk',19,ART+'ares.png',FANART,'')
    addItem('[B]No Issue Blog[/B]','http://no-issue.ca/blog/',19,'https://i.ytimg.com/vi/JEZOVXa8iGE/sddefault.jpg',FANART,'')
    addItem('[B]Archive.org[/B]','https://archive.org/',19,'http://blog.archive.org/wp-content/uploads/2013/04/Internetlogo.jpg',FANART,'')
    addItem('[B]seo-michael.co.uk/[/B]','https://seo-michael.co.uk/',19,'https://seo-michael.co.uk/content/images/2016/09/avatarnew-copy-2.png',FANART,'')
    addItem('[B]SPMC Website[/B]','http://spmc.semperpax.com/',19,'https://lh4.ggpht.com/HgeBIAMXkI9AXRWVmaA1-P1-yNTTGmLIhiWympkS2WWspj2qIOK8FOg3yY01VfDIR8qW=w300',FANART,'')
    addItem('[B]Kodi Website[/B]','https://kodi.tv/',19,'https://lh6.ggpht.com/RQvf62YkkS_hpGAfP2iBoT2yf7b0oohFQHhBB8Chp8nHNPSqmZgEkwwpKtqdtqQ_ZvM=w300',FANART,'')
    addItem('[B]Kodi Tips[/B]','http://koditips.com/',19,'http://koditips.com/wp-content/uploads/logo_3_half.png',FANART,'')
    addItem('[B]TVaddons Website[/B]','https://www.tvaddons.ag/',19,'https://www.tvaddons.ag/wp-content/uploads/2014/08/tvaddons_logo.png',FANART,'')
    addItem('[B]SuperRepo Website[/B]','https://superrepo.org/',19,'https://superrepo.org/wp-content/uploads/90x60xSuperRepo-Logo-transparent-141x100.png.pagespeed.ic.pSswIbNwLw.png',FANART,'')
    addItem('[B]Best for kodi website[/B]','http://bestforkodi.com/',19,'https://pbs.twimg.com/profile_images/682370419115081728/ISU3D2Sj.png',FANART,'')
    addItem('[B]Tekto\'s blog[/B]','http://www.tekto-kodi.com/',19,'http://i.huffpost.com/gen/1303817/images/o-ARE-YOU-A-JERK-QUIZ-facebook.jpg',FANART,'')
    try:
        link = OPEN_URL('http://websites.mkiv.ca').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,23,iconimage,fanart,description)
    except: pass

def AddonMenu():
        addItem('[B][COLOR deepskyblue]-----     Add-ons     -----[/COLOR][/B]',BASEURL,0,ICON,FANART,'')
        addItem('Webslinger','https://github.com/MK-IV/plugin.program.webslinger/archive/master.zip',10,'http://screenrant.com/wp-content/uploads/Spider-Man-Surrounded-by-Webs.jpg',FANART,'plugin.program.webslinger')
        addItem('Hue Ambilight Controller','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,'http://images.philips.com/is/image/PhilipsConsumer/PTA008_00-E3P-global-001?$jpglarge$&hei=700',FANART,'script.kodi.hue.ambilight-master')
        addItem('Python Requests Module','http://mkiv.netne.net/Admin/Addon%20Packs/script.module.requests-2.9.1.zip',10,'https://ee5817f8e2e9a2e34042-3365e7f0719651e5b8d0979bce83c558.ssl.cf5.rackcdn.com/python.png',FANART,'script.module.requests')
        addItem('Config Wizard (TVaddons)','http://fusion.tvaddons.ag/start-here/plugin.video.hubwizard-1.2.0.zip',10,'https://pbs.twimg.com/profile_images/687462449457541124/6YhPlu-3.png',FANART,'plugin.video.hubwizard')
        addItem('Wookie Wizard','http://wiz.wookiespmc.com/Click%20me%20-%20succumb%20to%20The%20Wookie.zip',10,'http://wookiespmc.com/wp-content/uploads/2015/07/Screenshot-2016-02-12-10.40.07.png',FANART,'plugin.video.aswizard')
        addItem('The Beast Wizard','http://thebeast1.com/repo/plugin.video.beast.zip',10,'https://seo-michael.co.uk/content/images/2016/05/beastfeat.jpg',FANART,'plugin.video.beast')
        addItem('Exodus','https://offshoregit.com/exodus/plugin.video.exodus/plugin.video.exodus-2.0.20.zip',10,'https://www.tvaddons.ag/kodi-addons/cache/images/f045187f652aaf04c824430ae1c4d3_icon.png',FANART,'plugin.video.exodus')
        addItem('Phoenix','https://offshoregit.com/xbmchub/xbmc-hub-repo/raw/master/plugin.video.phstreams/plugin.video.phstreams-3.1.15.zip',10,'https://www.tvaddons.ag/kodi-addons/cache/images/16ddd0b9ea1501f7cb5dcefffac205_icon.png',FANART,'plugin.video.phstreams')
        addItem('Sports Devil','https://offshoregit.com/unofficialsportsdevil/plugin.video.SportsDevil/plugin.video.SportsDevil-2016.10.10.zip',10,'https://www.tvaddons.ag/kodi-addons/cache/images/bd425777762040073f0077dc9838d8_icon.png',FANART,'plugin.video.SportsDevil')
        #addItem('[B]Hue Ambilight Controller[/B]','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,'mkiv4.png',FANART,'')
        #addItem('[B]Hue Ambilight Controller[/B]','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,'mkiv4.png',FANART,'')
        #addItem('[B]Hue Ambilight Controller[/B]','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,'mkiv4.png',FANART,'')
        addItem('[B][COLOR deepskyblue]-----     Repositories     -----[/COLOR][/B]',BASEURL,0,ICON,FANART,'')
        addItem('Exodus Repo','http://fusion.tvaddons.ag/xbmc-repos/english/repository.exodus-1.0.1.zip',10,'https://www.tvaddons.ag/kodi-addons/cache/images/f045187f652aaf04c824430ae1c4d3_icon.png',FANART,'repository.exodus')
        addItem('Metal Kettle Repo','http://fusion.tvaddons.ag/xbmc-repos/english/repository.metalkettle-1.7.1.zip',10,'https://pbs.twimg.com/profile_images/720521598495813632/0k6os-YG.jpg',FANART,'repository.metalkettle')
        addItem('PodGod Repo','http://fusion.tvaddons.ag/xbmc-repos/english/repository.podgod-1.7.zip',10,'https://www.tvaddons.ag/kodi-addons/cache/images/695c8650434761faf667d972d8da6d_icon.png',FANART,'repository.podgod')
        addItem('SchismTV Repo','http://www.schism-tv.net/repo/repository.schismtvaddons-1.3.0.zip',10,'https://superrepo.org/static/images/icons/original/xrepository.schismtv.official.png.pagespeed.ic.VbHND3KQCM.jpg',FANART,'repository.schismtvaddons')
        addItem('Titan Repo','https://archive.org/download/titanrepo/repository.titan.addons-1.0.0.zip',10,'https://i.ytimg.com/vi/dhd0iZdg95U/hqdefault.jpg',FANART,'repository.titan.addons')
        addItem('TDB Repo','http://tdbrepo.com/repository.echo-1.03.zip',10,'https://seo-michael.co.uk/content/images/2016/09/echofeat.png',FANART,'repository.echo')
        #addDir('[B]Hue Ambilight Controller[/B]','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,ART+'mkiv4.png',FANART,'','')
        #addDir('[B]Hue Ambilight Controller[/B]','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,ART+'mkiv4.png',FANART,'','')
        #addDir('[B]Hue Ambilight Controller[/B]','https://github.com/koying/script.kodi.hue.ambilight/archive/develop.zip',10,ART+'mkiv4.png',FANART,'','')
        addItem('[B][COLOR deepskyblue]-----     MK-IV Server     -----[/COLOR][/B]',BASEURL,0,ICON,FANART,'')
        try:
            link = OPEN_URL('http://addonmenu.mkiv.ca').replace('\n','').replace('\r','')
            match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)').findall(link)
            for name,url,iconimage,fanart,description in match:
                addItem(name,url,10,iconimage,fanart,description)
        except:
            pass
            xbmc.executebuiltin('Container.SetViewMode(50)')

def Crash():  #Exhaust resources to crash the interpreter *** Creates a crash log but good as a last resort.
        sys.setrecursionlimit(1<<30)
        f = lambda f:f(f)
        f(f) 

def ADULTCONTENT():
    if ADDON.getSetting('password') == "":
        choice = xbmcgui.Dialog().yesno(Title, 'This section contains access to adult content', 'To proceed please set a password','', nolabel='Take Me Back',yeslabel='Set Password')
        if choice == 0:
            return

        elif choice == 1:           
            password=xbmcgui.Dialog().input('Enter your password', type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
            SetSetting('password',password)
            return
    else:
        title=xbmcgui.Dialog().input('Enter your password', type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
       # vq = _get_keyboard( heading="Please Enter Your Password" )
        #if ( not vq ): return False, 0
        #title = urllib.quote_plus(vq)
        if title == ADDON.getSetting('password'):
            pass
        else:
            return
    addItem('Adults XXX Pack','http://mkiv.netne.net/Admin/Addon%20Packs/XXX.zip',10,'https://raw.githubusercontent.com/MK-IV/Dependencies/master/Pictures/xxx.jpg','https://raw.githubusercontent.com/MK-IV/Dependencies/master/Pictures/xxxfan.jpg','Adults Only Addons')

def HelpVideos():
        addItem('[B][COLOR deepskyblue]Press the \'select\' button then stop to stop a video[/COLOR][/B]','JVtHtoiKYAE',5,ICON,FANART,'')    
        addItem('[B]Making a repository[/B]','zm1pvAt5uvU',5,'https://i.ytimg.com/vi/zm1pvAt5uvU/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=bYzN0md-6CLuEcFLjZUDBk-8mbo',FANART,'')
        addItem('[B]Setting up SimpleIPTV client[/B]','vEkF5mkRw9Y',5,'https://i.ytimg.com/vi/vEkF5mkRw9Y/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=qQSzaPv93jJXeieC5bfjyqJTWiA',FANART,'')
        addItem('[B]Setting up a TV Guide[/B]','E0Rkr3q-9MM',5,'https://i.ytimg.com/vi/E0Rkr3q-9MM/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=R7K34rolnV1hytPWjC5i2ezV544',FANART,'')
        addItem('[B]Setting up Subtitles[/B]','TGbiYvcPSP8',5,'https://i.ytimg.com/vi/TGbiYvcPSP8/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=HspEw4gIBAHCQa4OTWL7mlVliSA',FANART,'')
        addItem('[B]Making a Build[/B]','SLmBuJl9214',5,'https://i.ytimg.com/vi/SLmBuJl9214/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=foM9ypslItq4laT-PcBbjyygMQs',FANART,'')
        addItem('[B]Change Audio & Video settings[/B]','2PubiLr5qoU',5,'https://i.ytimg.com/vi/2PubiLr5qoU/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=ZifutkQDg92FKO1uK3Dg5DD_mnA',FANART,'')
        addItem('[B]Setting up Trakt[/B]','N1UN1UWjqHg',5,'https://i.ytimg.com/vi/N1UN1UWjqHg/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=anD2Mu_hvaqeALOyZcebq4-eoHs',FANART,'')
        addItem('[B]Getting Kodi on FireStick and FireTv[/B]','V1mfXLJ0xRo',5,'https://i.ytimg.com/vi/V1mfXLJ0xRo/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=UXceQ7rax04gCAVou1s4hQ_nwlg',FANART,'')
        addItem('[B]Setting up ROM Collection Browser[/B]','2O8FGHDrI6o',5,'https://i.ytimg.com/vi/2O8FGHDrI6o/hqdefault.jpg?custom=true&w=260&h=146&stc=true&jpg444=true&jpgq=90&sp=68&sigh=Jeh8B6FM4uerZWCxYPXTYgd0ZAA',FANART,'')
        #addItem('[B]MK-IV Test Video[/B]','JVtHtoiKYAE',5,ART+'mkiv4.png',FANART,'')
        #addItem('[B]MK-IV Test Video[/B]','JVtHtoiKYAE',5,ART+'mkiv4.png',FANART,'')
        #addItem('[B]MK-IV Test Video[/B]','JVtHtoiKYAE',5,ART+'mkiv4.png',FANART,'')
        #addItem('[B]MK-IV Test Video[/B]','JVtHtoiKYAE',5,ART+'mkiv4.png',FANART,'')
        try:
            link = OPEN_URL('http://helpvids.mkiv.ca').replace('\n','').replace('\r','')
            match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?escription="(.+?)"').findall(link)
            for name,url,iconimage,fanart,description in match:
                addItem(name,url,5,iconimage,fanart,description)
        except: pass

def GetAceStream():
    myplatform = platform()
    if myplatform == 'android':
        dialog = xbmcgui.Dialog()
        if dialog.yesno(Title, 'The AceStream Engine is required to play some sports section content.', 'After its installed sign into the app and thats it.','Would you like to download and install now?', nolabel='SKIP',yeslabel='Yes'):
            if dialog.yesno(Title, 'Is your Android device x86 or ARM based', '','(If your not sure try ARM first)', nolabel='ARM',yeslabel='x86'):
                INSTALLAPK('acestreamsx86','https://archive.org/download/aappkk/AceStream-3.1.6.0-x86.apk','')
                    #mk4.INSTALLAPK('acestreams','http://dl.acestream.org/products/acestream-engine/android/latest','')
            else:
                INSTALLAPK('acestreamsARM','https://archive.org/download/aappkk/AceStream-3.1.6.0-armv7.apk','')
    else:
        dialog = xbmcgui.Dialog()
        if dialog.yesno(Title, 'The AceStream Engine is required to play some sports section content.', 'After its installed sign into the app and thats it.','Would you like to download and install now?', nolabel='SKIP',yeslabel='Yes'):
            dialog.ok(Title,'Press OK to launch your browser to the download page.','You only need the engine.','')
            OpenWebpage('http://wiki.acestream.org/wiki/index.php/AceStream_3.0/en')
            
            
            
def Contact():
    from email.mime.text import MIMEText
    choice = xbmcgui.Dialog().select('Choose a subject', ['Issue', 'Request', 'Comment','Other'])
    if choice == 0:
        subject = 'Issue'
        pass
    elif choice == 1:
        subject = 'Request'
        pass
    elif choice == 2:
        subject = 'Comment'
        pass
    elif choice == 3:
        subject = 'Other'
        pass
    
    vqsender = _get_keyboard(heading="Enter your email address (optional)" )
    if ( not vqsender ): vqsender = ""
    sender = urllib.unquote_plus(vqsender)
    vqbody = _get_keyboard(heading="Enter your message." )
    if ( not vqbody ): vqbody = ""
    body = urllib.unquote_plus(vqbody)
    
    f = urllib.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    msg = MIMEText(body+'Internal IP: '+s.getsockname()[0]+'External IP:'+m.group(0))

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject 
    msg['From'] = sender
    msg['To'] = 'mkiv@protonmail.com'

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    xbmc.log(msg.as_string())
    #s = smtplib.SMTP('localhost')
    server = smtplib.SMTP('gmail-smtp-in.l.google.com','25')
    server.starttls()
    server.ehlo("example.com")
    server.mail(me)
    server.rcpt([you])
    server.data(msg.as_string())
    server.quit()  
    #s = smtplib.SMTP('smtp.gmail.com','465')
   # s.sendmail(me, [you], msg.as_string())
    #s.quit()

#=========================================================   Android definitions   =======================================================

def APKDOWNWIZ(name,url):
    dp = xbmcgui.DialogProgress()
    dp.create(Title,"Downloading your Files...",'', 'Please Wait')
    lib=os.path.join(PACKAGES, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('sdcard','download'))
    time.sleep(.5)
    dp.update(0,"Downloading your files... [COLOR lime]Finished[/COLOR]", "Moving files...")
    extract.all(lib,addonfolder,dp)
    time.sleep(.5)
    try:
        os.remove(lib)
    except:
        pass
    dialog = xbmcgui.Dialog()
    dialog.ok(Title,"DOWNLOAD COMPLETE ", "The Files are stored in your Download folder.")

def OpenAndroidApp(package, intent, dateType, dataURI):    
    xbmc.executebuiltin('StartAndroidActivity('+package+','+intent+','+dataType+','+dataURI+')')
        #Example: StartAndroidActivity(com.android.chrome,android.intent.action.VIEW,,http://kodi.tv/)
                                          #package       ,    intent                ,dataType,  dataURI
def PlayStore(name, url, description):
        try:
            xbmc.log('======================   MK-IV Wizard   ========================')
            xbmc.log('==============**********************************================')
            xbmc.log('===============   Looking for local PlayStore   ================')
            OpenAndroidApp('com.android.vending','android.intent.action.VIEW','','market://details?id='+url)
        except:
            xbmc.log('=========   Local PlayStore not found, trying external   ================')
            os.system('am start --user 0 -a android.intent.action.VIEW -d market://details?id='+url)

def INSTALLAPK(name,url,description):
    path = xbmc.translatePath(os.path.join('/storage/emulated/0/Download',''))
    dp = xbmcgui.DialogProgress()
    dp.create(Title,"","",'APK: ' + name)
    lib=os.path.join(path, name+'.apk')
    downloader.download(url, lib, dp)
    dialog = xbmcgui.Dialog()
    dialog.ok(Title, "Press ok to launch the APK to be installed","Follow the install process to complete.", "(You may need to allow unknown sources)")
    xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.VIEW","application/vnd.android.package-archive","file:' + lib + '")' )
    if description=='Alpha': 
        dialog = xbmcgui.Dialog()
        if dialog.yesno(Title, 'Additional files are available for this app.', 'Would you like to download them?','(480.7M)', nolabel='SKIP',yeslabel='Yes'):
                APKDOWNWIZ('AlphaTest',Hs+A+P+mk4g+'ALPHA.zip')
    elif description=='Beta':
        dialog = xbmcgui.Dialog() 
        if dialog.yesno(Title, 'Additional files are available for this app.', 'Would you like to download them?','(342.8M)', nolabel='SKIP',yeslabel='Yes'):
            APKDOWNWIZ('BetaTest',Hs+A+P+mk4g+'BETA.zip')


def RunConsole():
    vq = _get_keyboard( default="" , heading="[COLOR lime]Enter command line[/COLOR]" )
    if ( not vq ): return False, 0
    CommandLine = urllib.unquote_plus(vq)
    os.system(''+CommandLine+'')
    Toast('[COLOR lime]Command sent[/COLOR]')
    RunConsole()

#====================================================   Maintenance Definitions   ============================================================

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def InstallAddon(id):
    xbmc.executebuiltin('InstallAddon('+id+')')
    
def HasAddon(id):
    xbmc.executebuiltin('System.HasAddon('+id+')')
    
def SetSetting(id, value):
    ADDON.setSetting(id, value)

def TriggerMigration():
    f = open(Addons27, mode='w')
    f.write('Wiped')
    f.close()
    try:
        os.remove(Addons27)
        os.remove(Textures13)
    except: pass
    
def UpdateKryptonDB():   
    try:
        os.remove(Addons20)
        pass
    except: 
        pass 
    try:
        conn = sqlite3.connect(Addons27)
        cursor = conn.cursor()

        sql = """
        UPDATE version 
        SET idVersion = '20' 
        WHERE idVersion = '27'
        """
        cursor.execute(sql)
        conn.commit()
        time.sleep(1)

        shutil.copy(Addons27,Addons20)
        try:
            os.remove(Textures13)
        except: pass
    except: pass

def RemoveTrigger():
    try:
        if os.path.exists(Addons20):
            os.remove(Addons20)
            try:
                os.remove(Textures13)
            except: pass
        else: 
            pass 
        conn = sqlite3.connect(Addons27)
        cursor = conn.cursor()

        sql = """
        UPDATE version 
        SET idVersion = '27' 
        WHERE idVersion = '20'
        """
        cursor.execute(sql)
        conn.commit()
        time.sleep(1)
    except: pass
def EnableAll():
    try:
        conn = sqlite3.connect(Addons27)
        cursor = conn.cursor()

        sql = """
        UPDATE installed 
        SET enabled = '1' 
        WHERE enabled = '0'
        """
        cursor.execute(sql)
        conn.commit()
        time.sleep(1)
        xbmc.executebuiltin('UpdateLocalAddons')
    except: pass

def DeletePackages():
    xbmc.log('======================   MK-IV Wizard   ========================')
    xbmc.log('==============**********************************================')
    xbmc.log('=================   Start deleting packages   ==================')
    xbmc.log('================================================================')
    try:    
        for root, dirs, files in os.walk(PACKAGES):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Package Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                    dialog = xbmcgui.Dialog()
                    dialog.ok(Title, "Packages Successfuly Removed", "")
                    xbmc.executebuiltin('Container.Refresh')

    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok(Title, "Sorry we were not able to remove Package Files", "")

def deletecachefiles():
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home/'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass

            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')

        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)

            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')

        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)

            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass
              # Set path to Cydia Archives cache files


    # Set path to What the Furk cache files
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete WTF Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass

                # Set path to 4oD cache files
    channel4_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.4od/cache'), '')
    if os.path.exists(channel4_cache_path)==True:    
        for root, dirs, files in os.walk(channel4_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete 4oD Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass

                # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete BBC iPlayer Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass


                # Set path to Simple Downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete Simple Downloader Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass

                # Set path to ITV cache files
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ITV Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass

                # Set path to temp cache files
    temp_cache_path = os.path.join(xbmc.translatePath('special://home/temp'), '')
    if os.path.exists(temp_cache_path)==True:    
        for root, dirs, files in os.walk(temp_cache_path):
            file_count = 0
            file_count += len(files)

        # Count files and give option to delete
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete TEMP dir Cache Files", str(file_count) + " files found", "Do you want to delete them?"):

                    exclude_files=('kodi.log','spmc.log','dbmc.log')
                    files[:] = [f for f in files if f not in exclude_files]
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

            else:
                pass


    dialog = xbmcgui.Dialog()
    dialog.ok(Title, " All Cache Files Removed", "")

def FRESHSTART(params):
    xbmc.log('================  MK-IV Wizard  ================')
    xbmc.log('=========     Begining Fresh Start     =========')
    xbmc.log('================================================')
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'android':
        choice1 = xbmcgui.Dialog().yesno("[COLOR=red]Full Wipe or Modified?[/COLOR]", 'A full wipe clears all addons and files', '', 'A modified wipe will leave Ares Wizard and MK-IV Wizard.', yeslabel='[COLOR lime]Modified Wipe[/COLOR]',nolabel='[COLOR red]Full Wipe[/COLOR]')
        if choice1 == 0:
            try: os.system('pm clear com.semperpax.spmc16')
            except: pass
            try: os.system('pm clear org.xbmc.kodi')
            except: pass ### insert unrecognized system notification. 
        elif choice1 == 1:
            pass
    else:
        pass
    choice2 = xbmcgui.Dialog().yesno("[COLOR=red]Are You Sure?[/COLOR]", 'Last chance...', '', '', yeslabel='[COLOR lime]Yes, Fresh Start[/COLOR]',nolabel='[COLOR red]No[/COLOR]')
    if choice2 == 0:
        return
    elif choice2 == 1:
        dp.create(Title,"Counting files",'', '')
        try:
            rootlen = len(HOME)#
            for_progress = []#
            ITEM =[]#
            for root, dirs, files in os.walk(HOME,topdown=True):
                dirs[:] = [d for d in dirs if d not in EXCLUDES]
                for file in files:#
                    ITEM.append(file)#
                    N_ITEM =len(ITEM)#
                    for_progress.append(file)# 
                    progress = len(for_progress) / float(N_ITEM) * 100#  
                    dp.update(int(progress),"Deleting:",'[COLOR lime]%s[/COLOR]'%file)#
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass

                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
        except: pass
    if not os.path.exists(Database):
        os.makedirs(Database)
        pass
    else: pass
    KillMK4Settings()
    time.sleep(.5)
    shutil.copy(FreshStart,Addons26)
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    REMOVE_EMPTY_FOLDERS()
    time.sleep(.5)
    dp.close()
    ResetMK4Settings()
    dialog = xbmcgui.Dialog()
    dialog.ok(Title,'Fresh Start Successful','','The MC will now close')
    killxbmc()
    xbmc.executebuiltin('Quit')

def FIX_SPECIAL():
    xbmc.log('======================   MK-IV Wizard   ========================')
    xbmc.log('==============**********************************================')
    xbmc.log('===================   Start fixing paths   =====================')
    myplatform = platform()            
    if myplatform == 'android':
        userpath="/storage/emulated/0/"
    elif myplatform != 'osx':
        UserPath=ADDON.getSetting('UserPath')
    elif myplatform == 'linux':
        UserPath=ADDON.getSetting('UserPath')
    elif myplatform == 'windows':
        UserPath=ADDON.getSetting('UserPath')
    else: pass
    urlUSERDATA=urllib.quote_plus(USERDATA)
    urlADDONS=urllib.quote_plus(ADDONS)
    urlMEDIA=urllib.quote_plus(MEDIA)
    dp.create(Title,"Renaming paths...",'[COLOR deepsky][/COLOR]', '')
    for root, dirs, files in os.walk(USERDATA):  #Search all xml and script.skinshortcuts files and replace physical with special
        for file in files:
            if file.endswith(".xml"):
                 dp.update(0,"Checking xml file: ",file, 'Please Wait')
                 a=open((os.path.join(root, file))).read()
                 b=a.replace(USERDATA, 'special://home/userdata/').replace(ADDONS,'special://home/addons/').replace(MEDIA,'special://home/media/').replace(urlUSERDATA, 'special://home/userdata/').replace(urlADDONS,'special://home/addons/').replace(urlMEDIA,'special://home/media/')
                 f = open((os.path.join(root, file)), mode='w')
                 f.write(str(b))
                 f.close()
    for root, dirs, files in os.walk(USERDATA):
        for file in files: 
            if file.endswith(".hash"):
                     dp.update(0,"Checking hash file: ",file, 'Please Wait')
                     a=open((os.path.join(root, file))).read()
                     b=a.replace(USERDATA, 'special://home/userdata/').replace(ADDONS,'special://home/addons/').replace(MEDIA,'special://home/media/').replace(urlUSERDATA, 'special://home/userdata/').replace(urlADDONS,'special://home/addons/').replace(urlMEDIA,'special://home/media/')
                     f = open((os.path.join(root, file)), mode='w')
                     f.write(str(b))
                     f.close()
    for root, dirs, files in os.walk(USERDATA):
        for file in files: 
            if file.endswith(".properties"):
                         dp.update(0,"Checking properties file: ",file, 'Please Wait')
                         a=open((os.path.join(root, file))).read()
                         b=a.replace(USERDATA, 'special://home/userdata/').replace(ADDONS,'special://home/addons/').replace(MEDIA,'special://home/media/').replace(urlUSERDATA, 'special://home/userdata/').replace(urlADDONS,'special://home/addons/').replace(urlMEDIA,'special://home/media/')
                         f = open((os.path.join(root, file)), mode='w')
                         f.write(str(b))
                         f.close()                     
    if os.path.exists:
        try:
            if userpath in open(SkinSettingsXML).read():
                if xbmcgui.Dialog().yesno('[COLOR yellow]Pictures outside of Backup Path Detected[/COLOR]','Would you like to migrate your Background pictures into your set-up?'):
                    xbmcgui.Dialog().ok('[COLOR yellow]Select your background pictures Parent folder[/COLOR]','This will contain your subfolders or pictures depending on your set-up')
                    Pictures=xbmcgui.Dialog().browse(0,'Choose your pictures Parent folder','files')
                    BGpics=xbmc.translatePath(os.path.join(USERDATA , 'Background_pictures/'))
                    if Pictures != '':
                        if not os.path.exists(BGpics):
                            os.makedirs(BGpics)
                        copytree(Pictures, BGpics)
                        for root, dirs, files in os.walk(USERDATA):
                            for file in files: 
                                if file.endswith(".xml"):
                                    dp.update(0,"Scanning",file, 'Please Wait')
                                    a=open((os.path.join(root, file))).read()
                                    b=a.replace(Pictures, 'special://home/userdata/Background_pictures/')
                                    f = open((os.path.join(root, file)), mode='w')                                                                                                                                      
                                    f.write(str(b))
                                    f.close()
        except: pass
    else: pass
                        
    xbmc.log('======================   MK-IV Wizard   ========================')
    xbmc.log('==============**********************************================')
    xbmc.log('===============   Paths successfully changed   =================')     
    if xbmcgui.Dialog().yesno(Title,'Would you like to scan your images and reduce their sizes?', 'This will reduce pixel count by 60% for files:','1mb+ in the addons folder and for files 500kb+ in userdata'):
        try:
            ReduceImageSize()
        except BaseException as e:
            pass
    
#=========================  Huge thanks to TV Addons and TDB Devs for the Log related code!!!  =========================================#  
def view_LastError():
        LogMenu()
        tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
        WindowsCache = xbmc.translatePath('special://home')
        found = 0

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

        xbmc.executebuiltin("Container.Refresh")

def viewErrors():
    LogMenu()
    tempPath = os.path.join(xbmc.translatePath('special://home'), 'temp')
    WindowsCache = xbmc.translatePath('special://home')
    found = 0
    i = 0
    String = " "

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
                            i = i + 1
                            if i == 1:
                                String = "[B][COLOR red]ERROR NUMBER " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'
                            else:
                                String = String + "[B][COLOR red]ERROR NUMBER: " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'

                        if found == 0:
                            dialog.ok(Title,'Great news! We did not find any errors in your log.')
                            sys.exit(0)
                        else:
                            c=String.replace('NEW_L','\n').replace('NEW_R','\r')
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
                            i = i + 1
                            if i == 1:
                                String = "[B][COLOR red]ERROR NUMBER " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'
                            else:
                                String = String + "[B][COLOR red]ERROR NUMBER " + str(i) + "[/B][/COLOR]\n\n" + checker + '\n'

                        if found == 0:
                            dialog.ok(Title,'Great news! We did not find any errors in your log.')
                            sys.exit(0)
                        else:
                            c=String.replace('NEW_L','\n').replace('NEW_R','\r')
                            TextBoxes(Title,"%s" % c)
                            sys.exit(0)
    if got_log == 0:
        dialog.ok(Title,'Sorry we could not find a log file on your system')

def viewLogFile():
    LogMenu()
    kodilog = xbmc.translatePath('special://logpath/kodi.log')
    spmclog = xbmc.translatePath('special://logpath/spmc.log')
    dbmclog = xbmc.translatePath('special://logpath/dbmc.log')
    kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
    spmcold = xbmc.translatePath('special://logpath/spmc.old.log')
    dbmcold = xbmc.translatePath('special://logpath/dbmc.old.log')

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

    elif os.path.exists(spmclog):
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
        
    elif os.path.exists(kodilog):
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
        dialog.ok(Title,'Sorry, No log file was found.','','[COLOR white]Thank you for using MK-IV Wizard[/COLOR]')

    xbmc.executebuiltin("Container.Refresh")

def Restore(url):
        xbmc.log('======================   MK-IV Wizard   ========================')
        xbmc.log('==============**********************************================')
        xbmc.log('===============   Start Restoring backup file   ================')
        if  os.path.exists(phoenix):
            choice = xbmcgui.Dialog().yesno(Title, 'It is recommended that you perform a Fresh Start before Restoring.', '','', nolabel='SKIP',yeslabel='FRESH START')
            if choice == 0:
                pass

            elif choice == 1:
                params=plugintools.get_params()
                FRESHSTART(params)
        else:
            pass
        '''if ADDON.getSetting('KodiVersion')=='Krypton':
            path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
            reqzip=os.path.join(path,'requests.zip')
            try:
                os.remove(reqzip)
            except:
                pass
            dp = xbmcgui.DialogProgress()
            dp.create(Title,"Applying patch... ",'','')
            downloader.download('https://github.com/MK-IV/Dependencies/raw/master/requests.zip', reqzip, dp)
            time.sleep(.5)
            dp.update(10,'Applying patch...[COLOR lime] Done[/COLOR]',"Extracting and Writing Files... ",'')
            try:
                shutil.rmtree(Requests)
            except: pass
            time.sleep(1)
            try: 
                extract.all(reqzip,ADDONS, dp) 
            except BaseException as e:
                pass
        else:'''
        dp = xbmcgui.DialogProgress()
        dp.create(Title,"Extracting and Writing Files... ",'','')
            #pass
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        try: 
            extract.all(url,addonfolder,dp)
        except BaseException as e:
            pass  
        dp.update(90,"Extracting and Writing Files... [COLOR lime] DONE[/COLOR]", "Checking paths and cleaning up...")
        time.sleep(.5)
        #FIX_SPECIAL()
        #time.sleep(.5)
        #xbmc.executebuiltin('UpdateLocalAddons')
        #time.sleep(.5)
        #xbmc.executebuiltin('ReloadSkin()')
        #time.sleep(.5)
        #xbmc.executebuiltin('RefreshRSS')
        #time.sleep(.5)
        #DeletePackages()
        try:
            #EnableAll() 
            #UpdateKryptonDB()
            dialog = xbmcgui.Dialog()
            dialog.ok("Your Restore Is Almost Finished...", 'The application will now close.', '', 'On your next start please leave it sit for a minute to allow add-ons to update.')
            killxbmc()
        except: pass
        dialog = xbmcgui.Dialog()
        dialog.ok("Your Restore Is Almost Finished...", 'The application will now close.', '', 'On your next start please leave it sit for a minute to allow add-ons to update.')
        killxbmc()

def DeleteThumbnails():
    xbmc.log('======================   MK-IV Wizard   ========================')
    xbmc.log('==============**********************************================')
    xbmc.log('===================   Deleting thumbails   =====================')
    xbmc.log('================================================================')
    Thumbnail_cache_path = xbmc.translatePath(os.path.join('special://home/userdata/Thumbnails', ''))
    try:    
        for root, dirs, files in os.walk(Thumbnail_cache_path):
            file_count = 0
            file_count += len(files)
        # Count files and give option to delete
            if file_count > 0:


                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        dialog = xbmcgui.Dialog()
                        dialog.ok(Title,'Thumbnails successfully removed.')
    except: 
        dialog = xbmcgui.Dialog()
        dialog.ok(Title, "Sorry we were not able to remove Thumbnail Files", "")
    xbmc.executebuiltin("Container.Refresh")

def Delete_Logs():  
    for infile in glob.glob(os.path.join(log_path, 'xbmc_crashlog*.*')):
         print infile
         os.remove(infile)

def ClearLog():
    kodilog = xbmc.translatePath('special://logpath/kodi.log')
    spmclog = xbmc.translatePath('special://logpath/spmc.log')

    if os.path.exists(kodilog): 
        localfile = open(kodilog, mode='w')
        localfile.write('')
        localfile.close()

    elif os.path.exists(spmclog):
        localfile = open(spmclog, mode='w')
        localfile.write('')
        localfile.close()
    else:
        dialog.ok(Title,'Sorry, we couldn\'t seem to find a log file to clear','','') 

def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing up:",'[COLOR lime]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.program.mkiv' in dirs:
                   import time
                   FORCE= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > FORCE:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
    time.sleep(1)                              

def UNIVERSAL_BACKUP():
    Delete_Logs()
    if not os.path.exists(BackupPath):
        if xbmcgui.Dialog().yesno(Title,'You need to select a backup folder in settings first','','Choose folder now?'):
            Backupfolder=xbmcgui.Dialog().browse(0,'Choose your Backup folder','files')
            SetSetting('backup',Backupfolder)
            pass
        else:
            return False, 0
    if not os.path.exists(fullbackuppath):
        os.makedirs(fullbackuppath)
    vq = _get_keyboard( heading="Enter a name for this backup" )
    if ( not vq ): return False, 0
    title = urllib.quote_plus(vq)
    backup_zip = xbmc.translatePath(os.path.join(fullbackuppath,title+'.zip'))
    '''if ADDON.getSetting('KodiVersion') == 'Krypton':
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        reqzip=os.path.join(path,'requests.zip')
        try:
            os.remove(reqzip)
        except:
            pass
        dp = xbmcgui.DialogProgress()
        dp.create(Title,"Checking for patches... ",'','')
        downloader.download('https://github.com/MK-IV/Dependencies/raw/master/requests.zip', reqzip, dp)
        time.sleep(.5)
        try:
            shutil.rmtree(Requests)
        except: pass
        time.sleep(.5)
        dp.update(50,"Applying patch... ",'','')
        try: 
            extract.all(reqzip,ADDONS, dp) 
        except BaseException as e:
            pass
        
    else:
        pass
    try: 
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, name+'.zip')
        time.sleep(.5)
        dp.update(0,"Applying Patch...[COLOR lime]DONE[/COLOR]","Extracting...")
        time.sleep(.5)
        extract.all(lib,addonfolder,dp)
    except BaseException as e:
        pass'''    
    #EnableAll() 
        #UpdateKryptonDB()
    time.sleep(.5)
    DeletePackages()
    exclude_dirs =  ['cache', 'system','temp','Thumbnails', "peripheral_data",'library','keymaps']
    exclude_files = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","spmc.log","spmc.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Addons19.db','saltscache.db-shm','saltscache.db-wal']
    if ADDON.getSetting('KodiVersion') == 'Jarvis': 
        exclude_dirs =  ['cache', 'system','temp','Thumbnails', "peripheral_data",'library','keymaps']
        exclude_files = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log","spmc.log","spmc.old.log","Textures13.db",'.DS_Store','.setup_complete','XBMCHelper.conf', 'advancedsettings.xml','Addons19.db','Addons20.db','saltscache.db-shm','saltscache.db-wal']
    message_header = "Creating Universal Backup"
    message1 = "Archiving..."
    message2 = ""
    message3 = "Please Wait"
    FIX_SPECIAL()
    time.sleep(.5)
    ARCHIVE_CB(HOME,backup_zip, message_header, message1, message2, message3, exclude_dirs, exclude_files)
    #if ADDON.getSetting('KodiVersion') == 'Krypton':
     #   RemoveTrigger()
      #  pass
    #else: pass
    dialog.ok("[COLOR lime][B]SUCCESS![/B][/COLOR]", 'You Are Now Backed Up.')
    dialog.ok("Backup has been saved to:", '[COLOR yellow]'+backup_zip+'[/COLOR]')
    xbmc.executebuiltin('Container.Refresh')

def RestoreOther():
    url=xbmcgui.Dialog().browse(1,'Choose your backup file','files','.zip')
    if url != '':
        try:
            Restore(url)
            killxbmc()
        except: sys.exit(0)
    else:
        sys.exit(0)

def ListBackRes(url):
    if dialog.yesno(Title,"[COLOR white]" + url + "[/COLOR]","Do you want to restore this backup?"):
        try:
            Restore(url)
            killxbmc()
        except: sys.exit(0)
    
    
def ListBackDel(url):
    if dialog.yesno(Title,"[COLOR white]" + url + "[/COLOR]","Do you want to delete this backup?"):
        os.remove(url)
        xbmc.executebuiltin('Container.Refresh')
        dialog.ok(Title,"[COLOR white]" + url + "[/COLOR]","Successfully deleted.")

def DeleteBackup(url):
    if dialog.yesno(Title,"[COLOR white]" + url + "[/COLOR]","Do you want to delete this backup?"):
        os.remove(url)
        xbmc.executebuiltin('Container.Refresh')
        dialog.ok(Title,"[COLOR white]" + url + "[/COLOR]","Successfully deleted.")
        xbmc.executebuiltin('Container.Refresh')



def DeleteAllBackups():
    if dialog.yesno(Title,"Do you want to delete all backups?"):
        shutil.rmtree(fullbackuppath)
        os.makedirs(fullbackuppath)
        xbmc.executebuiltin('Container.Refresh')
        dialog.ok(Title,"All backups successfully deleted.")

#============================================   Fanriffic Themes   ==========================================================

def INSTALL_FANRIFFIC(name,url,description):
    themename = name
    themename = themename.replace('[COLOR]','').replace('[/COLOR]','')
    choice = xbmcgui.Dialog().yesno(Title, '[COLOR white]Do you want to download the ' + themename + ' theme?[/COLOR]','',yeslabel='[B][COLOR lime]YES[/COLOR][/B]',nolabel='[B][COLOR lightskyblue]NO[/COLOR][/B]')
    if choice == 0:
        sys.exit(1)

    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    if not os.path.exists(path):
        os.makedirs(path)
    dp = xbmcgui.DialogProgress()
    dp.create(Title,'Downloading ' + themename +'...','','')
    lib=os.path.join(path, themename+'.zip')

    try:
        os.remove(lib)
    except:
        pass

    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    dp.update(0,'Downloading ' + themename +'...[COLOR lime]Done[/COLOR]',"Extracting Zip Please Wait","")
    unzip(lib,addonfolder,dp)
    #if ADDON.getSetting('KodiVersion','Krypton'):
    #    EnableAll()
    #    pass
    #else: pass
    dp.close()
    dialog = xbmcgui.Dialog()
    dialog.ok(Title, "The theme has now been installed. To save the changes you must now force close the Media Center.")
    killxbmc()

def ThemeMenu():
    addDir('Jarvis Builds and Themes',BASEURL,63,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','') 	
    addDir('Krypton Builds and Themes',BASEURL,64,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')
    addDir('Build Compatible Themes',BASEURL,65,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')
    addDir('Stand Alone Themes Old',BASEURL,66,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')
    addDir('Guide skins and stuff',BASEURL,67,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')	
    addDir('Updates',BASEURL,68,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')
    addDir('Requested Sky Menu Updates',BASEURL,69,'http://fanriffic.com/gallery_gen/f8cf5f20a1b5bd11d38f8f8292c430c0_383x400.png',FANART,'','')

def JarvisThemes():
    addItem('[COLOR red]SERVER 1 BUILDS[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/phooeybuilds.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
            pass
    except: pass
    addItem('[COLOR red]SERVER 1 THEMES[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/buildthemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
            pass
    except: pass
    addItem('[COLOR red]SERVER 2 BUILDS[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://ooogemaflop.co.uk/wizwiz/phooeybuilds.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
            pass
    except: pass
    addItem('[COLOR red]SERVER 2 THEMES[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/buildthemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
            pass
    except: pass
    addItem('[COLOR red]SERVER 3 THEMES[/COLOR]','',999,'','','')  
    try:
        link = OPEN_URL('http://ooogemaflop.co.uk/wizwiz/buildthemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass

def KryptonThemes():
    addItem('[COLOR red]SERVER 1 BUILDS[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/kryptonbuilds.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 1 THEMES[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/kryptonthemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2 BUILDS[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/kryptonbuilds.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2 THEMES[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/kryptonthemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass

def OldThemes():
    addItem('[COLOR red]SERVER 1[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/phooeythemesold.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/phooeythemesold.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass

def NewThemes():
    addItem('[COLOR red]SERVER 1[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/phooeythemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/phooeythemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 3[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://ooogemaflop.co.uk/wizwiz/phooeythemes.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass

def GuideThemes():
    addItem('[COLOR red]SERVER 1[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/phooeyguides.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/phooeyguides.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 3[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://ooogemaflop.co.uk/wizwiz/phooeyguides.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)  
    except: pass

def ThemeUpdates():
    addItem('[COLOR red]SERVER 1[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/phooeyupdates.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/phooeyupdates.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 3[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://ooogemaflop.co.uk/wizwiz/updates.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass

def SkyThemesGui():
    addItem('[COLOR red]SERVER 1[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://ooogemaflop.co.uk/wizwiz/skygui.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 2[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.quicksilver-music.com/wizwiz/skygui.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass
    addItem('[COLOR red]SERVER 3[/COLOR]','',999,'','','')
    try:
        link = OPEN_URL('http://fanriffic.com/wizwiz/skygui.txt').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        for name,url,iconimage,fanart,description in match:
            addItem(name,url,56,iconimage,fanart,description)
    except: pass

def unzip(_in, _out, dp):
    zin    = zipfile.ZipFile(_in,  'r')
    nFiles = float(len(zin.infolist()))
    count  = 0
    try:
        for item in zin.infolist():
            count += 1
            update = count / nFiles * 100
            dp.update(int(update),'','','[COLOR dodgerblue][B]' + str(item.filename) + '[/B][/COLOR]')
            try:
                zin.extract(item, _out)
            except Exception, e:
                print str(e)    
    except Exception, e:
        print str(e)
        return False

    return True

def MakePointerFile():
    if not os.path.exists(WorkPath) or WorkPath == "":
        if xbmcgui.Dialog().yesno(Title,'You need to select a Work Folder in Settings first.','','Choose your work folder now?'):
            Addon_Settings()
            pass
        else:
            return False, 0
    else:
        pass 
    xbmc.log('================  MK-IV Wizard  ================')
    xbmc.log('===========  Making A Pointer File  ============')
    fullworkpath = xbmc.translatePath(os.path.join(WorkFolder,'/KODI Work Folder/'))
    if not os.path.exists(fullworkpath):
        os.makedirs(fullworkpath)
    #if xbmcgui.Dialog().yesno(Title, 'A tutorial video is available for this section.', 'Would you like to see it?','', nolabel='SKIP',yeslabel='YES'):
        #YouTube('Enter the tutorial code here') #CamC
    vqname = _get_keyboard(heading="Enter the name of your build" )
    if ( not vqname ): return False, 0
    name = urllib.unquote_plus(vqname)
    choice = xbmcgui.Dialog().yesno(Title, 'For your builds zip file...', 'Does your link start with http:// or https://?','All links are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"   
    vqzip = _get_keyboard(default=protocol,heading="Enter the url of your build.zip" )
    if ( not vqzip ): return False, 0
    zip = urllib.unquote_plus(vqzip)
    #dialog.ok
    choice = xbmcgui.Dialog().yesno(Title, 'For your icon image...', 'Does your link start with http:// or https://?','All links are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"
    vqicon = _get_keyboard(default=protocol,heading="Enter the url of your icon image." )
    if ( not vqicon ): return False, 0
    icon = urllib.unquote_plus(vqicon)
    #dialog.ok
    choice = xbmcgui.Dialog().yesno(Title, 'For your Fanart image...', 'Does your link start with http:// or https://?','All links and are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"
    vqfan = _get_keyboard(default=protocol,heading="Enter the url of your fanart image." )
    if ( not vqfan ): vqfan = ""
    fan = urllib.unquote_plus(vqfan)
    #dialog.ok
    vqdes = _get_keyboard(heading="Enter a description of your build." )
    if ( not vqdes ): vqdes = ""
    description = urllib.unquote_plus(vqdes)
    vqver = _get_keyboard(default='1.0.0',heading="Enter the version of your build." )
    if ( not vqver ): vqdes = "1.0.0"
    version = urllib.unquote_plus(vqver)
    choice = xbmcgui.Dialog().select('What format would you like your pointer to be?', ['Wizard.xml', 'Wizard.txt', 'index.html'])
    if choice == 0:
        output = 0
        PointerFile = xbmc.translatePath(os.path.join(fullworkpath,'Wizard.xml'))
        WriteFile(PointerFile,'<MK4MakeAWizard>\n   name="'+name+'"\n   url="'+zip+'"\n   img="'+icon+'"\n   fanart="'+fan+'"\n   description="'+description+'"\n   version="'+version+'"\n</MK4MakeAWizard>')    
        pass
    elif choice == 1:
        output = 1
        PointerFile = xbmc.translatePath(os.path.join(fullworkpath,'Wizard.txt'))
        WriteFile(PointerFile,'\nname="'+name+'"\nurl="'+zip+'"\nimg="'+icon+'"\nfanart="'+fan+'"\ndescription="'+description+'"\nversion="'+version+'"\n\n\n')          
        pass
    elif choice == 2:
        output = 2
        PointerFile = xbmc.translatePath(os.path.join(fullworkpath,'index.html'))
        WriteFile(PointerFile,'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<html>\n <head>\n  <title>Index of /</title>\n </head>\n <body>\n<h1>Index of /</h1>\n  <table>\nname="'+name+'"<br>\nurl="'+zip+'"<br>\nimg="'+icon+'"<br>\nfanart="'+fan+'"<br>\ndescription="'+description+'"<br>\nversion="'+version+'"<br>\n<br>\n<br>\n</table>\n</body></html>')          
        pass
        
    AddBuild = xbmcgui.Dialog().yesno(Title,'Would you like to add another build to this file?')
    while AddBuild == 1:
        vqname = _get_keyboard(heading="Enter the name of your build" )
        if ( not vqname ): return False, 0
        name = urllib.unquote_plus(vqname)
        choice = xbmcgui.Dialog().yesno(Title, 'For your builds zip file...', 'Does your link start with http:// or https://?','All links are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
        if choice == 0:
            protocol="http://"
        elif choice == 1:
            protocol="https://"   
        vqzip = _get_keyboard(default=protocol,heading="Enter the url of your build.zip" )
        if ( not vqzip ): return False, 0
        zip = urllib.unquote_plus(vqzip)
        choice = xbmcgui.Dialog().yesno(Title, 'For your icon image...', 'Does your link start with http:// or https://?','All links are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
        if choice == 0:
            protocol="http://"
        elif choice == 1:
            protocol="https://"
        vqicon = _get_keyboard(default=protocol,heading="Enter the url of your icon image." )
        if ( not vqicon ): return False, 0
        icon = urllib.unquote_plus(vqicon)
        choice = xbmcgui.Dialog().yesno(Title, 'For your Fanart image...', 'Does your link start with http:// or https://?','All links and are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
        if choice == 0:
            protocol="http://"
        elif choice == 1:
            protocol="https://"
        vqfan = _get_keyboard(default=protocol,heading="Enter the url of your fanart image." )
        if ( not vqfan ): vqfan = ""
        fan = urllib.unquote_plus(vqfan)
        vqdes = _get_keyboard(heading="Enter a description of your build." )
        if ( not vqdes ): vqdes = ""
        description = urllib.unquote_plus(vqdes)
        vqver = _get_keyboard(default='1.0.0',heading="Enter the version of your build." )
        if ( not vqver ): vqdes = "1.0.0"
        version = urllib.unquote_plus(vqver)
        if output == 0:
            PointerFile = xbmc.translatePath(fullworkpath+'Wizard.xml')
            ReplaceText(PointerFile,'</MK4MakeAWizard>','\n   name="'+name+'"\n   url="'+zip+'"\n   img="'+icon+'"\n   fanart="'+fan+'"\n   description="'+description+'"\n   version="'+version+'"\n</MK4MakeAWizard>')    
            pass
        elif output == 1:
            PointerFile = xbmc.translatePath(fullworkpath+'Wizard.txt')
            ReplaceText(PointerFile,'End of file','name="'+name+'"\nurl="'+zip+'"\nimg="'+icon+'"\nfanart="'+fan+'"\ndescription="'+description+'"\nversion="'+version+'"\n\nEnd of file')          
            pass
        elif output == 2:
            PointerFile = xbmc.translatePath(fullworkpath+'index.html')
            ReplaceText(PointerFile,'End of file<br>','name="'+name+'"<br>\nurl="'+zip+'"<br>\nimg="'+icon+'"<br>\nfanart="'+fan+'"<br>\ndescription="'+description+'"<br>\nversion="'+version+'"<br>\n<br>\nEnd of file<br>')
            pass
        AddBuild = xbmcgui.Dialog().yesno(Title,'Would you like to add another build to this file?')

    xbmcgui.Dialog().ok(Title,'Pointer file successfully created!','It has been saved to:','[COLOR deepskyblue]'+PointerFile+'[/COLOR]')
    sys.exit()

def MakeRssFile():
    if not os.path.exists(WorkPath) or WorkPath == "":
        if xbmcgui.Dialog().yesno(Title,'You need to select a Work Folder in Settings first.','','Choose your work folder now?'):
            Addon_Settings()
            pass
        else:
            return False, 0
    else:
        pass    
    xbmc.log('================  MK-IV Wizard  ================')
    xbmc.log('===========  Started Making RSS File ===========')  
    fullworkpath = xbmc.translatePath(os.path.join(WorkFolder,'/KODI Work Folder/'))
    if not os.path.exists(fullworkpath):
        os.makedirs(fullworkpath)
    vqname = _get_keyboard(heading="Enter a Title for your rss feed" )
    if ( not vqname ): return False, 0
    name = urllib.unquote_plus(vqname)
    vqline1 = _get_keyboard(heading="Enter line 1 of your feed" )
    if ( not vqline1 ): return False, 0
    line1 = urllib.unquote_plus(vqline1)
    RssFile = xbmc.translatePath(os.path.join(fullworkpath,'rss.xml'))
    WriteFile(RssFile,'<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n<channel>\n  <title>'+name+'</title>\n  <item>\n    <title>'+line1+'                                                              </title>\n  </item>\n    </channel>\n</rss>') 
    addLine = xbmcgui.Dialog().yesno(Title,'Would you like to add another line?','', '', nolabel='No',yeslabel='Yes')
    while addLine == 1:
        newLine = _get_keyboard(heading="Enter the next line of your feed" )
        if ( not newLine ): newLine = ""
        line = urllib.unquote_plus(newLine)
        ReplaceText(RssFile,'    </channel>','  <item>\n   <title>'+line+'                                                       </title>\n  </item>\n    </channel>')
        addLine = xbmcgui.Dialog().yesno(Title,'Would you like to add another line?','', '', nolabel='No',yeslabel='Yes')  
    if xbmcgui.Dialog().yesno('Rss file made', 'If you would like to upload it now and get the url', 'you can update the media center ticker now.', '(Saved to: [COLOR deepskyblue]'+RssFile+'[/COLOR])', nolabel='No thanks',yeslabel='Enter URL'):
        choice = xbmcgui.Dialog().yesno(Title, 'For your rss.xml file...', 'Does your link start with http:// or https://?','All links are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
        if choice == 0:
            protocol="http://"
        elif choice == 1:
            protocol="https://"    
        vq = _get_keyboard(default=protocol,heading="Enter the url of your rss.xml" )
        if ( not vq ): return False, 0
        rssfeedlink = urllib.unquote_plus(vq)
        WriteFile(RSS,'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<rssfeeds>\n  <!--RSS feeds. To have multiple feeds, just add a feed to the set. You can also have multiple sets.-->\n  <!--To use different sets in your skin, each must be called from skin with a unique id.-->\n  <set id="1" rtl="false">\n    <feed updateinterval="30">'+rssfeedlink+'</feed>\n  </set>\n</rssfeeds>')
        xbmc.executebuiltin('RefreshRSS')
        xbmcgui.Dialog().ok(Title,'RssFeeds.xml edited successfully','', '')
        sys.exit()

def BuildAWizard():
    if not os.path.exists(WorkPath) or WorkPath == "":
        if xbmcgui.Dialog().yesno(Title,'You need to select a Work Folder in Settings first.','','Choose your work folder now?'):
			Addon_Settings()
        else:
            return False, 0    
    else:
        pass      
    xbmc.log('================  MK-IV Wizard  ================')
    xbmc.log('==========  Starting Build-A-Wizard  ===========')
    fullworkpath = xbmc.translatePath(os.path.join(WorkFolder,'/KODI Work Folder/'))
    if not os.path.exists(fullworkpath):
        os.makedirs(fullworkpath)
    dialog = xbmcgui.Dialog()
    dialog.ok('Step 1: Entering an ID for your wizard','The id is your addons xbmc ID... i.e. plugin.program.<your_id_here>','')
    vqid = _get_keyboard(heading="Enter an id for your wizard" )
    if ( not vqid ): return False, 0
    id = urllib.unquote_plus(vqid).replace(' ','_').replace('!','').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace('/','').replace("'","\'")
    dialog.ok('Step 2: Entering a name for your wizard','This is your wizard\'s name.','','i.e. MK-IV Wizard or My Wizard')
    vqname = _get_keyboard(heading="Enter a name for your wizard" )
    if ( not vqname ): return False, 0
    name = urllib.unquote_plus(vqname)
    dialog.ok('Step 3: Entering a provider name for your wizard','This is your name.','','i.e. CamC or Andy Anderson')
    vqproname = _get_keyboard(heading="Enter a provider name for your wizard" )
    if ( not vqproname ): return False, 0
    proname = urllib.unquote_plus(vqproname)
    choice = xbmcgui.Dialog().yesno('Step 4: Your Pointer file URL', 'For your URL to your pointer file.', 'Does your link start with http:// or https://?','All links and are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"
    vqurl = _get_keyboard(default=protocol,heading="Enter the url of your pointer file." )
    if ( not vqurl ): vqurl = ""
    url = urllib.unquote_plus(vqurl)
    dp.create(Title,'Checking URL','Resolving link...')
    dp.update(0)
    try: #Sleepers added to slow dialog down enough for user see whats happening.
        link = OPEN_URL(urllib.unquote_plus(vqurl)).replace('\n','').replace('\r','')
        match = re.compile('.+?ame="(.+?)".+?rl="(.+?)"').findall(link)
        if match:
            time.sleep(.5)
            dp.update(50,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...')
            time.sleep(.5)
            dp.update(99,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...[COLOR lime]Passed[/COLOR]')
            time.sleep(.5)
            dp.close()
            xbmcgui.Dialog().ok('[COLOR lime]Link is good![/COLOR]','The test showed we were able to reach the site you entered and read the name and url on your file!','','')
            pass
        else:
            time.sleep(.5)
            dp.update(50,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...')
            time.sleep(.5)
            dp.update(99,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...[COLOR red]Failed[/COLOR]')
            time.sleep(.5)
            dp.close()
            CheckLink = xbmcgui.Dialog().yesno('[COLOR red]Error[/COLOR]','We could not find a valid Pointer File at the link you provided!','Would you like to try again?','', nolabel='Skip',yeslabel='Retry')
            while CheckLink == 1:
                vqurl = _get_keyboard(default=urllib.unquote_plus(vqurl),heading="Try the url of your pointer file again." )
                if ( not vqurl ): vqurl = ""
                dp.create(Title,'Checking URL','Resolving link...')
                dp.update(0)
                try:
                    link = OPEN_URL(urllib.unquote_plus(vqurl)).replace('\n','').replace('\r','')
                    match = re.compile('.+?ame="(.+?)".+?rl="(.+?)"').findall(link)
                    if match:
                        time.sleep(.5)
                        dp.update(50,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...')
                        time.sleep(.5)
                        dp.update(99,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...[COLOR lime]Passed[/COLOR]')
                        time.sleep(.5)
                        dp.close()
                        xbmcgui.Dialog().ok('[COLOR lime]Link is good![/COLOR]','The test showed we were able to reach the site you entered and read the name and url on your file!','','')
                        url = urllib.unquote_plus(vqurl)
                        CheckLink = 0
                    else:
                        time.sleep(.5)
                        dp.update(50,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...')
                        time.sleep(.5)
                        dp.update(99,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...[COLOR red]Failed[/COLOR]')
                        time.sleep(.5)
                        dp.close()
                        CheckLink = xbmcgui.Dialog().yesno('[COLOR red]Error[/COLOR]','We could not find a valid Pointer File at the link you provided!','Would you like to try again?','', nolabel='Skip',yeslabel='Retry')
                except:
                    time.sleep(.5)
                    dp.update(50,'Checking URL','Resolving link...[COLOR red]Failed[/COLOR]')
                    time.sleep(.5)
                    dp.close()
                    CheckLink = xbmcgui.Dialog().yesno('[COLOR red]404 Error[/COLOR]','The site at the link you provided could not be reached!','Would you like to try again?','', nolabel='Skip',yeslabel='Retry') 
    except:
        time.sleep(1)
        dp.update(50,'Checking URL','Resolving link...[COLOR red]Failed[/COLOR]')
        time.sleep(.5)
        dp.close()
        CheckLink = xbmcgui.Dialog().yesno('[COLOR red]404 Error[/COLOR]','The site at the link you provided could not be reached!','Would you like to try again?','', nolabel='Skip',yeslabel='Retry')
        while CheckLink == 1:
            vqurl = _get_keyboard(default=urllib.unquote_plus(vqurl),heading="Try the url of your pointer file again." )
            if ( not vqurl ): vqurl = ""
            dp.create(Title,'Checking URL','Resolving link...')
            dp.update(0)
            try: 
                link = OPEN_URL(urllib.unquote_plus(vqurl)).replace('\n','').replace('\r','')
                match = re.compile('.+?ame="(.+?)".+?rl="(.+?)"').findall(link)
                if match:
                    time.sleep(.5)
                    dp.update(50,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...')
                    time.sleep(.5)
                    dp.update(99,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...[COLOR lime]Passed[/COLOR]')
                    time.sleep(.5)
                    dp.close()
                    xbmcgui.Dialog().ok('[COLOR lime]Link is good![/COLOR]','The test showed we were able to reach the site you entered and read the name and url on your file!','','')
                    url = urllib.unquote_plus(vqurl)
                    CheckLink = 0
                else:
                    time.sleep(.5)
                    dp.update(50,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...')
                    time.sleep(.5)
                    dp.update(99,'Checking URL','Resolving link...[COLOR lime]Passed[/COLOR]','Looking for pointer file...[COLOR red]Failed[/COLOR]')
                    time.sleep(.5)
                    dp.close()
                    CheckLink = xbmcgui.Dialog().yesno('[COLOR red]Error[/COLOR]','We could not find a valid Pointer File at the link you provided!','Would you like to try again?','', nolabel='Skip',yeslabel='Retry')
            except:
                time.sleep(.5)
                dp.update(50,'Checking URL','Resolving link...[COLOR red]Failed[/COLOR]')
                time.sleep(.5)
                dp.close()
                CheckLink = xbmcgui.Dialog().yesno('[COLOR red]404 Error[/COLOR]','The site at the link you provided could not be reached!','Would you like to try again?','', nolabel='Skip',yeslabel='Retry')  
  
    addontmp = xbmc.translatePath(os.path.join(Media1,'addon.xml'))
    defaulttmp = xbmc.translatePath(os.path.join(Media1,'default.py'))
    icontmp = xbmc.translatePath(os.path.join(Media1,'icon.png'))
    updater = xbmc.translatePath(os.path.join(Media1,'updater.py'))
    workfolder = xbmc.translatePath(os.path.join(Media1,name))
    outputfolder = xbmc.translatePath(os.path.join(workfolder,'plugin.program.'+id))
    outputfile = xbmc.translatePath(os.path.join(Media1,workfolder+'.zip'))
    addonxml =  xbmc.translatePath(os.path.join(outputfolder,'addon.xml'))
    defaultpy = xbmc.translatePath(os.path.join(outputfolder,'default.py'))
    iconpng = xbmc.translatePath(os.path.join(outputfolder,'icon.png'))
     
    if not os.path.exists(workfolder):
        os.makedirs(workfolder)
    if not os.path.exists(outputfolder):
        os.makedirs(outputfolder)        
    xbmcgui.Dialog().ok('Step 5: Your Wizards Icon','Select the image you want to use for your wizard.') 
    #icon = xbmcgui.Dialog().browse(1,'Add Wizard icon','files','.png|.jpg|.jpeg',True)
    #icon = xbmc.translatePath(''+icon+'')
    #Toast(icon)
    icon = xbmcgui.Dialog().browseMultiple(1,'Add icon image','files','.png|.jpg|.jpeg')
    for file in icon:
        file = xbmc.translatePath(file)
        shutil.copy(file,iconpng)
    dialog = xbmcgui.Dialog()
    if dialog.yesno(Title,'Would you like to allow your wizard to automatically check and apply updates to the source code when available?'):
        shutil.copy(updater,outputfolder)
    dp.create(Title,'Copying core files...')
    dp.update(0)
    time.sleep(1)
    shutil.copy(addontmp,outputfolder)
    shutil.copy(defaulttmp,outputfolder)
    shutil.copy(Extractor,outputfolder)
    shutil.copy(Downloader,outputfolder)
    dp.update(30,'Copying core files...[COLOR lime]Complete[/COLOR]','Personalizing [COLOR white]'+name+'[/COLOR]...')
    time.sleep(1)
    a=open(addonxml).read()
    b=a.replace('addonname','plugin.program.'+id).replace('wizardname',name).replace('providername',proname)
    f = open(addonxml, mode='w')
    f.write(str(b))
    f.close()
    time.sleep(1)
    a=open(defaultpy).read()
    b=a.replace('addonname','plugin.program.'+id).replace('wizardname',name).replace('providername',proname).replace('zipurl',url)
    f = open(defaultpy, mode='w')
    f.write(str(b))
    f.close()
    dp.update(60,'Personalizing [COLOR white]'+name+'[/COLOR]...[COLOR lime]Complete[/COLOR]','Creating installable zip file...')
    time.sleep(1)
    ZipIt(workfolder, workfolder,'plugin.program.'+id)
    time.sleep(.5)
    shutil.copy(outputfile,fullworkpath)
    time.sleep(.5)
    dp.update(90,'Creating installable zip file...[COLOR lime]Complete[/COLOR]','Cleaning up...')
    time.sleep(.5)
    shutil.rmtree(workfolder)
    os.remove(outputfile)
    dp.update(99,'Cleaning up...[COLOR lime]Complete[/COLOR]')
    time.sleep(1)
    dp.close()
    dialog.ok(Title, 'Your wizard is finished and saved to:','[COLOR deepskyblue]'+fullworkpath+'[/COLOR]')
    sys.exit()

def MKIVWIZARD():
	xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
	version=float(xbmc_version[:4])
	if version >= 17.0 and version <= 17.9:
		try:
			link = OPEN_URL('https://mk-iv.github.io/kRYPTON').replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
			for name,url,iconimage,fanart,description,version in match:
				addDir(name,url,27,iconimage,fanart,description,version)
		except:
			try:
			  	link = OPEN_URL('https://mk-iv.github.io/Pointer/').replace('\n','').replace('\r','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
				for name,url,iconimage,fanart,description,version in match:
					addDir(name,url,27,iconimage,fanart,description,version)
			except:
				Toast('The MK-IV servers are down at the moment. Please try again later.')
	elif version >= 16.0 and version <= 16.9:
		try:
			link = OPEN_URL('https://mk-iv.github.io/jARVIS').replace('\n','').replace('\r','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
			for name,url,iconimage,fanart,description,version in match:
				addDir(name,url,27,iconimage,fanart,description,version)
		except:
			try:
				link = OPEN_URL('https://mk-iv.github.io/Pointer/').replace('\n','').replace('\r','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
				for name,url,iconimage,fanart,description,version in match:
					addDir(name,url,27,iconimage,fanart,description,version)
			except:
				Toast('The MK-IV servers are down at the moment. Please try again later.')
	else:
		xbmcgui.Dialog().ok(Title,'Sorry, MK-IV is currently only available for Jarvis and Krypton')
		sys.exit(0)

def DONATE():
    OpenWebpage('http://paypal.me/mkiv')

def WEBSITE():
    myplatform = platform()
    if myplatform == 'android':
    	os.system('am start --user 0 -a android.intent.action.VIEW -d '+'http://mkiv.ca')
    elif myplatform != 'android':
        webbrowser.open_new_tab('http://mkiv.ca')

def BuildAWizardTextBox():
        TextBoxes('Build-A-Wizard Section','[B][COLOR dodgerblue]Making a Pointer File:[/COLOR][/B]\n\nA pointer file is a file that contains all of the information a wizard needs to make a menu item for your build.\n\nMore commonly known as a [COLOR yellow]\'Wizard.txt\'[/COLOR] file, this wizard will create a [COLOR yellow]\'Wizard.txt, \'Wizard.xml\' or \'Wizard.html\'[/COLOR] (output will be index.html for this one)\n\nTo successfully make this file you will need:\n\n[COLOR yellow]To have uploaded your builds/backups zip file and gotten the download url.[/COLOR] <---If you put this link in a webbrowser it should start downloading the zip file, not open a webpage.\n\n[COLOR yellow]A url to a .jpg or .png file for your icon.[/COLOR] <---This is the small picture that represents your build when highlighted\n\n[COLOR yellow]A url to a .jpg or .png file for your fanart[/COLOR] <---This is the background picture that appears when your build is highlighted.\n\n\n[B][COLOR dodgerblue]Making a Wizard:[/COLOR][/B]\n\nA Wizard is tool that downloads and installs your Media Center backup onto another device.\n\n To successfully make this a wizard you need to upload your pointer file and get its url.\n\n\n[B][COLOR dodgerblue]Making a RSS File:[/COLOR][/B]\n\nTo make a RSS file you only need the information you would like to provide.\n\n[COLOR yellow]***Once the file is made you will be prompted to upload it and enter its URL to apply the info to your build. (Optional)[/COLOR]\n\n\n[COLOR lime]Now, let\'s get started![/COLOR]') #Initial Textbox Explanation

def OpenTextbox(title,message):
        TextBoxes(title,message)

def OpenWebpage(url):
    myplatform = platform()
    if myplatform == 'android':
    	os.system('am start --user 0 -a android.intent.action.VIEW -d '+url) 
    elif myplatform != 'android': 
        webbrowser.open_new_tab(url)

def SUBMITREQUEST():
    OpenWebpage('http://submit.mkiv.ca')

def SPEEDTEST():
    speed = speedtest.speedtest()
    xbmc.executebuiltin('ShowPicture('+speed[0]+')')
    sys.exit()

    xbmc.executebuiltin("Container.Refresh")

def YouTube(url):
    try:
        window =GetWindowID()
        WizardWindow=xbmc.getCondVisibility('Window.IsTopMost('+window+')')
        id=url.replace('https://www.youtube.com/watch?v=','')
        url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
        xbmc.Player().play(url)
        #window =GetWindowID()
        #WizardWindow=xbmc.getCondVisibility('Window.IsTopMost(12005)')
        #while WizardWindow:
            #time.sleep(.5)
        #xbmc.Player().stop()
        #xbmc.executebuiltin('Action(Stop,12005')
        #sys.exit(0)
    except:
        return False, 0
        
def killxbmc():
    myplatform = platform()
    xbmc.log("Platform: " + str(myplatform))
    if myplatform == 'osx': # OSX
        xbmc.log('############   try osx force close  #################')
        try: os.system('killall -9 Kodi')
        except: pass
        try: os._exit(0)
        except: pass	
        try: sys.exit(2)
        except: pass
        Crash()
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        xbmc.log('############   try linux force close  #################')
        try: os.system('killall -9 kodi.bin')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os._exit(0)
        except: pass	
        try: sys.exit(2)
        except: pass
        Crash()
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        xbmc.log('############   try android force close  #################')
        try: os.system('kill $(ps com.semperpax.spmc16)')
        except: pass
        try: os.system('kill $(ps org.xbmc.kodi)')
        except: pass
        try : os.system('Process.killProcess(android.os.Process.org.fire.guru());')
        except: pass
        try : os.system('Process.killProcess(android.os.Process.org.fire.guruv());')
        except : pass
        try : os.system('Process.killProcess(android.os.Process.com.semperpax.spmc16());')
        except: pass
        try : os.system('Process.killProcess(android.os.Process.org.fire());')
        except: pass
        try : os.system('Process.killProcess(android.os.Process.org.fire,guru());')
        except: pass
        try: os._exit(0)
        except: pass	
        try: sys.exit(2)
        except: pass
        Crash()
        dialog.ok("[COLOR=red][B]PLEASE READ BELOW !!!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close the MC. [COLOR=red][B]DO NOT PRESS OK[/COLOR][/B]","Pull the power plug on your AndroidTV box now for changes to take effect.")
    elif myplatform == 'windows': # Windows
        xbmc.log('############   try windows force close  #################')
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try: os._exit(0)
        except: pass	
        try: sys.exit(2)
        except: pass
        Crash()
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        xbmc.log('############   try atv force close  #################')
        try: os.system('killall AppleTV')
        except: pass
        xbmc.log('############   try raspbmc force close  #################') #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
	try: os.system('killall -9 Kodi')
	except: pass
	try: os.system('killall -9 kodi')
	except: pass
        try: os._exit(0)
        except: pass	
        try: sys.exit(2)
        except: pass
        Crash()
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'
    elif xbmc.getCondVisibility('system.platform.Linux.RaspberryPi'):
        return 'linux'

def ReplaceText(File,ReplaceThis,WithThis):
    a=open(File).read()
    b=a.replace(ReplaceThis, WithThis)
    f = open(File, mode='w')
    f.write(str(b))
    f.close()

def WriteFile(File,Text):
    f = open(File, mode='w')
    f.write(Text)
    f.close()

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def WriteToLine(filename,Text,LineNum,ColumnNum):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(LineNum, ColumnNum)
        f.write(Text.rstrip('\r\n') + '\n' + content)

def get_Artwork():
    try:
        xbmc.log('======================   MK-IV Wizard   ========================')
        xbmc.log('==============**********************************================')
        xbmc.log('=================   Getting Add-on Artwork   ===================')
        name = 'MK4Art'
        url = 'http://art.mkiv.ca'
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        dp = xbmcgui.DialogProgress()        
        dp.create(Title,"Downloading required files... ",'', 'Please Wait')
        lib=os.path.join(path, name+'.zip')
        try:
            os.remove(lib)
        except:
            pass
        downloader.download(url, lib, dp)
        time.sleep(.5)
        dp.update(0,"Downloading required files...[COLOR lime]DONE[/COLOR]", "Extracting")
        extract.all(lib,ART,dp)
    except:
        Toast('Please try again later, (404)')

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


def EndUser():
    TextBoxes('[B][COLOR blue]A message from Team Kodi[/COLOR][/B]', '[COLOR blue]   The official Kodi version does not contain any content what so ever. This means that you\nshould provide your own content from a local or remote storage location, DVD, Blu-Ray or any other media carrier that you own. \n[CR]   Additionally Kodi allows you to install third-party plugins that may provide access to content that is freely available on the official content provider website. \n[CR]   The watching or listening of illegal or pirated content which would otherwise need to be paid for is not endorsed or approved by Team Kodi. \n[CR][COLOR yellow]   For more information please go to www.kodi.tv[/COLOR][/COLOR]                                                                                                                                                                                                                                           [COLOR deepskyblue][/COLOR]                                                                                                                                                                                  \n***Neither this addon nor its developer or contents have any affiliation what so ever with Team Kodi, the XBMC Foundation or any of its/their affiliates in any way.***')

def Notify(title,message,times,icon):
    icon = ICON
    xbmc.executebuiltin("XBMC.Notification("+title+","+message+","+times+","+icon+")")

def Toast(var):
    xbmcgui.Dialog().notification(Title, var, ICON, 5000, False)
    #xbmc.executebuiltin(Title,'+var+',5000,'''xbmcgui.NOTIFICATION_INFO''')

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def Addon_Settings():	
    ADDON.openSettings(sys.argv[0])
    while xbmc.getCondVisibility('Window.IsVisible(10140)'):  
        time.sleep(.5)
    xbmc.executebuiltin('Container.Refresh')
    #self.openSettings&query=0.0

def _get_keyboard( default="", heading="", hidden=False ):
    """ shows a keyboard and returns a value """
    keyboard = xbmc.Keyboard( default, heading, hidden )
    keyboard.doModal()
    if ( keyboard.isConfirmed() ):
        return unicode( keyboard.getText(), "utf-8" )
    return default  

def ZipIt(output_filename, dir_name, base_dir): #For folders
    shutil.make_archive(output_filename, 'zip', dir_name, base_dir)

def REMOVE_EMPTY_FOLDERS():
#initialize the counters
    xbmc.log('======================   MK-IV Wizard   ========================')
    xbmc.log('==============**********************************================')
    xbmc.log('==============   Start removing empty folders   ================')
    xbmc.log('================================================================')
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
            xbmc.log('======================   MK-IV Wizard   ========================')
            xbmc.log('==============**********************************================')
            xbmc.log('=====  "successfully removed: "+curdir   =============')
            xbmc.log('================================================================')
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count

def addDirectoryItem(handle, url, listitem, isFolder):
    xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)

def addBuildDir(name,url,mode,iconimage,fanart,video,description,skins,guisettingslink):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&video="+urllib.quote_plus(video)+"&description="+urllib.quote_plus(description)+"&skins="+urllib.quote_plus(skins)+"&guisettingslink="+urllib.quote_plus(guisettingslink)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        liz.setProperty( "Build.Video", video )
        if (mode==None) or (mode=='restore_option') or (mode=='backup_option') or (mode=='cb_root_menu') or (mode=='genres') or (mode=='grab_builds') or (mode=='community_menu') or (mode=='instructions') or (mode=='countries')or (url==None) or (len(url)<1):
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def GET_ADDON_STATS():
    dp.create(Title,'Counting total addons installed')
    dp.update(0)
    i=0
    for item in os.listdir(ADDONS):
        i=i+1
    addItem('[COLOR red][B]Add-on Information[/B][/COLOR]',BASEURL,666,ICON,FANART,'')
    addItem('[COLOR white]Total Addons = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(10,'[COLOR white]Counting the installed video addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "video" in item.lower():
            i=i+1
    addItem('[COLOR white]Video Addons = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(20,'[COLOR white]Counting the installed program addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "program" in item.lower():
            i=i+1
    addItem('[COLOR white]Program Addons = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(30,'[COLOR white]Counting the installed music addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "music" in item.lower():
            i=i+1
    addItem('[COLOR white]Music Addons = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(40,'[COLOR white]Counting the installed image addons.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):

        if "image" in item.lower():
            i=i+1
    addItem('[COLOR white]Picture Addons = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(50,'[COLOR white]Counting the installed scripts.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "script" in item.lower():
            i=i+1
    addItem('[COLOR white]Scripts = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    dp.update(55,'[COLOR white]Counting the installed skins.[/COLOR]')
    i=0
    for item in os.listdir(ADDONS):
        if "skin" in item.lower():
            i=i+1
    addItem('[COLOR white]Skins = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')


    dp.update(60,'[COLOR white]Counting the installed repositories.[/COLOR]')
    i=0
    for root, dirs, files in os.walk(ADDONS,topdown=True):
        dirs[:] = [d for d in dirs]
        for name in dirs:
            if "repo" in name.lower():
                i=i+1
    addItem('[COLOR white]Repositories = [/COLOR][COLOR dodgerblue]' + str(i) + '[/COLOR]',BASEURL,666,ICON,FANART,'')

    xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    dp.update(70,'[COLOR white]Finding which version of Kodi is installed.[/COLOR]')
    if version >= 11.0 and version <= 11.9:
        codename = 'Eden'
    if version >= 12.0 and version <= 12.9:
        codename = 'Frodo'
    if version >= 13.0 and version <= 13.9:
        codename = 'Gotham'
    if version >= 14.0 and version <= 14.9:
        codename = 'Helix'
    if version >= 15.0 and version <= 15.9:
        codename = 'Isengard'
    if version >= 16.0 and version <= 16.9:
        codename = 'Jarvis'
    if version >= 17.0 and version <= 17.9:
        codename = 'Krypton'

    dp.update(80,'[COLOR white]Getting your IP address.[/COLOR]')
    f = urllib.urlopen("http://www.canyouseeme.org/")
    html_doc = f.read()
    f.close()
    m = re.search('(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)',html_doc)
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    check = plugintools.get_setting("InstallRepo")
    check_build = plugintools.get_setting("AutoUpdate")

    dp.update(90,'[COLOR white]Getting your update preferences.[/COLOR]')
    if check=="true":
        a = "[COLOR lime]Yes[/COLOR]"
    else:
        a = "[COLOR lightskyblue]No[/COLOR]"
    if os.path.exists(Slave):    
        if check_build=="true":
            b = "[COLOR lime]Yes[/COLOR]"
        else:
            b = "[COLOR lightskyblue]No[/COLOR]"
    else:
        b = "[COLOR lightskyblue]No[/COLOR]"

    subnet=xbmc.getInfoLabel("Network.SubnetMask")
    gateway=xbmc.getInfoLabel("Network.GatewayAddress")
    dns1=xbmc.getInfoLabel("Network.DNS1Address")
    dns2=xbmc.getInfoLabel("Network.DNS2Address")
    cputemp=xbmc.getInfoLabel("System.CPUTemperature")

    addItem('[COLOR red][B]Network Information[/B][/COLOR]',BASEURL,666,ICON,FANART,'')
    addItem('[COLOR ghostwhite]Local IP: [/COLOR][COLOR white]' + s.getsockname()[0] + '[/COLOR]',BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]External IP: [/COLOR][COLOR white]' + m.group(0) + '[/COLOR]',BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]Subnet Mask: [/COLOR][COLOR white]%s' % subnet + "[/COLOR]",BASEURL,200,ICON,FANART,'') 
    addItem('[COLOR ghostwhite]Gateway Address: [/COLOR][COLOR white]%s' % gateway + "[/COLOR]",BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]DNS 1: [/COLOR][COLOR white]%s' % dns1 + "[/COLOR]",BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]DNS 2: [/COLOR][COLOR white]%s' % dns2 + "[/COLOR]",BASEURL,200,ICON,FANART,'')
    addItem('[COLOR red][B]System Information[/B][/COLOR]',BASEURL,666,ICON,FANART,'')
    addItem('[COLOR ghostwhite]Version: [/COLOR][COLOR dodgerblue]%s' % version + " " + codename + "[/COLOR]",BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]Auto-Install MK-IV Repo: [/COLOR]' + a,BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]Auto-Update on Media Center launch: [/COLOR]' + b + '    (Only on MK-IV Wizard Builds)',BASEURL,200,ICON,FANART,'')
    addItem('[COLOR ghostwhite]CPU Temperature: [/COLOR][COLOR white]%s' % cputemp + "[/COLOR]",BASEURL,200,ICON,FANART,'')

    dp.update(100)
    dp.close()
    xbmc.executebuiltin('Container.SetViewMode(50)')    

def GETFOLDERSIZE(path):
    global total_files
    global total_size
    total_size = 0
    total_files = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            total_files = total_files + 1
    total_size=float(total_size/1024)/float(1024)
    total_size=format(total_size, '.2f')
    total_size=str(total_size)+'mb'
    total_size = '[COLOR red]'+total_size+'[/COLOR]'
    return total_size

def WIZARD(name,url,version):
    if  os.path.exists(phoenix):
        choice = xbmcgui.Dialog().yesno(Title, 'It is recommended that you perform a Fresh Start before installing.', '','[COLOR lime]If you have just finished installing select "SKIP" then "Quit"[/COLOR]', nolabel='SKIP',yeslabel='FRESH START')
        if choice == 0:
            pass

        elif choice == 1:
            params=plugintools.get_params()
            FRESHSTART(params)
    else:
        pass
    choice = xbmcgui.Dialog().yesno('Install Wizard', '', '                            [COLOR lime]Select "Apply Changes" to begin[/COLOR]','[CR]', nolabel='Quit',yeslabel='Apply Changes')
    if choice == 0:
        sys.exit()
        time.sleep(.5)
    elif choice == 1:
        pass
    SetSetting('BuildName',name)
    SetSetting('BuildVersion',version)
    BackupAddonData()
    #localfile = open(AUTOEXEC, mode='w')
    #time.sleep(.5)
    #localfile.write('import xbmc\nxbmc.executebuiltin("RunAddon(script.mkiv)")')
    #localfile.close()
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()        
    dp.create(Title,"Downloading [COLOR white]"+name+"[/COLOR]... ",'', '')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    if ADDON.getSetting('KodiVersion')=='Krypton':
        dp.update(0,"Downloading [COLOR white]"+name+"[/COLOR]... [COLOR lime]DONE[/COLOR]","Extracting...")
        pass
    	'''dp.update(0,"Downloading [COLOR white]"+name+"[/COLOR]... [COLOR lime]DONE[/COLOR]","Applying Patch...", '')
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        reqzip=os.path.join(path,'requests.zip')
        try:
            os.remove(reqzip)
        except:
            pass
        downloader.download('https://github.com/MK-IV/Dependencies/raw/master/requests.zip', reqzip, dp)
        time.sleep(.5)
        try:
            shutil.rmtree(Requests)
        except: pass
        time.sleep(1)
        try:
            extract.all(reqzip,ADDONS, dp) 
        except BaseException as e:
            pass
        dp.update(0,"Applying Patch...[COLOR lime]DONE[/COLOR]","Extracting...")
        pass'''
    else:
        dp.update(0,"Downloading [COLOR white]"+name+"[/COLOR]... [COLOR lime]DONE[/COLOR]","Extracting...")
        pass
    try: 
        addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, name+'.zip')
        time.sleep(.5)

        time.sleep(.5)
        extract.all(lib,addonfolder,dp)
    except BaseException as e:
        pass       
    time.sleep(.5)
    try:
       os.remove(lib)
    except:
       pass
    #FIX_SPECIAL()
    #time.sleep(.5)
    #xbmc.executebuiltin('UpdateLocalAddons')
    #time.sleep(.5)
    #xbmc.executebuiltin('ReloadSkin()')
    #time.sleep(.5)
 #   xbmc.executebuiltin('RefreshRSS')
  #  time.sleep(.5)
    #DeletePackages()
    #if ADDON.getSetting('KodiVersion')=='Krypton':
    #    try:
    #        dp.update(0,"Extracting...[COLOR lime]DONE[/COLOR]", "Updating Krypton Database...")
            #EnableAll() 
    #        UpdateKryptonDB()
    #    except: pass
    #else: pass
    RestoreAddonData()
    dialog = xbmcgui.Dialog()
    dialog.ok("Your Setup Is Almost Finished...", 'The application will now close.', '', 'On your next start please leave it sit for a minute to allow add-ons to update.')
    killxbmc()
#   xbmc.executebuiltin("ActivateWindow(appearancesettings)")    
#    time.sleep(.5)
#    sys.exit()

def ShowPic(url):
        xbmc.executebuiltin('ShowPicture('+url+')')

def RepoAction(name, url):
    Source = xbmc.translatePath('special://home/userdata/sources.xml')
    if not os.path.isfile(Source):
            localfile = open(Source, mode='w')
            time.sleep(.5)
            localfile.write('<sources>\n    <programs>\n        <default pathversion="1"></default>\n    </programs>\n    <video>\n        <default pathversion="1"></default>\n    </video>\n    <music>\n        <default pathversion="1"></default>\n    </music>\n    <pictures>\n        <default pathversion="1"></default>\n    </pictures>\n    <files>\n        <default pathversion="1"></default>\n        <source>\n            <name>'+name+'</name>\n            <path pathversion="1">'+url+'</path>\n            <allowsharing>true</allowsharing>\n        </source>\n    </files>\n</sources>')
            localfile.close()            
            dialog = xbmcgui.Dialog()
            dialog.ok(Title,name+' has been added to your sources.','','It will appear on next Media Center start.')
          #  if dialog.yesno(Title,''+name+' has been added to your sources.\nWould you like to open the Add-on Browser now?'): 
          #      xbmc.executebuiltin('ActivateWindow(AddonBrowser,addons://install/,return')
            sys.exit()
    else:
        ReplaceText(Source,'<files>\n        <default pathversion="1"></default>','<files>\n        <default pathversion="1"></default>\n        <source>\n            <name>'+name+'</name>\n            <path pathversion="1">'+url+'</path>\n            <allowsharing>true</allowsharing>\n        </source>')
        dialog = xbmcgui.Dialog()
        dialog.ok(Title,name+' has been added to your sources.','','It will appear on next Media Center start.')
        #if dialog.yesno(Title,'' +name+ ' has been added to your sources.\nWould you like to open the Add-on Browser now?'): 
          #  xbmc.executebuiltin('ActivateWindow(AddonBrowser,addons://install/')
        sys.exit()

def TESTWIZARDMENU():
    xbmc.log('================  MK-IV Wizard  ================')
    xbmc.log('=================  Test Wizard  ================')
    link = OPEN_URL2('').replace('\n','').replace('\r','')
    match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,version in match:
        addDir(name,url,27,iconimage,fanart,description,version)
        setView('movies', 'MAIN')

def OPEN_URL2(url):
    vq = _get_keyboard( default="https://archive.org/download/" , heading="[COLOR lime]Enter Your Wizard.txt URL[/COLOR]" )
    if ( not vq ): return False, 0
    title = urllib.unquote_plus(vq)
    req = urllib2.Request(title)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def ADDONWIZ(name,url,description):
    xbmc.log('================  MK-IV Wizard  ================')
    xbmc.log('========     Starting Add-on Wizard    =========')
    xbmc.log('================================================')
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create(Title,"Downloading [COLOR white]"+name+"[/COLOR]",'', '')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://home/','addons/'))
    time.sleep(.5)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    dp.close()
    extract.all(lib,addonfolder,dp)
    time.sleep(1)
    if ADDON.getSetting('KodiVersion')=='Krypton':
        EnableAll()
        xbmc.executebuiltin('UpdateLocalAddons')
        pass
    else:
        xbmc.executebuiltin('UpdateLocalAddons')
        pass
    if 'Adults XXX Pack' in name:
            YouTube('1au5S9FknUM') 
            dialog = xbmcgui.Dialog()
            dialog.ok(Title, "Adult Add-ons Installed","")
    elif url=="http://thebeastkodi.com/repo/plugin.video.beast.zip":
        dialog = xbmcgui.Dialog()
        dialog.ok(Title,'Opening ad-page so you can sign in for your webcode to use The Beast','','')
        OpenWebpage('http://thebeastkodi.com/signup2/register.php')
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok(Title, name+" Successfully Installed","")

def InstallRequests():
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        reqzip=os.path.join(path,'requests.zip')
        try:
            os.remove(reqzip)
        except:
            pass
        dp = xbmcgui.DialogProgress()
        dp.create(Title,"Getting patch... ",'','')
        downloader.download('https://github.com/MK-IV/Dependencies/raw/master/requests.zip', reqzip, dp)
        time.sleep(.5)
        try:
            shutil.rmtree(Requests)
        except: pass
        time.sleep(1)
        try: 
            dp = xbmcgui.DialogProgress()
            dp.update(50,'Getting patch...[COLOR lime] Done[/COLOR]','Applying Patch...')
            extract.all(reqzip,ADDONS, dp) 
        except BaseException as e:
            pass
        #EnableAll()


def addItem(name,url,mode,iconimage,fanart,description):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addItem2(name,url,mode,iconimage,fanart,version):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&fanart="+urllib.quote_plus(fanart)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok

def addDir(name,url,mode,iconimage,fanart,description,version):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&version="+urllib.quote_plus(version)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description, "PlayCount": version } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==27 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok


def addDir2(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        if mode==27 :
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def CleanOnStart():
        DeleteThumbnails()
        time.sleep(1)
        DeletePackages()
        time.sleep(1)
        deletecachefiles()
        sys.exit(0)

def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

def ViewChangelog():
    f = open(ChangeLog,mode='r'); msg = f.read(); f.close()
    TextBoxes(Title+' - Changelog',"[COLOR white]" + msg + "[/COLOR]")

def BackupSkinSettings():
    if os.path.exists(SkinSettingsBackup):
        try:
            os.remove(SkinSettingsBackup)
            os.remove(GuiBackup)
        except: pass
    ZipIt(_SkinSettings,ADDON_DATA,skin) 
    if os.path.exists(ScriptSkin):
        ZipIt(ScriptSkin, ADDON_DATA,'ScriptSkinBackup')
        pass
    else: pass
    shutil.copy(GUI,GuiBackup)
    dialog = xbmcgui.Dialog()
    dialog.ok(Title,'Your Settings for '+skin+' have been saved','','')
    xbmc.executebuiltin("Container.Refresh")


def RestoreSkinSettings():
    #try:
        extract.all(SkinSettingsBackup,ADDON_DATA)
        if os.path.exists(ScriptSkinBackup):            
            extract.all(ScriptSkinBackup,ADDON_DATA)
        else: pass
        if os.path.exists(GuiBackup):
            f = open(GUI, mode='w')
            f.write('Wiped')
            f.close()
            os.remove(GUI)
            os.rename(GuiBackup,GUI)
        else: pass
        dialog = xbmcgui.Dialog()
        dialog.ok(Title,'Your Skin Settings have been restored','The MC will now close','')
        killxbmc()
    #except: pass
        xbmc.executebuiltin("Container.Refresh")

def DeleteSkinBackup():
    if os.path.exists(GuiBackup):
        os.remove(GuiBackup)
        pass
    else: pass
    if os.path.exists(SkinSettingsBackup):
        os.remove(SkinSettingsBackup)
        pass
    else: pass
    if os.path.exists(ScriptSkinBackup):
        os.remove(ScriptSkinBackup)
        pass
    else: pass
    xbmc.executebuiltin("Container.Refresh")

def BackupAddonData():
    exclude_dirs =  [skin, 'script.skinshortcuts']
    exclude_files = []
    message_header = "Saving addon data"
    message1 = "Archiving..."
    message2 = ""
    message3 = "Please Wait"
    ARCHIVE_CB(ADDON_DATA,addon_dataBackup, message_header, message1, message2, message3, exclude_dirs, exclude_files)

def RestoreAddonData():
    try:
        extract.all(addon_dataBackup,ADDON_DATA)
    except Exception, e:
        print str(e)  
    dialog = xbmcgui.Dialog()
    dialog.ok(Title,'Your addon settings have been restored','The MC will now close','')

def DeleteAddonDataBackup():
    if os.path.exists(addon_dataBackup):
        os.remove(addon_dataBackup)
        pass
    else: pass
    xbmc.executebuiltin("Container.Refresh")

def ReduceImageSize(): # Will add slider to choose > file size and int(quality)
    from PIL import Image
    dp.create(Title,"Reducing Image Sizes...",'[COLOR deepsky][/COLOR]', '')
    for root, dirs, files in os.walk(ADDONS):  #Search all png then optimize and reduce pixels by 60% if file larger than 800kb (keeps ratio)
        for file in files:
            if file.endswith(".png"):
                dp.update(0,"Checking image size on "+file,'',  'Please Wait')
                image=os.path.join(root, file)
                size = os.path.getsize(image)
                if size >= 1000000 :
                    i=1
                    renameimage=image.replace('.png','.jpg')
                    os.rename(image,renameimage)
                    try: os.remove(image)
                    except: pass
                    while size >= 1000000:
                        dp.update(0,"Resizing "+file,'',  'Please Wait')
                        a=Image.open(renameimage)
                        a.save(renameimage,optimize=True,quality=60)
                        if i==2: break
                        size = os.path.getsize(renameimage)
                        i=i+1
                    os.rename(renameimage, image)
    for root, dirs, files in os.walk(USERDATA):  #Search all png then optimize and reduce pixels by 60% if file larger than 800kb (keeps ratio)
        for file in files:
            if file.endswith(".png"):
                dp.update(0,"Checking image size on "+file,'',  'Please Wait')
                image=os.path.join(root, file)
                size = os.path.getsize(image)
                if size >= 500000 :
                    i=1
                    renameimage=image.replace('.png','.jpg')
                    os.rename(image,renameimage)
                    try: os.remove(image)
                    except: pass
                    while size >= 500000:
                        dp.update(0,"Resizing "+file,'',  'Please Wait')
                        a=Image.open(renameimage)
                        a.save(renameimage,optimize=True,quality=60)
                        if i==2: break
                        size = os.path.getsize(renameimage)
                        i=i+1
                    os.rename(renameimage, image)
    for root, dirs, files in os.walk(ADDONS):  #Search all jpg then optimize and reduce pixels by 60% if file larger than 800kb (keeps ratio)
        for file in files:
            if file.endswith(".jpg"):
                dp.update(0,"Checking image size on "+file,'',  'Please Wait')
                image=os.path.join(root, file)
                size = os.path.getsize(image)
                if size >= 1000000 :  
                    i=1
                    while size >= 1000000:
                        dp.update(0,"Resizing "+file,'',  'Please Wait')
                        a=Image.open(image)
                        a.save(image,optimize=True,quality=60)
                        if i==2: break
                        i=i+1
                        size = os.path.getsize(image)
    for root, dirs, files in os.walk(USERDATA):  #Search all jpg then optimize and reduce pixels by 60% if file larger than 800kb (keeps ratio)
        for file in files:
            if file.endswith(".jpg"):
                dp.update(0,"Checking image size on "+file,'',  'Please Wait')
                image=os.path.join(root, file)
                size = os.path.getsize(image)
                if size >= 500000 :  
                    i=1
                    while size >= 500000:
                        dp.update(0,"Resizing "+file,'',  'Please Wait')
                        a=Image.open(image)
                        a.save(image,optimize=True,quality=60)
                        if i==2: break
                        i=i+1
                        size = os.path.getsize(image)
    for root, dirs, files in os.walk(ADDONS):  #Search all jpeg then optimize and reduce pixels by 60% if file larger than 800kb (keeps ratio)
        for file in files:
            if file.endswith(".jpeg"):
                dp.update(0,"Checking image size on "+file,'',  'Please Wait')
                image=os.path.join(root, file)
                size = os.path.getsize(image)
                if size >= 1000000 :  
                    i=1
                    renameimage=image.replace('.jpeg', '.jpg')
                    os.rename(image,renameimage)
                    try: os.remove(image)
                    except: pass
                    while size >= 1000000:
                        dp.update(0,"Resizing "+file,'',  'Please Wait')
                        a=Image.open(renameimage)
                        a.save(renameimage,optimize=True,quality=60)
                        if i==2: break
                        size = os.path.getsize(renameimage)
                        i=i+1
                    os.rename(renameimage, image)
    for root, dirs, files in os.walk(USERDATA):  #Search all jpeg then optimize and reduce pixels by 60% if file larger than 800kb (keeps ratio)
        for file in files:
            if file.endswith(".jpeg"):
                dp.update(0,"Checking image size on "+file,'',  'Please Wait')
                image=os.path.join(root, file)
                size = os.path.getsize(image)
                if size >= 500000 :  
                    i=1
                    renameimage=image.replace('.jpeg', '.jpg')
                    os.rename(image,renameimage)
                    try: os.remove(image)
                    except: pass
                    while size >= 500000:
                        dp.update(0,"Resizing "+file,'',  'Please Wait')
                        a=Image.open(renameimage)
                        a.save(renameimage,optimize=True,quality=60)
                        if i==2: break
                        size = os.path.getsize(renameimage)
                        i=i+1
                    os.rename(renameimage, image)
                    

def MK4Backgrounds():
    Initial_Size = GETFOLDERSIZE(Backgrounds)
    #xbmc.executebuiltin('ActivateWindow(10003,'+folder+',return)')
    if ADDON.getSetting('KodiVersion') == 'Jarvis' and skin == 'skin.aeon.nox.silvo':
        Fix = os.path.join(Resources,'FileBrowser.xml')
        FB = xbmc.translatePath(os.path.join('special://home/addons/skin.aeon.nox.silvo/1080i/','FileBrowser.xml'))
        os.remove(FB)
        shutil.copy(Fix,FB)
        xbmc.executebuiltin('ReloadSkin')
    elif ADDON.getSetting('KodiVersion') == 'Krypton' and skin == 'skin.aeon.nox.silvo':
        Fix = os.path.join(Resources,'FileBrowser2.xml')
        FB = xbmc.translatePath(os.path.join('special://home/addons/skin.aeon.nox.silvo/1080i/','FileBrowser.xml'))
        os.remove(FB)
        shutil.copy(Fix,FB)
        xbmc.executebuiltin('ReloadSkin')
            
    section=xbmcgui.Dialog().select('Add images or browse in which section?',['LiveTV', 'TV Shows','Movies','Music','Kids Zone','Her Place','Man Cave','Add-ons','System','Premium TV'])
#                                                                                 0          1          2       3          4          5           6         7          8         9      
    if section == 0:
        folder = xbmc.translatePath(os.path.join('special://home/userdata/Background_pics/','sports/'))
        sec = 'LiveTV'
        pass
    elif section == 1:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/tv shows/')
        sec = 'TV Shows'
        pass
    elif section == 2:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/movies/')
        sec = 'Movies'
        pass
    elif section == 3:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/music/')
        sec = 'Music'
        pass
    elif section == 4:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/kids/')
        sec = 'Kids Zone'
        pass
    elif section == 5:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/ladies/')
        sec = 'Her Place'
        pass        
    elif section == 6:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/mens area/')
        sec = 'Man Cave'
        pass
    elif section == 7:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/addons/')
        sec = 'Add-ons'
        pass
    elif section == 8:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/settings/')
        sec = 'System'
        pass
    elif section == 9:
        folder = xbmc.translatePath('special://home/userdata/Background_pics/premium/')
        sec = 'Premium TV'
        pass

    if xbmcgui.Dialog().yesno(Title,'Do you want to add images to this section or view it in File Manager?',nolabel='[COLOR lime]Add[/COLOR]',yeslabel='[COLOR red]File Manager[/COLOR]'):
        Toast('[COLOR orangered]Directing File Manager to[/COLOR] [COLOR yellow]'+sec+'[/COLOR]')
        xbmc.executebuiltin('ActivateWindow(10003,'+folder+',return)')
        #images = xbmcgui.Dialog().browseMultiple(2,'Remove background images','files','',False,False,''+folder)
                #confirm = xbmcgui.Dialog().select('Confirm deletion',['Cancel','[COLOR red]Delete[/COLOR]'])

    else:
        Toast('[COLOR lime]Adding to[/COLOR] '+sec)
        Default = ADDON.getSetting('backup')
        images = xbmcgui.Dialog().browseMultiple(2,'Add background images','files','',False,False,Default)
        for file in images:
            file = xbmc.translatePath(file)
            shutil.copy(file, folder)
            
    EditMore = xbmcgui.Dialog().yesno(Title,'Would you like to edit another section?')
    while EditMore == 1:
        section=xbmcgui.Dialog().select('Add images or Browse in which section?',['LiveTV', 'TV Shows','Movies','Music','Kids Zone','Her Place','Man Cave','Add-ons','System','Premium TV'])
#                                                                                     0          1          2       3          4          5           6         7          8         9      
        if section == 0:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/sports/')
            sec = 'LiveTV'
            pass
        elif section == 1:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/tv shows/')
            sec = 'TV Shows'
            pass
        elif section == 2:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/movies/')
            sec = 'Movies'
            pass
        elif section == 3:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/music/')
            sec = 'Music'
            pass
        elif section == 4:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/kids/')
            sec = 'Kids Zone'
            pass
        elif section == 5:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/ladies/')
            sec = 'Her Place'
            pass        
        elif section == 6:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/mens area/')
            sec = 'Man Cave'
            pass
        elif section == 7:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/addons/')
            sec = 'Add-ons'
            pass
        elif section == 8:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/settings/')
            sec = 'System'
            pass
        elif section == 9:
            folder = xbmc.translatePath('special://home/userdata/Background_pics/premium/')
            sec = 'Premium TV'
            pass


        if xbmcgui.Dialog().yesno(Title,'Do you want to add images to this section or view it in File Manager?',nolabel='[COLOR lime]Add[/COLOR]',yeslabel='[COLOR red]File Manager[/COLOR]'):
            Toast('[COLOR orangered]Browsing[/COLOR] '+sec)
            xbmc.executebuiltin('ActivateWindow(10003,'+folder+',return)')
            '''images = xbmcgui.Dialog().browseMultiple(2,'Remove background images','files','',False,False,folder)
            for file in images:
                file = xbmc.translatePath(file)
                confirm = xbmcgui.Dialog().select('Confirm deletion',['Cancel','[COLOR red]Delete[/COLOR]'])
                if file == '':
                    return
                elif confirm == 0:
                    return
                elif confirm == 1:
                    try:
                        os.unlink(file)
                    except: 
                        shutil.rmtree(file)'''
        else:
            Toast('[COLOR lime]Adding to[/COLOR] [COLOR yellow]'+sec+'[/COLOR]')
            Default = ADDON.getSetting('backup')
            images = xbmcgui.Dialog().browseMultiple(2,'Add background images','files','',False,False,Default)
            for file in images:
                file = xbmc.translatePath(file)
                shutil.copy(file, folder)
        EditMore = xbmcgui.Dialog().yesno(Title,'Would you like to edit another section?')
    Post_Size = GETFOLDERSIZE(Backgrounds)
    if Post_Size != Initial_Size:
        Toast('Backing up changes')
        if os.path.exists(BackgroundsBackup):
            os.remove(BackgroundsBackup)
        else: pass
        ZipIt(BackgroundsBackup,USERDATA,'Background_pics')
        xbmc.executebuiltin('Container.Refresh')
    else:
        sys.exit(0)
        
def RestoreMK4Backgrounds():
    #try:
        if os.path.exists(BackgroundsBackup):   
            shutil.rmtree(Backgrounds)
            extract.all(BackgroundsBackup,USERDATA)
        else: pass
    #except: pass
        Toast('Backgrounds Restored')
        xbmc.executebuiltin("Container.Refresh")

def DeleteMK4BackgroundsBackup():
    if os.path.exists(BackgroundsBackupZip):
        os.remove(BackgroundsBackupZip)
        pass
    else:
        pass
    xbmc.executebuiltin("Container.Refresh")

def NewSession():
	if ADDON.getSetting('NewSession') == 'true':
		try:
			Toast('Welcome back to the '+Title)
			myplatform = platform()            
			if myplatform == 'android':
				if BackupPath=="":
					SetSetting('UserPath','/storage/emulated/0/')
					SetSetting("backup","/storage/emulated/0/")
					RepoAction('Android Device', '/storage/emulated/0/')
					if WorkPath=="":  
						SetSetting("MK4WorkFolder","/storage/emulated/0/")
						pass
					else: pass
				else: pass
			elif myplatform == 'osx':
				SetSetting('UserPath',HOME)
				time.sleep(.5)
				UserPath=ADDON.getSetting('UserPath')
				UserPath=UserPath.replace('/Library/Application Support/Kodi','')
				if BackupPath=="": 
					SetSetting('backup',UserPath+'Desktop/')
					RepoAction('Desktop',UserPath+'Desktop/')
					if WorkPath=="": 
						SetSetting('MK4WorkFolder',UserPath+'Desktop/')
						pass
					else: pass
				else: pass
			elif myplatform == 'linux':
				SetSetting('UserPath',HOME)
				time.sleep(.5)
				UserPath=ADDON.getSetting('UserPath')
				UserPath=UserPath.replace('/.kodi','')
				if BackupPath=="": 
					SetSetting('backup',UserPath+'Desktop/')
					RepoAction('Desktop',UserPath+'Desktop/')
					if WorkPath=="": 
						SetSetting('MK4WorkFolder',UserPath+'Desktop/')
						pass
					else: pass
				else: pass
			elif myplatform == 'windows':
				SetSetting('UserPath',HOME)
				time.sleep(.5)
				UserPath=ADDON.getSetting('UserPath')
				UserPath=UserPath.replace('\\AppData\\Roaming\\Kodi','')
				SetSetting('UserPath',UserPath)
				time.sleep(1) 
				if BackupPath=="": 
					SetSetting('backup',UserPath+'Desktop\\')
					RepoAction('Desktop',UserPath+'Desktop\\')
					if WorkPath=="": 
						SetSetting('MK4WorkFolder',UserPath+'Desktop\\')
						pass
					else: pass
				else: pass
			else: pass
		except: pass 
		SetSetting('NewSession','false')
		paths = ADDON.getSetting("backup")
		time.sleep(1)
		Toast('Backup folder set to: '+paths)
		#try:
		dp = xbmcgui.DialogProgress()
		dp.create(Title,'Checking for updates...','', 'Please Wait')
		link = OPEN_URL('https://raw.githubusercontent.com/MK-IV/plugin.program.mkiv/master/addon.xml').replace('\n','').replace('\r','')
		match = re.compile('id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(link)  
		for id, name, version in match:
			xbmc.log('version='+version+' Addon='+ADDON.getAddonInfo("version")+'')
			if version > ADDON.getAddonInfo('version'):
				#try:
				path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
				dp = xbmcgui.DialogProgress()
				dp.create(Title,'Downloading '+Title+' update...','', 'Please Wait')
				lib=os.path.join(path, 'plugin.program.mkiv-master.zip')
				try:
					os.remove(lib)
				except:
					pass
				downloader.download('https://github.com/MK-IV/plugin.program.mkiv/archive/master.zip', lib, dp)
				dp.update(0,'Downloading '+Title+' update... [COLOR lime]Finished[/COLOR]', 'Installing...')
				extract.all(lib,ADDONS,dp)
				time.sleep(.5)
				try:
					os.remove(lib)
				except:
					pass
				os.rename(Local,Localtmp)
				os.rename(Master,Local)
				shutil.rmtree(Localtmp)
				time.sleep(1)
				DeleteThumbnails()
				xbmc.executebuiltin('Container.Refresh')
				#xbmcgui.Dialog().ok(Title,Title+' Restart required...','','Press OK to close the add-on')
				#sys.exit(0)
				#except: pass
			else: pass
		#except: pass
        
def Check4Update():
    try:
        BuildName = ADDON.getSetting('BuildName')
        BuildVersion = ADDON.getSetting('BuildVersion')
        link = OPEN_URL('https://MK-IV.github.io/Check4Updates').replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?rl="(.+?)".+?ersion="(.+?)".+?resh="(.+?)"').findall(link)
        for name,url,version,fresh in match:
            xbmc.log('name= '+name+' url='+url+' version='+version+' fresh='+fresh)
            xbmc.log('BuildName='+BuildName+' BuildVersion='+BuildVersion)
            if name == BuildName and version > BuildVersion: 
                if fresh == "true" and os.path.exists(phoenix):
                    if not xbmcgui.Dialog().yesno(Title,'There appears to be a major update available for '+BuildName,'A Fresh Start was recommended before installing', nolabel='skip', yeslabel='Wipe'):
                        if xbmcgui.Dialog().yesno(Title,'Would you like to continue with the update anyway?'):
                            pass
                        else: sys.exit(0)
                    else:
                    	BackupAddonData() 
                        params=plugintools.get_params()
                        FRESHSTART(params)
                else: pass
                if not os.path.exists(addon_dataBackup):
                	BackupAddonData()
            	else: pass
                path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                dp = xbmcgui.DialogProgress()        
                dp.create(Title,'Downloading [COLOR white]'+name+'[/COLOR] update... ')
                lib=os.path.join(path, name+'.zip')
                try:
                    os.remove(lib)
                except:
                    pass
                downloader.download(url, lib, dp)
                addonfolder = xbmc.translatePath(os.path.join('special://','home'))
                time.sleep(.5)
                if fresh == 'false':
                    dp.update(0,'Downloading [COLOR white]'+name+'[/COLOR] update...[COLOR lime]DONE[/COLOR]','Applying update...')
                    pass
                else:
                    dp.update(0,'Downloading [COLOR white]'+name+'[/COLOR] update...[COLOR lime]DONE[/COLOR]','Applying update...','Screen will go black for a moment while extracting')
                    time.sleep(5)
                    xbmc.executebuiltin('UnloadSkin()')
                    pass
                try: 
                    extract.all(lib,addonfolder,dp)
                except BaseException as e:
                    pass 
                RestoreAddonData()
                SetSetting('BuildVersion',version)
                xbmc.executebuiltin('ReloadSkin()')
                time.sleep(.5)
                try:
                    os.remove(lib)
                except:
                    pass
                if fresh == 'true':
                    xbmcgui.Dialog().ok(Title,name+' Update successful!','The media center will now close...','Please leave it sit for a minute on next start.')
                    killxbmc()
                else: pass
    except: pass


def RequiredUpdate():
	try:
		LockXbmc()
		BuildName = 'MK-IV'
		link = OPEN_URL('https://MK-IV.github.io/Check4Updates').replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?ersion="(.+?)"').findall(link)
		for name,url,version in match:
			if name == BuildName:
				path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
				dp = xbmcgui.DialogProgress()        
				dp.create(Title,'Downloading [COLOR white]'+name+'[/COLOR]... ')
				lib=os.path.join(path, name+'.zip')
				try:
					os.remove(lib)
				except:
					pass
				downloader.download(url, lib, dp)
				addonfolder = xbmc.translatePath(os.path.join('special://','home'))
				time.sleep(.5)
				dp.update(0,'Downloading [COLOR white]'+name+'[/COLOR] --- [COLOR lime]DONE[/COLOR]','Applying changes...')
				try: 
					extract.all(lib,addonfolder,dp)
				except BaseException as e:
					pass 
				SetSetting('BuildVersion',version)
				time.sleep(.5)
				try:
					os.remove(lib)
				except:
					pass
				UnlockXbmc()
				killxbmc()
	except:
		UnlockXbmc()
		pass

def MK4WizUpdate():
    #try:
        dp = xbmcgui.DialogProgress()
        dp.create(Title,'Checking for updates...','', 'Please Wait')
        link = OPEN_URL('https://raw.githubusercontent.com/MK-IV/plugin.program.mkiv/master/addon.xml').replace('\n','').replace('\r','')
        match = re.compile('id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(link)
        for id, name, version in match:
            xbmc.log(name+'---'+id+'----version='+version+' Addon='+ADDON.getAddonInfo("version")+'')
            if version > ADDON.getAddonInfo('version'):
                #try:
                path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
                dp = xbmcgui.DialogProgress()
                dp.create(Title,'Downloading '+Title+' update...','', 'Please Wait')
                lib=os.path.join(path, 'plugin.program.mkiv-master.zip')
                try:
                    os.remove(lib)
                except:
                    pass
                downloader.download('https://github.com/MK-IV/plugin.program.mkiv/archive/master.zip', lib, dp)
                dp.update(0,'Downloading '+Title+' update... [COLOR lime]Finished[/COLOR]', 'Installing...')
                extract.all(lib,ADDONS,dp)
                time.sleep(.5)
                try:
                    os.remove(lib)
                except:
                    pass
                os.rename(Local,Localtmp)
                os.rename(Master,Local)
                shutil.rmtree(Localtmp)
                time.sleep(1)
                DeleteThumbnails()
                xbmc.executebuiltin('Container.Refresh')
                #xbmcgui.Dialog().ok(Title,Title+' Restart required...','','Press OK to close the add-on')
                #sys.exit(0)
                #except: pass
            else: pass
    #except: pass

def OpenExecute(addon, mode):
    xbmc.executebuiltin('ActivateWindow(10001,"plugin://'+addon+'&mode='+mode+')')

def AddonInstallWindow():
    xbmc.executebuiltin('ActivateWindow(10040,"addons://install/",return)')
    
def UpdateSwitch():
    build=ADDON.getSetting('BuildName')
    if ADDON.getSetting('Update') == 'false' and ADDON.getSetting('BuildName') != '':
        SetSetting('Update','true')
        Toast('AutoUpdate [COLOR lime]Enabled[/COLOR] for '+build)
        xbmc.executebuiltin('Container.Refresh')
    elif ADDON.getSetting('Update') == 'true' and ADDON.getSetting('BuildName') != '': 
        SetSetting('Update','false')
        Toast('AutoUpdate [COLOR red]Disabled[/COLOR] for '+build)
        xbmc.executebuiltin('Container.Refresh')
    else:
        Toast('[COLOR orangered]Feature is not available on your current set-up[/COLOR]')
        
def ResetMK4Settings():
    SetSetting('backup','')
    time.sleep(.5)
    SetSetting('InstallRepo','false')
    time.sleep(.5)
    SetSetting('UpdateAddons','false')
    time.sleep(.5)
    SetSetting('MK4Build','false')
    time.sleep(.5)
    SetSetting('FirstMK4Startup','true')
    time.sleep(.5)
    SetSetting('NewSession','true')
    time.sleep(.5)
    SetSetting('ShowAdult','false')
    time.sleep(.5)
    SetSetting('password','')
    time.sleep(.5)
    SetSetting('MK4WorkFolder','')
    time.sleep(.5)
    SetSetting('MAIN','500')
    time.sleep(.5)
    SetSetting('INFO','515')
    Toast(Title+' Settings reset')
    
def KillMK4Settings():
    settings=xbmc.translatePath(os.path.join(ADDON_DATA+addon_id,'settings.xml'))
    try: 
        os.remove(settings)
    except:
        pass
        
def RepoFiles():
    RepoFolder=xbmc.translatePath(os.path.join(fullworkpath,'Repository/'))
    if not os.path.exists(fullworkpath):
        os.makedirs(fullworkpath)
    if not os.path.exists(RepoFolder):
        os.makedirs(RepoFolder)
    Addonsxml = xbmc.translatePath(os.path.join(RepoFolder,'addons.xml'))
    Addonsxmlmd5 = xbmc.translatePath(os.path.join(RepoFolder,'addons.xml.md5'))
    if os.path.exists(Addonsxml) and not os.path.exists(Addonsxmlmd5):
        xbmcgui.Dialog().ok('[COLOR red]Warning![/COLOR]','addons.xml has been detected in your work folder.','It will be overwritten if you do not move them now.')
    elif os.path.exists(Addonsxmlmd5) and not os.path.exists(Addonsxml):
        xbmcgui.Dialog().ok('[COLOR red]Warning![/COLOR]','addons.xml.md5 has been detected in your work folder.','It will be overwritten if you do not move them now.')
    elif os.path.exists(Addonsxml) and  os.path.exists(Addonsxmlmd5):
        xbmcgui.Dialog().ok('[COLOR red]Warning![/COLOR]','addons.xml and addons.xml.md5 have been detected in your work folder.','They will be overwritten if you do not move them now.')
    else: pass
    Toast('Work Folder: '+fullworkpath)
    xbmcgui.Dialog().ok(Title,'Enter the first add-on ID to include in the addons.xml','')
    vqid = _get_keyboard(heading='[COLOR white]Enter a plugin id[/COLOR]  (i.e. plugin.program.mkiv)')
    if ( not vqid ): return False, 0
    try:
        a=open((os.path.join(ADDONS+'/'+vqid,'addon.xml'))).read()
        b=a.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>').replace('</addon>','</addon>\n</addons>').replace('<?xml version="1.0" encoding="UTF-8"?>','<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>').replace('<!--suppress ALL -->','')
        WriteFile(Addonsxml,str(b))
        pass
    except:
        Toast('Addon does not exist, Please try again')
        sys.exit(0)
    addmore = xbmcgui.Dialog().yesno(Title,'Add another add-on to include in the addons.xml file?')
    while addmore == 1:
        vqid = _get_keyboard(heading='[COLOR white]Enter a plugin id[/COLOR]  (i.e. plugin.program.mkiv)')
        if ( not vqid ): pass
        try:
            a=open((os.path.join(ADDONS+'/'+vqid,'addon.xml'))).read()
            b=a.replace('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>','').replace('<?xml version="1.0" encoding="UTF-8"?>','').replace('<!--suppress ALL -->','')
            c=open(Addonsxml).read()
            d=c.replace('</addons>',str(b)+'\n</addons>')
            f = open(Addonsxml, mode='w')
            f.write(str(d))
            f.close()
        except:
            Toast('Addon does not exist, Please try again')
        addmore = xbmcgui.Dialog().yesno(Title,'Add another add-on to include in the addons.xml file?')
    a=open(Addonsxml).read()
    b=hashlib.md5(str(a)).hexdigest()
    WriteFile(Addonsxmlmd5,str(b))
    xbmcgui.Dialog().ok(Title,'addons.xml & md5 saved to: '+fullworkpath)
    
def md5File():
        file = xbmcgui.Dialog().browseSingle(1,'Select Add-on','files','')
        file2 = xbmc.translatePath(file)
        a=open(file2).read()
        b=hashlib.md5(str(a)).hexdigest()
        output=file2+'.md5'
        WriteFile(output,str(b))
        
def BuildARepo():
    RepoFolder=xbmc.translatePath(os.path.join(fullworkpath,'Repository/'))
    plugins=xbmc.translatePath(os.path.join(RepoFolder,'plugins/'))
    Addonsxml = xbmc.translatePath(os.path.join(RepoFolder,'addons.xml'))
    if not os.path.exists(Addonsxml):
        RepoFiles()
    dp = xbmcgui.DialogProgress()
    dp.create(Title,'')
    a=open(Addonsxml).read()
    match = re.compile('id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(a)
    for id, name, version in match:
        dp.update(0,'[COLOR lime]Adding:[/COLOR] ID: '+id+' Version: '+version)
        PluginFolder=xbmc.translatePath(os.path.join(plugins,id))
        Pluginxml=xbmc.translatePath(os.path.join(PluginFolder,'addon.xml'))
        Pluginicon=xbmc.translatePath(os.path.join(PluginFolder,'icon.png'))
        Pluginchangelog=xbmc.translatePath(os.path.join(PluginFolder,'changelog.txt'))
        PluginZip=xbmc.translatePath(os.path.join(PluginFolder,id+'-'+version))
        addonfolder=xbmc.translatePath(os.path.join(ADDONS,id))
        addonxml=xbmc.translatePath(os.path.join(addonfolder,'addon.xml'))
        addonicon=xbmc.translatePath(os.path.join(addonfolder,'icon.png'))
        addonchangelog=xbmc.translatePath(os.path.join(addonfolder,'changelog.txt'))
        if not os.path.exists(plugins):
            os.makedirs(plugins)
        if not os.path.exists(PluginFolder):
            os.makedirs(PluginFolder)
        try:shutil.copy(addonxml,Pluginxml)
        except: pass
        try: shutil.copy(addonicon,Pluginicon)
        except: pass
        try: shutil.copy(addonchangelog,Pluginchangelog)
        except: pass
        ZipIt(PluginZip,ADDONS,id)
        
        # This next block is necessary for addons like 1channel that have the version and name switched in the addons.xml, 
        # but it screws up others adding folders named as the providername of other addons like this one and BOB.
    '''b=open(Addonsxml).read()
    match = re.compile('id="(.+?)".+?ersion="(.+?)".+?ame="(.+?)"').findall(b)
    for id, name, version in match:
        dp.update(0,'[COLOR lime]Adding:[/COLOR] ID: '+id+' Version: '+version)
        PluginFolder=xbmc.translatePath(os.path.join(plugins,id))
        Pluginxml=xbmc.translatePath(os.path.join(PluginFolder,'addon.xml'))
        Pluginicon=xbmc.translatePath(os.path.join(PluginFolder,'icon.png'))
        Pluginchangelog=xbmc.translatePath(os.path.join(PluginFolder,'changelog.txt'))
        PluginZip=xbmc.translatePath(os.path.join(PluginFolder,id+'-'+version))
        addonfolder=xbmc.translatePath(os.path.join(ADDONS,id))
        addonxml=xbmc.translatePath(os.path.join(addonfolder,'addon.xml'))
        addonicon=xbmc.translatePath(os.path.join(addonfolder,'icon.png'))
        addonchangelog=xbmc.translatePath(os.path.join(addonfolder,'changelog.txt'))
        if not os.path.exists(plugins):
            os.makedirs(plugins)
        if not os.path.exists(PluginFolder):
            os.makedirs(PluginFolder)
        try:shutil.copy(addonxml,Pluginxml)
        except: pass
        try: shutil.copy(addonicon,Pluginicon)
        except: pass
        try: shutil.copy(addonchangelog,Pluginchangelog)
        except: pass
        ZipIt(PluginZip,ADDONS,id)'''
    dp.close()
    xbmcgui.Dialog().ok('[COLOR lime]Your repository is ready![/COLOR]','Saved to: '+RepoFolder)
    
def RepoUpdater():
    RepoFolder=xbmc.translatePath(os.path.join(fullworkpath,'Repository/'))
    plugins=xbmc.translatePath(os.path.join(RepoFolder,'plugins/'))
    Addonsxml = xbmc.translatePath(os.path.join(RepoFolder,'addons.xml'))
    Addonsxmlmd5 = xbmc.translatePath(os.path.join(RepoFolder,'addons.xml.md5'))
    b=open(Addonsxml).read()
    match = re.compile('id="(.+?)".+?ame="(.+?)".+?ersion="(.+?)"').findall(b)
    for id, name, version in match:
        if xbmc.getCondVisibility('System.HasAddon('+id+')'):
            Addon=xbmcaddon.Addon(id)
            installedversion=Addon.getAddonInfo('version')
            if installedversion > version:
                dp = xbmcgui.DialogProgress()
                dp.create(Title,'')
                dp.update(0,'[COLOR lime]Updating:[/COLOR] ID: '+id+' From Version: '+version+' to Version: '+installedversion)
                Toast('[COLOR lime]Updating:[/COLOR] ID: '+id+' From Version: '+version+' to Version: '+installedversion)
                PluginFolder=xbmc.translatePath(os.path.join(plugins,id))
                Pluginxml=xbmc.translatePath(os.path.join(PluginFolder,'addon.xml'))
                Pluginicon=xbmc.translatePath(os.path.join(PluginFolder,'icon.png'))
                Pluginchangelog=xbmc.translatePath(os.path.join(PluginFolder,'changelog.txt'))
                PluginZip=xbmc.translatePath(os.path.join(PluginFolder,id+'-'+version))
                addonfolder=xbmc.translatePath(os.path.join(ADDONS,id))
                addonxml=xbmc.translatePath(os.path.join(addonfolder,'addon.xml'))
                addonicon=xbmc.translatePath(os.path.join(addonfolder,'icon.png'))
                addonchangelog=xbmc.translatePath(os.path.join(addonfolder,'changelog.txt'))
                if not os.path.exists(plugins):
                    os.makedirs(plugins)
                if not os.path.exists(PluginFolder):
                    os.makedirs(PluginFolder)
                try:shutil.copy(addonxml,Pluginxml)
                except: pass
                try: shutil.copy(addonicon,Pluginicon)
                except: pass
                try: shutil.copy(addonchangelog,Pluginchangelog)
                except: pass
                ZipIt(PluginZip,ADDONS,id)
                ReplaceText(Addonsxml,'version="'+version+'" provider', 'version="'+installedversion+'" provider' )
    a=open(Addonsxml).read()
    b=hashlib.md5(str(a)).hexdigest()
    WriteFile(Addonsxmlmd5,str(b))
    xbmcgui.Dialog().ok(Title,'[COLOR white]Repository update complete[/COLOR]')
    
def RemoveInstaller():
    try:
        shutil.rmtree(Installer)
    except: pass

def RepoAddon():
    dialog = xbmcgui.Dialog()
    dialog.ok('Step 1 of 7: Entering an ID for your repository','The id is your addons xbmc ID... i.e. repository.<your_id_here>','')
    id = _get_keyboard(heading="Enter an id for your repository" )
    if ( not id ): return False, 0
    id = urllib.unquote_plus(id).replace(' ','_').replace('!','').replace('@','').replace('#','').replace('$','').replace('%','').replace('^','').replace('&','').replace('*','').replace('(','').replace(')','').replace('/','').replace("'","\'")
    dialog.ok('Step 2 of 7: Entering an name for your wizard','The name is your addons name... i.e. CamC\'s Repository''','')
    name = _get_keyboard(heading="Enter an id for your wizard" )
    if ( not name ): return False, 0
    name=name.replace("'", "\'")
    dialog.ok('Step 3 of 7: Entering a provider name','This is your name or handle','')
    provider = _get_keyboard(heading="Enter the provider name for your repo" )
    if ( not provider ): return False, 0
    provider=provider.replace("'", "\'")
    choice = xbmcgui.Dialog().yesno('Step 4 of 7: Your addons.xml file URL', 'For your URL to your addons.xml file.', 'Does your link start with http:// or https://?','All links and are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"
    xmllink = _get_keyboard(default=protocol, heading="Enter your addons.xml link" )
    if ( not xmllink ): return False, 0
    choice = xbmcgui.Dialog().yesno('Step 5 of 7: Your addons.xml.md5 file URL', 'For your URL to your addons.xml.md5 file.', 'Does your link start with http:// or https://?','All links and are CaSe SeNsItIvE!', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"
    md5link = _get_keyboard(default=protocol, heading="Enter your addons.xml.md5 link" )
    if ( not md5link ): return False, 0
    choice = xbmcgui.Dialog().yesno('Step 6 of 7: Your plugins folder link', 'For your URL to your plugins folder.', 'Does your link start with http:// or https://?','It probably ends with plugins/', nolabel='HTTP://',yeslabel='HTTPS://')
    if choice == 0:
        protocol="http://"
    elif choice == 1:
        protocol="https://"
    pluginslink = _get_keyboard(default=protocol, heading="Enter your plugins folder link" )
    if ( not pluginslink ): return False, 0
    workfolder=xbmc.translatePath(os.path.join(fullworkpath,'repository.'+id))
    addonxml=xbmc.translatePath(os.path.join(workfolder,'addon.xml'))
    iconpng=xbmc.translatePath(os.path.join(workfolder,'icon.png'))
    if not os.path.exists(workfolder): os.makedirs(workfolder)
    if xbmcgui.Dialog().yesno('Step 7 of 7: Your Icon Image','Would you like to select an image to represent your repository?'):
        icon = xbmcgui.Dialog().browseMultiple(1,'Add icon image','files','.png|.jpg|.jpeg')
        if( not icon ): pass
        try:
            for file in icon:
                file = xbmc.translatePath(file)
                shutil.copy(file,iconpng)
        except: pass
    else: pass
    WriteFile(addonxml,'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addon id="repository.'+id+'" name="'+name+'" version="1.0" provider-name="'+provider+'">\n	<extension point="xbmc.addon.repository" name="'+name+'">\n		<info compressed="false">'+xmllink+'</info>\n		<checksum>'+md5link+'</checksum>\n		<datadir zip="true">'+pluginslink+'</datadir>\n	</extension>\n	<extension point="xbmc.addon.metadata">\n		<summary>'+id+'</summary>\n		<description>'+name+'</description>\n		<platform>all</platform>\n	</extension>\n</addon>')
    ZipIt(workfolder,fullworkpath,'repository.'+id)
    shutil.rmtree(workfolder)
    dialog.ok(Title,'[COLOR white]Your repository add-on is finished and saved to: [/COLOR][COLOR dodgerblue]'+fullworkpath+'[/COLOR]')
    
def ShowBusy():
    xbmc.executebuiltin('Dialog.Close(busydialog)')

def CloseBusy():
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    
def LockXbmc():
    xbmcgui.lock()
    
def UnlockXbmc():
    xbmcgui.unlock()
    
def ShowWindowId():
    window = xbmcgui.getCurrentWindowId()
    xbmcgui.Dialog().ok(Title,str(window))
    
def GetWindowID():
    window = xbmcgui.getCurrentWindowId()
    window =str(window)
    return window

def StopPlayer():
    if xbmc.Player().isPlaying() == 'True':
        xbmc.Player().stop()
        
def B64Encode():
    import base64
    input=xbmcgui.Dialog().browse(1,'Choose file to encode','files')
    input=xbmc.translatePath(input)
    a=open(input).read()
    b=base64.b64encode(str(a))
    c=PathLeaf(input).replace('(decoded)','').replace('(encoded)','')
    d=str(c)+'(encoded)'
    output=xbmc.translatePath(os.path.join(fullworkpath,d))
    WriteFile(output,str(b))
    xbmcgui.Dialog().ok(Title,'Your encoded file is saved as: '+output)
 
    
def B64Decode():
    import base64
    input=xbmcgui.Dialog().browse(1,'Choose file to decode','files')
    input=xbmc.translatePath(input)
    a=open(input).read()
    c=PathLeaf(input).replace('(encoded)','').replace('(decoded)','')
    d=str(c)+'(decoded)'
    output=xbmc.translatePath(os.path.join(fullworkpath,d))
    try:
        b=base64.b64decode(str(a))
        WriteFile(output,str(b))
    except: pass
    try:
        b=base64.urlsafe_b64decode(a)
        WriteFile(output,str(b))
    except: 
        b=base64.standard_b64decode(a)
        WriteFile(output,str(b))
        
    xbmcgui.Dialog().ok(Title,'Your decoded file is saved as: '+output)
    
def B64View():
    import base64
    input=xbmcgui.Dialog().browse(1,'Choose file to decode','files')
    input=xbmc.translatePath(input)
    a=open(input).read()
    try:
        b=base64.b64decode(str(a))
        TextBoxes(Title+' - Base64 Decode Viewer',b)
    except: pass
    try:
        b=base64.urlsafe_b64decode(a)
        TextBoxes(Title+' - Base64 Decode Viewer',b)
    except:  
        b=base64.standard_b64decode(a)
        TextBoxes(Title+' - Base64 Decode Viewer',b)
    

def PathLeaf(path):
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
    #i.e. for tuple below
'''>>> paths = ['a/b/c/', 'a/b/c', '\\a\\b\\c', '\\a\\b\\c\\', 'a\\b\\c', 'a/b/../../a/b/c/', 'a/b/../../a/b/c']
   >>> [PathLeaf(path) for path in paths]
   ['c', 'c', 'c', 'c', 'c', 'c', 'c']'''

def PathLeafHeads(path):
    import ntpath
    head, tail = ntpath.split(path)
    return head or ntpath.basename(tail)
