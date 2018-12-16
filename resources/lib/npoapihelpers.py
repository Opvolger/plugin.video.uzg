from resources.lib.zone import Zone
from datetime import datetime,tzinfo,timedelta
import time

import sys
if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
import re ,json

class NpoHelpers():

    def get_json_data(self, url):
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
        req.add_header('ApiKey', 'e45fe473feaf42ad9a215007c6aa5e7e')
        response = urlopen(req)
        link=response.read()
        response.close()
        return json.loads(link)

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

    def __get_data_from_url(self, url):
        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
        response = urlopen(req)
        data=response.read()
        response.close()
        return data

    @staticmethod
    def get_page_count(data):
        return (data['total'] // 20) + (data['total'] % 20)

    @staticmethod
    def get_dateitem(datumstring):
        try:
            datetimevalue = datetime.strptime(datumstring, "%Y-%m-%dT%H:%M:%SZ")
        except TypeError:
            datetimevalue = datetime(*(time.strptime(datumstring, "%Y-%m-%dT%H:%M:%SZ")[0:6]))
        UTC = Zone(+0,False,'UTC')
        datetimevalue = datetimevalue.replace(tzinfo=UTC)
        return datetimevalue

    @staticmethod
    def get_image(item):
        thumbnail = ''
        if item['images'] and item['images']['original']:
            if (item['images']['original']['formats'].get('original') is not None):
                thumbnail = item['images']['original']['formats']['original']['source']
            if (item['images']['original']['formats'].get('tv') is not None):
                thumbnail = item['images']['original']['formats']['tv']['source']
        return thumbnail

    @staticmethod
    def get_studio(item):
        return ', '.join(item['broadcasters'])

    @staticmethod
    def get_genres(item):
        genres = ''
        if item['genres']:
            genres = ', '.join(item['genres'][0]['terms'])
        return genres