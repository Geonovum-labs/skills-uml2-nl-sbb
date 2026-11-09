# geonovum-uml2-nl-sbb

## 0.0.1

### Patch Changes

- Eerste release. Skill `geonovum-uml2-nl-sbb` (voorheen `xmi-begrippenkader`): zet een UML-informatiemodel in XMI 1.1 of 2.x, of een Enterprise Architect-bestand (.eap, .eapx, .qea, .qeax, ook in een zip), om naar een begrippenkader volgens NL-SBB. Status `concept`.
  - Eén ingang, `scripts/bk.py`, voor alle vaste stappen. `bk.py status` noemt na elke stap de volgende, zodat ook kleinere modellen de werkwijze volledig doorlopen.
  - Elk beslispunt krijgt een voorstel van het script. `overnemen` en `zet` leggen keuzes vast in `project.yaml`, en `controleer` toetst dat bestand op sleutels, namen en regexen.
  - SHACL-validatie tegen het NL-SBB-profiel 1.0.0 plus extensie, met de telling per ernstniveau.
  - Inhoudelijke review in delen van 25 begrippen, met signalen van het script en een compleetheidscontrole. Oordelen blijven staan als het kader opnieuw wordt gemaakt.
  - Rapport met cijfers die het script schrijft; de assistent vult alleen de conclusie in.
  - MIM-ondersteuning: alias als voorkeursterm, notities met koppen, MIM-stereotypen, keuze-datatypen.
  - Getest op IMGeo, IMGeluid, IMEV, IMKL, IMRO en NEN 3610, en met drie modelgroottes; zie `testrapporten/`.
