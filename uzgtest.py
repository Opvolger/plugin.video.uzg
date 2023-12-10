from resources.lib.uzg import Uzg
from resources.lib.npoapihelpers import NpoHelpers
from resources.lib.npoapiclasses import AddonItems


a = NpoHelpers.getToken('LI_NL3_4188107')

print(a) 

b = NpoHelpers.getStream(a)

print(b)

c = 3

info, licenseKey = Uzg.getPlayInfo('LI_NL3_4188107')

a = NpoHelpers.getToken('VARA_101381121')

print(a) 

b = NpoHelpers.getStream(a)

print(b)

c = 3

info, licenseKey = Uzg.getPlayInfo('VARA_101381121')

def loopItems(items: list[AddonItems]):
    for item in items:
        print(item.kodiInfo.label)
        print(item.kodiInfo.action)
        print(item.npoInfo.productId)
        print(item.npoInfo.guid)
        print(item.kodiInfo.isFolder)
        print(item.kodiInfo.isPlayable)
        print('---')


# https://npo.nl/start/api/domain/guide-channels
loopItems(Uzg.getItems('Live kanalen'))

# https://npo.nl/start/api/domain/search-results?query=bijna&searchType=series&subscriptionType=anonymous
loopItems(Uzg.getItems('Zoeken', text="bijna"))

# https://npo.nl/start/api/domain/series-seasons?slug=freeks-wilde-wereld
loopItems(Uzg.getItems('seasons', slug="freeks-wilde-wereld"))

# https://npo.nl/start/api/domain/programs-by-season?guid=7e1d457a-ec0f-4c25-853d-2085e55567b7&sort=-firstBroadcastDate
loopItems(Uzg.getItems('episodesSeason', guid='7e1d457a-ec0f-4c25-853d-2085e55567b7'))

# https://npo.nl/start/api/domain/programs-by-series?seriesGuid=5328ea0b-beff-4c14-959e-675cc6eb8261&sort=-firstBroadcastDate
loopItems(Uzg.getItems('episodesSerie', guid='5328ea0b-beff-4c14-959e-675cc6eb8261'))

# https://npo.nl/start/_next/data/9gPO_EpYVoXUgPbn57qRY/categorie/programmas.json?slug=programmas
loopItems(Uzg.getItems('Alle programmas'))

# https://npo.nl/start/api/domain/page-collection?guid=bcd8b931-c2df-4d53-9bcf-01faa4ac7050
loopItems(Uzg.getItems('collection', guid='bcd8b931-c2df-4d53-9bcf-01faa4ac7050')) # SERIES
loopItems(Uzg.getItems('collection', guid='9443ce0c-b219-4f29-ba55-a96aca95beae')) # PROGRAM


# {
# "guid": "2042e1ee-0e79-4766-aea2-5b300d6839b2",
# "title": "NPO3",
# "externalId": "LI_NL3_4188107"
# },


# https://npo.nl/start/api/domain/search-results?query=bijna&searchType=series&subscriptionType=premium&profileid=premium
# https://npo.nl/start/api/domain/search-results?query=bijna&searchType=series&subscriptionType=anonymous
# https://npo.nl/start/api/domain/series-detail?slug=we-zijn-er-bijna
# https://npo.nl/start/api/domain/series-seasons?slug=we-zijn-er-bijna&type=timeless_series
# https://npo.nl/start/api/domain/search-results?query=bijna&searchType=series&subscriptionType=anonymous
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