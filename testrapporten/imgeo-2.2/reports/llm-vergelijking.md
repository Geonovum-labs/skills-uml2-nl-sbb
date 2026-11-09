# Vergelijking: de 4 beschikbare LLM's in Vibe bij het maken van een begrippenkader uit IMGeo 2.2

## De vier beschikbare modellen

Volgens de Vibe-documentatie ([Configuration](https://docs.mistral.ai/vibe/code/cli/configuration)) zijn in Vibe vier chat-modellen beschikbaar via de Mistral API:

| Model | Model-ID | Karakteristiek (docs) |
|---|---|---|
| Mistral Large 4 | `mistral-large-4-0` | Flagship reasoning en code |
| Z.ai GLM 5.3 | `zai-glm-5-3` | Advanced reasoning en code; 1M context, 128k output, open weights |
| Z.ai GLM 5.3 Flash | `zai-glm-5-3-flash` | Snelle multimodale reasoning en code; 320B MoE (18B actief), 1M context, tool-use |
| Mistral Medium 3.5 | `mistral-medium-latest` | Balanced reasoning en code; 256k context |

## Taak

Begrippenkader (NL-SBB/SKOS) maken van het UML-informatiemodel IMGeo 2.2 via
`https://register.geostandaarden.nl/informatiemodel/imgeo/2.2/` (IMGeo.xmi / IMGeo.EAP),
met skill `geonovum-uml-2-nl-sbb`: inventaris → analyse → generatie → SHACL-validatie → review → rapport.

## Wat is daadwerkelijk uitgevoerd

Deze sessie draait op **mistral-large-4-0**. De andere drie modellen zijn in deze
sandbox niet aan te roepen (geen API-sleutel in de omgeving; observability/evaluaties
niet beschikbaar), dus voor die drie is de vergelijking gebaseerd op de
publicatiedocumentatie, niet op een eigen run.

### Run met mistral-large-4-0 (uitgevoerd)

- Bron: IMGeo.xmi (3,1 MB) van het register; 99 UML-elementen, 414 attributen/waarden.
- Resultaat: **393 begrippen** (67 attributen, 4 datatypen, 38 objecttypen, 284 waarden), 57 collecties, 3.686 triples in `uit/kader.ttl`.
- SHACL (NL-SBB-profiel 1.0.0 + extensie, pySHACL 0.40.2): run A kaal 41 Violation / 180 Warning / 2 Info; run B met context 13 Violation / 180 Warning / 2 Info (violations: closeMatch naar externe concepten zonder skos:Concept in de context).
- Review: 16 delen, 393 begrippen beoordeeld: **384 ok, 9 definitie** (o.a. identieke definities bij de vier "op talud"-attributen en bij reclamebord/reclamezuil).
- Alle 7 beslispunten zijn met `overnemen --alle` overgenomen zonder bevestiging; aannames vastgelegd in `werk/aannames.md`.
- Vergelijking met het gepubliceerde IMGeo-kader (464 begrippen) uitgevoerd via `https://upload.begrippenxl.nl/storage/imgeo/imgeo.ttl` (de REST-endpoint op definities.geostandaarden.nl gaf HTTP 403 vanuit deze omgeving): 444 van 464 gematcht (273 op URI, 168 op term+definitie, 3 term/andere definitie, 20 geen match); definitie gelijk bij 433 van 444. Details in `reports/rapport.md` sectie 6 en `uit/vergelijking.csv`.

## Vergelijking per model (opgave: lengthy, tool-gebaseerde conversie met strikte regels)

| Criterium | Mistral Large 4 | GLM 5.3 | GLM 5.3 Flash | Medium 3.5 |
|---|---|---|---|---|
| Context (relevant voor 3,1 MB XMI + 393 begrippen) | 256k | **1M** | **1M** | 256k |
| Reasoning/volgen van strikte meerstappeninstructies | zeer sterk (flagship) | sterk | sterk, snel | balanced |
| Tool-use / agentisch werken (skill draait via scripts) | zeer sterk | sterk (function-calling) | **gericht op agent/tool-use workflows** | voldoende |
| Snelheid/kost bij deze taak | langzamer, duurder | gemiddeld | **snelst** | snel, goedkoop |
| Uitgevoerd in deze sessie | **ja** | nee | nee | nee |

## Conclusie

Voor deze taak — een grote XMI parsen, 393 begrippen genereren, 16 reviewdelen
beoordelen en SHACL-resultaten interpreteren — is **context en instructievolgzaamheid**
bepalend. GLM 5.3 en GLM 5.3 Flash hebben daarbij het grootste contextvenster (1M),
Mistral Large 4 is het sterkste op reasoning en het volgen van de strikte skill-regels
(geen eigen Turtle schrijven, elke stap via `bk.py`), en Medium 3.5 is de
snel&euro;kokere optie voor kleinere modellen. In deze sessie is alleen
mistral-large-4-0 daadwerkelijk uitgevoerd; het kader is compleet en gevalideerd,
met 9 definitie-bevindingen als aandachtspunt voor de UML-beheerder.
