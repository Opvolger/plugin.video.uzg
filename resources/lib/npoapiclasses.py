from resources.lib.npoapihelpers import NpoHelpers
from datetime import datetime
from typing import List

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
        self.videoItem = item
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
        uzgitemlist: List[AddonItems] = []
        items = json # nome times items are direct, sometimes in item
        if 'items' in json:
            items = json['items'] # nome times items are direct, sometimes in item
        for item in items:
            addItem = True
            restrictionPremium = False
            restrictionFree = False
            if 'restrictions' in item:
                for restriction in item['restrictions']: 
                    if restriction['subscriptionType'] == "premium":
                        restrictionPremium = True
                    if restriction['subscriptionType'] == "free":
                        restrictionFree = True
                        now = int(datetime.now().timestamp())
                        if restriction['available']['from']:
                            if restriction['available']['from'] < now:
                                addItem = True
                            else:
                                addItem = False
                        if restriction['available']['from'] and restriction['available']['till']:
                            if restriction['available']['from'] <= now <= restriction['available']['till']:
                                addItem = True
                            else:
                                addItem = False

            if restrictionPremium and restrictionFree == False:
                # only Premium members
                addItem = False
            if (addItem):
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
    def getItems(self, guid) -> List[AddonItems]:
        url = 'https://npo.nl/start/api/domain/programs-by-series?seriesGuid={}&sort=-firstBroadcastDate'.format(guid)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))

class AllItems(object):
    def __init__(self):
        self.buildId = None

    def getBuildId(self):
        if (self.buildId == None):
            url = 'https://npo.nl/start/categorie/programmas'
            self.buildId = NpoHelpers.getBuildId(url)
        return self.buildId

    def getItems(self, url) -> List[AddonItems]:
        result = NpoHelpers.getJsonData(url)
        uzgitemlist: List[AddonItems] = []
        for collection in result['pageProps']['dehydratedState']['queries'][0]['state']['data']['collections']:
            url = 'https://npo.nl/start/api/domain/page-collection?collectionId={}'.format(collection['collectionId'])
            result = NpoHelpers.getJsonData(url)
            uzgitemlist.append(AddonItems(
                KodiInfo(result),
                NpoInfo(collection['collectionId'],None,None)
                )
            )
        return uzgitemlist
    
class CollectionItems(object):
    def getItems(self, guid) -> List[AddonItems]:
        url = 'https://npo.nl/start/api/domain/page-collection?collectionId={}'.format(guid)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))

class EpisodesOfSeasonItems(object):
    def getItems(self, guid) -> List[AddonItems]:
        url = 'https://npo.nl/start/api/domain/programs-by-season?guid={}&sort=-firstBroadcastDate'.format(guid)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))

class SeasonItems(object):
    def getItems(self, slug) -> List[AddonItems]:
        url = 'https://npo.nl/start/api/domain/series-seasons?slug={}'.format(slug)
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))
    
class QueryItems(object):
    def getItems(self, text) -> List[AddonItems]:
        url = 'https://npo.nl/start/api/domain/search-collection-items?searchQuery={}&searchType=series&subscriptionType=anonymous'.format(text.replace(' ', '%20'))
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))

class Channels(object):   
    def getItems(self) -> List[AddonItems]:
        url = 'https://npo.nl/start/api/domain/guide-channels'
        return JsonToItems.getItems(NpoHelpers.getJsonData(url))
