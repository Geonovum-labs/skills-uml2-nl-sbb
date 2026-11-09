# UML-naar-NL-SBB-skill

Agent-skill van [Geonovum](https://www.geonovum.nl) die een UML-informatiemodel omzet naar een begrippenkader volgens [NL-SBB](https://docs.geostandaarden.nl/nl-sbb/nl-sbb/), de Nederlandse standaard voor het beschrijven van begrippen.

Een agent-skill is een map met een instructiedocument (`SKILL.md`) dat een AI-assistent erbij pakt zodra het onderwerp langskomt. De metadata staat in `publiccode.yml` en in de frontmatter van de skill; de status staat in `nl.gov.status`.

> **Let op.** De skill is een hulpmiddel en geen officieel product van Geonovum. Een begrippenkader dat ermee is gemaakt, voldoet niet vanzelf aan NL-SBB, en de definities blijven die van het bronmodel. Zie [DISCLAIMER.md](DISCLAIMER.md).

## Skills

| Skill | Status | Doel |
| --- | --- | --- |
| [`geonovum-uml2-nl-sbb`](skills/geonovum-uml2-nl-sbb/SKILL.md) | concept | Zet een UML-model in XMI (1.1 of 2.x) of een Enterprise Architect-bestand (.eap, .eapx, .qea, .qeax, ook in een zip) om naar een NL-SBB-begrippenkader in Turtle. Objecttypen, datatypen, attributen en waarden uit waardelijsten worden begrippen, waardelijsten worden collecties. Met vaste standaardkeuzes, SHACL-validatie, een inhoudelijke review in delen en een rapport. |

De status `concept` betekent dat de skill nog niet is vastgesteld. Een hogere status vraagt een expertreview, een gepubliceerde reviewprocedure met acceptatiecriteria, en een test met minstens twee assistenten waarvan één open source of Europees.

## Installeren

Kopieer de map `skills/geonovum-uml2-nl-sbb/` naar de skillmap van je assistent. Welke map dat is, staat in de documentatie van de assistent.

De repository is ook ingericht als plugin `geonovum-uml2-nl-sbb`, met manifesten per assistent in de verborgen mappen. Zodra de skill via de [skills-marketplace van developer.overheid.nl](https://github.com/developer-overheid-nl/skills-marketplace) wordt aangeboden, staan de installatie-instructies per assistent in de README van die marketplace.

Nodig: Python 3.10 of nieuwer, en `curl` voor het ophalen van het SHACL-profiel en externe kaders. De skill maakt bij de eerste stap een virtuele omgeving in de werkmap en installeert daarin [lxml](https://lxml.de), [rdflib](https://rdflib.readthedocs.io), [pySHACL](https://github.com/RDFLib/pySHACL), PyYAML en [access-parser](https://github.com/ClarotyICS/access_parser) (voor .eap en .eapx).

## Gebruik

Vraag je assistent om een model om te zetten, bijvoorbeeld: "Zet IMGeluid_v3_1_1.xmi om naar een begrippenkader volgens NL-SBB." De skill werkt in een eigen werkmap. Alle vaste stappen lopen via één script, `scripts/bk.py`. Na elke stap noemt `bk.py status` de volgende:

1. **`start`**: maakt een inventaris van het model. Bevat het bestand meer modellen (bijvoorbeeld NEN 3610, GML of een voorbeeldmodel), dan toont het script de packageboom met een voorstel, en kiest de gebruiker de package(s).
2. **`analyseer`**: zet op een rij wat de standaardkeuzes regelen (INFO) en waar een beslissing nodig is (VRAAG), met bij elke VRAAG een voorstel van het script. De assistent legt die voor; `overnemen` en `zet` leggen het antwoord vast in `project.yaml`, en `controleer` toetst dat bestand.
3. **`genereer`**: maakt `uit/kader.ttl`, een lijst van alle termen en een log van samenvoegingen en splitsingen. De assistent schrijft zelf nooit Turtle.
4. **`valideer`**: SHACL-validatie tegen het [NL-SBB-profiel 1.0.0](https://register.geostandaarden.nl/shacl/nl-sbb/1.0.0/skos-ap-nl.ttl) plus een extensie, met de telling per ernstniveau.
5. **`review`**: verdeelt alle begrippen in delen van 25, met signalen van het script per begrip. De assistent geeft elk begrip een oordeel (`ok`, `term`, `definitie` of `twijfel`). `review klaar` rondt pas af als elk begrip beoordeeld is.
6. **`rapport`**: schrijft het rapport met alle cijfers. De assistent vult alleen de conclusie in.

Optioneel, na een vraag aan de gebruiker: harmonisatierelaties naar externe kaders (`matches`), een vergelijking met een gepubliceerd kader (`vergelijk`), en een bronnencontrole (`bronnen`).

De standaardkeuzes staan in [`standaardkeuzes.yaml`](skills/geonovum-uml2-nl-sbb/standaardkeuzes.yaml), met uitleg per keuze in [`references/keuzes.md`](skills/geonovum-uml2-nl-sbb/references/keuzes.md). Ingevulde projectbestanden voor IMGeo, IMGeluid, IMEV, IMKL, IMRO en NEN 3610 staan in [`voorbeelden/`](skills/geonovum-uml2-nl-sbb/voorbeelden/).

## Relatie tot de bronnen

| Bron | Rol |
| --- | --- |
| [NL-SBB](https://docs.geostandaarden.nl/nl-sbb/nl-sbb/) | Hoe begrippen, begrippenkaders en collecties worden beschreven (`nl.gov.source`) |
| [SHACL-profiel NL-SBB 1.0.0](https://register.geostandaarden.nl/shacl/nl-sbb/1.0.0/skos-ap-nl.ttl) | Normatieve validatie; de skill haalt het bij elke validatie uit het register |
| [MIM](https://docs.geostandaarden.nl/mim/mim/) | Stereotypen en notitiestructuur van de meeste Geonovum-modellen |
| [SKOS](https://www.w3.org/TR/skos-reference/) en [ISO 25964](https://www.iso.org/standard/53657.html) | Vocabulaire van het begrippenkader |

[`shacl/skos-ap-nl-extensie.ttl`](skills/geonovum-uml2-nl-sbb/shacl/skos-ap-nl-extensie.ttl) is een kopie van de extensie uit de NL-SBB-reviewskill van Geonovum ([Geonovum/skills-nl-sbb](https://github.com/Geonovum/skills-nl-sbb)). Die extensie controleert regels die het profiel niet afdekt, zoals een topbegrip met een bovenliggend begrip en een dubbele notatie. Voor de inhoudelijke review sluit deze skill aan op die reviewskill.

## Testen

- **[`tests/`](tests/)**: offline tests van de scripts op een fictief testmodel, zonder assistent. Draai ze met:

  ```bash
  python3 -m unittest discover -s tests -v
  ```

  Dat vraagt een Python waarin de pakketten uit `requirements.txt` staan. Zet `BK_NETWERK=1` om ook de SHACL-validatie te testen. De workflow [`test.yml`](.github/workflows/test.yml) draait de tests bij elke push en pull request.
- **[`skills/geonovum-uml2-nl-sbb/evals/`](skills/geonovum-uml2-nl-sbb/evals/)**: vier testcases voor een assistent: het NEN 3610-template (XMI, met een voorbeeldmodel ernaast), IMGeluid (XMI 1.1, codes die in meer lijsten voorkomen), IMEV (EAP in een zip) en IMGeo 2.2 (XMI, met het ingevulde voorbeeld, matches en een vergelijking met het gepubliceerde kader). Elke testcase heeft een prompt, een script dat het model uit het register haalt en de checksum controleert, en controles die beschrijven wat een goed resultaat is.
- **[`testrapporten/`](testrapporten/)**: de uitkomsten:
  - de scripttest en de regressie tegen eerdere omzettingen;
  - een test met drie modelgroottes, met de verbeteringen die daaruit volgden.

## Bijdragen

Fouten in de skill meld je als [issue](https://github.com/fterpstra/skill-uml2-nl-sbb/issues). Werkafspraken voor wijzigingen staan in [CONTRIBUTING.md](CONTRIBUTING.md).

## Licentie

Copyright © 2026 Geonovum. Licensed under the EUPL.

De skill valt onder de [EUPL-1.2](LICENSE). Alle taalversies van de EUPL zijn gelijkwaardig; de [Nederlandse tekst](https://eur-lex.europa.eu/legal-content/NL/TXT/?uri=CELEX:32017D0863) staat in het Publicatieblad van de EU. De testmodellen van de evals staan niet in deze repository; de testcases halen ze uit het [Geonovum-register](https://register.geostandaarden.nl/informatiemodel/).
