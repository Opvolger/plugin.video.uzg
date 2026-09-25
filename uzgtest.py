from resources.lib.uzg import Uzg
from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import AddonItems
from typing import List
from urllib.parse import quote

uzg = Uzg()

a = NpoHelpers.getToken('LI_NL3_4188107')

print(a) 

b = NpoHelpers.getStream(a)

print(b)

c = 3

info, licenseKey = NpoHelpers.getPlayInfo('LI_NL3_4188107')

a = NpoHelpers.getToken('POW_05975335')

print(a) 

b = NpoHelpers.getStream(a)

print(b)

c = 3

info, licenseKey = NpoHelpers.getPlayInfo('POW_05975335')

# DRM: nieuwe api (stream.drm.licenseUrl, ezdrm) en oude api (drmToken) moeten een license key opleveren
for productId in ['AT_300013248', 'LI_NL3_4188107', 'POW_05975335']:
    info, licenseKey = NpoHelpers.getPlayInfo(productId)
    assert licenseKey, 'Geen license key voor {}: {}'.format(productId, info['stream'].get('drm'))
    url, headers, challenge, response = licenseKey.split('|')
    assert url.startswith('https://'), licenseKey
    assert challenge == 'R{SSM}', licenseKey
    print(productId, url.split('?')[0], headers, NpoHelpers.getServerCertificate(info['stream']))

assert NpoHelpers.getLicenseKeyFromStream({'drmToken': 'abc'}) == \
    'https://npo-drm-gateway.samgcloud.nepworldwide.nl/authentication?custom_data=abc||R{SSM}|'
assert NpoHelpers.getLicenseKeyFromStream({'drm': {'token': 'abc', 'licenseUrl': None}}) == \
    'https://npo-drm-gateway.samgcloud.nepworldwide.nl/authentication?custom_data=abc||R{SSM}|'
assert NpoHelpers.getLicenseKeyFromStream({'drm': {'token': None, 'licenseUrl': 'https://lic/?a=1', 'httpHeaders': {'x-token': 'a b'}}}) == \
    'https://lic/?a=1|user-agent={}&origin=https%3A%2F%2Fnpo.nl&referer=https%3A%2F%2Fnpo.nl%2F&x-token=a%20b|R{{SSM}}|'.format(quote(NpoHelpers.USER_AGENT, safe=''))
assert NpoHelpers.getLicenseKeyFromStream({'drm': None}) is None
assert NpoHelpers.getLicenseKeyFromStream({}) is None
assert NpoHelpers.getServerCertificate({'drm': {'certificateUrl': None}}) is None

def loopItems(items: List[AddonItems]):
    for item in items:
        print(item.kodiInfo.label)
        print(item.kodiInfo.action)
        print(item.npoInfo.productId)
        print(item.npoInfo.guid)
        print(item.npoInfo.slug)
        print(item.kodiInfo.isFolder)
        print(item.kodiInfo.isPlayable)
        print('---')


# https://npo.nl/start/api/domain/guide-channels
loopItems(uzg.getItems('Live kanalen'))

# https://npo.nl/start/api/domain/search-results?searchQuery=bijna&searchType=series&subscriptionType=anonymous
loopItems(uzg.getItems('Zoeken', text="bijna"))

# https://npo.nl/start/api/domain/series-seasons?slug=freeks-wilde-wereld
loopItems(uzg.getItems('seasons', slug="freeks-wilde-wereld"))

# https://npo.nl/start/api/domain/programs-by-season?guid=7e1d457a-ec0f-4c25-853d-2085e55567b7&sort=-firstBroadcastDate
loopItems(uzg.getItems('episodesSeason', guid='7e1d457a-ec0f-4c25-853d-2085e55567b7'))

# https://npo.nl/start/api/domain/programs-by-series?seriesGuid=5328ea0b-beff-4c14-959e-675cc6eb8261&sort=-firstBroadcastDate
loopItems(uzg.getItems('episodesSerie', guid='5328ea0b-beff-4c14-959e-675cc6eb8261'))

# https://npo.nl/start/_next/data/9gPO_EpYVoXUgPbn57qRY/categorie/programmas.json?slug=programmas
items = uzg.getItems('Alle programmas')
loopItems(items)

for item in items:
    loopItems(uzg.getItems(item.kodiInfo.action, guid=item.npoInfo.guid, slug=item.npoInfo.slug))
    print('---')

# {
# "guid": "2042e1ee-0e79-4766-aea2-5b300d6839b2",
# "title": "NPO3",
# "externalId": "LI_NL3_4188107"
# },


# https://npo.nl/start/api/domain/search-results?searchQuery=bijna&searchType=series&subscriptionType=premium&profileid=premium
# https://npo.nl/start/api/domain/search-results?searchQuery=bijna&searchType=series&subscriptionType=anonymous
# https://npo.nl/start/api/domain/series-detail?slug=we-zijn-er-bijna
# https://npo.nl/start/api/domain/series-seasons?slug=we-zijn-er-bijna&type=timeless_series
# https://npo.nl/start/api/domain/search-results?searchQuery=bijna&searchType=series&subscriptionType=anonymous
# https://npo.nl/start/api/domain/programs-by-season?guid=7e1d457a-ec0f-4c25-853d-2085e55567b7&type=timeless_series
# https://npo.nl/start/api/domain/series-seasons?slug=we-zijn-er-bijna&type=timeless_series
# https://npo.nl/start/api/domain/programs-by-season?guid=d89e22bb-6983-49ac-8cad-faf539e5245e&type=timeless_series
# https://npo.nl/start/api/domain/programs-by-series?seriesGuid=a9c7142c-d94e-4c13-ad2b-42e2772925aa&sort=-firstBroadcastDate
# https://npo.nl/start/api/domain/programs-by-series?seriesGuid=a9c7142c-d94e-4c13-ad2b-42e2772925aa&limit=20&sort=firstBroadcastDate
# https://npo.nl/start/api/domain/series-seasons?slug=we-zijn-er-bijna&type=timeless_series
# https://npo.nl/start/api/domain/series-seasons?slug=we-zijn-er-bijna
# https://npo.nl/start/api/domain/series-seasons?slug=we-zijn-er-bijna
# https://npo.nl/start/_next/data/9gPO_EpYVoXUgPbn57qRY/serie/we-zijn-er-bijna.json?seriesSlug=we-zijn-er-bijna
# https://npo.nl/start/_next/data/9gPO_EpYVoXUgPbn57qRY/serie/ik-durf-het-bijna-niet-te-vragen.json?seriesSlug=ik-durf-het-bijna-niet-te-vragen
# https://npo.nl/start/_next/data/9gPO_EpYVoXUgPbn57qRY/categorie/series.json?slug=series
# https://npo.nl/start/_next/data/9gPO_EpYVoXUgPbn57qRY/categorie/programmas.json?slug=programmas
# https://npo.nl/start/api/domain/page-collection?guid=bcd8b931-c2df-4d53-9bcf-01faa4ac7050