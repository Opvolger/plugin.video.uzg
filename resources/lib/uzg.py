'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~
    An XBMC addon for watching NPO Start
    :license: GPLv3, see LICENSE.txt for more details.
    NPO Start = Made by Bas Magre (Opvolger)

'''

from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import QueryItems, SeasonItems, Channels, SeasonItems, EpisodesOfSeasonItems, EpisodesOfSerieItems


class Uzg:
    def getChannels(self):
        return Channels().getItems()

    def getQueryPage(self, tekst):
        return QueryItems('zoek', tekst).getItems()

    def getEpisodesOfSeason(self, guid):
        return EpisodesOfSeasonItems(guid).getItems()

    def getEpisodesOfSerie(self, guid):
        return EpisodesOfSerieItems(guid).getItems()

    def getSeasons(self, slug):
        return SeasonItems(slug).getItems()
    
    def getPlayInfo(self, externalId):
        token = NpoHelpers.getToken(externalId)
        info = NpoHelpers.getStream(token)
        licenseKey = None
        if "drmToken" in info["stream"]:
            licenseKey = NpoHelpers.getLicenseKey(info["stream"]["drmToken"])
        return info, licenseKey
