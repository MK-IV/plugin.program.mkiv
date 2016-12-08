import xbmc
import os
import downloader
import time
import shutil
import extract
import mk4

Addons=xbmc.translatePath(os.path.join('special://home/','addons/'))
Requests=xbmc.translatePath(os.path.join('special://home/addons/','script.module.requests'))
path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
reqzip=os.path.join(path,'requests.zip')
try:
    os.remove(reqzip)
except:
    pass
downloader.download('https://github.com/MK-IV/Dependencies/raw/master/requests.zip', reqzip)
time.sleep(.5)
try:
    shutil.rmtree(Requests)
except: pass
time.sleep(2)
try: 
    extract.all(reqzip,Addons) 
except BaseException as e:
    pass
        
mk4.EnableAll() 
