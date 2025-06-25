import json, re

from datetime import datetime
from resources.lib.jsonhelper import ToJsonObject
from urllib.request import urlopen, Request
from typing import List

class NpoHelpers():

    @staticmethod
    def getPlayInfo(externalId):
        token = NpoHelpers.getToken(externalId)
        info = NpoHelpers.getStream(token)
        licenseKey = None
        if "drmToken" in info["stream"]:
            licenseKey = NpoHelpers.getLicenseKey(info["stream"]["drmToken"])
        return info, licenseKey

    @staticmethod
    def getBuildId(url):
        req = Request(url)
        req.add_header(
            'User-Agent',
            'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        response = urlopen(req)
        website = response.read()
        response.close()

        regex = r"buildId\":\"([A-z0-9_-]*)"

        match = re.findall(regex, str(website))
        if match:
            return match[0]

    @staticmethod
    def getJsonData(url):
        req = Request(url)
        req.add_header(
            'User-Agent',
            'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        response = urlopen(req)
        link = response.read()
        response.close()
        return json.loads(link)

    @staticmethod
    def getStream(token):
        headers = {
            'authority': 'prod.npoplayer.nl',
            'accept': '*/*',
            'accept-language': 'en,en-US;q=0.9,nl;q=0.8,nl-NL;q=0.7,en-NL;q=0.6',
            'authorization': token,
            'content-type': 'application/json',
            'dnt': '1',
            'origin': 'https://npo.nl',
            'referer': 'https://npo.nl/',
            'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        data = ToJsonObject()
        data.profileName = 'dash'
        data.drmType = 'widevine'
        data.referrerUrl = 'https://npo.nl/start/live?channel=NPO3'
        req = Request('https://prod.npoplayer.nl/stream-link')
        if (headers):
            for key in headers:
                req.add_header(key, headers[key])
        response = urlopen(req, data.toJSON().encode('utf-8'))
        link = response.read()
        response.close()
        return json.loads(link)

    @staticmethod
    def getLicenseKey(drmToken):
        url = "https://npo-drm-gateway.samgcloud.nepworldwide.nl/authentication?custom_data={}".format(drmToken)
        return "{}||R{{SSM}}|".format(url)

    @staticmethod
    def getToken(externalId):

        headers = {
            'authority': 'npo.nl',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en,en-US;q=0.9,nl;q=0.8,nl-NL;q=0.7,en-NL;q=0.6',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        }

        req = Request('https://npo.nl/start/api/domain/player-token?productId={}'.format(externalId), method='GET')
        if (headers):
            for key in headers:
                req.add_header(key, headers[key])
        response = urlopen(req)
        link = response.read()
        response.close()
        return json.loads(link)['jwt']


    @staticmethod
    def getImage(item):
        thumbnail = ''
        if 'images' in item:
            if item['images']:
                thumbnail = item['images'][0]['url']
        return thumbnail


    @staticmethod
    def isFolder(item):
        return not NpoHelpers.isPlayable(item)

    @staticmethod
    def isPlayable(item):
        if 'externalId' in item:
            return True
        if 'publishedDateTime' in item:
            return True
        if 'durationInSeconds' in item:
            return True
        return False

    @staticmethod
    def getPlot(item):
        if 'synopsis' in item:
            if item['synopsis']:
                if 'long' in item['synopsis']:
                    return item['synopsis']['long']
                else:
                    return item['synopsis']
        return None

    @staticmethod
    def getAction(item):
        if NpoHelpers.isPlayable(item):
            return 'play'
        if 'seasonKey' in item:
            # We have seasonKey go to the episodes view
            return 'episodesSeason'
        if 'type' in item:
            if item['type'] == "SERIES":
                return 'collection'
            if item['type'] == "PROGRAM":
                return 'collection'
            if item['type'] == "DYNAMIC_PAGE":
                return 'collection'
            if item['type'] == "timeless_series":
                return 'seasons'
            if item['type'] == "timebound_daily":
                return 'episodesSerie'
            if item['type'] == "timebound_series":
                return 'seasons'
            if item['type'] == "umbrella_series":
                return 'seasons'
            print(item['type'])
        if 'slug' in item:
            return 'webcollectie'
        return 'unknown'

    @staticmethod
    def getLabel(item):
        if 'title' in item:
            if item['title']:
                # hack for journaal
                if item['title'] == "NOS Journaal":
                    if 'publishedDateTime' in item:
                        return '{} - {}'.format(item['title'],datetime.fromtimestamp(int(item['publishedDateTime'])).strftime("%H:%M"))
                return item['title']
        if 'label' in item:
            if item['label']:
                return item['label']
        if 'seasonKey' in item:
            return 'Season {}'.format(item['seasonKey'])
        print(item)
        return '-?-'

    @staticmethod
    def getDuration(item) -> int:
        if 'durationInSeconds' in item:
            return int(item['durationInSeconds'])
        return None

    @staticmethod
    def getDateAdded(item):
        if 'firstBroadcastDate' in item:
            if item['firstBroadcastDate']:
                return datetime.fromtimestamp(int(item['firstBroadcastDate'])).strftime("%Y-%m-%d %H:%M:%S")
        return None

    @staticmethod
    def getYear(item) -> int:
        if 'firstBroadcastDate' in item:
            if item['firstBroadcastDate']:
                return int(datetime.fromtimestamp(int(item['firstBroadcastDate'])).strftime("%Y"))
        return None
    
    @staticmethod
    def getFirstAired(item):
        if 'publishedDateTime' in item:
            if item['publishedDateTime']:
                return datetime.fromtimestamp(int(item['publishedDateTime'])).strftime("%Y-%m-%d %H:%M:%S")
        return None

    @staticmethod
    def getPremiered(item):
        if 'firstBroadcastDate' in item:
            if item['firstBroadcastDate']:
                return datetime.fromtimestamp(int(item['firstBroadcastDate'])).strftime("%Y-%m-%d %H:%M:%S")
        return None

    @staticmethod
    def getStudios(item) -> List[str]:
        broadcasters: List[str] = []
        if 'broadcasters' in item:
            if item['broadcasters']:
                for broadcaster in item['broadcasters']:
                    broadcasters.append(broadcaster['name'])
            return broadcasters
        return None

    @staticmethod
    def getGenres(item) -> List[str]:
        genres: List[str] = []
        if 'genres' in item:
            if item['genres']:
                for genre in item['genres']:
                    genres.append(genre['name'])
            return genres
        return None