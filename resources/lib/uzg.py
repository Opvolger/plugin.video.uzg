'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~
    An XBMC addon for watching NPO Start
    :license: GPLv3, see LICENSE.txt for more details.
    NPO Start = Made by Bas Magre (Opvolger)

'''

from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import AddonItems, QueryItems, SeasonItems, Channels, SeasonItems, EpisodesOfSeasonItems, EpisodesOfSerieItems, AllItems, CollectionItems

class Uzg:
    
    @staticmethod
    def getPlayInfo(externalId):
        token = NpoHelpers.getToken(externalId)
        info = NpoHelpers.getStream(token)
        licenseKey = None
        if "drmToken" in info["stream"]:
            licenseKey = NpoHelpers.getLicenseKey(info["stream"]["drmToken"])
        return info, licenseKey

    @staticmethod
    def getItems(action, guid = None, productId = None, slug = None, text = None) -> list[AddonItems]:
        if action == 'Live kanalen':
            return Channels().getItems()
        elif action == 'Alle programmas':
            return AllItems().getItems()
        elif action == 'Zoeken':
            if text:
                return QueryItems(text).getItems()
            return list()
        elif action == 'episodesSeason':
            return EpisodesOfSeasonItems(guid).getItems()
        elif action == 'episodesSerie':
            return EpisodesOfSerieItems(guid).getItems()
        elif action == 'collection':
            return CollectionItems(guid).getItems()
        elif action == 'seasons':
            return SeasonItems(slug).getItems()
        return None