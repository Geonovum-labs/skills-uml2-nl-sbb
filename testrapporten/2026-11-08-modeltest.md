# Modeltest: drie modelgroottes

Datum: 8 november 2026. Skillversie: de versie van 0.0.1, vóór en na de verbeteringen uit deze test.

## Opzet

Getest zijn drie taalmodellen van één aanbieder, in oplopende grootte en prijs: **klein**, **middel** en **groot**. Elk model kreeg dezelfde opdracht: zet het model om met de skill, zonder gebruiker om vragen te beantwoorden. De opdracht omvatte de volledige werkwijze, inclusief de review van alle begrippen en een rapport met conclusie. De optionele modules (matches, vergelijking, bronnencontrole) vielen erbuiten.

Uit de testkopie van de skill zijn de voorbeeldbestanden van de twee testmodellen (`voorbeelden/imev.yaml` en `voorbeelden/nen3610.yaml`) gehaald, zodat geen model het antwoord kon overnemen.

**Referentie.** Elk resultaat is vergeleken met een kader dat tijdens de ontwikkeling van de skill met dezelfde scripts is gemaakt, met keuzes die met de hand zijn beoordeeld. Dat is een goede vergelijkingsbasis, maar geen door een domeinexpert gecontroleerde waarheid.

| | NEN 3610:2022-template (XMI 1.1) | IMEV 3.0.2 (EAP in zip) |
|---|---|---|
| Omvang | 38 begrippen | ±465 begrippen, 19 reviewdelen |
| Moeilijk | Packagekeuze: het bestand bevat ook een voorbeeldmodel (IMGolf) met kopieën van NEN 3610-klassen | Packagekeuze; de waarde "gegeven in transitie" staat in 19 lijsten met bijna gelijke definities; een memoveld is onleesbaar |

De testcases staan als eval in [`skills/geonovum-uml2-nl-sbb/evals/`](../skills/geonovum-uml2-nl-sbb/evals/).

## Ronde 1: de skill vóór de verbeteringen uit deze test

| | Klein | Middel | Groot |
|---|---|---|---|
| **NEN 3610** | | | |
| Package | **fout**: IMGolf (het voorbeeldmodel) | NEN3610 | NEN3610 (probeerde eerst ook IMGolf, zag een URI-botsing en herstelde dat) |
| Begrippen gelijk aan referentie | 7 van 38 (ander model) | **38 van 38** | 36 van 38 (2 eigen termcorrecties) |
| SHACL violations / warnings / info | 4 / 2 / 5 | 0 / 10 / 0 | 0 / 10 / 0 |
| Review ok / term / definitie / twijfel | 24 / 3 / 16 / 0 | 33 / 0 / 3 / 2 | 29 / 0 / 5 / 4 |
| Tijd, tokens, tool-aanroepen | 3,1 min, 112k, 30 | **1,4 min, 74k, 16** | 4,6 min, 110k, 33 |
| **IMEV** | | | |
| Package | goed (dezelfde 136 klassen) | goed | goed |
| Begrippen (referentie 465) | 486 | 486 | 463 |
| "gegeven in transitie" | scriptvoorstel gevolgd: 19 bijna gelijke begrippen | idem | **zelf afgeweken**: één begrip |
| SHACL violations / warnings / info | 8 / **370** / 20 | 8 / **370** / 20 | 8 / 18 / 20 |
| Review ok / term / definitie / twijfel | 193 / 145 / 133 / 15 | 182 / 187 / 115 / 2 | 240 / 8 / 212 / 3 (na 174 eigen termcorrecties) |
| Gemiddelde lengte reviewopmerking | 98 tekens | 80 | 116 |
| Tijd, tokens, tool-aanroepen | 6,7 min, 202k, 55 | 6,4 min, 159k, 36 | 17,6 min, 286k, 74 |
| **Alle runs** | `status` meldde KLAAR, de review dekte 100% van de begrippen, de conclusie was ingevuld, de aannames waren vastgelegd, en niemand bewerkte het kader met de hand. | | |

## Ronde 2: het kleine model met de verbeterde skill

| | NEN 3610 | IMEV |
|---|---|---|
| Package | **NEN3610 (goed)** | goed |
| Begrippen gelijk aan referentie | **38 van 38** | 463 van 467. Verschil: twee waarden "overig" zijn automatisch gesplitst, waar de referentie een eigen term gebruikt. |
| SHACL violations / warnings / info | 0 / 10 / 0 | 8 / **26** / 20 |
| Review ok / term / definitie / twijfel | 30 / 0 / 8 / 0 | 174 / 147 / 145 / 1 |
| Tijd, tokens, tool-aanroepen | 1,6 min, 84k, 20 | 7,4 min, 202k, 48 |

Met de verbeterde skill haalt het kleine model op beide testmodellen hetzelfde kader als de grotere modellen, en op NEN 3610 precies de referentie. Het middelgrote en het grote model zijn niet opnieuw gedraaid.

## Kwaliteitsverschillen

**Wat alle drie goed doen** (dankzij de scripts):
- Ze voltooien het proces zonder iets over te slaan: de compleetheidscontrole van de review laat geen gaten toe.
- De cijfers in het rapport kloppen, omdat het script ze schrijft. Het model schrijft alleen de conclusie.
- Geen enkel model heeft het kader met de hand bewerkt.

**Waar ze verschillen: het oordeel bij keuzes die het script niet maakt.**

- **Klein** volgt de instructies letterlijk.
  - In ronde 1 koos het het verkeerde package: de regel "niet NEN 3610" nam het te letterlijk. Met het packagevoorstel uit de bestandsnaam en een scherpere regel ging het in ronde 2 goed.
  - De review is degelijk en vindt echte problemen, zoals een definitie die naar het verkeerde risico verwijst en dubbele woorden in contexttermen. Wel markeert het relatief veel termen als fout.
  - Per token het goedkoopst, maar het gebruikt evenveel tokens als het middelgrote model en meer tool-aanroepen.
- **Middel** is het snelst en zuinigst, en koos de packages direct goed.
  - Het neemt scriptvoorstellen over zonder het effect te toetsen: 370 SHACL-warnings leidden niet tot een andere keuze.
  - Het markeert de meeste termen als fout (187), ook de contexttermen die het script bewust zo maakt.
- **Groot** is het meest zelfstandig.
  - Het zag het effect van het splitsvoorstel en week terecht af. Het ontdekte de URI-botsing met IMGolf, en schreef de uitgebreidste reviewopmerkingen.
  - Het ging ook verder dan gevraagd: zonder gebruiker voerde het 174 termcorrecties door (bv. *accetone* → *aceton*). Inhoudelijk zijn dat meestal verbeteringen, maar zulke beslissingen horen bij de gebruiker.
  - Het is 2,5 tot 3 keer zo duur en traag als het middelgrote model.

**Conclusie.** Dankzij de scripts en de review in delen is de *compleetheid* voor alle drie gelijk. De kwaliteit verschilt in het oordeel bij keuzes die niet in een script te vangen zijn. Elk verschil uit ronde 1 is omgezet in een beter scriptvoorstel of een scherpere regel, waarna ook het kleine model hetzelfde kader haalde. Voor de inhoudelijke review blijft een groter model beter, en voor termcorrecties en matches blijft een domeinexpert nodig.

## Wat deze test aan de skill heeft veranderd

| Bevinding | Aanpassing |
|---|---|
| Het kleine model koos het voorbeeldmodel IMGolf | `bk.py start` stelt een package voor op basis van de bestandsnaam. De regel over basismodellen heeft een uitzondering voor het model zelf. |
| Het splitsvoorstel gaf 19 bijna gelijke begrippen | Waarden met bijna gelijke definities (gelijkenis ≥ 0,8) worden als `zelfde_begrip` voorgesteld |
| `review --opnieuw` wiste alle oordelen | Oordelen van begrippen met dezelfde definitie blijven staan; een gecorrigeerde term wordt opnieuw beoordeeld |
| Veel vrijwel gelijke waarden één voor één invullen | `bk.py oordeel` accepteert een reeks (`0101-0112 ok \| …`, hoogstens 25) |
| Het signaal "definitie begint met de term" gaf veel ruis | Het signaleert nu alleen korte definities die vooral de term herhalen (IMEV: van 91 naar 68 signalen) |
| altLabel@en bij Nederlandse UML-namen | MIM-modellen krijgen het voorstel `alias_naam_als_altlabel: null` |
| Codes als F4 en GT5 werden *f4* en *gt5* | Hoofdletter plus cijfer blijft staan |
| Een sleutel met een punt kon niet in `bk.py zet` | `bk.py zet 'termen.vast[Naam.x]' …` |
| `review klaar` moest twee keer draaien; de volgende stap na `overnemen` was inconsistent | Opgelost |
| Termcorrecties zonder gebruiker doorgevoerd | SKILL.md: zonder gebruiker geen termcorrecties doorvoeren, alleen rapporteren |
| Contexttermen bij een keuze-datatype, zoals *afstand afstand of geometrie van de overige contour* (alle drie de modellen vonden deze) | Is het attribuut een van de alternatieven, dan wordt het *afstand van de overige contour*. Per klasse corrigeren kan met `attributen.term_correcties['Klasse.attribuut']`. |

**Nog open.** `termen.vast` werkt op de UML-naam, dus gelijknamige klassen in verschillende packages kun je niet apart benoemen.

## Beperkingen

- Eén run per model per testmodel; de spreiding tussen runs is niet gemeten.
- Het middelgrote en het grote model zijn niet opnieuw getest met de verbeterde skill.
- De kwaliteit van de review is met steekproeven beoordeeld, niet per begrip.
- Er was geen gebruiker in de test; het voorleggen van vragen is niet getest.
- Alle modellen zijn van één aanbieder. Een status boven `concept` vraagt een test met minstens twee assistenten, waarvan één open source of Europees.
