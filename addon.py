'''
    NPO Start
    ~~~~~~~
    An XBMC addon for watching uzg 
    :license: GPLv3, see LICENSE.txt for more details.
    NPO Start / uzg = Made by Bas Magre (Opvolger)
    
'''
import xbmcaddon
import xbmcgui
import xbmcplugin
import inputstreamhelper
import sys

from resources.lib.uzg import Uzg
from resources.lib.npoapiclasses import AddonItems

from urllib.parse import urlencode
from urllib.parse import parse_qsl


PROTOCOL = 'mpd'
DRM = 'com.widevine.alpha'
#DRM = 'widevine'
PLUGIN_NAME = 'uzg'
PLUGIN_ID = 'plugin.video.uzg'

uzg = Uzg()

_url = sys.argv[0]
_handle = int(sys.argv[1])
_addon = xbmcaddon.Addon()

# het in elkaar klussen van een url welke weer gebruikt word bij router
def getUrl(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def setMediaView():
    # juiste skin selecteren alleen voor confluence maar die gebruik ik prive nog steeds
    try:
        skinTheme = xbmc.getSkinDir().lower()
        if 'onfluence' in skinTheme:
            xbmc.executebuiltin('Container.SetViewMode(504)')
    except:
        pass

def homeMenu():
    xbmcplugin.setPluginCategory(_handle, 'NPO Start')
    # for category in ['Live kanalen', 'Zoeken']:
    for category in ['Live kanalen', 'Zoeken', 'Alle programmas']:
        list_item = xbmcgui.ListItem(label=category)
        url = getUrl(action=category, guid=None, productId=None, slug=None)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)

def addItems(addonitems: list[AddonItems], action):
    xbmcplugin.setPluginCategory(_handle, action)
    if addonitems:
        if addonitems[0].kodiInfo.isPlayable:
            # hack do not sort live-streams
            if not addonitems[0].kodiInfo.label == 'NPO1':
                xbmcplugin.setContent(_handle, 'videos')
                xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_DATE)
                xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
                setMediaView()
        for addonitem in addonitems:
            # weergave video's die kan direct onder een franchise zijn of vanaf een sub-level "seasons"
            list_item = xbmcgui.ListItem(label=addonitem.kodiInfo.label)
            list_item.setInfo('video', addonitem.kodiInfo.video)
            list_item.setArt(addonitem.kodiInfo.art)
            if addonitem.kodiInfo.isPlayable:
                list_item.setProperty('IsPlayable', 'true')
            url = getUrl(action=addonitem.kodiInfo.action, productId=addonitem.npoInfo.productId, guid=addonitem.npoInfo.guid, slug=addonitem.npoInfo.slug)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, addonitem.kodiInfo.isFolder)        
    xbmcplugin.endOfDirectory(_handle)

def playVideo(productId):
    stream_info, licenseKey = Uzg.getPlayInfo(productId)
    playitem = xbmcgui.ListItem(path=stream_info["stream"]["streamURL"])
    # xbmc.log('playVideo - {}'.format(productId),level=xbmc.LOGERROR)
    is_helper = inputstreamhelper.Helper(PROTOCOL, DRM)
    if is_helper.check_inputstream():
        playitem.setProperty('inputstream','inputstream.adaptive')
        playitem.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
        playitem.setProperty('inputstream.adaptive.license_type', DRM)
        if licenseKey:
            playitem.setProperty('inputstream.adaptive.license_key', licenseKey)
        xbmcplugin.setResolvedUrl(_handle, True, listitem=playitem)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        text = None
        if params['action'] == 'Zoeken':
            dialog = xbmcgui.Dialog()
            input_dialog = dialog.input(_addon.getLocalizedString(32004), type=xbmcgui.INPUT_ALPHANUM)
            if input_dialog:
                text = input_dialog
        
        if params['action'] == 'play':
            playVideo(params['productId'])
        else:
            # action will give list of items from api
            items = Uzg.getItems(params['action'], params['guid'], params['productId'], params['slug'], text)
            if items:
                addItems(items, params['action'])
            else:
                raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        homeMenu()
        setMediaView()

if __name__ == '__main__':
    router(sys.argv[2][1:])
