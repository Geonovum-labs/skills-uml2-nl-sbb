---
"geonovum-uml2-nl-sbb": minor
---

Drie verbeteringen uit de vergelijking met ea2rdf (testrapport 2026-11-16).

- **ea2rdf-export als invoer.** `bk.py start model-ea.ttl` leest een export van [ea2rdf](https://github.com/architolk/ea2rdf) (`java -jar ea2rdf.jar -ea -e model.eap`). ea2rdf leest Access-bestanden met Jackcess en mist geen memovelden en GUID's, zoals access-parser soms wel doet. Bij IMEV 3.0.2 levert dat de definitie van `OpslagOntplofbaarMilitair_TeBerekenenAfstand` op. Een export in cp1252 (Java op Windows) en dubbel gecodeerde UTF-8 (`reÃ«le`, door de optie `-ea`) worden hersteld en gemeld. De LET OP-meldingen over onleesbare velden noemen deze route.
- **Associaties worden `skos:related`.** Relatiesoorten tussen twee klassen in het kader worden gerelateerde begrippen (XMI 1.1, XMI 2.x, EAP/QEA en ea2rdf). Uit te zetten met `relaties.associatie: geen`. `analyseer` toont ze als INFO-punt `associaties`.
- **De MIM-tag *begrip* wordt een match.** Een http(s)-URI in de tag `begrip` (hoofdletterongevoelig, instelbaar met `relaties.begrip_tag`) wordt `skos:exactMatch` naar dat bestaande begrip; `relaties.begrip_relatie` kiest een ander matchtype of `geen`. URI's in het eigen kader worden overgeslagen. NEN 3610:2022 staat nu bij de externe kaders, zodat de validatie (run B) die begrippen als context ophaalt.

Ook opgelost: `valideer` telde match-doelen waarvan de URI met de kader-URI begint (bv. `…/nen3610-2022/…` bij kader `…/nen3610`) als eigen begrip, en meldde violations door ontbrekende match-doelen niet als zodanig.
