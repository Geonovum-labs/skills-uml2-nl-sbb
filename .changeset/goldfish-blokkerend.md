---
"geonovum-uml2-nl-sbb": patch
---

Correcties na een goldfish-review van PR #8 op een model buiten de ontwikkelset (IMBRT):

- `bk.py waarden` is veilig voor invoer van derden. Een lijstnaam uit het model wordt nooit een pad; lokale paden blijven binnen de projectmap. Interne adressen (loopback, privé, link-local) worden geweigerd en doorverwijzingen niet gevolgd. Alleen `.xml`, `.csv` en `.tsv`, zonder `#`. De cache kijkt ook naar de URL. Een bron-URL uit het model wordt in `waarden-extern` alleen genoemd en niet meer overgenomen met `bk.py overnemen --alle`; zonder bron worden de kolommen van zulke lijsten geen begrippen.
- `termen-codes` stelt alleen afkortingen voor die ergens los in het model staan (`BAGObject`, `BRTVlakOfPunt` geven geen "BAGO bject" of "BRTV lak" meer) en toont per keuze het effect (naam -> term). Een afkorting in kleine letters geldt alleen in een code zonder spaties ('weg in aanleg' blijft).
- `termen.normcodes`: 'en' tussen cijfers is een voegwoord (`veel10en20` → "veel 10 en 20", niet "EN").
- `termen.getallen`: vaste namen als `top10nl`, `lod2`, `co2`, `epsg28992` en `2D` blijven heel.
- `genereer` stopt weer bij twee begrippen met dezelfde voorkeursterm en geeft per paar het `bk.py zet`-commando om het op te lossen.
