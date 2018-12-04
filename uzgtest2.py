import resources.lib.uzg

uzg = resources.lib.uzg.Uzg()

#print(uzg.getAZPage())

print(uzg.episodesOrseason('https://start-api.npo.nl/page/franchise/VPWON_1260597'))

print(uzg.episodesOrseason('https://start-api.npo.nl/page/franchise/POW_03108581'))

print(uzg.episodesOrseason('https://start-api.npo.nl/media/series/POW_03108581/episodes?seasonId=POW_03137258'))

