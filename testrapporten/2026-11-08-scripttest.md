# Scripttest en regressie

Datum: 8 november 2026. Skillversie: 0.0.1. Python 3.14, pySHACL 0.40.2, NL-SBB-profiel 1.0.0.

Deze tests gebruiken geen taalmodel. Ze toetsen de scripts.

## 1. Offline tests (`tests/test_scripts.py`)

Dit draait de hele keten van `bk.py` op het fictieve testmodel [`tests/fixtures/fietsparkeren.xmi`](../tests/fixtures/fietsparkeren.xmi). Daarnaast zijn er losse controles op de termomzetting, `project.yaml` en het packagevoorstel.

```text
python3 -m unittest discover -s tests -v
Ran 15 tests in 8.4s — OK   (met BK_NETWERK=1, dus inclusief de SHACL-validatie)
```

| Test | Controleert |
|---|---|
| `Keten` (7) | packagekeuze, geen open vragen na `overnemen --alle`, 21 begrippen, contexttermen, automatisch splitsen, samenvoegen bij leestekenverschil, geldige Turtle met 3 collecties, log van ontbrekende definities, review in delen met compleetheidscontrole en overname van oordelen, rapport |
| `ProjectControle` (2) | een tikfout in een sleutel geeft een suggestie; een onbekende klasse wordt gemeld |
| `Termen` (4) | camelCase en afkortingen (ook F4, GT5), getallen met decimaalteken, unieke URI's bij cijfergroepen, contextterm bij een keuze-datatype |
| `Package` (1) | packagevoorstel uit de bestandsnaam (NEN3610 en niet IMGolf) |
| `Validatie` (1, alleen met `BK_NETWERK=1`) | SHACL-telling: 1 violation (het attribuut zonder definitie) |

## 2. De keten op de evalmodellen, zonder assistent

Hier nemen de scripts alle eigen voorstellen over (`bk.py overnemen --alle`), en is gevalideerd met `bk.py valideer`. Zo is te zien wat de scripts zelf opleveren. De verwachte uitkomsten in de [evals](../skills/geonovum-uml2-nl-sbb/evals/) zijn hierop gebaseerd.

| Model | Package | Begrippen | Violations / warnings / info |
|---|---|---|---|
| NEN 3610:2022-template (XMI 1.1) | `NEN3610` | 38 (24 objecttypen, 9 attributen, 5 waarden) | 0 / 10 / 0 |
| IMGeluid 3.1.1 (XMI 1.1) | `IMGeluid` | 388 (44 objecttypen, 11 datatypen, 211 attributen, 122 waarden) | 19 / 2 / 218 |
| IMEV 3.0.2 (EAP in zip) | `IMEV-conceptueel` zonder `deprecated` | 467 (89 objecttypen, 18 datatypen, 168 attributen, 192 waarden) | 8 / 26 / 20 |

De violations zijn begrippen zonder definitie in het UML-model. De warnings bij NEN 3610 komen van de waarden van een waardelijst die geen attribuut gebruikt.

## 3. Regressie tegen eerdere omzettingen

| Model | Uitkomst |
|---|---|
| IMGeo 2.1 | XMI en EAP geven hetzelfde kader: isomorf, 3.997 triples |
| IMGeluid 3.1.1 | `termen.tsv` byte voor byte gelijk aan de eerdere omzetting |
| IMEV 3.0.2 | Gelijk, op twee bewuste wijzigingen na: codes als F4 en GT5 houden hun hoofdletters (17 termen), en 9 contexttermen bij keuze-datatypen hebben geen dubbele woorden meer (*afstand van de overige contour*) |

## 4. Eerdere omzetting van Geonovum-modellen (november 2026)

Met de skill zijn ook de vastgestelde versies uit het [Geonovum-register](https://register.geostandaarden.nl/informatiemodel/) omgezet. Daarna zijn ze vergeleken met de kaders op definities.geostandaarden.nl.

| Model | Bron | Begrippen | Violations / warnings / info | Vergelijking met het gepubliceerde kader |
|---|---|---|---|---|
| IMGeluid 3.1.1 | XMI 1.1 | 388 | 19 / 2 / 218 | 122 van 122 waarden terug; bij elke waarde met een definitie is die gelijk |
| IMEV 3.0.2 | EAP | 465 | 8 / 36 / 20 | 83 van 83 terug, 80 met gelijke definitie (2 verschillen door coderingsfouten in de publicatie) |
| IMKL 3.0.0 | EAP | 201 | 0 / 0 / 163 | 178 van 179 terug, 158 met gelijke definitie |
| IMRO2012 | EAP | 1204 | 1157 / 336 / 1200 | 258 van 262 terug; het UML-model heeft bijna geen definities bij attributen en waarden |
| NEN 3610:2022 | XMI 1.1 | 38 | 0 / 10 / 0 | 38 van 86; het gepubliceerde kader bevat vooral terminologie uit de normtekst |

Gevonden en in de skill opgelost:
- de IMRO-XMI in het register is afgebroken (daarom is de EAP gebruikt);
- access-parser verminkte tekens buiten Latin-1 en liet in IMEV 16 klassen samenvallen;
- XMI 1.1 werd niet gelezen.
