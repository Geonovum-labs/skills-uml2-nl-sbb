---
"geonovum-uml2-nl-sbb": minor
---

Meer keuze voor `skos:notation` bij waarden. Nieuw: `waarden.notatie: afwijkend` zet alleen een notatie als de code uit het model anders is dan de voorkeursterm (bij IMGeo krijgt 'half verhard' dan geen notatie, die is gelijk aan de term). Nieuw: `waarden.notatie_datatype: false` schrijft de notatie als gewone tekst in plaats van met de waardelijst als datatype; tools die geen eigen datatypes kennen (zoals ModelDesk) tonen zo'n notatie anders als onbekende eigenschap. `waarden.notatie: geen` laat de notatie helemaal weg. `bk.py controleer` keurt ongeldige waarden af. De standaard blijft `code` met datatype.
