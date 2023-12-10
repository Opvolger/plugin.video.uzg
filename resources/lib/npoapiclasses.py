from resources.lib.npoapihelpers import NpoHelpers

class KodiInfo(object):
    def __init__(self, item, art = None) -> None:
        self.action = NpoHelpers.getAction(item) 
        self.label = NpoHelpers.getLabel(item)
        self.isFolder = NpoHelpers.isFolder(item)
        self.isPlayable = NpoHelpers.isPlayable(item)
        if art:
            self.art = art
        else:
            image = NpoHelpers.getImage(item)
            self.art = {'thumb': image,
                'icon':  image,
                'fanart': image}
        self.video = {
                        'aired': NpoHelpers.getAired(item),
                        'duration': NpoHelpers.getDuration(item),
                        'date': NpoHelpers.getDate(item),
                        'genre': NpoHelpers.getGenres(item),
                        'plot': NpoHelpers.getPlot(item),
                        'premiered': NpoHelpers.getPremiered(item),
                        'studio': NpoHelpers.getStudio(item),
                        'title': NpoHelpers.getLabel(item),
                        'year': NpoHelpers.getYear(item),
                        'mediatype': 'video'
                      }

class NpoInfo(object):
    def __init__(self, guid, productId, slug) -> None:
        self.guid = guid
        self.productId = productId
        self.slug = slug

class AddonItems(object):
    def __init__(self, kodiInfo: KodiInfo, npoInfo: NpoInfo) -> None:
        self.kodiInfo = kodiInfo
        self.npoInfo = npoInfo

class JsonToItems(object):
    @staticmethod
    def getItems(json):
        # TODO paging
        uzgitemlist = list()
        items = json # nome times items are direct, sometimes in item
        if 'items' in json:
            items = json['items'] # nome times items are direct, sometimes in item
        for item in items:
            productId = None
            slug = None
            if 'slug' in item:
                slug = item['slug']
            if 'productId' in item:
                productId = item['productId']
            if 'externalId' in item:
                productId = item['externalId']
            uzgitemlist.append(AddonItems(
                KodiInfo(item),
                NpoInfo(item['guid'],productId,slug)
                )
            )
        return uzgitemlist

class EpisodesOfSerieItems(object):
    def __init__(self, guid):
        self.guid = guid

    def getItems(self) -> list[AddonItems]:
        url = 'https://npo.nl/start/api/domain/programs-by-series?seriesGuid={}&sort=-firstBroadcastDate'.format(self.guid)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))

class EpisodesOfSeasonItems(object):
    def __init__(self, guid):
        self.guid = guid

    def getItems(self) -> list[AddonItems]:
        url = 'https://npo.nl/start/api/domain/programs-by-season?guid={}&sort=-firstBroadcastDate'.format(self.guid)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))

class SeasonItems(object):
    def __init__(self, slug):
        self.slug = slug

    def getItems(self) -> list[AddonItems]:
        url = 'https://npo.nl/start/api/domain/series-seasons?slug={}'.format(self.slug)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))
    
class QueryItems(object):
    def __init__(self, type, tekst):
        self.url = ''
        if type == 'zoek':
            self.url = 'https://npo.nl/start/api/domain/search-results?query={}&searchType=series&subscriptionType=anonymous'.format(tekst.replace(' ', '%20'))
        

    def getItems(self) -> list[AddonItems]:
        return JsonToItems.getItems(NpoHelpers.getJsonData(self.url))

class Channels(object):   
    def getItems(self) -> list[AddonItems]:
        url = 'https://npo.nl/start/api/domain/guide-channels'
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))
