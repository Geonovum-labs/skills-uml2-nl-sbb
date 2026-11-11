"""Waarden van extern beheerde waardelijsten in de inventaris zetten. Deterministisch.

Gebruik: python waarden_extern.py werk/inventaris.json project.yaml werk/lijsten/

Sommige informatiemodellen (bv. de BRO-catalogi) hebben bij een waardelijst alleen de kolommen
(Waarde, Omschrijving, ...) en beheren de waarden zelf in losse bestanden. Met `waarden.extern.bron`
(URL of pad met {lijst}) haalt dit script per waardelijst dat bestand op en vervangt de attributen
van de lijst door de waarden: veld `naam` wordt de waardenaam, veld `definitie` de definitie,
de velden in `tags` gaan als tagged values mee. Ondersteund: XML (één element per waarde, met
velden als kindelementen), CSV en TSV (kopregel met veldnamen).

De inventaris krijgt `waarden_extern` met de bron en de aantallen; `bk.py status` ziet daaraan
of deze stap (na een nieuwe `bk.py start`) opnieuw moet.
"""
import csv
import io
import json
import os
import shutil
import sys
import unicodedata
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kern import curl_status, indeling, laad_keuzes  # noqa: E402


def zonder_diakrieten(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def lees_rijen(tekst, ext):
    """Bestandsinhoud -> lijst van {veld: waarde}. Formaat volgt uit de extensie (xml, csv, tsv)."""
    if ext == ".xml":
        root = ET.fromstring(tekst)
        rijen = []
        for rij in root:
            velden = {c.tag.split("}")[-1]: (c.text or "").strip() for c in rij}
            if velden:
                rijen.append(velden)
        return rijen
    scheiding = "\t" if ext == ".tsv" else ","
    return [{k.strip(): (v or "").strip() for k, v in r.items() if k}
            for r in csv.DictReader(io.StringIO(tekst), delimiter=scheiding)]


def haal_lijst(sjabloon, lijst, doelmap):
    """Haal het bestand voor één lijst op (URL of lokaal pad). Probeert ook de naam zonder diakrieten
    (Coördinaattransformatie -> Coordinaattransformatie). Geeft (pad, gebruikte naam) of (None, None)."""
    namen = [lijst] + ([zonder_diakrieten(lijst)] if zonder_diakrieten(lijst) != lijst else [])
    ext = os.path.splitext(sjabloon.split("?")[0])[1].lower() or ".xml"
    for naam in namen:
        bron = sjabloon.format(lijst=naam)
        doel = os.path.join(doelmap, zonder_diakrieten(lijst) + ext)
        if bron.startswith(("http://", "https://")):
            if os.path.exists(doel) and os.path.getsize(doel) > 0:
                return doel, naam  # al eerder opgehaald
            code, deny = curl_status(bron, doel, accept="*/*")
            if code == "200" and os.path.getsize(doel) > 0:
                return doel, naam
            if os.path.exists(doel):
                os.remove(doel)
            if deny:
                print(f"  GEBLOKKEERD door omgeving: {bron}")
                return None, None
        elif os.path.exists(bron):
            shutil.copyfile(bron, doel)
            return doel, naam
    return None, None


def main(inv_pad, project, doelmap):
    cfg = laad_keuzes(project)
    ex = (cfg["waarden"].get("extern") or {})
    sjabloon = ex.get("bron")
    if not sjabloon or "{lijst}" not in sjabloon:
        sys.exit("waarden.extern.bron ontbreekt of bevat geen {lijst}")
    if not sjabloon.startswith(("http://", "https://")) and not os.path.isabs(sjabloon):
        sjabloon = os.path.join(os.path.dirname(os.path.abspath(project)), sjabloon)
    veld_naam, veld_def = ex.get("naam") or "Waarde", ex.get("definitie") or "Omschrijving"
    extra = ex.get("tags") or []
    alleen = set(ex.get("lijsten") or [])
    os.makedirs(doelmap, exist_ok=True)

    inv = json.load(open(inv_pad, encoding="utf-8"))
    _, _, cod, _ = indeling(inv, cfg)
    gevuld, ontbreekt, zonder_def, totaal = [], [], [], 0
    for k, c in sorted(cod.items(), key=lambda kv: kv[1]["name"]):
        if alleen and c["name"] not in alleen:
            continue
        pad, naam = haal_lijst(sjabloon, c["name"], doelmap)
        if not pad:
            ontbreekt.append(c["name"])
            continue
        tekst = open(pad, encoding="utf-8-sig").read()
        try:
            rijen = lees_rijen(tekst, os.path.splitext(pad)[1].lower())
        except (ET.ParseError, csv.Error) as e:
            sys.exit(f"{c['name']}: bestand {pad} niet te lezen: {e}")
        attrs = []
        for i, r in enumerate(rijen):
            w = r.get(veld_naam, "").strip()
            if not w:
                continue
            d = r.get(veld_def, "").strip()
            if not d:
                zonder_def.append(f"{c['name']}.{w}")
            attrs.append({"id": f"{k}_extern_{i:04d}", "name": w, "doc": d, "type_id": None, "type": None,
                          "stereo": "externe waarde", "lower": None, "upper": None,
                          "tags": {t: r.get(t, "") for t in extra}})
        if not attrs:
            ontbreekt.append(f"{c['name']} (bestand zonder waarden in veld '{veld_naam}')")
            continue
        c["kolommen"] = [a["name"] for a in c["attrs"]]
        c["attrs"] = attrs
        c.setdefault("tags", {})["waarden_bron"] = sjabloon.format(lijst=naam)
        gevuld.append(c["name"])
        totaal += len(attrs)

    inv["waarden_extern"] = {"bron": ex.get("bron"), "lijsten": len(gevuld), "waarden": totaal,
                             "ontbreekt": ontbreekt}
    json.dump(inv, open(inv_pad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(gevuld)} waardelijsten gevuld met {totaal} waarden uit {ex.get('bron')}")
    if ontbreekt:
        print(f"LET OP: {len(ontbreekt)} waardelijsten zonder extern bestand (houden hun UML-inhoud): "
              + ", ".join(ontbreekt[:20]) + (" ..." if len(ontbreekt) > 20 else ""))
    if zonder_def:
        print(f"LET OP: {len(zonder_def)} waarden zonder definitie (veld '{veld_def}'): "
              + ", ".join(zonder_def[:20]) + (" ..." if len(zonder_def) > 20 else ""))


if __name__ == "__main__":
    main(*sys.argv[1:4])
