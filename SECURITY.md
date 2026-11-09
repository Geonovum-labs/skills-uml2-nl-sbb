# Beveiligingsbeleid

## Ondersteunde versies

Alleen de laatste release krijgt beveiligingscorrecties.

| Versie | Ondersteund |
| ------ | ----------- |
| laatste release | ja |
| eerdere releases | nee |

## Een kwetsbaarheid melden

Deze repository bevat skillteksten, Python-scripts die UML-modellen lezen (XMI en Access/SQLite-bestanden van Enterprise Architect) en begrippenkaders maken en valideren, en twee kleine Python-scripts voor de repo-opzet. Een beveiligingsprobleem kan hier bijvoorbeeld zijn: een instructie die een assistent een onveilige opdracht laat uitvoeren, een modelbestand dat bij het inlezen code laat uitvoeren of bestanden buiten de werkmap schrijft, een verwijzing naar een bron die kwaadaardige inhoud levert, of een fout in de scripts.

> **Meld beveiligingskwetsbaarheden nooit via openbare GitHub-issues.**

Gebruik het [meldformulier van Geonovum](https://fd10.formdesk.com/geonovum/beveiligingsmelding), zoals vermeld in de [security.txt](https://www.geonovum.nl/.well-known/security.txt) van Geonovum. Vermeld waar mogelijk:

- welk bestand het betreft (pad en commit, tag of URL);
- stappen om het probleem te reproduceren;
- de mogelijke gevolgen.

Geonovum handelt meldingen af volgens haar eigen beveiligingsbeleid. Een correctie verschijnt als patchrelease en staat in de [releasenotes](https://github.com/fterpstra/skill-uml2-nl-sbb/releases).
