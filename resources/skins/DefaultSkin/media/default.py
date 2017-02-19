import xbmcaddon, xbmcgui, xbmc, os, sys, urllib, urllib2, xbmcplugin, re, extract, downloader, time, sqlite3


USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
addon_id="plugin.program.testwizard"
ADDON=xbmcaddon.Addon(id=addon_id)
version=ADDON.getAddonInfo('version')
AddonTitle="Test Wizard"
proname="CamC SandBox"
pointerurl="https://mk-iv.github.io/Pointer"
dialog=xbmcgui.Dialog()
HOME=xbmc.translatePath('special://home/')
dp=xbmcgui.DialogProgress()
FANART=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png')) 
Updater=xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'updater.py'))
VERSION="1.0.0"
Addons26=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons26.db'))
Addons27=xbmc.translatePath(os.path.join('special://home/userdata/Database/','Addons27.db'))
EXCLUDES=['kodi.log',addon_id,Addons26,Addons27,'script.module.addon.common','autoexec.py','service.xbmc.versioncheck','metadata.tvdb.com','metadata.common.imdb.com']
phoenix=xbmc.translatePath(os.path.join('special://home/addons/','plugin.video.phstreams'))


def Index():
        try:
            link = Open_Url(pointerurl).replace('\n','').replace('\r','')
            match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ersion="(.+?)"').findall(link)
            for name,url,iconimage,fanart,description in match:
                addDir(name,url,1,iconimage,fanart,description,version)
        except:
            link = Open_Url(pointerurl).replace('\n','').replace('\r','')
            match = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
            for name,url,iconimage,fanart,description in match:
                addDir(name,url,1,iconimage,fanart,description,999)

def addDir(name,url,mode,iconimage,fanart,description,version):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&version="+str(version)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

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


def Open_Url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
def Wizard(name,url,description,version):
    if  os.path.exists(phoenix):
        choice = xbmcgui.Dialog().yesno(AddonTitle, 'It is recommended that you perform a Fresh Start before installing.', '','', nolabel='SKIP',yeslabel='FRESH START')
        if choice == 0:
            pass

        elif choice == 1:
            FRESHSTART()
    else:
        pass
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()        
    dp.create(AddonTitle,"Downloading "+name+"... ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    '''xbmc_version=xbmc.getInfoLabel("System.BuildVersion")
    version=float(xbmc_version[:4])
    if version >= 17.0 and version <= 17.9:
        dp.update(0,"Downloading "+name+"...[COLOR lime]DONE[/COLOR]","Applying Patch...")
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
        time.sleep(2)
        try: 
            extract.all(reqzip,ADDONS, dp) 
        except BaseException as e:
            pass
        dp.update(0,"Applying Patch...[COLOR lime]DONE[/COLOR]","Extracting...")
        pass
    else:'''
    dp.update(0,"Downloading "+name+"...[COLOR lime]DONE[/COLOR]", "Extracting...")
    try: 
        '''addonfolder = xbmc.translatePath(os.path.join('special://','home'))
        path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
        lib=os.path.join(path, name+'.zip')
        time.sleep(.5)'''
        extract.all(lib,addonfolder,dp)
    except BaseException as e:
        pass       
    time.sleep(.5)
    try:
       os.remove(lib)
    except:
       pass
    '''if version >= 17.0 and version <= 17.9:
        dp.update(0,"Extracting...[COLOR lime]DONE[/COLOR]", "Updating Krypton Database")
        conn = sqlite3.connect(Addons26)
        cursor = conn.cursor()

        sql = """
        UPDATE installed 
        SET enabled = '1' 
        WHERE enabled = '0'
        """
        cursor.execute(sql)
        conn.commit()
        time.sleep(2)
        xbmc.executebuiltin('UpdateLocalAddons')
        pass
    else: pass'''
    dialog.ok("Your Setup Is Almost Finished...", 'The application will now close.', '', 'On your next start please leave it sit for a minute to allow add-ons to update.')
    KillKodi()
 
 
def Crash():  #Exhaust resources to crash the interpreter *** Creates a crash log but good for a last resort.
        sys.setrecursionlimit(1<<30)
        f = lambda f:f(f)
        f(f)
 
def KillKodi():
    myplatform = platform()
    xbmc.log("Platform: " + str(myplatform))
    if myplatform == 'osx': # OSX
        xbmc.log('############   try osx force close  #################')
        try: os.system('killall -9 XBMC')
        except: pass
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
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
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
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
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
        try: os.system('sudo initctl stop xbmc')
        except: pass
        try: os._exit(0)
        except: pass    
        try: sys.exit(2)
        except: pass
        Crash()
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close the MC [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

def TriggerMigration():
    f = open(Addons27, mode='w')
    f.write('Wiped')
    f.close()
    os.remove(Addons27)
    
def FRESHSTART():
    if xbmcgui.Dialog().yesno("[COLOR=red]Are You Sure?[/COLOR]", 'Last chance...', '', '', yeslabel='[COLOR lime]Yes, Fresh Start[/COLOR]',nolabel='[COLOR red]No[/COLOR]'):
        dp.create(AddonTitle,"Counting files",'', '')
        HOME=xbmc.translatePath('special://home/')
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
                    dp.update(int(progress),"Deleting:",'[COLOR dodgerblue]%s[/COLOR]'%file)#
                for name in files:
                    try:
                        os.remove(os.path.join(root,name))
                        os.rmdir(os.path.join(root,name))
                    except: pass

                for name in dirs:
                    try: os.rmdir(os.path.join(root,name)); os.rmdir(root)
                    except: pass
            REMOVE_EMPTY_FOLDERS()
            REMOVE_EMPTY_FOLDERS()
            REMOVE_EMPTY_FOLDERS()
            REMOVE_EMPTY_FOLDERS()
            REMOVE_EMPTY_FOLDERS()
            REMOVE_EMPTY_FOLDERS()
            REMOVE_EMPTY_FOLDERS()
            time.sleep(.5)
            dp.close()
            dialog = xbmcgui.Dialog()
            dialog.ok(AddonTitle,'Fresh Start Successful','','The MC will now close')
            KillKodi()
            xbmc.executebuiltin('Quit')
        except: pass
    else: return

def REMOVE_EMPTY_FOLDERS():
    empty_count = 0
    used_count = 0
    for curdir, subdirs, files in os.walk(HOME):
        if len(subdirs) == 0 and len(files) == 0: #check for empty directories. len(files) == 0 may be overkill
            empty_count += 1 #increment empty_count
            os.rmdir(curdir) #delete the directory
        elif len(subdirs) > 0 and len(files) > 0: #check for used directories
            used_count += 1 #increment used_count

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
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


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
        
        
print str(AddonTitle)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


if mode==None or url==None or len(url)<1:
        xbmc.log('-------------------------------'+AddonTitle+' Started-------------------------------------')
        if os.path.exists(Updater):
            import updater 
            updater.UpdateCheck(AddonTitle, addon_id)
            pass
        else: pass
        Index()
elif mode==1: Wizard(name,url,description,version)        
elif mode==2: FRESHSTART()

        
xbmcplugin.endOfDirectory(int(sys.argv[1]))