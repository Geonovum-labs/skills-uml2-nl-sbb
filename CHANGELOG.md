# geonovum-uml2-nl-sbb

## 0.1.0

### Minor Changes

- 5759b0d: Extern beheerde waardelijsten. `analyseer` herkent waardelijsten die alleen kolommen bevatten (zoals de referentielijsten in de BRO-catalogi: Waarde, IMBRO, IMBRO/A, Omschrijving) en telt die kolommen niet meer als waarden. Het beslispunt `waarden-extern` stelt een bron voor uit de tag met de lijstlocatie. Het nieuwe commando `bk.py waarden` haalt per lijst het XML-, CSV- of TSV-bestand op (`waarden.extern`) en zet de waarden in de inventaris; `bk.py status` meldt wanneer dat (na een nieuwe `start`) opnieuw moet.
- 8112feb: Verwerking van de feedback op het IMGeo-begrippenkader.
  
  - **URI's van een gepubliceerd kader behouden.** Nieuwe keuze `uris.bestaand` en commando `bk.py bestaand <url|bestand>`. Begrippen, collecties en het kader zelf houden hun gepubliceerde URI. Koppeling op URI, dan op term met gelijke definitie, dan op een unieke term; waarden via hun waardelijst. Heeft het gepubliceerde kader een waarde per lijst als eigen begrip, dan blijft dat zo (identiteit eerst). `analyseer` vraagt ernaar (beslispunt `bestaand-kader`); de koppeling staat in `uit/uri-koppeling.tsv`. Het IMGeo-voorbeeld gebruikt het gepubliceerde IMGeo-kader: 443 van de 464 URI's blijven gelijk.
  - **Identiteit ook uit het URI-pad.** Heeft het gepubliceerde kader geen collecties (BHR-GT), dan komt de identiteit van attributen en waarden uit het pad (`Klasse/attribuut`, `Lijst/waarde`) of uit het deel na `_` (IMGeo). Bij BHR-GT 2.2 blijven 1707 van de 1824 URI's gelijk.
  - **URI-botsing stopt `genereer` niet meer.** Twee termen met dezelfde URI (`NITG-code`, `NITGcode`): de tweede krijgt de soort erbij, in het log.
  - **SHACL run B** telt de begrippen van het eigen kader, ook als hun URI uit een gepubliceerd kader komt.
  - **Standaard `skos:broader`**, zonder `isothes:broaderGeneric` (`relaties.generalisatie: broader`).
  - **Geen parent-tag meer als standaard** (`relaties.waarde_parent_tag: null`); dat was IMGeo-specifiek.
  - **Botsingen volgens NL-SBB.** Een waardeterm die al een ander begrip is: gelijke definitie wordt één begrip, anders de waardelijst tussen haakjes (`weg (functie)`), in plaats van het achtervoegsel " waarde". Het splitsvoorstel van `analyseer` en het IMGeluid-voorbeeld gebruiken ook die vorm (`1 (bovenbouwcode)`), en het IMGeo-voorbeeld `onverhard (wegdeel)`.
  - **Code van een waarde altijd in `skos:notation`** (`waarden.notatie: code`): de naam in het model, getypeerd met de waardelijst, zodat de code stabiel en uniek per lijst is.
- 8e3918f: Meer keuze voor `skos:notation` bij waarden. Nieuw: `waarden.notatie: afwijkend` zet alleen een notatie als de code uit het model anders is dan de voorkeursterm (bij IMGeo krijgt 'half verhard' dan geen notatie, die is gelijk aan de term). Nieuw: `waarden.notatie_datatype: false` schrijft de notatie als gewone tekst in plaats van met de waardelijst als datatype; tools die geen eigen datatypes kennen (zoals ModelDesk) tonen zo'n notatie anders als onbekende eigenschap. `waarden.notatie: geen` laat de notatie helemaal weg. `bk.py controleer` keurt ongeldige waarden af. De standaard blijft `code` met datatype.
- d092b7b: Nettere termen voor codes in namen. Nieuwe keuzes `termen.getallen` (getallen los van woorden, decimale komma, µm en kPa), `termen.normcodes` (`iso17892d4v2016` → `ISO 17892-4:2016`) en `termen.afkortingen` (`RTKGPS0tot2cm` → `RTK-GPS 0 tot 2 cm`, `PPgroot` → `PP groot`). Ze staan standaard uit; `analyseer` stelt ze voor in het nieuwe beslispunt `termen-codes` als het model zulke namen heeft. Daarnaast twee correcties in de camelCase-splitsing die bestaande kaders kunnen raken: `IJ` blijft één letter (`obstakelIJzervloer` → `obstakel ijzervloer`, was `obstakel i jzervloer`) en een losse hoofdletter blijft staan (`klasseA` → `klasse A`, was `klasse a`).

### Patch Changes

- 05cf908: Betere voorstellen in `analyseer`. Het alias-voorstel kijkt naar de taal: zijn de aliassen Engels en de UML-namen Nederlands (zoals in de BRO-catalogi), dan stelt het script voor de UML-naam als voorkeursterm te houden in plaats van de alias. Het kadervoorstel vervangt een algemene packagenaam ("Model") door de bovenliggende package en gebruikt een afkorting tussen haakjes als URI-naam ("Geotechnisch booronderzoek (BHR-GT)" → `.../bhr-gt`). Het voorstel voor `waarden.zelfde_begrip` voegt geen waarden meer samen waarvan de definities andere getallen noemen.
- e8f6277: Correcties na een goldfish-review van PR #8 op een model buiten de ontwikkelset (IMBRT):
  
  - `bk.py waarden` is veilig voor invoer van derden. Een lijstnaam uit het model wordt nooit een pad; lokale paden blijven binnen de projectmap. Interne adressen (loopback, privé, link-local) worden geweigerd en doorverwijzingen niet gevolgd. Alleen `.xml`, `.csv` en `.tsv`, zonder `#`. De cache kijkt ook naar de URL. Een bron-URL uit het model wordt in `waarden-extern` alleen genoemd en niet meer overgenomen met `bk.py overnemen --alle`; zonder bron worden de kolommen van zulke lijsten geen begrippen.
  - `termen-codes` stelt alleen afkortingen voor die ergens los in het model staan (`BAGObject`, `BRTVlakOfPunt` geven geen "BAGO bject" of "BRTV lak" meer) en toont per keuze het effect (naam -> term). Een afkorting in kleine letters geldt alleen in een code zonder spaties ('weg in aanleg' blijft).
  - `termen.normcodes`: 'en' tussen cijfers is een voegwoord (`veel10en20` → "veel 10 en 20", niet "EN").
  - `termen.getallen`: vaste namen als `top10nl`, `lod2`, `co2`, `epsg28992` en `2D` blijven heel.
  - `genereer` stopt weer bij twee begrippen met dezelfde voorkeursterm en geeft per paar het `bk.py zet`-commando om het op te lossen.
- e64f597: Verbeteringen uit vier testruns op IMGeo 2.2 (zie `testrapporten/2026-11-10-imgeo-vier-runs.md`).
  
  - `bk.py valideer` haalt de SHACL-extensie zelf op als de map `shacl/` bij de installatie ontbreekt, en geeft anders een duidelijke melding. Het profiel staat nu in `werk/` in plaats van `reports/`.
  - De SHACL-samenvatting telt apart hoeveel violations komen door match-doelen die geen `skos:Concept` zijn (extern kader niet bereikbaar).
  - `bk.py start` noemt een passend voorbeeld uit `voorbeelden/`; het nieuwe commando `bk.py voorbeeld <naam>` kopieert het met schrijfrechten naar `project.yaml`.
  - `project.yaml` dat alleen-lezen is (gekopieerd uit een alleen-lezen installatie) krijgt bij schrijven zelf schrijfrechten.
  - `bk.py overnemen` overschrijft geen keuzes die al in `project.yaml` staan.
  - `bk.py zet` leest een waarde met een dubbele punt (`'IMGeo 2.2: …'`) als tekst.
  - Een attribuutterm die al met de objecttype-context eindigt, krijgt die context niet nog eens (*type scheiding scheiding* wordt *type scheiding (plus)*), en `IMGeo-object` wordt niet meer *IM geo-object* (`termen.woorden_behouden`).
  - Het reviewsignaal "leesteken in term" geeft waar mogelijk een voorstel (*recreatie: camping* → *camping*). Elk reviewbegrip heeft een vaste `id`.
  - `bk.py vergelijk` schrijft `uit/vergelijking.txt`, zodat de vergelijking in het rapport komt, en groepeert gelijke regels.
  - `bk.py rapport` neemt `werk/rapport-aanvulling.md` op, zodat eigen secties niet verloren gaan.

## 0.0.1

### Patch Changes

- Eerste release. Skill `geonovum-uml2-nl-sbb` (voorheen `xmi-begrippenkader`): zet een UML-informatiemodel in XMI 1.1 of 2.x, of een Enterprise Architect-bestand (.eap, .eapx, .qea, .qeax, ook in een zip), om naar een begrippenkader volgens NL-SBB. Status `concept`.
  - Eén ingang, `scripts/bk.py`, voor alle vaste stappen. `bk.py status` noemt na elke stap de volgende, zodat ook kleinere modellen de werkwijze volledig doorlopen.
  - Elk beslispunt krijgt een voorstel van het script. `overnemen` en `zet` leggen keuzes vast in `project.yaml`, en `controleer` toetst dat bestand op sleutels, namen en regexen.
  - SHACL-validatie tegen het NL-SBB-profiel 1.0.0 plus extensie, met de telling per ernstniveau.
  - Inhoudelijke review in delen van 25 begrippen, met signalen van het script en een compleetheidscontrole. Oordelen blijven staan als het kader opnieuw wordt gemaakt.
  - Rapport met cijfers die het script schrijft; de assistent vult alleen de conclusie in.
  - MIM-ondersteuning: alias als voorkeursterm, notities met koppen, MIM-stereotypen, keuze-datatypen.
  - Getest op IMGeo, IMGeluid, IMEV, IMKL, IMRO en NEN 3610, en met drie modelgroottes; zie `testrapporten/`.
