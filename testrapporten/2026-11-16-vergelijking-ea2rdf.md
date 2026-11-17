# Vergelijking met ea2rdf

Datum: 16 november 2026. Skillversie: commit `8e3918f` (gelijk aan `main` na de merge van `notatie-uit`). ea2rdf: versie 1.3.3, commit `5764ed5` van [architolk/ea2rdf](https://github.com/architolk/ea2rdf) (8 juli 2026). Voor de vervolgstap zijn ook [rdf2rdf](https://github.com/architolk/rdf2rdf) 1.6.0 en `ea2mim.yaml` uit [mimtools](https://github.com/architolk/mimtools) gebruikt.

## Opzet

ea2rdf leest een Enterprise Architect-bestand en schrijft de inhoud als RDF. De vraag was hoe de skill zich daartoe verhoudt. Beide zijn gedraaid op de twee standaardtestmodellen van de skill (de evals `nen3610-template-xmi` en `imev-eap`, zie ook het [modeltest-rapport](2026-11-08-modeltest.md)). De bronbestanden kwamen uit het Geonovum-register; de checksums klopten met die in de evals.

| | NEN 3610:2022-template | IMEV 3.0.2 |
|---|---|---|
| Bestand | `NEN3610-2022-template-20221116.xmi` (XMI 1.1) | `IMEV3.0.2_10072025.zip` met `IMEV3.0.2.EAP` (Access/JET 3, 47 MB) |
| Verwachting eval | 38 begrippen (24 objecttypen, 9 attributen, 5 waarden), 0 violations | ±465 begrippen, 8 violations (begrippen zonder definitie) |

**Skill.** De scripts zijn zonder assistent gedraaid: `bk.py start`, `analyseer`, `overnemen --alle`, `genereer` en `valideer`, met de standaardkeuzes en zonder gebruiker. Het package is het scriptvoorstel (NEN 3610: `NEN3610`). Bij IMEV is `IMEV-conceptueel` gekozen zonder `deprecated`, zoals de eval vraagt. De ingevulde voorbeelden (`voorbeelden/*.yaml`) zijn in de hoofdrun niet gebruikt, want ea2rdf heeft ook geen modelkennis. Een tweede run mét voorbeeld staat ter vergelijking in de tabellen. De review en het rapport zijn niet gedraaid: daarvoor is een assistent nodig, en ea2rdf heeft geen tegenhanger.

**ea2rdf.** De code is eerst gelezen: drie Java-klassen (950 regels) die de tabellen van de EA-database lezen en Turtle naar standaarduitvoer schrijven, zonder netwerk of bestandsbewerkingen. Daarna is een JDK 17 en Maven 3.9.9 in een tijdelijke map gezet. De door ea2rdf vereiste fork van Jackcess (een Java-bibliotheek voor Access-bestanden) is gebouwd zonder tests, daarna ea2rdf zelf. Gedraaid met de standaardopties uit de README: `java -jar ea2rdf.jar -ea -e IMEV3.0.2.EAP`. Daarna is als tweede stap `rdf2rdf` met `ea2mim.yaml` gedraaid. Dat is de keten die architolk zelf gebruikt (`mimtools/ea2mim.sh`), en die maakt van de ruwe export een MIM-model in RDF.

## Wat ea2rdf is

ea2rdf is een **verliesvrije export van de EA-database naar RDF**, geen omzetting naar begrippen.

- **Invoer:** `.eap`, `.eapx` en `.mdb` (Access/JET, via Jackcess) en met `-sql` ook `.qea` en `.xea` (SQLite). **Geen XMI.**
- **Uitvoer:** Turtle in een eigen vocabulaire `ea:` (`http://www.sparxsystems.eu/def/ea#`) plus `rdfs:label` en `rdfs:comment`. Elke rij uit `t_package`, `t_object`, `t_attribute`, `t_connector`, de tagged-value-tabellen, `t_xref` en de diagramtabellen wordt een resource. Zonder `-ea` wordt elke tabel generiek geëxporteerd (`db:`-vocabulaire).
- **URI's:** `<urn:object:1234>`, `<urn:attribute:5678>` enz., op de interne database-id. De EA-GUID staat erbij als `ea:guid`.
- **Geen** SKOS, SHACL of NL-SBB. Semantiek komt pas in vervolgstappen:
  - `ea2mim.yaml` (78 SPARQL-updates) maakt er MIM-RDF van, met `mim:Objecttype`, `mim:Attribuutsoort`, `mim:Enumeratiewaarde`, `mim:definitie` en URI's `urn:uuid:<GUID>`.
  - `mim2onto.yaml` maakt daarvan een OWL/SHACL-ontologie; andere scripts maken diagrammen (GraphML) en Markdown.

## Resultaten

### Draaien

| | Skill | ea2rdf |
|---|---|---|
| NEN 3610 (XMI) | Gelukt | **Niet mogelijk**: ea2rdf leest geen XMI. Een EAP-versie van het template staat niet in het register. |
| IMEV (EAP in zip) | Gelukt; de zip pakt het script zelf uit | Gelukt na handmatig uitpakken |
| Installatie | Python-venv met 5 pakketten van PyPI | JDK, Maven, en een eigen build van de Jackcess-fork (de gepubliceerde Jackcess-versie volstaat volgens de README niet voor EAP met JET 3) |
| Op Windows | `valideer` liep vast op een tijdelijk bestand (zie "Bevindingen over de skill"); met een vooraf opgehaald profiel ging het goed | Uitvoer standaard in cp1252, wat ongeldige Turtle gaf; goed met `-Dfile.encoding=UTF-8 -Dsun.stdout.encoding=UTF-8` |

### IMEV: hetzelfde model gelezen

Beide lezen hetzelfde: binnen `IMEV-conceptueel` zonder `deprecated` vindt ea2rdf precies de 136 klassen en 423 attributen en waarden die `bk.py start` meldt. De verschillen zitten in de details.

| | Skill (access-parser) | ea2rdf (Jackcess) |
|---|---|---|
| Memoveld definitie `OpslagOntplofbaarMilitair_TeBerekenenAfstand` | **Onleesbaar**, als leeg behandeld (LET OP) | Gelezen: "Opslaan en bewerken van ontplofbare stoffen … met een te berekenen afstand." |
| `ea_guid` in `t_object` | 16 onleesbaar; id uit `Object_ID` (LET OP) | Alle 256 objecten hebben een GUID |
| Memovelden `t_connector` | 6 onleesbaar | Alle gelezen |
| Tekenset | Geen mojibake; HTML-entiteiten (`&#235;`) omgezet | Standaard (`-ea`): 25 keer mojibake (`reÃ«le`, `Ã©Ã©n`); met `-0`: 37 vervangingstekens. Entiteiten als `&#171;` en `&#239;` blijven staan. |
| Leestijd IMEV | `start` 4–6 s (inclusief uitpakken) | 1,5 s |

### IMEV: wat eruit komt

Aantallen per soort. "Bron" telt de elementen in de scope. "Skill" telt de begrippen in `uit/kader.ttl`. ea2rdf en ea2mim nemen het hele bestand mee, dus ook GML, NEN 3610 en `deprecated`.

| Soort | Bron (scope) | Skill, standaard | Skill, met voorbeeld | ea2rdf (`ea:`) | ea2mim (`mim:`) |
|---|---|---|---|---|---|
| Objecttypen | 88 + 1 extern | 89 `skos:Concept` | 89 | 256 `ea:Object` (alle soorten, ook notities en packages) | 125 `mim:Objecttype` |
| Datatypen | 18 | 18 `skos:Concept` | 18 | (in `ea:Object`) | 21 primitief, 7 gestructureerd, 13 keuze |
| Waardelijsten | 29 | 28 `skos:Collection` (1 leeg) | 28 | (in `ea:Object`) | 43 `mim:Enumeratie`, 3 `mim:Codelijst` |
| Attributen | 210 | 168 `skos:Concept` (gelijke naam en definitie samengevoegd) | 168 | 695 `ea:Attribute` (attributen en waarden samen) | 164 `mim:Attribuutsoort`, 19 `mim:DataElement` |
| Waarden | 213 | 191 `skos:Concept` ("gegeven in transitie" is één begrip in 20 collecties) | 189 | (in `ea:Attribute`) | 278 `mim:Enumeratiewaarde` |
| Generalisaties | 146 (hele bestand) | 87 `skos:broader` | | 146 `ea:Connector` | 146 `mim:Generalisatie` |
| Associaties | 8 (hele bestand) | Niet omgezet | | 8 `ea:Connector` | 1 relatiesoort, 7 relatierollen |
| Diagrammen | 77 (hele bestand) | Niet omgezet | | 77 diagrammen, 1731 objecten, 1253 lijnen, met posities en kleuren | 74 `mim:Diagram` |
| **Totaal** | | **466 begrippen**, 4567 triples | 464 begrippen, 4498 triples | 50.187 triples | 19.304 triples |

### NL-SBB

| Eis | Skill (IMEV) | ea2rdf / ea2mim |
|---|---|---|
| `skos:ConceptScheme` met titel | Ja, URI `http://definities.geostandaarden.nl/imevconceptueel` | Nee |
| `skos:Concept` met `skos:prefLabel` | 466, termen in kleine letters met spaties (`gegeven in transitie`); UML-naam als `altLabel` | Nee; alleen `rdfs:label` en `mim:naam` met de UML-naam |
| `skos:definition` | 458 (8 elementen hebben in het model geen definitie) | `rdfs:comment` / `mim:definitie` met de hele notitie. In 49 definities blijft de sectie `--Regels--` staan. |
| `skos:scopeNote` | 121, uit de sectie `--Toelichting--` en de toelichting-tag | Nee (in de ea2mim-uitvoer van IMEV één `mim:toelichting`) |
| `dct:source` | 446 begrippen met een bron (22 bronresources) | `mim:herkomst` en `mim:herkomstDefinitie` als tekst |
| `skos:broader` / `related` / topbegrippen | 87 / 846 (bij 429 begrippen) / 20 | `mim:supertype` en `mim:attribuut`, geen SKOS-relaties |
| `skos:Collection` per waardelijst | 28, met `skos:member` | Nee (`mim:Enumeratie` met `mim:waarde`) |
| `skos:notation` | 516, bij elk begrip; bij waarden de code met de waardelijst als datatype | Nee |
| **SHACL** (NL-SBB 1.0.0 + extensie van de skill) | 8 violations, 24 warnings, 20 info (verwacht: 8 violations) | **Conform, maar betekenisloos**: er is geen enkel `skos:Concept`, dus het profiel toetst niets |
| SHACL, NEN 3610 | 0 violations, 10 warnings, 0 info | Niet gedraaid (geen XMI) |

De warnings van de skill bij IMEV zijn 20 keer dezelfde definitie bij verschillende begrippen (bijvoorbeeld *aardgas* en *natural gas*) en twee verweesde waarden. Met het ingevulde voorbeeld zijn het er 34: het voorbeeld splitst meer waarden, waardoor 10 waarden zonder relatie blijven.

### URI's, packages en basismodellen

| | Skill | ea2rdf / ea2mim |
|---|---|---|
| URI-strategie | HTTP-URI's: `{kader}/id/begrip/{PascalCase van de term}`, collecties op UML-naam. Een al gepubliceerd kader houdt zijn URI's (`uris.bestaand`). URI's resolven pas na publicatie. | `urn:object:<database-id>` (verandert bij een nieuwe export of een ander bestand) en in ea2mim `urn:uuid:<EA-GUID>` (stabiel, maar niet resolvebaar) |
| Packagekeuze | `start` toont de boom en stelt een package voor; `--package` en `--zonder` | Geen: altijd het hele bestand, met `ea:parent` voor de boom |
| Basismodellen (NEN 3610, GML) | Weggelaten; superklassen buiten de scope via `externe_superklasse_op_naam` en de NEN 3610-matches (`externe_kaders`) | Meegenomen als gewone objecten |
| Tag `begrip` (MIM: koppeling naar een bestaand begrip) | Niet gebruikt | Overgenomen als `mim:begrip`. In IMEV staan alle 34 in het ingesloten NEN 3610-package, dus niet in de scope van deze test. |

### Waardelijsten en notaties

| | Skill | ea2rdf / ea2mim |
|---|---|---|
| Waarden | Begrip per waarde. Gelijke naam en definitie = één begrip, lid van meerdere collecties. Bijna gelijke definities = voorstel `zelfde_begrip`. Andere definitie = splitsen of stoppen. | Elke waarde apart, per lijst: "gegeven in transitie" staat 20 keer in de scope; ea2mim maakt er 22 losse waarden van (hele bestand) |
| Code | `skos:notation` met de code, getypeerd met de collectie (instelbaar: `code`, `afwijkend`, `tag`, `geen`) | Naam en definitie per waarde, geen code of notatie in SKOS-zin |
| Extern beheerde lijsten | `bk.py waarden` haalt XML/CSV/TSV op | Nee |

### Automatisering, interactie en snelheid

| | Skill | ea2rdf |
|---|---|---|
| Aanroepen tot resultaat | IMEV: `start` (twee keer, eerst voor de packageboom), `analyseer`, `overnemen --alle`, `analyseer`, `genereer` | Eén commando (plus `ea2mim` voor MIM) |
| Keuzes | 6 tot 8 beslispunten per model (wortel, alias, bronnen, splitsen, codes, kader-URI …). Zonder gebruiker neemt `overnemen --alle` de voorstellen over en legt dat vast. | Geen. De interpretatie zit vast in de SPARQL van `ea2mim.yaml`. |
| Scripttijd IMEV | ±20 s tot en met `genereer`; `valideer` 158 s | 1,5 s export + 3,5 s ea2mim |
| Met assistent | Review van alle begrippen en rapport: volgens het modeltest-rapport 6 tot 18 minuten voor IMEV | Niet van toepassing |
| Uitleg van keuzes | `uit/beslissingen.md` (55 regels bij IMEV), `werk/aannames.md`, rapport | Logregels per SPARQL-query |

## Wat ea2rdf beter doet

1. **Het leest EAP-bestanden vollediger.** Jackcess leest het memoveld en de 16 GUID's die de access-parser van de skill niet leest. Bij IMEV mist het kader van de skill daardoor één definitie, en 16 begrippen krijgen een id uit de database in plaats van de GUID.
2. **Het verliest niets.** Associaties, rollen, kardinaliteiten, alle tagged values en de diagrammen met posities en kleuren komen mee. De skill neemt alleen mee wat een begrip wordt.
3. **Scheiding tussen lezen en interpreteren.** De ruwe export staat los van de interpretatie, en die interpretatie is declaratief: SPARQL in YAML. Wie wil weten waarom iets een `mim:Objecttype` wordt, leest één query.
4. **Snel en deterministisch**, zonder keuzes: geschikt voor een pijplijn (CI, nachtelijke export).
5. **Breder bruikbaar.** Dezelfde export voedt MIM-validatie, een OWL/SHACL-ontologie, diagrammen en documentatie.

## Wat de skill beter doet

1. **Het eindproduct is een NL-SBB-begrippenkader.** ea2rdf en ea2mim leveren geen enkel `skos:Concept`, dus de NL-SBB-validatie toetst niets.
2. **Termen volgens de conventies**: kleine letters, spaties, alias als voorkeursterm, en objecttype-context bij attributen met dezelfde naam maar een andere betekenis.
3. **Definities netjes gescheiden**: definitie, toelichting en regels. In ea2mim staat `--Regels--` nog in 49 definities.
4. **Gelijke waarden samengevoegd**: "gegeven in transitie" is één begrip in 20 collecties, niet 20 losse waarden.
5. **XMI én EAP**, ook in een zip, met packagekeuze en het weglaten van basismodellen.
6. **Bruikbare URI's**: HTTP, op de term, met behoud van gepubliceerde URI's.
7. **Tekst zonder coderingsfouten**, en LET OP-meldingen wanneer iets niet leesbaar is. ea2rdf meldt een onleesbaar veld niet; het schrijft wat Jackcess teruggeeft.
8. **Verantwoording**: beslispunten, aannames, SHACL-rapport, review en rapport.

## Ideeën voor de skill

| Idee | Waarom | Grootte |
|---|---|---|
| Jackcess (of ea2rdf-uitvoer) als alternatieve EAP-lezer: `bk.py start model-ea.ttl` leest een ea2rdf-export | Lost het onleesbare memoveld en de ontbrekende GUID's op, zonder eigen Java-code in de skill. Bij een LET OP kan `start` deze route noemen. | Middel |
| De tag `begrip` (MIM) gebruiken als `skos:exactMatch`, of als URI-voorstel bij `uris.bestaand` | Het model zegt dan zelf welk gepubliceerd begrip bedoeld is | Klein |
| Associaties (relatiesoorten) als `skos:related` tussen objecttypen, of als begrip | Het IMEV-bestand heeft 8 associaties met rolnamen (zoals *voertUit*, *hoortBij*); zulke relaties ontbreken nu in het kader | Klein tot middel |
| De mapping van stereotypen en relaties declaratief maken (zoals `ea2mim.yaml`) | Transparanter dan Python. Maar `standaardkeuzes.yaml` doet dit al voor een groot deel, dus de winst is beperkt. | Groot, lage prioriteit |
| HTML-entiteiten en mojibake ook blijven controleren bij nieuwe lezers | ea2rdf laat zien hoe makkelijk dit misgaat | Klein (test) |

## Bevindingen over de skill

- **Op Windows faalt `bk.py valideer`** bij het ophalen van het SHACL-profiel. `kern.curl_status` opent een `NamedTemporaryFile` en laat curl daarin schrijven. Op Windows mag een tweede proces dat bestand niet openen zolang het open is: `PermissionError`. Omweg in deze test: het profiel vooraf in `werk/skos-ap-nl.ttl` zetten. Dit raakt elke download via `haal` (ook `waarden` en `bestaand`).
- Begrip-URI's kunnen niet-ASCII-tekens bevatten, zoals `nen3610:ReëelObject`. Dat is een geldige IRI, maar niet elke tool gaat er goed mee om.

## Conclusie

ea2rdf en de skill zijn geen concurrenten maar opeenvolgende stappen. ea2rdf is een snelle, verliesvrije export van een EA-database naar RDF, met MIM-RDF als vervolg. De skill maakt van een UML-model een NL-SBB-begrippenkader. Op IMEV lezen beide precies dezelfde 136 klassen en 423 attributen en waarden. Alleen de skill levert begrippen (466), collecties (28) en een SHACL-uitslag die iets zegt (8 violations, zoals verwacht). ea2rdf leest de EAP beter: het memoveld en 16 GUID's die de skill mist, leest ea2rdf wel. Daar staan coderingsfouten tegenover (25 keer mojibake), geen XMI-ondersteuning, en een bewerkelijke installatie met een eigen Jackcess-build. Het meest bruikbare idee om over te nemen is ea2rdf-uitvoer als alternatieve invoer voor `bk.py start`, als terugvaloptie bij onleesbare velden.

## Beperkingen

- ea2rdf is alleen op IMEV gedraaid. NEN 3610 bestaat alleen als XMI, en die kan ea2rdf niet lezen.
- De skill is zonder assistent gedraaid, tot en met `genereer` en `valideer`. De review en het rapport zijn niet getest; daarvoor zie het [modeltest-rapport](2026-11-08-modeltest.md).
- De tijden zijn van één run op één Windows-laptop. Voor ea2rdf zijn JDK 17 en Maven 3.9.9 gebruikt; de Jackcess-fork is gebouwd zonder tests (`-DskipTests`). De aanpassingen in die fork die tests betreffen, doen er dan niet toe; de aanpassing die wel telt (de `FallbackTableFinder`) zit in de gewone code.
- De vergelijking op aantallen is grof: ea2rdf telt databaserijen, de skill telt begrippen. Gelijke aantallen per soort zeggen niets over de kwaliteit van definities of termen.
- Op Windows moest de skill met een omweg valideren (zie "Bevindingen over de skill"), en ea2rdf met extra Java-opties voor UTF-8.
- `mim2onto` en de andere vervolgstappen van architolk (ontologie, GraphML, Markdown) zijn niet gedraaid.
