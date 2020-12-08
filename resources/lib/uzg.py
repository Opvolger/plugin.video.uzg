'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~
    An XBMC addon for watching NPO Start
    :license: GPLv3, see LICENSE.txt for more details.
    NPO Start = Made by Bas Magre (Opvolger)

'''

from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import SerieItems, EpisodesItems, Channels, SeasonItems


class Uzg:
    def __init__(self):
        self.npoHelpers = NpoHelpers()

    # def getLivePage(self):
    #    return LiveItems('https://start-api.npo.nl/page/live').uzgitemlist

    def getChannels(self):
        return Channels('https://start-api.npo.nl/channel').uzgitemlist

    def getQueryPage(self, tekst):
        # default is page 1
        return SerieItems('https://start-api.npo.nl/search?query=' + tekst.replace(' ', '%20')).uzgitemlist

    def getAZPage(self, letter):
        # default is page 1
        return SerieItems('https://start-api.npo.nl/media/series?az=' + letter).uzgitemlist

    def episodesOrseason(self, url):
        if ('episodes?seasonId' in url):
            # we hebben te maken met items onder een season, deze kunnen gelijk terug.
            return EpisodesItems(url=url).get_episodes_info_and_items()
        if ('/media/series/' in url and '?page=' in url):
            # we hebben met een next page te maken
            return EpisodesItems(url=url).get_episodes_info_and_items()
        # we gaan uitvragen wat we hebben, zodat we kunnen zien wat we moeten doen.
        data = self.npoHelpers.get_json_data(url, None)
        series_id = ''
        for component in data['components']:
            # dit is de eerste dus word netjes gevuld in de for loop
            if (component['type'] == 'franchiseheader'):
                # deze waarde is nodig voor als er een season filter is
                series_id = component['series']['id']
            if ((component['type'] == 'grid') and (component['id'] == 'grid-episodes')):
                if (component['filter'] is None):
                    # geen filter = afleveringen
                    return EpisodesItems(json=component['data']).get_episodes_info_and_items()
                else:
                    # we hebben een filter, we maken een season overzicht
                    # ['filter']['options'] bevat de seasons welke er zijn. (b.v. "2018", "2017" enz.)
                    # series_id = id van serie (b.v. "We zijn er bijna")
                    return {'type': 'season', 'items': SeasonItems(component['filter']['options'], series_id).uzgitemlist}
        # we hebben niks gevonden, dus stuur maar een lege lijst terug
        return EpisodesItems().get_episodes_info_and_items()

    def get_play_url(self, whatson_id):
        return self.npoHelpers.get_play_url(whatson_id)

    def get_ondertitel(self, whatson_id):
        return self.npoHelpers.get_subtitles(whatson_id)
