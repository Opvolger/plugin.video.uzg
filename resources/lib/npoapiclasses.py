import time
import json

from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.amsterdamzone import AmsterdamZone
from resources.lib.zone import Zone
from datetime import datetime


class EpisodesItems(object):
    def __init__(self, url=None, json=None):
        if url:
            self.npoHelpers = NpoHelpers()
            json = self.npoHelpers.get_json_data(url)
        self.linknext = None
        self.episodes = None
        self.uzgitemlist = list()
        # als we json hebben, kunnen we items aanmaken
        if json:
            self.episodes = self.__episodes(json)
            # if (json['_links'].get('next')):
            #     self.linknext = json['_links']['next']['href']

    def __episodes(self, items):
        # items of uit season of wel uit franchise (opbouw is gelijk)
        uzgitemlist = list()
        for episode in items:
            # we hebben geen premium/plus account
            # if (episode['isOnlyOnNpoPlus'] == False):
            uzgitemlist.append(NpoEpisodesItem(episode).get_item())
        show_time_in_label = False
        for item in uzgitemlist:
            for ref in uzgitemlist:
                if (item['video']['aired'] == ref['video']['aired'] and item['label'] == ref['label'] and item['whatson_id'] != ref['whatson_id']):
                    # Er zijn meerdere afleveringen op dezelfde dag: toon de tijd in het label.
                    show_time_in_label = True
        if (show_time_in_label):
            # we hebben items op de zelfde dag met de zelfde naam, we proberen er een timestamp voor te zetten:
            uzgitemlist = [self.__rebuild_item(i) for i in uzgitemlist]
        return uzgitemlist

    @staticmethod
    def __rebuild_item(item):
        # item op tijd gesorteerd zodat ze op volgorde staan en verschil is te zien
        titelnaam = item['label']
        if (titelnaam is None):
            titelnaam = ''
        if (item['timestamp'] is not None):
            titelnaam += ' (' + item['timestamp'] + ')'

        item['label'] = titelnaam
        item['video']['title'] = titelnaam
        return item

    def get_episodes_info_and_items(self):
        return {
            'type': 'episodes',
            'items': self.episodes
        }


class NpoEpisodesItem(object):
    def __init__(self, episode):
        self.episode = episode  # data
        self.datetime = self.get_dateitem(self.episode['publishedDateTime'])

    @staticmethod
    def get_dateitem(timestamp):
        # try:
        dt= datetime.fromtimestamp(timestamp)
        dt.astimezone(AmsterdamZone(dt))
        # datetimevalue = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # except TypeError:
        #     datetimevalue = datetime(
        #         *(time.strptime(datumstring, "%Y-%m-%dT%H:%M:%SZ")[0:6]))
        # UTC = Zone(+0, False, 'UTC')
        # datetimevalue = datetimevalue.replace(tzinfo=UTC)  # UTC
        # we hebben een datetime nodig om zomer/wintertijd te kunnen bepalen
        # datetimevalue = datetimevalue.astimezone( AmsterdamZone(datetimevalue))  # Amsterdam

        return dt
    
    def __get_timestamp(self):
        return self.datetime.strftime("%H:%M:%S")

    def get_art(self):
        image = NpoHelpers.get_image(self.episode)
        return {'thumb': image,
                'icon':  image,
                'fanart': image}

    def __get_label(self):
        return self.episode['title']

    

    def __get_video(self):
        plot = "";
        if(self.episode.get('synopsis')):
          plot = self.episode['synopsis']['long']
      
        return {
            'title': self.episode['title'],
            'premiered':  self.datetime.strftime("%Y-%m-%d"),
            'aired':  self.datetime.strftime("%Y-%m-%d"),
            'date': self.datetime.strftime("%d-%m-%Y"),
            'plot': plot,
            'studio': NpoHelpers.get_studio(self.episode),
            'year': self.datetime.strftime("%Y"),
            'duration': self.episode['durationInSeconds'],
            'genre': NpoHelpers.get_genres(self.episode),
            'mediatype': 'video',
            'link': "https://npo.nl/start/serie/{}/{}/{}/afspelen".format(self.episode['series']['slug'],  self.episode['season']['slug'],self.episode['slug'])
            }
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14

    def get_item(self):
        return {'label': self.__get_label(),
                'art': self.get_art(),
                'video': self.__get_video(),
                'timestamp': self.__get_timestamp(),
                'whatson_id': self.episode['productId'],
                }


class SerieItems(object):
    def __init__(self, url):
        self.npoHelpers = NpoHelpers()
        json = self.npoHelpers.get_json_data(url)
        # hier staan de totaal aantal pagina's in.
        self.page_count = json['pageCount'] 
        # (json['total'] // json['count']) + (json['total'] % json['count'])
        
        # we beginnen met de items uit de meegegeven url (page 1)
        self.uzgitemlist = self.__get_items(json)
        # als er nog meer pages zijn, dan halen we die data erbij.
        if (self.page_count > 1):
            for x in range(self.page_count-1):
                page = x + 2  # ( beginnen bij pagina 2 )
                data = self.npoHelpers.get_json_data(
                    url + '&page=' + str(page))
                self.uzgitemlist.extend(self.__get_items(data))  # page 2 t/m x
        # sorteer alle items
        self.uzgitemlist = sorted(
            self.uzgitemlist, key=lambda x: x['label'].upper(), reverse=False)

    def __get_items(self, json):
        uzgitemlist = list()
        items = json['items']
        for serie in items:
            # alleen series (todo andere content)
            image = NpoHelpers.get_image(serie)
            #if (serie['type'] == 'series'):
            uzgitemlist.append({
                'label': serie['title'],
                'art': {'thumb': image,
                        'icon':  image,
                        'fanart': image},
                'video': {
                    'title': serie['title'],
                    # 'plot': serie['description'],
                    'studio': NpoHelpers.get_studio(serie),
                    'genre': NpoHelpers.get_genres(serie),
                    'mediatype': 'video'},
                'guid': serie['guid'], 
                # 'nebo_id': serie['id'],
                'apilink': "https://npo.nl/start/api/domain/series-seasons?slug={}".format(serie['slug'])
            #serie['_links']['page']['href']
            })
        return uzgitemlist


class SeasonItems(object):
    def __init__(self, seasons):
        self.uzgitemlist = list()
        for season in seasons:
            # url nu nog samengesteld, netter om uit api te halen?
            url = "https://npo.nl/start/api/domain/programs-by-season?guid={}".format(season['guid'] )
            uzg_item = {'label': season['label'], 'link': url}
            self.uzgitemlist.append(uzg_item)


class Channels(object):
    def __init__(self, url):
        self.npoHelpers = NpoHelpers()
        channels = self.npoHelpers.get_json_data(url)
        self.uzgitemlist = list()
        self.uzgitemlist.extend(self.__get_channel_items(channels))

    def __get_channel_items(self, channels):
        uzgitemlist = list()

        for channel in channels:
            # if(channel['type'] == "TvChannel"):
            image = None, # NpoHelpers.get_image(channel)
            uzgitemlist.append({
                'label': channel['title'],
                'art': {'thumb': "",
                        'icon':  "",
                        'fanart': ""},
                'video': {
                    'title': channel['title'],
                    'plot': channel['title'] + ' LIVE TV',
                    'mediatype': 'video',
                    'link':   "https://npo.nl/start/live/{}".format( channel['title']) 
                },
                'whatson_id': channel['externalId'],
                    
                # 'apilink': channel['_links']['page']['href']
            })
        return uzgitemlist
