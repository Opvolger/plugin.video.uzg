import resources.lib.uzg
import resources.lib.npoapihelpers

uzg = resources.lib.uzg.Uzg()
npoapihelpers= resources.lib.npoapihelpers.NpoHelpers()

#print(uzg.getAZPage('W'))

# {
# "guid": "2042e1ee-0e79-4766-aea2-5b300d6839b2",
# "title": "NPO3",
# "externalId": "LI_NL3_4188107"
# },

a = npoapihelpers.getToken('LI_NL3_4188107')

print(a) 

b = npoapihelpers.getStream(a)

print(b)

c = 3

info, licenseKey = uzg.getPlayInfo('LI_NL3_4188107')

a = npoapihelpers.getToken('VARA_101381121')

print(a) 

b = npoapihelpers.getStream(a)

print(b)

c = 3

info, licenseKey = uzg.getPlayInfo('VARA_101381121')

result = uzg.getChannels()

print(uzg.getChannels())

for item in result:
    print(item.npoInfo.productId)
    print(item.kodiInfo.isFolder)
    print(item.kodiInfo.isPlayable)
    print(item.kodiInfo.label)
    print(item.kodiInfo.action)
    print('---')

print(uzg.getQueryPage('bijna'))

result = uzg.getSeasons('we-zijn-er-bijna')

for item in result:
    print(item.npoInfo.slug)

print(uzg.getSeasons('we-zijn-er-bijna'))

result = uzg.getEpisodesOfSeason('d89e22bb-6983-49ac-8cad-faf539e5245e')

for item in result:
    print(item.npoInfo.productId)
    print(item.kodiInfo.isFolder)
    print(item.kodiInfo.isPlayable)
    print(item.kodiInfo.label)
    print(item.kodiInfo.video)
    print('---')


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