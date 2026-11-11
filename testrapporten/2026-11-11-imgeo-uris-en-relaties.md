# IMGeo: URI's behouden, relaties en botsingen

Datum: 11 november 2026. Aanleiding: feedback van de beheerders van het IMGeo-begrippenkader.

## Feedback en verwerking

| Opmerking | Verwerking |
|---|---|
| URI's van een al gepubliceerd kader gelijk houden; het gepubliceerde kader als invoer gebruiken | Nieuwe keuze `uris.bestaand` en `bk.py bestaand <url>`. Koppeling op URI, dan term met gelijke definitie, dan unieke term; waarden via hun waardelijst. Resultaat in `uit/uri-koppeling.tsv` |
| Standaard `skos:broader` in plaats van `isothes:broaderGeneric` | `relaties.generalisatie: broader` is de standaard |
| De parent-tag is IMGeo-specifiek | `relaties.waarde_parent_tag` staat standaard uit, ook in het IMGeo-voorbeeld |
| `botsing_achtervoegsel: " waarde"` niet gewenst: eerst op identificatie, dan op definitie, anders de onderscheidende term tussen haakjes | Met een gepubliceerd kader gaat de identiteit voor: een waarde die daar per lijst een eigen begrip is, blijft dat. Daarna: gelijke definitie = één begrip, anders `term (lijst)`. Ook het splitsen gebruikt die vorm (`onverhard (wegdeel)`, `1 (bovenbouwcode)`) |
| Waarden altijd in de eigenschap Code | De waardenaam uit het model staat in `skos:notation`, getypeerd met de waardelijst. Zo is de code stabiel, en uniek binnen de lijst ook als dezelfde code in meer lijsten voorkomt |

## IMGeo 2.2 met het voorbeeld en het gepubliceerde kader

Alleen de scripts, op `IMGeo.xmi` uit het register en het kader van definities.geostandaarden.nl (464 begrippen, 57 collecties).

| | Voor | Na |
|---|---|---|
| Begrippen | 393 | 453 (344 waarden: per lijst apart waar het gepubliceerde kader dat ook doet) |
| Gepubliceerde URI's behouden | 273 | 441 begrippen en alle 57 collecties; het kader zelf ook |
| `isothes:broaderGeneric` | 87 | 0 |
| SHACL run B (V / W / I) | 0 / 26 / 2 | 0 / 444 / 2 |

- **Niet gekoppeld (23).** 20 gepubliceerde begrippen staan niet in het UML-model van 2.2 (13 keer `transitie`, `historie`, de inwinningsmethoden). Drie zijn attributen die het gepubliceerde kader per klasse apart heeft, terwijl ze in het model dezelfde definitie hebben (`identificatie` bij Plaatsbepalingspunt, `plus-type` bij Waterdeel en OverigeScheiding). Het gepubliceerde kader legt geen relatie naar de klasse, dus de skill kan die identiteit niet afleiden.
- **Meer waarschuwingen.** De 418 extra waarschuwingen zijn `DuplicateDefinitionWithinScheme`. Doordat waarden zoals *asfalt* per lijst een eigen begrip blijven, delen 93 begrippen hun definitie met een ander. Dat is de prijs van gelijke URI's; het gepubliceerde kader heeft dezelfde dubbelingen. Samenvoegen kan later, met een besluit over de URI's die dan vervallen.

## Regressie (met de voorbeelden, zonder gepubliceerd kader)

| Model | Uitkomst |
|---|---|
| NEN 3610 | 38 begrippen, SHACL 0 / 10 / 0: gelijk |
| IMGeluid | 388 begrippen, 19 / 2 / 218: gelijk; termen nu `1 (bovenbouwcode)` in plaats van `bovenbouwcode 1` |
| IMEV | 464 begrippen (was 465): de waarde *basisnet* heeft dezelfde definitie als het attribuut *basisnet* en is nu één begrip; 8 / 34 / 20 |

Tests: 37, allemaal geslaagd.
