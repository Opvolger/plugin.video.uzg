'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~

    An XBMC addon for watching Uitzendinggemist(NPO)
   
    :license: GPLv3, see LICENSE.txt for more details.

    Uitzendinggemist (NPO) = Made by Bas Magre (Opvolger)    

'''
import sys
if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
import re ,time ,json
from datetime import datetime,tzinfo,timedelta

from resources.lib.amsterdamzone import AmsterdamZone
from resources.lib.zone import Zone

class Uzg:
    def getAZPage2(self, letter):
        # default is page 1
        urlAz = 'https://start-api.npo.nl/media/series?az=' + letter
        data = self.__getJsonData(urlAz)
        pages = self.__getPageCount(data)
        # de eerste hebben we al gehad.
        uzgitemlist = list()
        uzgitemlist.extend(self.__getAZItems(data)) # page 1
        if (pages > 1):
            for x in range(pages-1):
                page = x + 2
                data = self.__getJsonData(urlAz + '&page=' + str(page))
                uzgitemlist.extend(self.__getAZItems(data)) #page 2 t/m x                   
        sortedlist = sorted(uzgitemlist, key=lambda x: x['label'].upper(), reverse=False)
        return sortedlist

    def episodesOrseason(self, link):
        if ('episodes?seasonId' in link):
            # we hebben te maken met items onder een season, deze kunnen gelijk terug.
            return self.__get_episodesitems(self.__getJsonData(link))
        if ('/media/series/' in link and '?page=' in link):
            # we hebben met een nex page te maken
            return self.__get_episodesitems(self.__getJsonData(link))
        data = self.__getJsonData(link)
        series_id = ''
        for component in data['components']:
            # dit is de eerste dus word netjes gevuld in de for loop
            if (component['type'] == 'franchiseheader'):
                # deze waarde is nodig voor als er een season filter is
                series_id = component['series']['id']
            if ((component['type'] == 'grid') and (component['id'] == 'grid-episodes')):
                if (component['filter'] is None):
                    return self.__get_episodesitems(component['data'])
                else:
                    # we hebben een filter, we maken een season overzicht
                    # TODO controle of filter ook echt season is.
                    return { 'type': 'season',
                                'items': self.__season(component['filter']['options'], series_id) }
        # we hebben niks gevonden, dus stuur maar een lege lijst terug
        return { 'type': 'episodes',
                    'items': list(),
                    'linknext': None }
        
    def __get_episodesitems(self, data):
        linknext = None
        if (data['_links'].get('next')):
            linknext = data['_links']['next']['href']
        return { 'type': 'episodes',
                    'items': self.__episodes(data['items']),
                    'linknext': linknext }


    def __getJsonData(self, url):
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
        req.add_header('ApiKey', 'e45fe473feaf42ad9a215007c6aa5e7e')
        response = urlopen(req)
        link=response.read()
        response.close()
        return json.loads(link)

    def __getAZItems(self, data):
        uzgitemlist = list()
        items = data['items']
        for serie in items:
            # alleen series (todo andere content)
            if (serie['type'] == 'series'):
                uzgitem = {
                    'label': serie['title']
                    , 'art': {  'thumb': self.__getimage(serie),
                                'icon':  self.__getimage(serie),
                                'fanart':  self.__getimage(serie) }
                    , 'video': {
                                'title': serie['title'],
                                'plot': serie['description'],
                                'studio':  ', '.join(serie['broadcasters']),
                                'genres': self.__getgenres(serie),
                                'mediatype': 'video' } 
                    ,'nebo_id': serie['id']
                    ,'apilink': serie['_links']['page']['href']
                }
                uzgitemlist.append(uzgitem)
        return uzgitemlist

    def __getPageCount(self, data):
        return (data['total'] // 20) + (data['total'] % 20)

    def __season(self, options, series_id):
        uzgitemlist = list()
        for seasonfiler in options:
            # url nu nog samengesteld, netter om uit api te halen.
            url = 'https://start-api.npo.nl/media/series/'+ series_id  +'/episodes?seasonId=' + seasonfiler['value']
            uzgitem = { 'label': seasonfiler['display']
                        , 'link': url }
            uzgitemlist.append(uzgitem)
        return uzgitemlist

    def __getimage(self, item):
        thumbnail = ''
        if item['images'] and item['images']['original']:
            if (item['images']['original']['formats'].get('original') is not None):
                thumbnail = item['images']['original']['formats']['original']['source']
            if (item['images']['original']['formats'].get('tv') is not None):
                thumbnail = item['images']['original']['formats']['tv']['source']
        return thumbnail

    def __getgenres(self, item):
        genres = ''
        if item['genres']:
            genres = ', '.join(item['genres'][0]['terms'])
        return genres

    def __episodes(self, items):
        #items of uit season of wel uit franchise (opbouw is gelijk)
        uzgitemlist = list()
        for episode in items:
            if (episode['isOnlyOnNpoPlus'] == False):
                genres = ''
                datetime_episode = self.__dateitem(episode['broadcastDate']) # UTC
                datetime_episode = datetime_episode.astimezone(AmsterdamZone(datetime_episode)) # Amsterdam
                if episode['genres']:
                    genres = ', '.join(episode['genres'][0]['terms'])
                uzgitem = { 'label': episode['episodeTitle']
                            , 'art': {  'thumb': self.__getimage(episode),
                                        'icon':  self.__getimage(episode),
                                        'fanart':  self.__getimage(episode) }
                            , 'video': {
                                        'title': episode['episodeTitle'],
                                        'premiered':  datetime_episode.strftime("%Y-%m-%d"),
                                        'aired':  datetime_episode.strftime("%Y-%m-%d"),
                                        'date': datetime_episode.strftime("%d-%m-%Y"),
                                        'plot': episode['descriptionLong'],
                                        'studio': ', '.join(episode['broadcasters']),
                                        'year': episode['broadcastDate'].split('-')[0],
                                        'duration': episode['duration'],
                                        'genre': self.__getgenres(episode),
                                        'mediatype': 'video' } 
                            # 'mediatype' is needed for skin to display info for this ListItem correctly.
                            # https://codedocs.xyz/xbmc/xbmc/group__python__xbmcgui__listitem.html#ga0b71166869bda87ad744942888fb5f14
                            , 'timeStamp': datetime_episode.strftime("%H:%M:%S")
                            , 'whatson_id': episode['id']}
                uzgitemlist.append(uzgitem)
        show_time_in_label = False
        for item in uzgitemlist:
            for ref in uzgitemlist:
                if (item['video']['aired'] == ref['video']['aired'] and item['label'] == ref['label'] and item['whatson_id'] != ref['whatson_id']):
                    # Er zijn meerdere afleveringen op dezelfde dag: toon de tijd in het label.
                    show_time_in_label = True
        itemsreturn = [self.__rebuild_item(i, show_time_in_label) for i in uzgitemlist]
        return itemsreturn

    def __dateitem(self, datumstring):
        try:
            datetimevalue = datetime.strptime(datumstring, "%Y-%m-%dT%H:%M:%SZ")
        except TypeError:
            datetimevalue = datetime(*(time.strptime(datumstring, "%Y-%m-%dT%H:%M:%SZ")[0:6]))
        UTC = Zone(+0,False,'UTC')
        datetimevalue = datetimevalue.replace(tzinfo=UTC)
        return datetimevalue

    def __get_data_from_url(self, url):
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
        response = urlopen(req)
        data=response.read()
        response.close()
        return data    

    def get_ondertitel(self, whatson_id):
        return 'https://tt888.omroep.nl/tt888/'+whatson_id
        
    def get_play_url(self, whatson_id):
        ##token aanvragen
        data = self.__get_data_from_url('http://ida.omroep.nl/app.php/auth')
        token = re.search(r'token\":"(.*?)"', data.decode('utf-8')).group(1)
        ##video lokatie aanvragen
        data = self.__get_data_from_url('http://ida.omroep.nl/app.php/'+whatson_id+'?adaptive&adaptive=yes&part=1&token='+token)
        json_data = json.loads(data)
        ##video file terug geven vanaf json antwoord
        streamdataurl = json_data['items'][0][0]['url']
        streamurl = str(streamdataurl.split("?")[0]) + '?extension=m3u8'
        data = self.__get_data_from_url(streamurl)
        json_data = json.loads(data)
        url_play = json_data['url']
        return url_play

    def __rebuild_item(self, post, show_time_in_label):    
        ##item op tijd gesorteerd zodat ze op volgorde staan en verschil is te zien
        titelnaam = post['label']
        if (titelnaam is None):
            titelnaam = ''
        if (show_time_in_label and post['timeStamp'] is not None ):
            titelnaam += ' (' + post['timeStamp'] + ')'

        item = post
        item['label'] = titelnaam
        item['video']['title'] = titelnaam
        return item
