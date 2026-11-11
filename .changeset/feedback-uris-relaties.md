---
"geonovum-uml2-nl-sbb": minor
---

Verwerking van de feedback op het IMGeo-begrippenkader.

- **URI's van een gepubliceerd kader behouden.** Nieuwe keuze `uris.bestaand` en commando `bk.py bestaand <url|bestand>`. Begrippen, collecties en het kader zelf houden hun gepubliceerde URI. Koppeling op URI, dan op term met gelijke definitie, dan op een unieke term; waarden via hun waardelijst. Heeft het gepubliceerde kader een waarde per lijst als eigen begrip, dan blijft dat zo (identiteit eerst). `analyseer` vraagt ernaar (beslispunt `bestaand-kader`); de koppeling staat in `uit/uri-koppeling.tsv`. Het IMGeo-voorbeeld gebruikt het gepubliceerde IMGeo-kader: 441 van de 464 URI's blijven gelijk.
- **Standaard `skos:broader`**, zonder `isothes:broaderGeneric` (`relaties.generalisatie: broader`).
- **Geen parent-tag meer als standaard** (`relaties.waarde_parent_tag: null`); dat was IMGeo-specifiek.
- **Botsingen volgens NL-SBB.** Een waardeterm die al een ander begrip is: gelijke definitie wordt één begrip, anders de waardelijst tussen haakjes (`weg (functie)`), in plaats van het achtervoegsel " waarde". Het splitsvoorstel van `analyseer` en het IMGeluid-voorbeeld gebruiken ook die vorm (`1 (bovenbouwcode)`), en het IMGeo-voorbeeld `onverhard (wegdeel)`.
- **Code van een waarde altijd in `skos:notation`** (`waarden.notatie: code`): de naam in het model, getypeerd met de waardelijst, zodat de code stabiel en uniek per lijst is.
