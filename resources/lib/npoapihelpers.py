import json
import re
import sys


from resources.lib.jsonhelper import ToJsonObject

if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    from urllib import urlencode


class NpoHelpers():

    def get_json_data(self, url, data=None, headers=None, add_headers=False):
        req = Request(url)
        req.add_header(
            'User-Agent',
            'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('ApiKey', '07896f1ee72645f68bc75581d7f00d54')
        if (headers):
            for key in headers:
                req.add_header(key, headers[key])
        response = urlopen(req, data)
        link = response.read()
        response.close()
        if (add_headers):
            response.headers.headers
            if (sys.version_info[0] == 3):
                response_headers = response.getheaders()
            else:
                response_headers = response.headers.headers
            return json.loads(link), response_headers
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
        # video = self.get_stream_url(whatson_id)
        # if (video['stream']['type'] == 'application/dash+xml'):
        #     xcdata_value = video['stream']['keySystemOptions'][0]['options']['httpRequestHeaders']['x-custom-data']
        #     license_url = video['stream']['keySystemOptions'][0]['options']['licenseUrl']
        #     item = {
        #         'url': video['stream']['src'],
        #         'drm': True,
        #         'license_key': license_url + '|Content-Type=&User-Agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3041.0 Safari/537.36&x-custom-data=%s|R{SSM}|' % xcdata_value
        #     }
        #     return item
        url = 'https://start-api.npo.nl/media/'+whatson_id+'/stream'
        data_dash = self.get_json_data(
            url, NpoHelpers.__get_video_request_data('dash'))
        if (data_dash['drm']):
            data_dash['license_key'] = data_dash['licenseServer'] + \
                '|X-Custom-Data=' + data_dash['licenseToken'] + '|R{SSM}|'
        else:
            # als we geen DRM hebben, pak dan de hls profile. Deze werkt ook op Kodi met oude filmpjes b.v. 2011 POW_00398490 (We zijn er bijna)
            return self.get_json_data(url, NpoHelpers.__get_video_request_data('hls'))
        return data_dash

    # werkt ook, maar met GEO blokking en omslachtig en kwaliteit is niet beter.
    def get_stream_url(self, whatson_id):
        # https://github.com/RandomIntermition/k4y108837s/blob/30dc07ee017978dafbe77ad651a9cf0a9cfc267d/HAX/18.CocoJoe/plugin.video.catchuptvandmore/resources/lib/channels/nl/npo.py
        headers = {'X-Requested-With': 'XMLHttpRequest'}
        data, cookies = self.get_json_data("https://www.npostart.nl/api/token", headers=headers, add_headers=True)
        for cookie in cookies:
            if (sys.version_info[0] == 3):
                if cookie[1].startswith("npo_session="):
                    session_token = cookie[1]
            else:
                if cookie.startswith("Set-Cookie: npo_session="):
                    session_token = cookie[12:].split('\r\n')[0]

        api_token = data['token']        
        payload = json.dumps({"_token": api_token}).encode('utf-8')

        headers = { "Cookie": session_token }
        
        resp2 = self.get_json_data("https://www.npostart.nl/player/{0}".format(whatson_id), data=payload, headers=headers)
        token_id = resp2['token']
        # video uitvraag
        video = self.get_json_data("https://start-player.npo.nl/video/{}/streams?profile=dash-widevine&quality=npo&tokenId={}&streamType=broadcast&mobile=0&ios=0&isChromecast=0".format(whatson_id, token_id))
        return video

    @staticmethod
    def __get_video_request_data(profile):
        data = ToJsonObject()
        data.profile = profile
        data.options = ToJsonObject()
        # moet False zijn om alle live kanalen te kunnen starten.
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
        # for channel images
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
