import json
import re
from resources.lib.jsonhelper import ToJsonObject
import sys

import xbmc

if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    from urllib import urlencode


class NpoHelpers():

    def get_json_data(self, url, data=None):
        req = Request(url)
        req.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('ApiKey', '07896f1ee72645f68bc75581d7f00d54')
        response = urlopen(req, data)
        link = response.read()
        response.close()
        return json.loads(link)

    def get_subtitles(self, whatson_id):
        url = 'https://rs.poms.omroep.nl/v1/api/subtitles/'+whatson_id+'/nl_NL/CAPTION.vtt'
        # door deze controle geen ERROR in de logging van Kodi als er geen ondertitel bestaat
        req = Request(url)
        try:
            response = urlopen(req)
            response.close()
        except:
            return None
        return url

    def get_play_url(self, whatson_id):

        url = 'https://start-api.npo.nl/media/'+whatson_id+'/stream'
        data_dash = self.get_json_data(url, NpoHelpers.__get_video_request_data('dash'))

        if (data_dash['drm']):
            data_dash['license_key'] = data_dash['licenseServer'] + \
                '|X-Custom-Data=' + data_dash['licenseToken'] + '|R{SSM}|'
        else:
            # als we geen DRM hebben, pak dan de hls profile. Deze werkt ook op Kodi met oude filmpjes b.v. 2011 POW_00398490 (We zijn er bijna)
            return self.get_json_data(url, NpoHelpers.__get_video_request_data('hls'))
        return data_dash

    @staticmethod
    def __get_video_request_data(profile):
        data = ToJsonObject()
        data.profile = profile
        data.options = ToJsonObject()
        data.options.startOver = False
        data.options.platform = 'npo'
        return data.toJSON().encode('utf-8')

    @staticmethod
    def get_image(item):
        thumbnail = ''
        if item['images'] and item['images'].get('chromecast.post-play') and item['images']['chromecast.post-play']:
            if (item['images']['chromecast.post-play']['formats'].get('tv-expanded') is not None):
                thumbnail = item['images']['chromecast.post-play']['formats']['tv-expanded']['source']
            if thumbnail == '' and (item['images']['chromecast.post-play']['formats'].get('tv') is not None):
                thumbnail = item['images']['chromecast.post-play']['formats']['tv']['source']
        if thumbnail == '' and item['images'] and item['images'].get('grid.tile') and item['images']['grid.tile']:
            if (item['images']['grid.tile']['formats'].get('tv') is not None):
                thumbnail = item['images']['grid.tile']['formats']['tv']['source']      
            if (item['images']['grid.tile']['formats'].get('tv-expanded') is not None):
                thumbnail = item['images']['grid.tile']['formats']['tv-expanded']['source']  
        #for channel images
        if thumbnail == '' and item['images'] and item['images'].get('original') and item['images']['original']:
            if (item['images']['original']['formats'].get('tv') is not None):
                thumbnail = item['images']['original']['formats']['tv']['source']      
            if (item['images']['original']['formats'].get('tv-expanded') is not None):
                thumbnail = item['images']['original']['formats']['tv-expanded']['source']  
        
        return thumbnail

    @staticmethod
    def get_studio(item):
        if item['broadcasters']:
            return ', '.join(item['broadcasters'])
        return ''

    @staticmethod
    def get_genres(item):
        genres = ''
        if item['genres']:
            genres = ', '.join(item['genres'][0]['terms'])
        return genres
