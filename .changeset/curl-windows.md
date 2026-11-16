---
"geonovum-uml2-nl-sbb": patch
---

Downloads werken nu ook op Windows. `bk.py valideer`, `bk.py waarden` en `bk.py bestaand` liepen daar vast met `PermissionError` op een tijdelijk headerbestand, omdat curl schreef in een bestand dat het script nog open had. Het bestand wordt nu gesloten voordat curl start en daarna opgeruimd. De bronnencontrole schrijft de opgehaalde pagina naar het lege apparaat van het systeem in plaats van naar `/dev/null`, dat op Windows niet bestaat.
