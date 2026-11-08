# Disclaimer

De skill in deze repository is een hulpmiddel van [Geonovum](https://www.geonovum.nl) voor het omzetten van UML-informatiemodellen naar begrippenkaders. Hij is **informatief**: een begrippenkader dat met deze skill is gemaakt, is geen bewijs dat het aan NL-SBB voldoet, en geen vastgesteld begrippenkader van de beheerder van het informatiemodel.

## De skill is niet de norm

Een skill is een samenvatting en een werkinstructie, niet de regel zelf. Leidend zijn altijd:

- de publicatie van [NL-SBB](https://docs.geostandaarden.nl/nl-sbb/nl-sbb/) en het normatieve [SHACL-profiel](https://register.geostandaarden.nl/shacl/nl-sbb/1.0.0/skos-ap-nl.ttl) in het register;
- het informatiemodel zelf, zoals de beheerder het heeft vastgesteld;
- voor MIM-modellen: het [Metamodel Informatiemodellering (MIM)](https://docs.geostandaarden.nl/mim/mim/).

De standaardkeuzes van de skill (zoals objecttype-context in attribuuttermen, splitsen van waarden met een andere betekenis, en alias als voorkeursterm bij MIM-modellen) zijn werkkeuzes. Ze staan in `standaardkeuzes.yaml` met uitleg in `references/keuzes.md`, en zijn per project aan te passen.

## De definities blijven die van het bronmodel

De skill herschrijft geen definities. Vage, circulaire of ontbrekende definities meldt hij als advies voor de beheerder van het UML-model. Matchtypen naar externe begrippenkaders en termcorrecties zijn inhoudelijke oordelen: laat ze door een domeinexpert bevestigen.

## Gebruik van generatieve AI

De skill wordt uitgevoerd door AI-assistenten. Een begrippenkader kan daardoor onvolledig of onjuist zijn, ook als de skill zelf klopt. De scripts beperken dat: zij maken het kader, tellen de SHACL-uitkomsten en controleren of de review volledig is. Keuzes, voorstellen en reviewoordelen komen wel van de assistent. Of bij het schrijven van de skill generatieve AI is gebruikt, staat in het veld `nl.gov.generated-with` van de skill. Overheidsorganisaties die generatieve AI inzetten, ook via deze skill, dienen te voldoen aan het [Overheidsbreed standpunt voor de inzet van generatieve AI](https://open.overheid.nl/documenten/bc03ce31-0cf1-4946-9c94-e934a62ebe73/file) en aan eigen beleid en kaders over AI.

## Externe diensten

De skill haalt het SHACL-profiel uit het [register van Geonovum](https://register.geostandaarden.nl/) en begrippen uit externe kaders van [definities.geostandaarden.nl](https://definities.geostandaarden.nl). De optionele bronnencontrole stuurt verzoeken naar de URI's in het begrippenkader. Het informatiemodel zelf wordt nergens naartoe gestuurd, op de tekst na die de assistent leest.

## Status en onderhoud

De status van de skill staat in het veld `nl.gov.status` in de frontmatter van `SKILL.md`, met een herzieningsdatum in `nl.gov.review-by`. Een skill met status `concept` is nog niet vastgesteld.

## Geen garantie

De inhoud wordt aangeboden zonder garantie van volledigheid, juistheid of actualiteit. Fouten en verbeteringen graag als [issue](https://github.com/fterpstra/skill-uml2-nl-sbb/issues) in deze repository.
