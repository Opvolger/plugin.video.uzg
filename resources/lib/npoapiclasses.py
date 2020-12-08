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
            self.episodes = self.__episodes(json['items'])
            if (json['_links'].get('next')):
                self.linknext = json['_links']['next']['href']

    def __episodes(self, items):
        # items of uit season of wel uit franchise (opbouw is gelijk)
        uzgitemlist = list()
        for episode in items:
            # we hebben geen premium/plus account
            if (episode['isOnlyOnNpoPlus'] == False):
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
        return {'type': 'episodes',
                'items': self.episodes,
                'linknext': self.linknext}


class NpoEpisodesItem(object):
    def __init__(self, episode):
        self.episode = episode  # data
        self.datetime = self.get_dateitem(self.episode['broadcastDate'])

    @staticmethod
    def get_dateitem(datumstring):
        try:
            datetimevalue = datetime.strptime(
                datumstring, "%Y-%m-%dT%H:%M:%SZ")
        except TypeError:
            datetimevalue = datetime(
                *(time.strptime(datumstring, "%Y-%m-%dT%H:%M:%SZ")[0:6]))
        UTC = Zone(+0, False, 'UTC')
        datetimevalue = datetimevalue.replace(tzinfo=UTC)  # UTC
        # we hebben een datetime nodig om zomer/wintertijd te kunnen bepalen
        datetimevalue = datetimevalue.astimezone(
            AmsterdamZone(datetimevalue))  # Amsterdam
        return datetimevalue

    def get_art(self):
        image = NpoHelpers.get_image(self.episode)
        return {'thumb': image,
                'icon':  image,
                'fanart': image}

    def __get_label(self):
        return self.episode['episodeTitle']

    def __get_timestamp(self):
        return self.datetime.strftime("%H:%M:%S")

    def __get_video(self):
        return {
            'title': self.episode['episodeTitle'],
            'premiered':  self.datetime.strftime("%Y-%m-%d"),
            'aired':  self.datetime.strftime("%Y-%m-%d"),
            'date': self.datetime.strftime("%d-%m-%Y"),
            'plot': self.episode['descriptionLong'],
            'studio': NpoHelpers.get_studio(self.episode),
            'year': self.datetime.strftime("%Y"),
            'duration': self.episode['duration'],
            'genre': NpoHelpers.get_genres(self.episode),
            'mediatype': 'video'}
        # 'mediatype' is needed for skin to display info for this ListItem correctly.
        # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14

    def get_item(self):
        return {'label': self.__get_label(),
                'art': self.get_art(),
                'video': self.__get_video(),
                'timestamp': self.__get_timestamp(),
                'whatson_id': self.episode['id']}


class SerieItems(object):
    def __init__(self, url):
        self.npoHelpers = NpoHelpers()
        json = self.npoHelpers.get_json_data(url)
        # hier staan de totaal aantal pagina's in.
        self.page_count = (json['total'] // json['count']
                           ) + (json['total'] % json['count'])
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
            if (serie['type'] == 'series'):
                uzgitemlist.append({
                    'label': serie['title'],
                    'art': {'thumb': image,
                            'icon':  image,
                            'fanart': image},
                    'video': {
                        'title': serie['title'],
                        'plot': serie['description'],
                        'studio': NpoHelpers.get_studio(serie),
                        'genre': NpoHelpers.get_genres(serie),
                        'mediatype': 'video'},
                    'nebo_id': serie['id'],
                    'apilink': serie['_links']['page']['href']
                })
        return uzgitemlist


class SeasonItems(object):
    def __init__(self, options, series_id):
        self.uzgitemlist = list()
        for seasonfiler in options:
            # url nu nog samengesteld, netter om uit api te halen?
            url = 'https://start-api.npo.nl/media/series/' + series_id + '/episodes?seasonId=' + seasonfiler['value']
            uzg_item = {'label': seasonfiler['display'], 'link': url}
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
            if(channel['type'] == "TvChannel"):
                image = NpoHelpers.get_image(channel)
                uzgitemlist.append({
                    'label': channel['name'],
                    'art': {'thumb': image,
                            'icon':  image,
                            'fanart': image},
                    'video': {
                        'title': channel['name'],
                        'plot': channel['name'] + 'LIVE TV',
                        'mediatype': 'video'},
                    'whatson_id': channel['liveStream']['id'],
                    'apilink': channel['_links']['page']['href']
                })
        return uzgitemlist
