'''
    resources.lib.uzg
    ~~~~~~~~~~~~~~~~~

    An XBMC addon for watching Uitzendinggemist(NPO)
   
    :license: GPLv3, see LICENSE.txt for more details.

    Uitzendinggemist (NPO) = Made by Bas Magre (Opvolger)    
    based on: https://github.com/jbeluch/plugin.video.documentary.net

'''
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request    
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request    
import re ,time ,json
from datetime import datetime

class Uzg:

        def getJsonData(self, url):
            req = Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
            req.add_header('ApiKey', 'e45fe473feaf42ad9a215007c6aa5e7e')
            response = urlopen(req)
            link=response.read()
            response.close()            
            return json.loads(link)
        
        def getAZPage(self):
            # default is page 1
            urlAz = 'https://start-api.npo.nl/page/catalogue?az=Z'
            #urlAz = 'https://start-api.npo.nl/page/catalogue?az='
            data = self.getJsonData(urlAz)
            pages = self.getPageCount(data)
            # de eerste hebben we al gehad.
            print(pages)
            uzgitemlist = list()
            uzgitemlist.extend(self.getAZItems(data))
            if (pages > 1):
                for x in range(pages-1):
                    page = x + 2
                    data = self.getJsonData(urlAz + '&page=' + str(page))
                    uzgitemlist.extend(self.getAZItems(data))                    
            sortedlist = sorted(uzgitemlist, key=lambda x: x['label'], reverse=False)
            return sortedlist
        
        def getAZItems(self, data):
            uzgitemlist = list()
            for component in data['components']:
                if (component['type'] == 'grid'):
                    items = component['data']['items']
                    for serie in items:
                        uzgitem = {
                            'label': serie['title'],
                            'nebo_id': serie['id'],
                            'thumbnail': '',
                            'genres': '',
                            'plot': serie['description'],
                            'studio': ', '.join(serie['broadcasters']),
                            'apilink': serie['_links']['page']['href'],
                        }
                        uzgitemlist.append(uzgitem)
                    return uzgitemlist

        def getPageCount(self, data):
            for component in data['components']:
                if (component['type'] == 'grid'):
                    print(component['data']['total'])
                    return (component['data']['total'] // 20) + (component['data']['total'] % 20)
            return 0

        def episodes(self, link):
            data = self.getJsonData(link)
            uzgitemlist = list()
            # todo page count!
            for component in data['components']:
                if ((component['type'] == 'grid') and (component['id'] == 'grid-episodes')):
                    items = component['data']['items']                    
                    for episode in items:
                        thumbnail = ''
                        if episode['images']['original']:
                            thumbnail = episode['images']['original']['formats']['original']['source']
                        datum = (episode['broadcastDate'].split('T')[0])
                        uzgitem = { 'label': episode['title']
                                    , 'aired': datum
                                    , 'premiered':datum
                                    , 'year': datum.split('-')[0]
                                    , 'date': self.dateitem(datum)
                                    , 'TimeStamp': episode['broadcastDate'].split('Z')[0]
                                    , 'thumbnail': thumbnail
                                    , 'genres': ''
                                    , 'duration': episode['duration']
                                    , 'plot': episode['descriptionLong']
                                    , 'studio': ', '.join(episode['broadcasters'])
                                    , 'whatson_id': episode['id']}
                        uzgitemlist.append(uzgitem)
                    return uzgitemlist

        def dateitem(self, datum):
            try:
                return datetime.strptime(datum, "%Y-%m-%d").strftime("%d-%m-%Y")
            except TypeError:
                return datetime(*(time.strptime(datum, "%Y-%m-%d")[0:6])).strftime("%d-%m-%Y")

        def items(self, link):
            nebo_id = 'VARA_101377717'
            req = Request('http://apps-api.uitzendinggemist.nl/series/'+nebo_id+'.json')
            req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
            response = urlopen(req)
            link=response.read()
            response.close()
            json_data = json.loads(link)
            uzgitemlist = list()
            for aflevering in json_data['episodes']:
                urlcover = ''
                if aflevering['stills']:
                    urlcover = aflevering['stills'][0]['url']
                uzgitem = { 'label': aflevering['name']
                            , 'count': int(aflevering['broadcasted_at'])
                            , 'aired': datetime.fromtimestamp(int(aflevering['broadcasted_at'])).strftime('%Y-%m-%d')
                            , 'premiered': datetime.fromtimestamp(int(aflevering['broadcasted_at'])).strftime('%Y-%m-%d')
                            , 'date': datetime.fromtimestamp(int(aflevering['broadcasted_at'])).strftime('%d-%m-%Y')
                            , 'year': datetime.fromtimestamp(int(aflevering['broadcasted_at'])).strftime('%Y')
                            , 'TimeStamp': datetime.fromtimestamp(int(aflevering['broadcasted_at'])).strftime('%Y-%m-%dT%H:%M')
                            , 'thumbnail': urlcover
                            , 'genres': aflevering['genres']
                            , 'duration': aflevering['duration']
                            , 'serienaam': json_data['name']
                            , 'plot': aflevering['description']
                            , 'studio': ', '.join(aflevering['broadcasters'])
                            , 'whatson_id': aflevering['whatson_id']}
                uzgitemlist.append(uzgitem)
                #print(uzgitem['date'])
            return uzgitemlist

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
            
        def get_overzicht(self):
            return self.getAZPage()
            #return self.__overzicht()         


        def get_items(self, link):
            items = self.episodes(link)
            show_time_in_label = False
            
            for item in items:
                for ref in items:
                    if (item['aired'] == ref['aired'] and item['whatson_id'] != ref['whatson_id']):
                        # Er zijn meerdere afleveringen op dezelfde
                        # dag: toon de tijd in het label.
                        show_time_in_label = True

            return [self.__build_item(i, show_time_in_label) for i in items]
    
        def __build_item(self, post, show_time_in_label):    
            ##item op tijd gesorteerd zodat ze op volgorde staan.
            titelnaam = post['label']

            if (show_time_in_label):
                titelnaam += ' (' + post['TimeStamp'].split('T')[1] + ')'

            item = post
            item['label'] = titelnaam
            return item

        def __stringnaardatumnaarstring(self, datumstring):
            b = datetime(*(time.strptime(datumstring.split('T')[0], "%Y-%m-%d")[0:6]))
            return b.strftime("%d-%m-%Y")
