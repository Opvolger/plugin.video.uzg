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
import time
import json
import sys

from resources.lib.uzg import Uzg

if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.parse import urlencode
    from urllib.parse import parse_qsl
    import storageserverdummy as StorageServer
else:
    # Fall back to Python 2's urllib2
    from urllib import urlencode
    from urlparse import parse_qsl
    try:
        import StorageServer
    except:
        import storageserverdummy as StorageServer


PROTOCOL = 'mpd'
DRM = 'com.widevine.alpha'
#DRM = 'widevine'
PLUGIN_NAME = 'uzg'
PLUGIN_ID = 'plugin.video.uzg'

uzg = Uzg()

_url = sys.argv[0]
_handle = int(sys.argv[1])
# (Your plugin name, Cache time in hours)
_cache = StorageServer.StorageServer(PLUGIN_ID, 24)
_addon = xbmcaddon.Addon()

# het in elkaar klussen van een url welke weer gebruikt word bij router


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def setMediaView():
    # juiste skin selecteren alleen voor confluence maar die gebruik ik prive nog steeds
    try:
        kodiVersion = xbmc.getInfoLabel('System.BuildVersion').split()[0]
        kodiVersion = kodiVersion.split('.')[0]
        skinTheme = xbmc.getSkinDir().lower()
        if 'onfluence' in skinTheme:
            xbmc.executebuiltin('Container.SetViewMode(504)')
    except:
        pass


def home_menu():
    xbmcplugin.setPluginCategory(_handle, 'NPO Start')
    for category in ['Live kanalen', 'Zoeken', 'Letters']:
        list_item = xbmcgui.ListItem(label=category)
        url = get_url(action='keuze', keuze=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)


def list_keuze(keuze):
    xbmcplugin.setPluginCategory(_handle, keuze)
    xbmcplugin.setContent(_handle, 'videos')

    if(keuze == 'Live kanalen'):
        list_livestreams()

    elif (keuze == 'Zoeken'):
        dialog = xbmcgui.Dialog()
        franchises = list()
        input_dialog = dialog.input(_addon.getLocalizedString(32004), type=xbmcgui.INPUT_ALPHANUM)
        if input_dialog:
            # als hij hier niet komt is hij geannuleerd of afgebroken
            franchises = _cache.cacheFunction(uzg.getQueryPage, input_dialog)
        displays_franchises(franchises)

    elif(keuze == 'Letters'):
        list_overzicht()


def list_livestreams():
    videos = list()
    videos = _cache.cacheFunction(uzg.getChannels)
    if videos:
        add_video_items(videos)

    xbmcplugin.endOfDirectory(_handle)


def list_letter(letter):
    # ophalen franchises aan de hand van een "letter"
    franchises = _cache.cacheFunction(uzg.getAZPage, letter)
    displays_franchises(franchises)


def displays_franchises(franchises):
    # displays franchises
    if franchises:
        for franchise in franchises:
            list_item = xbmcgui.ListItem(label=franchise['label'])
            list_item.setArt(franchise['art'])
            list_item.setInfo('video', franchise['video'])
            url = get_url(action='episodes', link=franchise['apilink'])
            is_folder = True
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        xbmcplugin.addSortMethod(
            _handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)

    xbmcplugin.endOfDirectory(_handle)


def list_overzicht():
    xbmcplugin.setPluginCategory(_handle, 'Letters')
    # Alle mogelijke "begin" "letters"
    for letter in [
        '0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']:
        list_item = xbmcgui.ListItem(label=letter)
        url = get_url(action='letter', letter=letter)
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)


def list_franchise(link):
    xbmcplugin.setPluginCategory(_handle, link)
    # enable media info viewtype zodat "plot" van een aflevering ook getoond kan worden (indien gewenst)
    xbmcplugin.setContent(_handle, 'movies')
    episodesOrseason = uzg.episodesOrseason(link)
    if (episodesOrseason['type'] == 'episodes'):
        # het zijn gelijk afleveringen, pak de items en voeg deze toe!
        add_video_items(episodesOrseason['items'])
        # next 20 afleveringen
        if (episodesOrseason['linknext'] is not None):
            list_item = xbmcgui.ListItem(label='. -- ' + _addon.getLocalizedString(32003) + ' -- .')
            list_item.setProperty('IsPlayable', 'false')
            url = get_url(action='episodes', link=episodesOrseason['linknext'])
            is_folder = True
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_DATE)
        xbmcplugin.addSortMethod(
            _handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    else:
        # het zijn seasons, we hebben dus een sub-level "seasons" nodig
        add_season_items(episodesOrseason['items'])
    xbmcplugin.endOfDirectory(_handle)


def add_season_items(seasonitems):
    for seasonitem in seasonitems:
        # weergave seasons van franchise
        list_item = xbmcgui.ListItem(label=seasonitem['label'])
        url = get_url(action='episodes', link=seasonitem['link'])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


def add_video_items(videoitems):
    for video in videoitems:
        # weergave video's die kan direct onder een franchise zijn of vanaf een sub-level "seasons"
        list_item = xbmcgui.ListItem(label=video['label'])
        list_item.setInfo('video', video['video'])
        list_item.setArt(video['art'])
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', whatson_id=video['whatson_id'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)


def play_video(whatson_id):
    subtitle = uzg.get_ondertitel(whatson_id)
    stream_info = uzg.get_play_url(whatson_id)
    playitem = xbmcgui.ListItem(path=stream_info['url'])

    if (subtitle != None and xbmcplugin.getSetting(_handle, "subtitle") == 'true'):
        playitem.setSubtitles([subtitle])
    if (stream_info['drm']):
        is_helper = inputstreamhelper.Helper(
            PROTOCOL, DRM)  # drm=stream_info['drm'])
        if is_helper.check_inputstream():
            if (sys.version_info[0] == 3):
                # Kodi 19
                playitem.setProperty('inputstream','inputstream.adaptive')
            else:
                # Kodi 18
                playitem.setProperty('inputstreamaddon', is_helper.inputstream_addon)
            playitem.setProperty('inputstream.adaptive.manifest_type', PROTOCOL)
            # stream_info['drm'])
            playitem.setProperty('inputstream.adaptive.license_type', DRM)
            playitem.setProperty('inputstream.adaptive.license_key', stream_info['license_key'])
    xbmcplugin.setResolvedUrl(_handle, True, listitem=playitem)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'letter':
            list_letter(params['letter'])
        elif params['action'] == 'keuze':
            list_keuze(params['keuze'])
        elif params['action'] == 'episodes':
            list_franchise(params['link'])
            setMediaView()
        elif params['action'] == 'play':
            play_video(params['whatson_id'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        home_menu()
        setMediaView()


if __name__ == '__main__':
    router(sys.argv[2][1:])
