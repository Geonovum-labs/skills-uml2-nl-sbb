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
  titel: IMGeo-begrippenkader
  omschrijving: 'Begrippen uit het Informatiemodel Geografie (IMGeo) 2.2: objecttypen, attributen en waarden uit
    waardelijsten, omgezet uit het UML-model (XMI) volgens NL-SBB.'
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
    (haven)kraan: havenkraan
    benzine- / olieput: benzine- of olieput
    beton element: betonelement
    brandkraan / -put: brandkraan of brandkraanput
    'functioneel beheer: hondenuitlaatplaats': hondenuitlaatplaats
    inspectie- / rioolput: inspectie- of rioolput
    radar detector: radardetector
  samenstellingen:
    gebouw installatie: gebouwinstallatie
    vegetatie object: vegetatieobject
  alias_als_voorkeursterm:
  - ADEElement
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
relaties:
  wortel: _CityObject
  zelfstandig:
  - Plaatsbepalingspunt
  gebruik:
    Status:
    - _CityObject
    - bgt-status
    StatusPlus:
    - _CityObject
    - plus-status
    FunctieWeg:
    - TrafficArea
    - null
    FunctieWegPlus:
    - TrafficArea
    - plus-functieWegdeel
    FysiekVoorkomenWeg:
    - TrafficArea
    - null
    FysiekVoorkomenWegPlus:
    - TrafficArea
    - plus-fysiekVoorkomenWegdeel
    FunctieOndersteunendWegdeel:
    - AuxiliaryTrafficArea
    - null
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
    FysiekVoorkomenOnbegroeidTerrein:
    - OnbegroeidTerreindeel
    - bgt-fysiekVoorkomen
    FysiekVoorkomenOnbegroeidTerreinPlus:
    - OnbegroeidTerreindeel
    - plus-fysiekVoorkomen
    FysiekVoorkomenBegroeidTerrein:
    - PlantCover
    - null
    FysiekVoorkomenBegroeidTerreinPlus:
    - PlantCover
    - plus-fysiekVookomen
    TypeWater:
    - Waterdeel
    - null
    TypeWaterPlus:
    - Waterdeel
    - plus-type
    TypeOndersteunendWaterdeel:
    - OndersteunendWaterdeel
    - null
    TypeOverigBouwwerk:
    - OverigBouwwerk
    - bgt-type
    TypeOverigBouwwerkPlus:
    - OverigBouwwerk
    - plus-type
    TypeOverbrugging:
    - BridgeConstructionElement
    - hoortBijTypeOverbrugging
    TypeOverbruggingsdeel:
    - BridgeConstructionElement
    - null
    TypeKunstwerk:
    - Kunstwerkdeel
    - bgt-type
    TypeKunstwerkPlus:
    - Kunstwerkdeel
    - plus-type
    TypeScheiding:
    - Scheiding
    - bgt-type
    TypeScheidingPlus:
    - Scheiding
    - plus-type
    TypeOpenbareRuimte:
    - OpenbareRuimteLabel
    - openbareRuimteType
    TypeFunctioneelGebied:
    - FunctioneelGebied
    - bgt-type
    TypeFunctioneelGebiedPlus:
    - FunctioneelGebied
    - plus-type
    Inwinningsmethode:
    - Plaatsbepalingspunt
    - inwinningsmethode
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
    TypeWaterinrichting:
    - Waterinrichtingselement
    - null
    TypeWaterinrichtingPlus:
    - Waterinrichtingselement
    - plus-type
    TypeWeginrichting:
    - Weginrichtingselement
    - null
    TypeWeginrichtingPlus:
    - Weginrichtingselement
    - plus-type
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
```

Notities bij de keuzes:

- termen.vast[(haven)kraan]: review 0110: leestekens uit UML-waardenaam verwijderd
- termen.vast[benzine- / olieput]: review 0126
- termen.vast[beton element]: review 0131
- termen.vast[brandkraan / -put]: review 0150
- termen.vast[functioneel beheer: hondenuitlaatplaats]: review 0189: parent-context niet nodig, naam is uniek
- termen.vast[inspectie- / rioolput]: review 0232
- termen.vast[radar detector]: review 0296

Beslispunten: {'INFO': 10}.


Aannames (zonder bevestiging door de gebruiker):

- project.yaml is gebaseerd op het IMGeo-2.1-voorbeeld uit de skill, aangepast naar IMGeo 2.2 (versienummer en XMI-datum); keuzes niet door de gebruiker bevestigd
- wortel: _CityObject (IMGeo-object) als wortelbegrip, volgens scriptvoorstel, niet bevestigd
- waardelijst-koppelingen (relaties.gebruik) overgenomen uit het IMGeo-2.1-voorbeeld, niet per lijst tegen IMGeo 2.2 gecontroleerd
- bronmappings overgenomen uit het IMGeo-2.1-voorbeeld
- matches (NEN 3610 / BAG) overgenomen uit het IMGeo-2.1-voorbeeld, niet bevestigd
- review-oordelen: niet met de gebruiker besproken; termcorrecties blijven als advies in reports/review.md

## 3. Resultaat

- 393 begrippen: attribuut 67, datatype 4, objecttype 38, waarde 284
- zonder definitie: 0
- log: 56 regels in uit/beslissingen.md

## 4. SHACL-validatie

Instellingen: NL-SBB-profiel + skill-extensie, advanced=True, inference=rdfs. Oordeel op de telling per ernstniveau, niet op `conforms`.

    profiel 1.0.0, pySHACL 0.40.2, advanced=True, inference=rdfs
    === A-kaal ===
    conforms-veld: False (niet leidend) | telling: Violation 41, Warning 46, Info 2
    === B-context ===
    conforms-veld: False (niet leidend) | telling: Violation 13, Warning 46, Info 2

Belangrijkste violations:

- [Violation] Concept-closeMatch x13: Value does not have class skos:Concept

## 5. Inhoudelijke review

ok: 390 | term: 0 | definitie: 3 | twijfel: 0

Details: reports/review.md

## Conclusie

Het gegenereerde IMGeo 2.2-begrippenkader bevat 393 begrippen (38 objecttypen, 67 attributen, 4 datatypen, 284 waarden) in 57 collecties, alle met definitie en 391 met bronverwijzing. De 7 termcorrecties uit de eerste reviewronde zijn doorgevoerd (havenkraan, benzine- of olieput, betonelement, brandkraan of brandkraanput, hondenuitlaatplaats, inspectie- of rioolput, radardetector); de tweede reviewronde beoordeelt 390 begrippen als ok met 3 definitieadviezen. De SHACL-validatie geeft run A 41 violations en run B 13 violations; de grootste groep (28 SemanticRelations + 13 Concept-closeMatch) ontstaat doordat de externe kaders van definities.geostandaarden.nl en de BAG tijdens validatie niet ophaalbaar waren (HTTP 403), zodat match-doelen niet als skos:Concept herkend werden. Verder zijn er 46 warnings, vooral 16 niet-onderscheidende definities en 5 verweesde void-begrippen, en 2 info-meldingen over ontbrekende bronverwijzing. De vergelijking met de gepubliceerde versie laat zien dat ons kader structuur geeft die de publicatie mist: 6 topbegrippen met 87 broader- en 409 related-relaties, 33 matches en 391 bronverwijzingen tegen 0 bij de publicatie, en geen van de 32 dubbele voorkeurstermen; 20 gepubliceerde begrippen (met name 13x "transitie") hebben geen tegenhanger in IMGeo 2.2 en 12 van onze begrippen (datatypen en label-attributen) ontbreken in de publicatie. Belangrijke aannames: de keuzes zijn overgenomen uit het IMGeo-2.1-voorbeeld van de skill (wortel _CityObject, waardelijst-koppelingen, bron- en matchmappings) en niet door de gebruiker bevestigd (werk/aannames.md). De gebruiker moet nog beslissen over de 3 definitieadviezen, en bedenken dat de nieuwe URI's (nog) niet resolven; het gepubliceerde kader gebruikt bovendien rdfs:label voor alle 57 collecties in plaats van skos:prefLabel.

## 6. Doorgevoerde termcorrecties

De 7 termadviezen uit de eerste reviewronde zijn vastgelegd in project.yaml (termen.vast) en het kader is opnieuw gegenereerd. De oorspronkelijke UML-waardenaam blijft als altLabel behouden.

| UML-waardenaam | Nieuwe voorkeursterm |
|---|---|
| (haven)kraan | havenkraan |
| benzine- / olieput | benzine- of olieput |
| beton element | betonelement |
| brandkraan / -put | brandkraan of brandkraanput |
| functioneel beheer: hondenuitlaatplaats | hondenuitlaatplaats |
| inspectie- / rioolput | inspectie- of rioolput |
| radar detector | radardetector |

Na de correcties is de review opnieuw gedraaid: 386 oordelen overgenomen (zelfde definitie), 7 nieuwe oordelen, allemaal ok. De 3 definitieadviezen (reclamebord/reclamezuil identiek, landschappelijk gebied zonder BAG-definitie, en het derde advies) blijven als advies aan de modelbeheerder staan.

## 7. Vergelijking met de gepubliceerde versie (imgeo.ttl, BegrippenXL)

- Gepubliceerd kader: 464 begrippen, 57 collecties; ons kader: 393 begrippen, 57 collecties.
- Koppeling: 170 begrippen gekoppeld op term+definitie, 271 op URI, 3 op term met andere definitie, 20 zonder match; definities gelijk bij 433 van 444 vergeleken begrippen. (Vóór de termcorrecties was dit 168 op term+definitie en 273 op URI.)
- Gepubliceerd zonder tegenhanger in IMGeo 2.2 (20): waarden "transitie" (13x), "bouwtekening", "digitaliseren", "geconstrueerd", "historie", "scannen", "OngeclassificeerdObject", "OverigeScheiding".
- Ons kader zonder tegenhanger (12): NEN3610ID, label, labelpositie, lokaal ID, namespace, nummeraanduidingreeks, plaatsingspunt, positie label, tekst label, hoek labelpositie, identificatie BAGVBO hoogste/laagste huisnummer.
- Zelfde term, andere definitie (3): brandkraan / -put, inspectie- / rioolput, plus-type.
- Structurele verschillen: gepubliceerd kader heeft 464 topbegrippen, 0 broader/related-relaties, 0 matches en 0 bronverwijzingen; ons kader heeft 6 topbegrippen, 87 broader, 409 related, 33 matches en 391 bronverwijzingen. Alle 57 collecties in het gepubliceerde kader gebruiken rdfs:label in plaats van skos:prefLabel; er zijn 32 dubbele voorkeurstermen (o.a. "transitie" 13x).

Details: reports/vergelijking.txt
