from datetime import datetime, tzinfo, timedelta
import time
from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.amsterdamzone import AmsterdamZone


class NpoEpisodesItem():
    def __init__(self, episode):
        self.episode = episode
        datetime_episode = NpoHelpers.get_dateitem(
            self.episode['broadcastDate'])  # UTC
        datetime_episode = datetime_episode.astimezone(
            AmsterdamZone(datetime_episode))  # Amsterdam
        self.datetime = datetime_episode

    def get_art(self):
        image = NpoHelpers.get_image(self.episode)
        return {'thumb': image,
                'icon':  image,
                'fanart': image}

    def get_label(self):
        return self.episode['episodeTitle']

    def get_timestamp(self):
        return self.datetime.strftime("%H:%M:%S")

    def get_video(self):
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
        return {'label': self.get_label(),
                'art': self.get_art(),
                'video': self.get_video(),
                'timestamp': self.get_timestamp(),
                'whatson_id': self.episode['id']}
