# Rapport omzetting naar NL-SBB

## 1. Bron

- bestand: IMGeo.xmi
- packages: (alles)
- inventaris: 99 UML-elementen, 414 attributen/waarden

## 2. Keuzes

Standaardkeuzes uit de skill, met deze afwijkingen (project.yaml):

```yaml
relaties:
  wortel: _CityObject
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
    TypeGebouwInstallatie:
    - BuildingInstallation
    - null
    TypeGebouwInstallatiePlus:
    - BuildingInstallation
    - plus-typeGebouwInstallatie
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
    TypeVegetatieObject:
    - SolitaryVegetationObject
    - null
    TypeVegetatieObjectPlus:
    - SolitaryVegetationObject
    - plus-type
besloten:
- wortel
- prefixen
- waarden-splitsen
- gebruik
- bronnen-onbekend
- alias
- kader
termen:
  naam_prefixen_verwijderen:
  - bgt-
  - plus-
  alias_als_voorkeursterm:
  - '*'
  alias_naam_als_altlabel: null
waarden:
  automatisch_splitsen: '{lijst} {waarde}'
bronnen:
  mapping:
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
kader:
  uri: http://definities.geostandaarden.nl/imgeo
  titel: IMGeo-begrippenkader
  omschrijving: Begrippen uit het informatiemodel IMGeo.xmi, omgezet volgens NL-SBB.
```

Notities bij de keuzes:

- wortel: scriptvoorstel overgenomen
- prefixen: scriptvoorstel overgenomen
- waarden-splitsen: scriptvoorstel overgenomen
- gebruik: scriptvoorstel overgenomen
- bronnen-onbekend: scriptvoorstel overgenomen
- alias: scriptvoorstel overgenomen
- kader: scriptvoorstel overgenomen

Beslispunten: {'INFO': 11}.


Aannames (zonder bevestiging door de gebruiker):

- wortel: _CityObject als wortelbegrip gekozen, niet bevestigd
- prefixen: bgt- en plus- prefixen verwijderd uit termen, niet bevestigd
- waarden-splitsen: waarden met gelijke naam en andere definitie automatisch gesplitst volgens '{lijst} {waarde}', niet bevestigd
- gebruik: waardelijsten gekoppeld aan objecttypen/attributen volgens scriptvoorstel, niet bevestigd
- bronnen-onbekend: bronmapping gemaakt voor herkomstwaarden, niet bevestigd
- alias: alle aliases als voorkeursterm gebruikt, niet bevestigd
- kader: URI, titel en omschrijving ingesteld volgens scriptvoorstel, niet bevestigd
- review: termcorrecties niet uitgevoerd (zelfstandig werken), de gebruiker beslist over reviewbevindingen

## 3. Resultaat

- 396 begrippen: attribuut 67, datatype 4, objecttype 38, waarde 287
- zonder definitie: 0
- log: 70 regels in uit/beslissingen.md

## 4. SHACL-validatie

Instellingen: NL-SBB-profiel + skill-extensie, advanced=True, inference=rdfs. Oordeel op de telling per ernstniveau, niet op `conforms`.

    profiel 1.0.0, pySHACL 0.40.2, advanced=True, inference=rdfs
    === A-kaal ===
    conforms-veld: False (niet leidend) | telling: Violation 0, Warning 72, Info 0
    === B-context ===
    conforms-veld: False (niet leidend) | telling: Violation 0, Warning 72, Info 0

## 5. Inhoudelijke review

ok: 396 | term: 0 | definitie: 0 | twijfel: 0

Details: reports/review.md

## 6. Vergelijking met gepubliceerde versie

Vergelijking met https://upload.begrippenxl.nl/storage/imgeo/imgeo.ttl:

- Gepubliceerd: 464 begrippen, 57 collecties, 464 topbegrippen (geen hiërarchie)
- Nieuw gegenereerd: 396 begrippen, 57 collecties, 5 topbegrippen (met hiërarchie)
- Koppeling: 170 term+definitie matches, 271 URI matches, 20 geen match, 3 term (andere definitie)
- 433 van 444 definities zijn gelijk tussen beide versies
- 12 begrippen in nieuw kader hebben geen tegenhanger in gepubliceerde versie
- 68 begrippen in gepubliceerde versie hebben geen tegenhanger in nieuw kader

## Conclusie

De omzetting van IMGeo 2.2 naar een NL-SBB-begrippenkader is technisch geslaagd met 396 begrippen en 0 SHACL-violations. De 72 warnings in de SHACL-validatie betreffen begrippen zonder bovenliggende of gerelateerde begrippen, wat een structureel verschil is met de gepubliceerde versie die 464 topbegrippen heeft (geen hiërarchie). De inhoudelijke review toont aan dat alle 396 begrippen als 'ok' zijn beoordeeld, maar dit is gebaseerd op automatische acceptatie van signalen zonder handmatige controle. Belangrijkste verschillen met de gepubliceerde versie: 68 begrippen minder, 20 begrippen zonder tegenhanger, en 3 begrippen met dezelfde term maar andere definitie. De 8 aannames zonder bevestiging (zoals wortelkeuze, prefixverwijdering, aliasgebruik) moeten door de gebruiker worden beoordeeld alvorens het kader te publiceren.
