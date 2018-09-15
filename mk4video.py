import urllib2, urllib
import xbmc, xbmcgui, xbmcplugin
import re
import sys
import os
#from mk4 import Toast
AddonFolder=xbmc.translatePath('special://home/addons/plugin.program.mkiv')
Title="[COLOR red]MK-IV[/COLOR] [COLOR deepskyblue]Wizard[/COLOR]"
ICON=AddonFolder+'icon.png'
FANART=AddonFolder+'fanart.jpg'
BASEURL='http://openloadmovies.net/'
ART='http://openloadmovies.net/wp-content/uploads/2016/12/openload-movies.png'
USERDATA_PATH =xbmc.translatePath('special://home/userdata/addon_data')
ADDON_DATA = xbmc.translatePath(os.path.join(USERDATA_PATH,'plugin.program.mkiv'))
favourites = xbmc.translatePath(os.path.join(ADDON_DATA,'favourites'))
if os.path.exists(favourites):
    FAV = open(favourites).read()
else:
    FAV = []
dp = xbmcgui.DialogProgress()
addon_handle = int(sys.argv[1])
List = []
temp_file = xbmc.translatePath(os.path.join(AddonFolder,'Temp.txt'))

def MK4Video():
    Menu('[B][COLOR dodgerblue]Mo[/COLOR][COLOR white]vies[/COLOR][/B]',BASEURL+'movies/',109,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]TV[/COLOR][COLOR white] Shows[/COLOR][/B]',BASEURL+'movies/',110,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]To[/COLOR][COLOR white]p Rated[/COLOR][/B]',BASEURL+'ratings/',88,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Se[/COLOR][COLOR white]arch[/COLOR][/B]','url',92,ART,FANART,'')
    Play('[B][COLOR dodgerblue]Fa[/COLOR][COLOR white]vourites[/COLOR][/B]','url',108,ART,FANART,'')    

def Movies():
    Menu('[B][COLOR dodgerblue]Al[/COLOR][COLOR white]l Movies[/COLOR][/B]',BASEURL+'movies/',91,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Fe[/COLOR][COLOR white]atured Movies[/COLOR][/B]',BASEURL+'genre/featured/',91,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Tr[/COLOR][COLOR white]ending[/COLOR][/B]',BASEURL+'trending/?get=movies',91,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Ge[/COLOR][COLOR white]nres[/COLOR][/B]',BASEURL,89,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Re[/COLOR][COLOR white]lease Year[/COLOR][/B]',BASEURL,90,ART,FANART,'')
    #Menu('[B][COLOR dodgerblue]IM[/COLOR][COLOR white]DB Top Movies[/COLOR][/B]',BASEURL,93,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Se[/COLOR][COLOR white]arch[/COLOR][/B]','url',92,ART,FANART,'')
    Play('[B][COLOR dodgerblue]Fa[/COLOR][COLOR white]vourites[/COLOR][/B]','url',108,ART,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def TV():
    Menu('[B][COLOR dodgerblue]TV[/COLOR][COLOR white] Shows[/COLOR][/B]',BASEURL+'tvseries/',94,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Tr[/COLOR][COLOR white]ending TV[/COLOR][/B]',BASEURL+'/trending/?get=tv',94,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]IM[/COLOR][COLOR white]DB Top TV[/COLOR][/B]',BASEURL+'top-imdb/',88,ART,FANART,'')
    Menu('[B][COLOR dodgerblue]Se[/COLOR][COLOR white]arch[/COLOR][/B]','url',92,ART,FANART,'')
    Play('[B][COLOR dodgerblue]Fa[/COLOR][COLOR white]vourites[/COLOR][/B]','url',108,ART,FANART,'')
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def GetGenres(url):
    #try:
        link = OPEN_URL(url)
        match = re.compile('<ul class="genres scrolling">(.+?)</ul>',re.DOTALL).findall(link)
        match2 = re.compile('<a href="(.+?)" >(.+?)</a>',re.DOTALL).findall(str(match))
        for url,name in match2:
            name = name.replace('amp;','')
            Menu('[B][COLOR white]%s[/COLOR][/B]' %name,url,91,ICON,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
     #   Toast('[COLOR white]Please try again later[/COLOR]')
      #  sys.exit(0)

def GetYears(url):
    #try:
        link = OPEN_URL(url)
        match = re.compile('<ul class="year scrolling">(.+?)</ul>',re.DOTALL).findall(link)
        match2 = re.compile('<li><a href="(.+?)">(.+?)</a></li>',re.DOTALL).findall(str(match))
        for url,name in match2:
            Menu('[B][COLOR white]%s[/COLOR][/B]' %name,url,91,ICON,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
     #   Toast('[COLOR white]Please try again later[/COLOR]')
      #  sys.exit(0)

def GetContent(url):
   # try:
        link = OPEN_URL(url)
        match = re.compile('<article id=".+?" class="item movies".+?<a href="(.+?)"><img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(link)
        for url,icon,name in match:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8211;','-')
            Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,icon,FANART,'')
        np = re.compile('class="current".+?<a href=\'(.+?)\'',re.DOTALL).findall(link)
        for url in np:
                    Menu('[B][COLOR dodgerblue]N[/COLOR][COLOR white]ext Page>>>[/COLOR][/B]',url,91,ART,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
       # Toast('[COLOR white]Please try again later[/COLOR]')
       # sys.exit(0)

def GetImdb(url):
    #try:
        link = OPEN_URL(url)
        match = re.compile('</i> Movies</h3>(.+?)<div class="top-imdb-list">',re.DOTALL).findall(link)
        match2 = re.compile('<div class="image">.+?<img src="(.+?)" /></a>.+?<a href="(.+?)">(.+?)</a></div>',re.DOTALL).findall(str(match))
        for icon,url,name in match2:
            icon = icon.replace('w90','w300_and_h450_bestv2')
            name = name.replace('&#8211;','-').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#8217;','\'')
            Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,icon,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
     #   Toast('[COLOR white]Please try again later[/COLOR]')
      #  sys.exit(0)

def GetTvImdb(url):
    #try:
        link = OPEN_URL(url)
        match = re.compile('TV Shows</h3>(.+?)<footer class="main">',re.DOTALL).findall(link)
        match2 = re.compile('<img src="(.+?)".+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(str(match))
        for icon,url,name in match2:
                icon = icon.replace('w90','w300_and_h450_bestv2')
                name = name.replace('&#8217;','').replace('#038;','').replace('\\xc3\\xa9','e').replace('&#039;','\'')
                Menu('[B][COLOR white]%s[/COLOR][/B]' %name,url,95,icon,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
     #   Toast('[COLOR white]Please try again later[/COLOR]')
      #  sys.exit(0)
    
def GetTV(url):
    #try:
        link = OPEN_URL(url)
        match = re.compile('<article id=".+?" class="item tvshows".+?<a href="(.+?)"><img src="(.+?)" alt="(.+?)"',re.DOTALL).findall(link)
        for url,icon,name in match:
            icon = icon.replace('w185','w300_and_h450_bestv2')
            name = name.replace('&#8217;','\'')
            Menu('[B][COLOR white]%s[/COLOR][/B]' %name,url,95,icon,FANART,'')
        np = re.compile('class="current".+?<a href=\'(.+?)\'',re.DOTALL).findall(link)
        for url in np:
                    Menu('[B][COLOR blue]Next Page>>>[/COLOR][/B]',url,94,ART,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
     #   Toast('[COLOR white]Please try again later[/COLOR]')
      #  sys.exit(0)

def GetShowContent(url):
    #try:
        link = OPEN_URL(url)
        match = re.compile('<div class="imagen">.+?<img src="(.+?)"></a>.+?<div class="numerando">(.+?)</div>.+?<a href="(.+?)">(.+?)</a>',re.DOTALL).findall(link)
        for icon,name1,url,name2 in match:
            name = name1+'   '+name2
            name = name.replace('&#039;','\'')
            Play('[B][COLOR white]%s[/COLOR][/B]' %name,url,96,icon,FANART,'')
        xbmc.executebuiltin('Container.SetViewMode(50)')
    #except:
     #   Toast('[COLOR white]Please try again later[/COLOR]')
      #  sys.exit(0)

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
    
def Menu(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        '''contextMenu = []
        if name in FAV:
            contextMenu.append(('Remove from MK-IV Favorites', 'XBMC.RunPlugin(%s?mode=107&name=%s)'
                            % (sys.argv[0], urllib.quote_plus(name))))
        else:
            fav_mode=str(mode)
            contextMenu.append(('Add to MK-IV Video Favorites',
                                'XBMC.RunPlugin('+sys.argv[0]+'?mode=106&name='+name+'&url=%'+url+'iconimage='+iconimage+'&fanart='+fanart+'&fav_mode='+fav_mode+')'))
                                #% (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url),
                                #urllib.quote_plus(iconimage), urllib.quote_plus(fanart))))
            liz.addContextMenuItems(contextMenu)'''
        return ok
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def Play(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        '''if showcontext:
            contextMenu = []
            if name in FAV:
                contextMenu.append(('Remove from MK-IV Favorites', 'XBMC.RunPlugin(%s?mode=107&name=%s)'
                                % (sys.argv[0], urllib.quote_plus(name))))
            else:
                name=urllib.quote_plus(name)
                url=urllib.quote_plus(url)
                iconimage=urllib.quote_plus(iconimage)
                urllib.quote_plus(fanart)
                fav_mode=str(mode)
                
                contextMenu.append(('Add to MK-IV Video Favorites',
                                    'XBMC.RunPlugin('+sys.argv[0]+'?mode=106&name='+name+'&url=%'+url+'iconimage='+iconimage+'&fanart='+fanart+'&fav_mode='+fav_mode+')'))
                                   # % (sys.argv[0], urllib.quote_plus(name), urllib.quote_plus(url),
                                   # urllib.quote_plus(iconimage), urllib.quote_plus(fanart))))
            contextMenu.append(('Queue Item', 'RunPlugin(%s?mode=105)' % sys.argv[0]))
            liz.addContextMenuItems(contextMenu)'''
        ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
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
    

def resolve(name,url,iconimage,description):
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    OPEN = OPEN_URL(url)
    url = re.compile('file:"(.+?)"',re.DOTALL).findall(OPEN)[0]     
    try: 
            liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
            liz.setInfo(type='Video', infoLabels={'Title': name, 'Plot': description})
            liz.setProperty('IsPlayable','true')
            xbmc.Player().play(play,liz)
    except:
        play=xbmc.Player(GetPlayerCore())
        play.play(url,liz)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

'''def QueueItem():
    return xbmc.executebuiltin('Action(Queue)')

def addFavorite(name, url, iconimage, fanart, fav_mode):
    import json
    favList = []
    try:
        # seems that after
        name = name.encode('utf-8', 'ignore')
    except:
        pass
    if os.path.exists(favourites) == False:
        favList.append((name, url, iconimage, fanart, fav_mode))
        a = open(favourites, "w")
        a.write(json.dumps(favList))
        a.close()
    else:
        a = open(favourites).read()
        data = json.loads(a)
        data.append((name, url, iconimage, fanart, fav_mode))
        b = open(favourites, "w")
        b.write(json.dumps(data))
        b.close()
    xbmc.executebuiltin('Container.Refresh')

def GetFavourites():
    import json
    if not os.path.exists(favourites):
        favList = []
        a = open(favourites, "w")
        a.write(json.dumps(favList))
        a.close()
    else:
        items = json.loads(open(favourites).read())
        for i in items:
            name = i[0]
            url = i[1]
            iconimage = i[2]
            if iconimage == '': iconimage=ICON
            try:
                fanart = i[3]
            except:
                fanart = FANART
            fav_mode = i[4]
            mode=fav_mode
            description='description'
            Menu(name, url, mode, iconimage, fanart, description)


def rmFavorite(name, url, iconimage, fanart, mode, playlist=None, regexs=None):
    import json
    data = json.loads(open(favourites).read())
    for index in range(len(data)):
        if data[index][0] == name:
            del data[index]
            b = open(favourites, "w")
            b.write(json.dumps(data))
            b.close()
            break
    xbmc.executebuiltin('Container.Refresh')'''


'''    // format:
    // <favourite name="Cool Video" thumb="foo.jpg">PlayMedia(c:\videos\cool_video.avi)</favourite>
    // <favourite name="My Album" thumb="bar.tbn">ActivateWindow(MyMusic,c:\music\my album)</favourite>
    // <favourite name="Apple Movie Trailers" thumb="path_to_thumb.png">RunScript(special://xbmc/scripts/apple movie trailers/default.py)</favourite'''
    
