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
  omschrijving: Begrippen uit het informatiemodel IMGeo.xmi, omgezet volgens NL-SBB.
besloten:
- kader
- wortel
- prefixen
- waarden-splitsen
- gebruik
- bronnen-onbekend
- alias
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
termen:
  naam_prefixen_verwijderen:
  - bgt-
  - plus-
  alias_als_voorkeursterm:
  - '*'
  alias_naam_als_altlabel: null
  vast:
    NEN3610ID: NEN 3610-id
    BuildingInstallation: gebouwinstallatie
    _CityObject: IMGeo object
    SolitaryVegetationObject: vegetatieobject
    (haven)kraan: havenkraan
    benzine- / olieput: benzine- of olieput
    beton element: betonelement
    brandkraan / -put: brandkraan of brandput
    'functioneel beheer: hondenuitlaatplaats': hondenuitlaatplaats
    greppel, droge sloot: greppel of droge sloot
    hoogstam boomgaarden: hoogstamboomgaard
    inspectie- / rioolput: inspectie- of rioolput
    laagstam boomgaarden: laagstamboomgaard
    maatschappelijke en/of publieksvoorziening: maatschappelijke of publieksvoorziening
    meer, plas, ven, vijver: meer of plas, ven of vijver
    oever, slootkant: oever of slootkant
    openbare verlichtingkast: openbare verlichtingskast
    radar detector: radardetector
    'recreatie: bungalowpark': bungalowpark
    'recreatie: camping': camping
    'recreatie: park': park
    'recreatie: speeltuin': speeltuin
    'recreatie: sportterrein': sportterrein
    'recreatie: volkstuin': volkstuin
    telecom kast: telecomkast
    zand- / zoutbak: zand- of zoutbak
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
attributen:
  term_correcties:
    eindRegistratie: eindregistratie
    plus-fysiekVookomen: fysiek voorkomen
    plus-fysiekVoorkomen: fysiek voorkomen onbegroeid terreindeel (plus)
    overbruggingIsBeweegbaar: beweegbaarheid overbrugging
    bgt-status: status geo-object
    plus-status: status geo-object (plus)
    FunctioneelGebied.plus-type: type functioneel gebied (plus)
    plus-typeGebouwInstallatie: type gebouwinstallatie
    Kunstwerkdeel.plus-type: type kunstwerkdeel (plus)
    OverigBouwwerk.plus-type: type overig bouwwerk (plus)
    Scheiding.plus-type: type scheiding (plus)
    SolitaryVegetationObject.plus-type: type vegetatieobject
    _CityObject.bgt-status: status geo-object
    _CityObject.plus-status: status geo-object (plus)
    OnbegroeidTerreindeel.plus-fysiekVoorkomen: fysiek voorkomen onbegroeid terreindeel (plus)
```

Notities bij de keuzes:

- kader: scriptvoorstel overgenomen
- wortel: scriptvoorstel overgenomen
- prefixen: scriptvoorstel overgenomen
- waarden-splitsen: scriptvoorstel overgenomen
- gebruik: scriptvoorstel overgenomen
- bronnen-onbekend: scriptvoorstel overgenomen
- alias: scriptvoorstel overgenomen
- attributen.term_correcties.eindRegistratie: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties.plus-fysiekVookomen: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties.plus-fysiekVoorkomen: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties.overbruggingIsBeweegbaar: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties.bgt-status: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties.plus-status: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[FunctioneelGebied.plus-type]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties.plus-typeGebouwInstallatie: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[Kunstwerkdeel.plus-type]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[OverigBouwwerk.plus-type]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[Scheiding.plus-type]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[SolitaryVegetationObject.plus-type]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast.NEN3610ID: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast.BuildingInstallation: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast._CityObject: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast.SolitaryVegetationObject: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[(haven)kraan]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[benzine- / olieput]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[beton element]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[brandkraan / -put]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[functioneel beheer: hondenuitlaatplaats]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[greppel, droge sloot]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[hoogstam boomgaarden]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[inspectie- / rioolput]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[laagstam boomgaarden]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[maatschappelijke en/of publieksvoorziening]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[meer, plas, ven, vijver]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[oever, slootkant]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[openbare verlichtingkast]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[radar detector]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[recreatie: bungalowpark]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[recreatie: camping]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[recreatie: park]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[recreatie: speeltuin]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[recreatie: sportterrein]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[recreatie: volkstuin]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[telecom kast]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- termen.vast[zand- / zoutbak]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[_CityObject.bgt-status]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[_CityObject.plus-status]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd
- attributen.term_correcties[OnbegroeidTerreindeel.plus-fysiekVoorkomen]: termcorrectie uit de review (2026-11-09), door gebruiker bevestigd

Beslispunten: {'INFO': 11}.


Aannames (zonder bevestiging door de gebruiker):

# Aannames

- Alle scriptvoorstellen van de beslispunten zijn overgenomen zonder gebruikersbevestiging (wortel, prefixen, waarden-splitsen, gebruik, bronnen-onbekend, alias, kader).
- Kader-URI http://definities.geostandaarden.nl/imgeo: komt overeen met de gepubliceerde versie op upload.begrippenxl.nl.
- Model: IMGeo 2.2 zoals gepubliceerd in het register (IMGeo.xmi, 2020-09-08).

## 3. Resultaat

- 396 begrippen: attribuut 67, datatype 4, objecttype 38, waarde 287
- zonder definitie: 0
- log: 83 regels in uit/beslissingen.md

## 4. SHACL-validatie

Instellingen: NL-SBB-profiel + skill-extensie, advanced=True, inference=rdfs. Oordeel op de telling per ernstniveau, niet op `conforms`.

    profiel 1.0.0, pySHACL 0.40.2, advanced=True, inference=rdfs
    === A-kaal ===
    conforms-veld: False (niet leidend) | telling: Violation 0, Warning 168, Info 2
    === B-context ===
    conforms-veld: False (niet leidend) | telling: Violation 0, Warning 168, Info 2

## 5. Inhoudelijke review

ok: 389 | term: 0 | definitie: 7 | twijfel: 0

Details: reports/review.md

## 6. Vergelijking met gepubliceerd kader

```
gepubliceerd: {'begrippen': 464, 'collecties': 57, 'topbegrippen': 464, 'broader': 0, 'related': 0, 'matches': 0, 'bronnen': 0}
ons:          {'begrippen': 396, 'collecties': 57, 'topbegrippen': 5, 'broader': 90, 'related': 259, 'matches': 0, 'bronnen': 394}
koppeling: {'term+definitie': 182, 'URI': 259, 'geen match': 20, 'term (andere definitie)': 3} | definitie gelijk bij 433 van 444

== gepubliceerd zonder tegenhanger ==
   bouwtekening | De geometrie is van een bouwtekening afgeleid.
   digitaliseren | De geometrie is handmatig van analoog naar digitale informatie omgezet.
   geconstrueerd | De geometrie is in een GIS of CAD systeem geconstrueerd.
   historie | Situatie waarin het geregistreerde object fysiek niet meer bestaat.
   OngeclassificeerdObject | Object waarvoor geen bronhouder aangewezen is en/of dat niet nader is geclassificeerd.
   OverigeScheiding | Kunstmatig, meestal lineair obstakel met een werende functie, met kleinere afmetingen dan 
   scannen | De geometrie is geautomatiseerd van analoog naar digitale informatie omgezet.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De gebruikte inwinningsmethode is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.
   transitie | De waarde is tijdens transitie niet bekend.

== zelfde term, andere definitie ==
   brandkraan / -put -> brandkraan of brandput
   inspectie- / rioolput -> inspectie- of rioolput
   plus-type -> type straatmeubilair; type weginrichtingselement; type paal; type waterdeel; type overig bouwwerk (plus); type bak; type kunstwerkdeel (plus); type functioneel gebied (plus); type kast; type vegetatieobject; type sensor; type mast; type bord; type scheiding (plus); type put; type waterinrichtingselement; type installatie

== ons zonder tegenhanger (12) ==
   ['NEN 3610-id', 'hoek labelpositie', 'identificatie BAGVBO hoogste huisnummer', 'identificatie BAGVBO laagste huisnummer', 'label', 'labelpositie', 'lokaal ID', 'namespace', 'nummeraanduidingreeks', 'plaatsingspunt', 'positie label', 'tekst label']

dubbele voorkeurstermen in gepubliceerd kader: 32
collecties met rdfs:label i.p.v. skos:prefLabel (gepubliceerd): 57
```

## Conclusie

Het kader is bruikbaar: van de 396 begrippen heeft elk een definitie en telt de SHACL-validatie 0 violations, 168 warnings en 2 info-meldingen (vooral verweesde begrippen zonder relatie en definities die niet onderscheidend zijn). De review is compleet met 0 term-adviezen en 7 definitie-adviezen; de 38 termcorrecties zijn op verzoek van de gebruiker doorgevoerd en opnieuw beoordeeld. Alle beslispunten zijn zonder gebruikersbevestiging op de scriptvoorstellen gezet (zie de aannames in sectie 2). Tegen de gepubliceerde versie (464 begrippen) koppelen 259 begrippen via URI en 182 via term+definitie; 20 gepubliceerde begrippen hebben geen tegenhanger (vooral de dertien keer herhaalde waarde "transitie" en inwinningsmethoden als "bouwtekening" en "scannen") en 12 van onze begrippen (datatype-attributen rond labels en de NEN 3610-id's) hebben geen tegenhanger in het gepubliceerde kader. In het gepubliceerde kader staan 32 dubbele voorkeurstermen en gebruiken alle 57 collecties rdfs:label in plaats van skos:prefLabel; het nieuwe kader kent deze twee problemen niet.
