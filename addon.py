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
import xbmc

from resources.lib.uzg import Uzg
from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import AddonItems
from typing import List

from urllib.parse import urlencode
from urllib.parse import parse_qsl


PROTOCOL = 'mpd'
DRM = 'com.widevine.alpha'
#DRM = 'widevine'
PLUGIN_NAME = 'uzg'
PLUGIN_ID = 'plugin.video.uzg'
KODI_VERSION = int(xbmc.getInfoLabel("System.BuildVersion").split('.', 1)[0])

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

def executeFunctionWithValueIfValueIsNotNone(function, valueForFunction):
    if valueForFunction:
        function(valueForFunction)

def addItems(addonitems: List[AddonItems], action):
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
            list_item = xbmcgui.ListItem(label=addonitem.kodiInfo.label)
            if KODI_VERSION == 19:
                list_item.setInfo('video', 
                                {
                                    'duration': NpoHelpers.getDuration(addonitem.kodiInfo.videoItem),
                                    'premiered':  NpoHelpers.getPremiered(addonitem.kodiInfo.videoItem),
                                    'date': NpoHelpers.getLabel(addonitem.kodiInfo.videoItem),
                                    'year': NpoHelpers.getYear(addonitem.kodiInfo.videoItem),
                                    'plot': NpoHelpers.getPlot(addonitem.kodiInfo.videoItem),
                                    'title': NpoHelpers.getLabel(addonitem.kodiInfo.videoItem),
                                    'studio': NpoHelpers.getStudios(addonitem.kodiInfo.videoItem),
                                    'aired': NpoHelpers.getFirstAired(addonitem.kodiInfo.videoItem),
                                    'dateadded': NpoHelpers.getDateAdded(addonitem.kodiInfo.videoItem)
                                })
            else:
                info_tag = list_item.getVideoInfoTag()
                executeFunctionWithValueIfValueIsNotNone(info_tag.setTitle, NpoHelpers.getLabel(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setDuration, NpoHelpers.getDuration(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setPremiered, NpoHelpers.getPremiered(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setFirstAired, NpoHelpers.getFirstAired(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setYear, NpoHelpers.getYear(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setDateAdded, NpoHelpers.getDateAdded(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setGenres, NpoHelpers.getGenres(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setGenres, NpoHelpers.getGenres(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setPlot, NpoHelpers.getPlot(addonitem.kodiInfo.videoItem))
                executeFunctionWithValueIfValueIsNotNone(info_tag.setStudios, NpoHelpers.getStudios(addonitem.kodiInfo.videoItem))
                list_item.setDateTime(NpoHelpers.getFirstAired(addonitem.kodiInfo.videoItem))
            # works for Kodi 19 and up
            list_item.setSubtitles(["https://cdn.npoplayer.nl/subtitles/nl/{0}.vtt".format(addonitem.npoInfo.productId)])
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
            # xbmc.log('licenseKey - {}'.format(licenseKey),level=xbmc.LOGINFO)
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
            items = uzg.getItems(params['action'], params['guid'], params['productId'], params['slug'], text)
            if items is not None:
                addItems(items, params['action'])
            else:
                raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        homeMenu()
        setMediaView()

if __name__ == '__main__':
    router(sys.argv[2][1:])
