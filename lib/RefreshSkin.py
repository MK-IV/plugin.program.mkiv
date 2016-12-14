import xbmc
import sys

try:
    xbmc.executebuiltin('ReloadSkin()')
except: 
    sys.exit(0)
