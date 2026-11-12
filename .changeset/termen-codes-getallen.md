---
"geonovum-uml2-nl-sbb": minor
---

Nettere termen voor codes in namen. Nieuwe keuzes `termen.getallen` (getallen los van woorden, decimale komma, µm en kPa), `termen.normcodes` (`iso17892d4v2016` → `ISO 17892-4:2016`) en `termen.afkortingen` (`RTKGPS0tot2cm` → `RTK-GPS 0 tot 2 cm`, `PPgroot` → `PP groot`). Ze staan standaard uit; `analyseer` stelt ze voor in het nieuwe beslispunt `termen-codes` als het model zulke namen heeft. Daarnaast twee correcties in de camelCase-splitsing die bestaande kaders kunnen raken: `IJ` blijft één letter (`obstakelIJzervloer` → `obstakel ijzervloer`, was `obstakel i jzervloer`) en een losse hoofdletter blijft staan (`klasseA` → `klasse A`, was `klasse a`).
