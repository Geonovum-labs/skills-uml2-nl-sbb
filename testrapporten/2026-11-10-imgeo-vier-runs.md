# Vier testruns op IMGeo 2.2

Datum: 10 november 2026. Skillversie: 0.0.1, vóór de verbeteringen uit dit rapport.

## Opzet

Vier taalmodellen van twee aanbieders hebben de skill in dezelfde agentomgeving uitgevoerd op IMGeo 2.2 ([XMI uit het register](https://register.geostandaarden.nl/informatiemodel/imgeo/2.2/), sha256 `3f621ded…9123`), zonder gebruiker. De opdracht omvatte ook de vergelijking met het [gepubliceerde kader](https://upload.begrippenxl.nl/storage/imgeo/imgeo.ttl). Elk model leverde de uitkomst en eigen verbetervoorstellen aan als pull request (#3 t/m #6).

| Run | Model |
|---|---|
| A | groot (de grootste van de vier) |
| B | middel |
| C | groot, open gewichten |
| D | klein en snel |

**Referentie.** Twee runs met alleen de scripts, op hetzelfde bestand:
- met het voorbeeld `voorbeelden/imgeo.yaml`: 393 begrippen, SHACL run B 0 / 26 / 2;
- zonder voorbeeld, alle scriptvoorstellen overgenomen: 396 begrippen, 0 / 168 / 2.

## Resultaat

| | A | B | C | D |
|---|---|---|---|---|
| Basis | voorbeeld | voorbeeld | scriptvoorstellen | scriptvoorstellen |
| Kader tegenover de referentie | voorbeeld, maar de koppelingen van waardelijsten weer overschreven (300 `skos:related` minder) | gelijk, plus 7 termcorrecties | gelijk, plus 38 termcorrecties | gelijk |
| SHACL run B (V / W / I) | 13 / 180 / 2 | 13 / 46 / 2 | 0 / 168 / 2 | 0 / 72 / 0 |
| Review ok / term / definitie | 384 / 0 / 9 | 383 / 7 / 3 | 351 / 38 / 7 | 396 / 0 / 0 |
| Vergelijking met de publicatie | 444 van 464 gekoppeld | idem | idem | idem |

- **Violations bij A en B.** De 13 violations komen doordat de externe kaders in die omgeving HTTP 403 gaven. Met de kaders erbij zijn het er 0.
- **Kaders.** Elk kader is precies wat de scripts maken; geen model schreef zelf Turtle. De verschillen zitten in de keuzes, de review en de rapportage.
- **Review.**
  - **C** vond met de review twee fouten in de scripts: *type scheiding scheiding* en *IM geo-object*. Eén eigen correctie was fout: *meer of plas, ven of vijver*.
  - **B** vond 7 termproblemen, met één discutabele correctie: *brandkraan of brandkraanput*, waar *brandput* bedoeld is.
  - **A** keurde termen met leestekens goed als "deel van de bronterm".
  - **D** keurde alles goed, ook *status IM geo-object IM geo-object*. Bij 42 signalen stonden maar vier verschillende standaardzinnen.
- **Rapportage.**
  - **B en C** volgden de afspraken, en hun cijfers kloppen.
  - **A** voegde een vergelijking van modellen toe die niet gedraaid zijn, met productnamen.
  - **D** zette de bestanden op een verkeerde plek, committe het bronmodel en noemde cijfers die niet uit de run komen.

## Verbetervoorstellen van de modellen

| Voorstel | Van | Besluit |
|---|---|---|
| SHACL-extensie ontbreekt na installatie | A, B, C, D | Overgenomen: `valideer` haalt een kopie op en meldt het duidelijk |
| `project.yaml` alleen-lezen na kopiëren van een voorbeeld | A, B | Overgenomen: schrijfrechten bij schrijven; nieuw commando `bk.py voorbeeld` |
| `zet` met dubbele punt in de waarde | A | Overgenomen |
| `vergelijk` komt niet in het rapport; herhaalde regels | B, A, D | Overgenomen: `uit/vergelijking.txt`, gegroepeerde regels |
| Violations door onbereikbare kaders apart tellen | B | Overgenomen |
| Reviewnummers verschuiven na opnieuw genereren | B | Overgenomen: vaste `id` per begrip |
| `rapport` overschrijft eigen toevoegingen | B | Overgenomen: `werk/rapport-aanvulling.md` |
| Profiel in `werk/` in plaats van `reports/` | B | Overgenomen |
| Dubbele context, *IM geo-object* (uit de review van C) | C | Overgenomen: vaste regel in het script |
| Termvoorstel bij leestekens | A, B, C | Overgenomen als hint bij het signaal |
| Automatisch `ok`, of alleen begrippen met signalen reviewen | A, D | Niet overgenomen: compleetheid gaat voor; run D laat zien waarom |
| Andere wortel, prefixen standaard laten staan, `zelfde_begrip` voor attributen, URI-mapping | D | Niet overgenomen: staat al goed in het voorbeeld, of past niet bij de werking |
| Voorbeeld voor IMGeo 2.2 | A, B | Niet nodig: het bestand in het register geeft met het bestaande voorbeeld hetzelfde kader |
| Vergelijking over meerdere kaders | A | Later |

**Eigen bevinding.** Runs C en D gebruikten het IMGeo-voorbeeld niet, en D stelde voor een voorbeeld toe te voegen dat al bestond. `bk.py start` noemt daarom nu een passend voorbeeld.

## Na de verbeteringen

| Model | Uitkomst |
|---|---|
| IMGeo 2.2, zonder voorbeeld | De zes termen met dubbele context en *IM geo-object* zijn nu goed: *type scheiding (plus)*, *status IMGeo-object (plus)*, *IMGeo-object*. Dit zijn dezelfde correcties die run C met de hand deed. |
| IMGeo 2.2, met voorbeeld | Gelijk aan eerder: 393 begrippen, 0 / 26 / 2 |
| NEN 3610, IMGeluid, IMEV | Ongewijzigde termen |
| Voorbeeld bij `start` | Herkend bij alle vier de modellen |
| Ontbrekende SHACL-extensie | Getest door de map `shacl/` weg te halen: de kopie wordt gebruikt, met een melding |
| Tests | 22 tests, allemaal geslaagd (was 15) |

## Beperkingen

- Eén run per model. De koppeling van run naar model is door de tester opgegeven; alleen run A noemde zelf zijn model.
- De runs zijn niet opnieuw gedraaid met de verbeterde skill.
