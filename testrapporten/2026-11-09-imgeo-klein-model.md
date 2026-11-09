# IMGeo 2.2 door een klein, snel model

Datum: 9 november 2026. Skillversie: 0.0.1.

Een klein, snel taalmodel heeft de skill zelfstandig uitgevoerd op IMGeo 2.2 (XMI uit het register), zonder gebruiker, inclusief de vergelijking met het gepubliceerde kader. Dit is run D in [2026-11-10-imgeo-vier-runs.md](2026-11-10-imgeo-vier-runs.md). De uitkomst van deze run is de basis voor de eval [`imgeo-xmi`](../skills/geonovum-uml2-nl-sbb/evals/imgeo-xmi/).

## Resultaat

| | Run | Referentie (alleen scripts) |
|---|---|---|
| Keuzes | alle scriptvoorstellen; het voorbeeld `voorbeelden/imgeo.yaml` niet gebruikt | met voorbeeld |
| Begrippen | 396 | 393 |
| Matches naar NEN 3610 en BAG | 0 | 33 |
| SHACL run B (V / W / I) | 0 / 72 / 0 | 0 / 26 / 2 |
| Review ok / term / definitie / twijfel | 396 / 0 / 0 / 0 | – |
| Vergelijking met de publicatie | 444 van 464 gekoppeld, definitie gelijk bij 433 | gelijk |

Het kader is precies het kader dat de scripts zonder voorbeeld maken. De scripts werkten dus goed. De zwakke punten zitten in wat het model zelf moest doen.

## Wat niet goed ging

- **Voorbeeld niet gebruikt.** De skill bevat een ingevuld voorbeeld voor IMGeo. Het model gebruikte het niet en stelde daarna voor zo'n voorbeeld toe te voegen.
- **Review zonder inhoud.** Alle 396 begrippen kregen `ok`. Bij de 42 begrippen met een signaal stonden maar vier verschillende standaardzinnen, zoals "gelijke definitie is acceptabel in deze context". Daardoor bleven fouten staan:
  - termen met een herhaalde context: *type scheiding scheiding*, *status IM geo-object IM geo-object*;
  - termen met leestekens: *recreatie: camping*, *(haven)kraan*;
  - de spelfout *fysiek vookomen*;
  - de identieke definities van *reclamebord* en *reclamezuil*;
  - de definitie "Definitie ontbreekt in de BAG." bij *landschappelijk gebied*.
- **Rapportage.** Het verbeterdocument noemde cijfers die niet uit de run komen, zoals de bespaarde tijd. Het bronmodel en het gepubliceerde kader waren in de repository gezet.

## Wat het heeft opgeleverd

- **Voor de eval** [`imgeo-xmi`](../skills/geonovum-uml2-nl-sbb/evals/imgeo-xmi/): die toetst precies deze punten. Is het voorbeeld gebruikt? Zijn er geen violations met de externe kaders als context? Signaleert de review de identieke en ontbrekende definities en de termen met leestekens? Staat de vergelijking in het rapport?
- **Voor de skill:** de verbeteringen uit [2026-11-10-imgeo-vier-runs.md](2026-11-10-imgeo-vier-runs.md):
  - `start` noemt het voorbeeld;
  - de scripts maken geen dubbele context meer;
  - het reviewsignaal bij leestekens geeft een voorstel.
