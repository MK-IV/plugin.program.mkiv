import os,xbmc

addon_path = xbmc.translatePath(os.path.join('special://home/addons', 'repository.mkiv'))
addonxml=xbmc.translatePath(os.path.join('special://home/addons', 'repository.mkiv','addon.xml'))


Repo='''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="repository.mkiv" name="MK-IV Repository" version="1.0" provider-name="CamC">
	<extension point="xbmc.addon.repository" name="MK-IV Repository">
		<info compressed="false">https://github.com/MK-IV/Dependencies/raw/master/plugins/addons.xml</info>
		<checksum>https://github.com/MK-IV/Dependencies/raw/master/plugins/addons.xml.md5</checksum>
		<datadir zip="true">https://github.com/MK-IV/Dependencies/raw/master/plugins</datadir>
	</extension>
	<extension point="xbmc.addon.metadata">
		<summary>MK-IV</summary>
		<description>MK-IV Repository</description>
		<platform>all</platform>
	</extension>
</addon>
'''




def InstallRepo():
    if os.path.exists(addon_path) == False:
        os.makedirs(addon_path)
    if os.path.exists(addonxml) == False:
        f = open(addonxml, mode='w')
        f.write(Repo)
        f.close()

    xbmc.executebuiltin('UpdateLocalAddons') 
    xbmc.executebuiltin("UpdateAddonRepos")
