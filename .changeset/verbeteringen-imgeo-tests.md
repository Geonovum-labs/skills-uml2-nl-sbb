---
"geonovum-uml2-nl-sbb": patch
---

Verbeteringen uit vier testruns op IMGeo 2.2 (zie `testrapporten/2026-11-10-imgeo-vier-runs.md`).

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
