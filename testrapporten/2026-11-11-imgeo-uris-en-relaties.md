# IMGeo: URI's behouden, relaties en botsingen

Datum: 11 november 2026. Aanleiding: feedback van de beheerders van het IMGeo-begrippenkader.

## Feedback en verwerking

| Opmerking | Verwerking |
|---|---|
| URI's van een al gepubliceerd kader gelijk houden; het gepubliceerde kader als invoer gebruiken | Nieuwe keuze `uris.bestaand` en `bk.py bestaand <url>`. Koppeling op URI, dan term met gelijke definitie, dan unieke term; waarden via hun waardelijst. Resultaat in `uit/uri-koppeling.tsv` |
| Standaard `skos:broader` in plaats van `isothes:broaderGeneric` | `relaties.generalisatie: broader` is de standaard |
| De parent-tag is IMGeo-specifiek | `relaties.waarde_parent_tag` staat standaard uit, ook in het IMGeo-voorbeeld |
| `botsing_achtervoegsel: " waarde"` niet gewenst: eerst op identificatie, dan op definitie, anders de onderscheidende term tussen haakjes | Met een gepubliceerd kader gaat de identiteit voor: een waarde of attribuut dat daar per lijst of klasse een eigen begrip is (collectie, of URI-pad zoals `Lijst/waarde` of `Waarde_lijst`), blijft dat. Daarna: gelijke definitie = één begrip, anders `term (lijst)`. Ook het splitsen gebruikt die vorm (`onverhard (wegdeel)`, `1 (bovenbouwcode)`) |
| Waarden altijd in de eigenschap Code | De waardenaam uit het model staat in `skos:notation`, getypeerd met de waardelijst. Zo is de code stabiel, en uniek binnen de lijst ook als dezelfde code in meer lijsten voorkomt |

## IMGeo 2.2 met het voorbeeld en het gepubliceerde kader

Alleen de scripts, op `IMGeo.xmi` uit het register en het kader van definities.geostandaarden.nl (464 begrippen, 57 collecties).

| | Voor | Na |
|---|---|---|
| Begrippen | 393 | 456 (70 attributen en 344 waarden: per klasse of lijst apart waar het gepubliceerde kader dat ook doet) |
| Gepubliceerde URI's behouden | 273 | 443 begrippen en alle 57 collecties; het kader zelf ook |
| `isothes:broaderGeneric` | 87 | 0 |
| SHACL run B (V / W / I) | 0 / 26 / 2 | 0 / 444 / 2 |

- **Niet gekoppeld (21).** Deze gepubliceerde begrippen staan niet in het UML-model van 2.2: 13 keer `transitie`, `historie`, de inwinningsmethoden, `OngeclassificeerdObject` en `OverigeScheiding`. Attributen die het gepubliceerde kader per klasse apart heeft (`Plus-type_waterdeel`), vindt de skill via het deel na `_` in de URI.
- **Meer waarschuwingen.** De 418 extra waarschuwingen zijn `DuplicateDefinitionWithinScheme`. Doordat waarden zoals *asfalt* per lijst een eigen begrip blijven, delen 93 begrippen hun definitie met een ander. Dat is de prijs van gelijke URI's; het gepubliceerde kader heeft dezelfde dubbelingen. Samenvoegen kan later, met een besluit over de URI's die dan vervallen.

## Regressie (met de voorbeelden, zonder gepubliceerd kader)

| Model | Uitkomst |
|---|---|
| NEN 3610 | 38 begrippen, SHACL 0 / 10 / 0: gelijk |
| IMGeluid | 388 begrippen, 19 / 2 / 218: gelijk; termen nu `1 (bovenbouwcode)` in plaats van `bovenbouwcode 1` |
| IMEV | 464 begrippen (was 465): de waarde *basisnet* heeft dezelfde definitie als het attribuut *basisnet* en is nu één begrip; 8 / 34 / 20 |

Tests: 39, allemaal geslaagd. Zie ook [2026-11-11-bhr-gt.md](2026-11-11-bhr-gt.md) voor de test op BHR-GT 2.2.
