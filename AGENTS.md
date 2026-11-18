# AGENTS.md

Kodi add-on `plugin.video.uzg` (NPO Start).

## Versie ophogen (release)

Bij het ophogen van de versie altijd **alle** onderstaande bestanden aanpassen:

1. `addon.xml` – het `version="x.y.z"` attribuut op het `<addon>` element.
2. `changelog.txt` – bovenaan een nieuw blok toevoegen in het bestaande formaat:

   ```text
   Version x.y.z
   * Korte omschrijving van de wijziging (eventueel met issue-nummer / bedankje)

   ```

   Het bestand is UTF-8 zonder BOM; houd dat zo.
3. `README.md` – de `kodiversion="x.y.z"` in het commando onder "Create zip-file".

Gebruik semantische versies: bugfixes ophogen in het patch-nummer (bijv. 4.2.3 → 4.2.4).

## GitHub release

1. Commit en push naar `master`.
2. Maak de zip met het commando uit `README.md` ("Create zip-file"); die komt in de map boven de repo terecht.
3. `gh release create x.y.z ../plugin.video.uzg-x.y.z.zip --title "x.y.z - <korte omschrijving>" --notes "..."`
   (tag = versienummer zonder `v`).
