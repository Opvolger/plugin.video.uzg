plugin.video.uzg
================

NPO Start NPO NED1, NED2, NED3

Voor eigen gebruik.

Buy me a beer / betaal een biertje voor mij
------------------------------------------
[![Donate-Ideal](https://img.shields.io/badge/Donate-Ideal-green.svg)](https://www.bunq.me/opvolger)

Deze addon werkt sinds de aanpassing van NPO alleen nog maar op Kodi 18.x en later!
Alleen alles vanaf versie 3.4.2 werkt nog na 9 okt. 2019.

Reden van ontwikkeling
----------------------

Mijn LG Smart tv, stopte opeens met spelen van NPO en RTLxl video's. Dit omdat men vond dat mijn tv niet meer ondersteund hoefde te worden.
Het was nog steeds een prima HD tv. Dus heb ik een raspberry pi gekocht en daar XBMC het huidige Kodi opgezet.
Er was helaas geen addon voor NPO of RTLxl, deze heb ik dus maar zelf gemaakt.

Ik kwam er achter dat meerdere mensen het zelfde probleem hadden dat ik had. Dus heb ik mijn addons maar online gezet.

Geniet dus van de addons, als jouw smart tv ook niet meer mag werken.

Create zip-file
---------------

```bash
kodiversion="4.1.3" && cd .. && rm plugin.video.uzg-$kodiversion.zip -f &&  zip -r plugin.video.uzg-$kodiversion.zip plugin.video.uzg -x "*/\.*" -x "*.pyc" -x "*.pyo" -x plugin.video.uzg/**/__pycache__\* && cd plugin.video.uzg
```
