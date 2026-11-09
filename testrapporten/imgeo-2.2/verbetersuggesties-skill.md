# Verbetersuggesties voor de skill (uit de IMGeo 2.2-run, 2026-11-09)

Bevindingen tijdens het uitvoeren van de skill op IMGeo 2.2, met per punt een Voorstel.

1. **Ontbrekende SHACL-extensie in de geïnstalleerde skill.** `bk.py valideer` crashte met `FileNotFoundError: shacl/skos-ap-nl-extensie.ttl`; het bestand moest handmatig worden opgehaald uit `Geonovum/skills-nl-sbb`. Voorstel: bundel het bestand in de skill, of laat `valideer` het automatisch downloaden met fallback-URL.

2. **Netwerk-fallbacks voor `vergelijk`.** De REST-endpoint op `definities.geostandaarden.nl` gaf HTTP 403; de vergelijking lukte pas via een alternatieve bron (`upload.begrippenxl.nl/storage/imgeo/imgeo.ttl`). Voorstel: configureerbare fallback-bronnen per kader in `standaardkeuzes.yaml`.

3. **YAML-quoting bij `bk.py zet`.** Een waarde met dubbele punt (`kader.omschrijving '... IMGeo 2.2: ...'`) werd als YAML-mapping geïnterpreteerd. Voorstel: waarden automatisch quoten in `zet`.

4. **Leesrechten bij kopiëren van voorbeelden.** `cp voorbeelden/imgeo.yaml project.yaml` gaf een read-only bestand, waardoor `overnemen` faalde met `PermissionError`. Voorstel: een `init`-commande die het voorbeeld kopieert mét schrijfrechten.

5. **Versieverschillen in de voorbeelden.** `voorbeelden/imgeo.yaml` is voor IMGeo 2.1; bij 2.2 bleken 20 gepubliceerde waarden (o.a. `transitie`, `historie`) niet in het XMI te zitten. Voorstel: versienotitie per voorbeeld, of een automatische delta-check tegen het gepubliceerde kader in het rapport.

6. **Review-automatisering.** Van 393 begrippen waren 384 `ok`; de 9 `definitie`-bevindingen worden nu alleen weggeschreven. Voorstel: automatisch een issue-lijst voor de UML-beheerder genereren, en desgewenst een `--auto-ok`-modus voor delen zonder term-signalen.

7. **`vergelijk` uitbreiden naar meerdere kaders.** Nu één gepublished kader per run; een vergelijkingstabel over meerdere modellen (IMGeo, IMKL, IMRO, IMEV) in één rapport zou direct vergelijken over modellen mogelijk maken.
