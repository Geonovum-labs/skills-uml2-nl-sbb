# Rapport omzetting naar NL-SBB

## 1. Bron

- bestand: IMGeo.xmi
- packages: (alles)
- inventaris: 99 UML-elementen, 414 attributen/waarden

## 2. Keuzes

Standaardkeuzes uit de skill, met deze afwijkingen (project.yaml):

```yaml
kader:
  uri: http://definities.geostandaarden.nl/imgeo
  titel: IMGeo 2.2-begrippenkader
  omschrijving: Begrippen uit het Informatiemodel Geografie (IMGeo) 2.2 — objecttypen, attributen en waarden uit
    waardelijsten, omgezet uit het UML-model (XMI) volgens NL-SBB
prefixen:
  imgeo: http://definities.geostandaarden.nl/imgeo/id/begrip/
  col: http://definities.geostandaarden.nl/imgeo/id/collectie/
  bron: http://definities.geostandaarden.nl/imgeo/id/bron/
termen:
  naam_prefixen_verwijderen:
  - bgt-
  - plus-
  vast:
    IMGeo-Object: IMGeo-object
    NEN3610ID: NEN3610ID
  samenstellingen:
    gebouw installatie: gebouwinstallatie
    vegetatie object: vegetatieobject
  alias_als_voorkeursterm:
  - '*'
  alias_naam_als_altlabel: null
attributen:
  context_altijd:
  - type
  - naam
  - tekst
  - positie
  - hoek
  - fysiek voorkomen
  prefix_term:
    plus-: 'plus '
  term_correcties:
    plus-fysiekVookomen: fysiek voorkomen
waarden:
  hernoem:
    niet-bgt: niet-BGT-object
  splitsingen:
    onverhard|FysiekVoorkomenWeg: onverhard wegdeel
    onverhard|FysiekVoorkomenOndersteunendWegdeel: onverhard wegdeel
    onverhard|FysiekVoorkomenOnbegroeidTerrein: onverhard terreindeel
    zand|FysiekVoorkomenOnbegroeidTerrein: zand terreindeel
    zand|FysiekVoorkomenWegPlus: zand deklaag
    zand|FysiekVoorkomenOndersteunendWegdeelPlus: zand deklaag
    zand|FysiekVoorkomenOnbegroeidTerreinPlus: zand deklaag
  automatisch_splitsen: '{lijst} {waarde}'
relaties:
  wortel: _CityObject
  zelfstandig:
  - Plaatsbepalingspunt
  gebruik:
    Status: null
    StatusPlus: null
    FunctieWeg: null
    FunctieWegPlus: null
    FysiekVoorkomenWeg: null
    FysiekVoorkomenWegPlus: null
    FunctieOndersteunendWegdeel:
    - AuxiliaryTrafficArea
    - plus-functieOndersteunendWegdeel
    FysiekVoorkomenOndersteunendWegdeel:
    - AuxiliaryTrafficArea
    - null
    FysiekVoorkomenOndersteunendWegdeelPlus:
    - AuxiliaryTrafficArea
    - plus-fysiekVoorkomenOndersteunendWegdeel
    FunctieSpoor:
    - Railway
    - null
    FunctieSpoorPlus:
    - Railway
    - plus-functieSpoor
    FysiekVoorkomenOnbegroeidTerrein: null
    FysiekVoorkomenOnbegroeidTerreinPlus: null
    FysiekVoorkomenBegroeidTerrein: null
    FysiekVoorkomenBegroeidTerreinPlus: null
    TypeWater: null
    TypeWaterPlus: null
    TypeOndersteunendWaterdeel:
    - OndersteunendWaterdeel
    - plus-type
    TypeOverigBouwwerk:
    - OverigBouwwerk
    - bgt-type
    TypeOverigBouwwerkPlus:
    - OverigBouwwerk
    - plus-type
    TypeOverbrugging: null
    TypeOverbruggingsdeel:
    - BridgeConstructionElement
    - null
    TypeKunstwerk: null
    TypeKunstwerkPlus: null
    TypeScheiding:
    - Scheiding
    - bgt-type
    TypeScheidingPlus:
    - Scheiding
    - plus-type
    TypeOpenbareRuimte:
    - OpenbareRuimte
    - null
    TypeFunctioneelGebied:
    - FunctioneelGebied
    - bgt-type
    TypeFunctioneelGebiedPlus:
    - FunctioneelGebied
    - plus-type
    Inwinningsmethode: null
    VoidReasonValue: null
    TypeGebouwInstallatie:
    - BuildingInstallation
    - null
    TypeGebouwInstallatiePlus:
    - BuildingInstallation
    - plus-typeGebouwInstallatie
    TypeVegetatieObject:
    - SolitaryVegetationObject
    - null
    TypeVegetatieObjectPlus:
    - SolitaryVegetationObject
    - plus-type
    TypeBak:
    - Bak
    - null
    TypeBakPlus:
    - Bak
    - plus-type
    TypeBord:
    - Bord
    - null
    TypeBordPlus:
    - Bord
    - plus-type
    TypeInstallatie:
    - Installatie
    - null
    TypeInstallatiePlus:
    - Installatie
    - plus-type
    TypeKast:
    - Kast
    - null
    TypeKastPlus:
    - Kast
    - plus-type
    TypeMast:
    - Mast
    - null
    TypeMastPlus:
    - Mast
    - plus-type
    TypePaal:
    - Paal
    - null
    TypePaalPlus:
    - Paal
    - plus-type
    TypePut:
    - Put
    - null
    TypePutPlus:
    - Put
    - plus-type
    TypeSensor:
    - Sensor
    - null
    TypeSensorPlus:
    - Sensor
    - plus-type
    TypeStraatmeubilair:
    - Straatmeubilair
    - null
    TypeStraatmeubilairPlus:
    - Straatmeubilair
    - plus-type
    TypeWaterinrichting: null
    TypeWaterinrichtingPlus: null
    TypeWeginrichting: null
    TypeWeginrichtingPlus: null
bronnen:
  mapping:
  - patroon: ^NEN3610
    sleutel: NEN3610-2011
    titel: NEN 3610:2011 Basismodel geo-informatie
  - patroon: ^BAG
    sleutel: BAG-catalogus
    titel: Catalogus Basisregistraties Adressen en Gebouwen (BAG)
  - patroon: ^(BGT|BGT1\.1)$
    sleutel: BGT-catalogus
    titel: Gegevenscatalogus Basisregistratie Grootschalige Topografie (BGT)
  - patroon: ^IMGEO\D*(?P<v>[0-9][0-9.]*)?
    sleutel: IMGeo-{v}
    titel: Informatiemodel Geografie (IMGeo) {v}
  - patroon: ^CROW$
    sleutel: CROW
    titel: CROW-publicaties (kennisplatform infrastructuur, verkeer en vervoer)
  - patroon: ^AQUO$
    sleutel: Aquo
    titel: Aquo-standaard (Informatiehuis Water)
  - patroon: ^WIKIPEDIA$
    sleutel: Wikipedia
    titel: Wikipedia (Nederlandstalig)
  - patroon: ^CITYGML(1\.0)?$
    sleutel: CityGML-1.0
    titel: OGC City Geography Markup Language (CityGML) 1.0
  - patroon: ^BRTSTELSELCATALOGUS$
    sleutel: BRT-stelselcatalogus
    titel: Stelselcatalogus, catalogus Basisregistratie Topografie (BRT)
  - patroon: ^STELSELCATALOGUS$
    sleutel: Stelselcatalogus
    titel: Stelselcatalogus basisregistraties
  - patroon: ^RSGB$
    sleutel: RSGB
    titel: Referentiemodel Stelsel van Gemeentelijke Basisgegevens (RSGB)
  - patroon: ^GWBRGEGEVENSWOORDENBOEKRIOLERING$
    sleutel: GWSW
    titel: Gegevenswoordenboek Riolering (GWBR)
  - patroon: ^NEN2660$
    sleutel: NEN2660
    titel: NEN 2660 Ordeningsregels gebouwde omgeving
  - patroon: ^INSPIRE$
    sleutel: INSPIRE
    titel: INSPIRE-dataspecificaties
  - patroon: ^WEGENWIKI\.NL$
    sleutel: Wegenwiki
    titel: Wegenwiki (wegenwiki.nl)
  - patroon: BGT$
    sleutel: BGT
    titel: BGT
  - patroon: IMGEO1\.0$
    sleutel: IMGEO-1-0
    titel: IMGEO 1.0
  - patroon: IMGEO2\.0$
    sleutel: IMGEO-2-0
    titel: IMGEO 2.0
  - patroon: CROW$
    sleutel: CROW
    titel: CROW
  - patroon: IMGEO2\.1$
    sleutel: IMGEO-2-1
    titel: IMGEO 2.1
  - patroon: AQUO$
    sleutel: aquo
    titel: aquo
  - patroon: NEN3610:2011$
    sleutel: NEN-3610-2011
    titel: NEN 3610:2011
  - patroon: IMGEO$
    sleutel: IMGEO
    titel: IMGEO
  - patroon: WIKIPEDIA$
    sleutel: Wikipedia
    titel: Wikipedia
  - patroon: BGT1\.1$
    sleutel: BGT-1-1
    titel: BGT 1.1
  - patroon: BAG$
    sleutel: BAG
    titel: BAG
  - patroon: STELSELCATALOGUS$
    sleutel: Stelselcatalogus
    titel: Stelselcatalogus
  - patroon: BAGSTELSELCATALOGUS$
    sleutel: BAG-stelselcatalogus
    titel: BAG stelselcatalogus
  - patroon: BRTSTELSELCATALOGUS$
    sleutel: BRT-stelselcatalogus
    titel: BRT stelselcatalogus
  - patroon: CITYGML1\.0$
    sleutel: CityGML-1-0
    titel: CityGML 1.0
  - patroon: RSGB$
    sleutel: RSGB
    titel: RSGB
  - patroon: CITYGML$
    sleutel: CityGML
    titel: CityGML
  - patroon: NEN3610$
    sleutel: NEN-3610
    titel: NEN 3610
  - patroon: WEGENWIKI\.NL$
    sleutel: wegenwiki-nl
    titel: wegenwiki.nl
  - patroon: NEN2660$
    sleutel: NEN-2660
    titel: NEN 2660
  - patroon: INSPIRE$
    sleutel: Inspire
    titel: Inspire
  - patroon: GWBRGEGEVENSWOORDENBOEKRIOLERING$
    sleutel: GWBR-gegevenswoordenboek-riolering
    titel: GWBR gegevenswoordenboek riolering
matches:
- term: IMGeo-object
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/GeoObject
- term: wegdeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Weg
- term: ondersteunend wegdeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Weg
- term: spoor
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Spoorbaan
- term: onbegroeid terreindeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Terrein
- term: begroeid terreindeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Terrein
- term: waterdeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Water
- term: ondersteunend waterdeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Water
- term: pand
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Gebouw
- term: kunstwerkdeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Kunstwerk
- term: overbruggingsdeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Kunstwerk
- term: tunneldeel
  relatie: broadMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Kunstwerk
- term: inrichtingselement
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Inrichtingselement
- term: functioneel gebied
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/FunctioneelGebied
- term: registratief gebied
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/RegistratiefGebied
- term: identificatie
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/Identificatie
- term: tijdstip registratie
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/TijdstipRegistratie
- term: eind registratie
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/EindRegistratie
- term: geen waarde
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/GeenWaarde
- term: niet ondersteund
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/NietOndersteund
- term: waarde onbekend
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/WaardeOnbekend
- term: vastgesteld onbekend
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/VastgesteldOnbekend
- term: niet geautoriseerd
  relatie: closeMatch
  uri: http://definities.geostandaarden.nl/nen3610/id/begrip/NietGeautoriseerd
- term: pand
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/Pand
- term: openbare ruimte
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/OpenbareRuimte
- term: openbare ruimte type
  relatie: closeMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/TypeOpenbareRuimte
- term: weg
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/Weg
- term: water
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/Water
- term: spoorbaan
  relatie: closeMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/Spoorbaan
- term: terrein
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/Terrein
- term: kunstwerk
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/Kunstwerk
- term: landschappelijk gebied
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/LandschappelijkGebied
- term: administratief gebied
  relatie: exactMatch
  uri: http://bag.basisregistraties.overheid.nl/id/concept/AdministratiefGebied
besloten:
- wortel
- prefixen
- waarden-splitsen
- gebruik
- bronnen-onbekend
- alias
- kader
```

Notities bij de keuzes:

- wortel: scriptvoorstel overgenomen
- prefixen: scriptvoorstel overgenomen
- waarden-splitsen: scriptvoorstel overgenomen
- gebruik: scriptvoorstel overgenomen
- bronnen-onbekend: scriptvoorstel overgenomen
- alias: scriptvoorstel overgenomen
- kader: scriptvoorstel overgenomen
- kader.titel: aangepast: bron is IMGeo 2.2
- kader.omschrijving: aangepast naar 2.2

Beslispunten: {'INFO': 10}.


Aannames (zonder bevestiging door de gebruiker):

- wortel: scriptvoorstel overgenomen, niet bevestigd
- prefixen: scriptvoorstel overgenomen, niet bevestigd
- waarden-splitsen: scriptvoorstel overgenomen, niet bevestigd
- gebruik: scriptvoorstel overgenomen, niet bevestigd
- bronnen-onbekend: scriptvoorstel overgenomen, niet bevestigd
- alias: scriptvoorstel overgenomen, niet bevestigd
- kader: URI/titel/omschrijving overgenomen uit skill-voorbeeld imgeo.yaml (definities.geostandaarden.nl/imgeo), niet bevestigd; titel/omschrijving aangepast naar IMGeo 2.2
- project.yaml gestart vanuit skill-voorbeeld imgeo.yaml (bedoeld voor IMGeo 2.1), niet bevestigd voor 2.2

## 3. Resultaat

- 393 begrippen: attribuut 67, datatype 4, objecttype 38, waarde 284
- zonder definitie: 0
- log: 69 regels in uit/beslissingen.md

## 4. SHACL-validatie

Instellingen: NL-SBB-profiel + skill-extensie, advanced=True, inference=rdfs. Oordeel op de telling per ernstniveau, niet op `conforms`.

    profiel 1.0.0, pySHACL 0.40.2, advanced=True, inference=rdfs
    === A-kaal ===
    conforms-veld: False (niet leidend) | telling: Violation 41, Warning 180, Info 2
    === B-context ===
    conforms-veld: False (niet leidend) | telling: Violation 13, Warning 180, Info 2

Belangrijkste violations:

- [Violation] Concept-closeMatch x13: Value does not have class skos:Concept

## 5. Inhoudelijke review

ok: 384 | term: 0 | definitie: 9 | twijfel: 0

Details: reports/review.md

## 6. Vergelijking met het gepubliceerde IMGeo-kader

Bron: `https://upload.begrippenxl.nl/storage/imgeo/imgeo.ttl` (464 gepubliceerde begrippen, 57 collecties; de REST-endpoint op definities.geostandaarden.nl gaf HTTP 403 vanuit deze omgeving). Resultaten in `uit/vergelijking.csv`:

- 273 van 464 gematcht op URI, 168 op term+definitie, 3 op term met andere definitie, 20 geen match (totaal 444 van 464 = 95,7% match)
- definitie gelijk bij 433 van 444 gematchte begrippen
- 20 gepubliceerde begrippen zonder tegenhanger bij ons (o.a. de waarden `transitie`, `historie`, `bouwtekening`, `digitaliseren`, `scannen`, `geconstrueerd` en de klassen `OngeclassificeerdObject`, `OverigeScheiding`)
- 12 van onze begrippen zonder tegenhanger in het gepubliceerde kader (o.a. `NEN3610ID`, `label`, `labelpositie`, `lokaal ID`, `namespace`, `nummeraanduidingreeks`)
- 3 termen met andere definitie: `brandkraan / -put`, `inspectie- / rioolput`, `plus-type` (in het gepubliceerde kader één begrip met dubbele voorkeurstermen; bij ons gesplitst per objecttype)

## Conclusie

Het gegenereerde IMGeo 2.2-begrippenkader bevat 393 begrippen (67 attributen, 4 datatypen, 38 objecttypen, 284 waarden) in 57 collecties en is bruikbaar als concept-kader; alle 393 begrippen hebben een definitie en de review gaf 384 ok en 9 definitie-bevindingen (o.a. identieke definities bij de vier "op talud"-attributen en bij reclamebord/reclamezuil). Belangrijkste aandachtspunten zijn de 13 SHACL-violations in run B (closeMatch naar externe concepten zonder skos:Concept in de context) en 180 warnings (vooral 72 verweesde begrippen zonder semantische relatie). De vergelijking met het gepubliceerde IMGeo-kader (464 begrippen) laat 444 van 464 matches zien (273 op URI, 168 op term+definitie), met definitie gelijk bij 433 van 444; 20 gepubliceerde waarden (o.a. `transitie`, `historie`) en 12 van onze begrippen (o.a. `NEN3610ID`, `label`) hebben geen tegenhanger. Alle 7 beslispunten zijn overgenomen zonder bevestiging (zie werk/aannames.md); de kader-URI is die van het gepubliceerde IMGeo-kader, dus de nieuwe URI's resolven (nog) niet als apart kader.
