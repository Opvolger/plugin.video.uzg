'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~

    An XBMC addon for watching Uitzendinggemist(NPO)
   
    :license: GPLv3, see LICENSE.txt for more details.

    Uitzendinggemist (NPO) = Made by Bas Magre (Opvolger)    

'''
from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoepisodesitem import NpoEpisodesItem

class Uzg:
    def __init__(self):
        self.npoHelpers = NpoHelpers()

    def getQueryPage(self, tekst):
        # default is page 1
        url = 'https://start-api.npo.nl/media/series?query=' + tekst
        return self.__getPage(url)

    def getAZPage(self, letter):
        # default is page 1
        urlAz = 'https://start-api.npo.nl/media/series?az=' + letter
        return self.__getPage(urlAz)

    def episodesOrseason(self, link):
        if ('episodes?seasonId' in link):
            # we hebben te maken met items onder een season, deze kunnen gelijk terug.
            return self.__get_episodesitems(self.npoHelpers.get_json_data(link))
        if ('/media/series/' in link and '?page=' in link):
            # we hebben met een next page te maken
            return self.__get_episodesitems(self.npoHelpers.get_json_data(link))
        # we gaan uitvragen wat we hebben, zodat we kunnen zien wat we moeten doen.
        data = self.npoHelpers.get_json_data(link)
        series_id = ''
        for component in data['components']:
            # dit is de eerste dus word netjes gevuld in de for loop
            if (component['type'] == 'franchiseheader'):
                # deze waarde is nodig voor als er een season filter is
                series_id = component['series']['id']
            if ((component['type'] == 'grid') and (component['id'] == 'grid-episodes')):
                if (component['filter'] is None):
                    # geen filter = afleveringen
                    return self.__get_episodesitems(component['data'])
                else:
                    # we hebben een filter, we maken een season overzicht
                    # ['filter']['options'] bevat de seasons welke er zijn. (b.v. "2018", "2017" enz.)
                    # series_id = id van serie (b.v. "We zijn er bijna")
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

    def __getAZItems(self, data):
        uzgitemlist = list()
        items = data['items']
        for serie in items:
            # alleen series (todo andere content)
            if (serie['type'] == 'series'):
                image = NpoHelpers.get_image(serie)
                uzgitem = {
                    'label': serie['title']
                    , 'art': {  'thumb': image,
                                'icon':  image,
                                'fanart': image }
                    , 'video': {
                                'title': serie['title'],
                                'plot': serie['description'],
                                'studio': NpoHelpers.get_studio(serie),
                                'genres': NpoHelpers.get_genres(serie),
                                'mediatype': 'video' } 
                    ,'nebo_id': serie['id']
                    ,'apilink': serie['_links']['page']['href']
                }
                uzgitemlist.append(uzgitem)
        return uzgitemlist

    def __season(self, options, series_id):
        uzgitemlist = list()
        for seasonfiler in options:
            # url nu nog samengesteld, netter om uit api te halen.
            url = 'https://start-api.npo.nl/media/series/'+ series_id  +'/episodes?seasonId=' + seasonfiler['value']
            uzgitem = { 'label': seasonfiler['display']
                        , 'link': url }
            uzgitemlist.append(uzgitem)
        return uzgitemlist

    def __getPage(self, url):
        data = self.npoHelpers.get_json_data(url)
        pages = self.npoHelpers.get_page_count(data)
        # de eerste hebben we al gehad.
        uzgitemlist = list()
        uzgitemlist.extend(self.__getAZItems(data)) # page 1
        if (pages > 1):
            for x in range(pages-1):
                page = x + 2
                data = self.npoHelpers.get_json_data(url + '&page=' + str(page))
                uzgitemlist.extend(self.__getAZItems(data)) #page 2 t/m x                   
        sortedlist = sorted(uzgitemlist, key=lambda x: x['label'].upper(), reverse=False)
        return sortedlist

    def __episodes(self, items):
        #items of uit season of wel uit franchise (opbouw is gelijk)
        uzgitemlist = list()
        for episode in items:
            if (episode['isOnlyOnNpoPlus'] == False):
                episodedata = NpoEpisodesItem(episode)
                uzgitem = { 'label': episodedata.get_label()
                            , 'art': episodedata.get_art()
                            , 'video': episodedata.get_video()
                            , 'timestamp': episodedata.get_timestamp()
                            , 'whatson_id': episode['id']}
                uzgitemlist.append(uzgitem)
        show_time_in_label = False
        for item in uzgitemlist:
            for ref in uzgitemlist:
                if (item['video']['aired'] == ref['video']['aired'] and item['label'] == ref['label'] and item['whatson_id'] != ref['whatson_id']):
                    # Er zijn meerdere afleveringen op dezelfde dag: toon de tijd in het label.
                    show_time_in_label = True
        if (show_time_in_label):
            uzgitemlist = [self.__rebuild_item(i) for i in uzgitemlist]
        return uzgitemlist

    def get_play_url(self, whatson_id):
        return self.npoHelpers.get_play_url(whatson_id)

    @staticmethod
    def get_ondertitel(whatson_id):
        return 'https://tt888.omroep.nl/tt888/'+whatson_id

    @staticmethod
    def __rebuild_item(item):    
        ##item op tijd gesorteerd zodat ze op volgorde staan en verschil is te zien
        titelnaam = item['label']
        if (titelnaam is None):
            titelnaam = ''
        if (item['timestamp'] is not None ):
            titelnaam += ' (' + item['timestamp'] + ')'

        item['label'] = titelnaam
        item['video']['title'] = titelnaam
        return item
