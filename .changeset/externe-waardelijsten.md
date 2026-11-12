---
"geonovum-uml2-nl-sbb": minor
---

Extern beheerde waardelijsten. `analyseer` herkent waardelijsten die alleen kolommen bevatten (zoals de referentielijsten in de BRO-catalogi: Waarde, IMBRO, IMBRO/A, Omschrijving) en telt die kolommen niet meer als waarden. Het beslispunt `waarden-extern` stelt een bron voor uit de tag met de lijstlocatie. Het nieuwe commando `bk.py waarden` haalt per lijst het XML-, CSV- of TSV-bestand op (`waarden.extern`) en zet de waarden in de inventaris; `bk.py status` meldt wanneer dat (na een nieuwe `start`) opnieuw moet.
