import resources.lib.uzg

uzg = resources.lib.uzg.Uzg()

print(uzg.get_overzicht())

print('\n\n')

print(uzg.get_items('POMS_S_RKK_687752'))

print('\n\n')

print(uzg.get_play_url('AT_2096873'))

print('\n\n')

print(uzg.get_ondertitel('AT_2096873'))
