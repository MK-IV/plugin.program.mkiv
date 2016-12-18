import urllib2, urllib
import xbmc, xbmcgui, xbmcplugin
import re
import sys
AddonFolder=xbmc.translatePath('special://home/addons/plugin.program.mkiv')
Title="[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
ICON=AddonFolder+'icon.png'
FANART=AddonFolder+'fanart.jpg'
BASEURL='http://openloadmovies.net/'
ART='http://openloadmovies.net/wp-content/uploads/2016/12/openload-movies.png'

def MK4Video():
    Menu('[B][COLOR dodgerblue]A[/COLOR][COLOR white]ll Movies[/COLOR][/B]',BASEURL+'movies/',91,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]T[/COLOR][COLOR white]rending[/COLOR][/B]',BASEURL+'trending/?get=movies',91,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]G[/COLOR][COLOR white]enres[/COLOR][/B]',BASEURL,89,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]R[/COLOR][COLOR white]elease Year[/COLOR][/B]',BASEURL,90,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]I[/COLOR][COLOR white]MDB Top Movies[/COLOR][/B]',BASEURL,93,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]T[/COLOR][COLOR white]V Shows[/COLOR][/B]',BASEURL+'tvseries/',94,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]T[/COLOR][COLOR white]rending TV[/COLOR][/B]',BASEURL+'/trending/?get=tv',94,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]I[/COLOR][COLOR white]MDB Top TV[/COLOR][/B]',BASEURL+'top-imdb/',88,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]S[/COLOR][COLOR white]earch[/COLOR][/B]','url',92,ART,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GetGenres(url):
    link = OPEN_URL(url)
    match = re.compile('<ul class="genres scrolling">(.+?)</ul>',re.DOTALL).findall(link)
    match2 = re.compile('<a href="(.+?)" >(.+?)</a>',re.DOTALL).findall(str(match))
    for url,name in match2:
            name = name.replace('amp;','')
            Menu('[B][COLOR cornflowerblue]%s[/COLOR][/B]' %name,url,91,ICON,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GetYears(url):
    link = OPEN_URL(url)
    match = re.compile('<ul class="year scrolling">(.+?)</ul>',re.DOTALL).findall(link)
    match2 = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(match))
    for url,name in match2:
            Menu('[B][COLOR cornflowerblue]%s[/COLOR][/B]' %name,url,91,ICON,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GetContent(url):
    link = OPEN_URL(url)
    match = re.compile('<article id=".+?" class="item movies".+?<a href="(.+?)"><img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(link)
    for url,icon,name in match:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8211;','-')
            Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,icon,FANART,'')
    np = re.compile('class="current".+?<a href=\'(.+?)\'',re.DOTALL).findall(link)
    for url in np:
                    Menu('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,91,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GetImdb(url):
    link = OPEN_URL(url)
    match = re.compile('</i> Movies</h3>(.+?)<div class="top-imdb-list">',re.DOTALL).findall(link)
    match2 = re.compile('<div class="image">.+?<img src="(.+?)" /></a>.+?<a href="(.+?)">(.+?)</a></div>',re.DOTALL).findall(str(match))
    for icon,url,name in match2:
            icon = icon.replace('w90','w300_and_h450_bestv2')
            name = name.replace('&#8211;','-').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8217;','\'')
            Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GetTvImdb(url):
    link = OPEN_URL(url)
    match = re.compile('TV Shows</h3>(.+?)<footer class="main">',re.DOTALL).findall(link)
    match2 = re.compile('<img src="(.+?)".+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
    for icon,url,name in match2:
            icon = icon.replace('w90','w300_and_h450_bestv2')
            name = name.replace('&#8217;','').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#039;','\'')
            Menu('[B][COLOR cornflowerblue]%s[/COLOR][/B]' %name,url,95,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def GetTV(url):
    link = OPEN_URL(url)
    match = re.compile('<article id=".+?" class="item tvshows".+?<a href="(.+?)"><img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(link)
    for url,icon,name in match:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'')
            Menu('[B][COLOR white]%s[/COLOR][/B]' %name,url,95,icon,FANART,'')
    np = re.compile('class="current".+?<a href=\'(.+?)\'',re.DOTALL).findall(link)
    for url in np:
                    Menu('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,94,ART + 'nextpage.jpg',FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def GetShowContent(url):
    link = OPEN_URL(url)
    match = re.compile('<div class="imagen">.+?<img src="(.+?)"></a>.+?<div class="numerando">(.+?)</div>.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
    for icon,name1,url,name2 in match:
            name = name1+'   '+name2
            name = name.replace('&#039;','\'')
            Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,ICON,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')

def Search():
        keyb = xbmc.Keyboard('', 'Search')
        keyb.doModal()
        if (keyb.isConfirmed()):
                search = keyb.getText().replace(' ','+')
                url = BASEURL + '/?s=' + search
                SearchRes(url)
    
def SearchRes(url):
    link = OPEN_URL(url)
    match = re.compile('<div class="result-item">.+?<a href="(.+?)">.+?<img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(link)
    for url,icon,name in match:
            name = name.replace('&#8217;','').replace('#038;','')
            icon = icon.replace('w90','w300_and_h450_bestv2')
            if '/tvseries/' in url:
                Menu('[B][COLOR white]%s[/COLOR][/B]' %name,url,95,icon,FANART,'')    
            else:
                Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,icon,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')  

def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Menu(name,url,mode,ICON,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&ICON="+urllib.quote_plus(ICON)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=ICON)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Play(name,url,mode,ICON,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&ICON="+urllib.quote_plus(ICON)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=ICON)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def GetPlayerCore(): 
    try: 
        PlayerMethod=getSet("core-player") 
        if   (PlayerMethod=='DVDPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_DVDPLAYER 
        elif (PlayerMethod=='MPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_MPLAYER 
        elif (PlayerMethod=='PAPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_PAPLAYER 
        else: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    except: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    return PlayerMeth 
    return True 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    

def resolve(name,url,description):
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    link = OPEN_URL(url)
    url = re.compile('file:"(.+?)"',re.DOTALL).findall(link)[0]
    title = xbmc.getInfoLabel('listitem.title')
    if title == '': title = xbmc.getInfoLabel('listitem.label')    
    icon = xbmc.getInfoLabel('listitem.icon')
    item = xbmcgui.ListItem(path=url, iconImage=icon, thumbnailImage=icon)
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    play=xbmc.Player(GetPlayerCore())
    play.play(url,item)
    '''while xbmc.getCondVisibility('Window.IsVisible(12005)'):
        time.sleep(.5)
    xbmc.Player().stop()'''
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


	

