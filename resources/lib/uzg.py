'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~
    An XBMC addon for watching NPO Start
    :license: GPLv3, see LICENSE.txt for more details.
    NPO Start = Made by Bas Magre (Opvolger)

'''

from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import AddonItems, QueryItems, SeasonItems, Channels, SeasonItems, EpisodesOfSeasonItems, EpisodesOfSerieItems, AllItems, CollectionItems
from typing import List

class Uzg:
    def __init__(self):
        self.channels = Channels()
        self.allItems = AllItems()
        self.queryItems = QueryItems()
        self.episodesOfSeasonItems = EpisodesOfSeasonItems()
        self.episodesOfSerieItems = EpisodesOfSerieItems()
        self.collectionItems = CollectionItems()
        self.seasonItems = SeasonItems()

    def getItems(self, action, guid = None, productId = None, slug = None, text = None) -> List[AddonItems]:
        if action == 'Live kanalen':
            return self.channels.getItems()
        elif action == 'Alle programmas':
            return self.allItems.getItems('programmas')
        elif action == 'webcollectie':
            return self.allItems.getItems(slug)
        elif action == 'Zoeken':
            if text:
                return self.queryItems.getItems(text)
            return []
        elif action == 'episodesSeason':
            return self.episodesOfSeasonItems.getItems(guid)
        elif action == 'episodesSerie':
            return self.episodesOfSerieItems.getItems(guid)
        elif action == 'collection':
            return self.collectionItems.getItems(guid, slug)
        elif action == 'seasons':
            return self.seasonItems.getItems(slug)
        return None
