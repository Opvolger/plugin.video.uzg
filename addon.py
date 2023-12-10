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
    for category in ['Live kanalen', 'Zoeken']:
    #for category in ['Live kanalen', 'Zoeken', 'Letters']:
        list_item = xbmcgui.ListItem(label=category)
        url = getUrl(action='keuze', keuze=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)

def listSeasons(slug):
    items = uzg.getSeasons(slug)
    addItems(items)

def listEpisodesofSerie(guid):
    items = uzg.getEpisodesOfSerie(guid)
    addItems(items)

def listEpisodesofSeason(guid):
    items = uzg.getEpisodesOfSeason(guid)
    addItems(items)

def listKeuze(keuze):
    xbmcplugin.setPluginCategory(_handle, keuze)
    xbmcplugin.setContent(_handle, 'videos')

    if(keuze == 'Live kanalen'):
        listLiveStreams()

    elif (keuze == 'Zoeken'):
        dialog = xbmcgui.Dialog()
        franchises = list()
        input_dialog = dialog.input(_addon.getLocalizedString(32004), type=xbmcgui.INPUT_ALPHANUM)
        if input_dialog:
            # als hij hier niet komt is hij geannuleerd of afgebroken
            franchises = uzg.getQueryPage(input_dialog)
        addItems(franchises)


def listLiveStreams():
    videos = list()
    videos = uzg.getChannels()
    if videos:
        addItems(videos)

    xbmcplugin.endOfDirectory(_handle)


def addItems(addonitems: list[AddonItems]):
    if addonitems:
        if addonitems[0].kodiInfo.isPlayable:
            xbmcplugin.setContent(_handle, 'videos')
            xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_DATE)
            xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        for addonitem in addonitems:
            # weergave video's die kan direct onder een franchise zijn of vanaf een sub-level "seasons"
            list_item = xbmcgui.ListItem(label=addonitem.kodiInfo.label)
            list_item.setInfo('video', addonitem.kodiInfo.video)
            list_item.setArt(addonitem.kodiInfo.art)
            if addonitem.kodiInfo.isPlayable:
                list_item.setProperty('IsPlayable', 'true')
            url = getUrl(action=addonitem.kodiInfo.action, productId=addonitem.npoInfo.productId, guid=addonitem.npoInfo.guid, slug=addonitem.npoInfo.slug)
            xbmcplugin.addDirectoryItem(_handle, url, list_item, addonitem.kodiInfo.isFolder)        
        # xbmcplugin.addSortMethod(
        #     _handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def playVideo(productId):
    stream_info, licenseKey = uzg.getPlayInfo(productId)
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
        if params['action'] == 'keuze':
            listKeuze(params['keuze'])
        elif params['action'] == 'episodesSeason':
            listEpisodesofSeason(params['guid'])
            setMediaView()
        elif params['action'] == 'episodesSerie':
            listEpisodesofSerie(params['guid'])
            setMediaView()
        elif params['action'] == 'seasons':
            listSeasons(params['slug'])
        elif params['action'] == 'play':
            playVideo(params['productId'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        homeMenu()
        setMediaView()


if __name__ == '__main__':
    router(sys.argv[2][1:])
