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
import ipaddress
import json
import os
import re
import shutil
import socket
import sys
import unicodedata
import urllib.parse
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


EXTENSIES = (".xml", ".csv", ".tsv")


def veilige_naam(lijst):
    """Bestandsnaam voor de cache: alleen letters, cijfers, '_' en '-'. Een lijstnaam komt uit het model
    (invoer van derden) en mag geen pad worden (../, /etc/...)."""
    return re.sub(r"[^A-Za-z0-9_-]+", "_", zonder_diakrieten(lijst)).strip("_-") or "lijst"


def binnen(pad, map_):
    pad, map_ = os.path.realpath(pad), os.path.realpath(map_)
    return pad == map_ or pad.startswith(map_ + os.sep)


def controleer_sjabloon(sjabloon):
    """Geeft de extensie of stopt met een melding. Geen fragment (#), alleen http(s), XML/CSV/TSV."""
    if "#" in sjabloon:
        sys.exit("waarden.extern.bron mag geen '#' bevatten")
    pad = urllib.parse.urlsplit(sjabloon).path if "://" in sjabloon else sjabloon
    ext = os.path.splitext(pad.replace("{lijst}", "x"))[1].lower()
    if ext not in EXTENSIES:
        sys.exit(f"waarden.extern.bron moet eindigen op {', '.join(EXTENSIES)} (nu: '{ext or 'geen extensie'}')")
    if "://" in sjabloon and urllib.parse.urlsplit(sjabloon).scheme not in ("http", "https"):
        sys.exit("waarden.extern.bron: alleen http(s) of een lokaal pad")
    return ext


def interne_host(url):
    """True als de host een intern adres is (loopback, privé, link-local zoals 169.254.169.254). Een naam die
    niet lokaal op te lossen is (bv. achter een proxy), telt niet als intern."""
    host = (urllib.parse.urlsplit(url).hostname or "").lower()
    if not host or host == "localhost" or host.endswith((".local", ".localhost", ".internal")):
        return True
    try:
        adressen = {ipaddress.ip_address(host)}
    except ValueError:
        try:
            adressen = {ipaddress.ip_address(i[4][0].split("%")[0]) for i in socket.getaddrinfo(host, None)}
        except (socket.gaierror, UnicodeError):
            return False
    return any(a.is_private or a.is_loopback or a.is_link_local or a.is_reserved or a.is_multicast
               or a.is_unspecified for a in adressen)


def haal_lijst(sjabloon, lijst, doelmap, ext, projectmap):
    """Haal het bestand voor één lijst op (URL of lokaal pad binnen de projectmap). Probeert ook de naam zonder
    diakrieten (Coördinaattransformatie -> Coordinaattransformatie). Geeft (pad, gebruikte naam, melding)."""
    namen = [lijst] + ([zonder_diakrieten(lijst)] if zonder_diakrieten(lijst) != lijst else [])
    doel = os.path.join(doelmap, veilige_naam(lijst) + ext)
    if not binnen(doel, doelmap):
        return None, None, "ongeldige lijstnaam"
    for naam in namen:
        if sjabloon.startswith(("http://", "https://")):
            bron = sjabloon.format(lijst=urllib.parse.quote(naam, safe=""))  # naam kan geen pad of query worden
            if interne_host(bron):
                return None, None, f"intern adres geweigerd: {bron}"
            spoor = doel + ".bron"
            if os.path.exists(doel) and os.path.getsize(doel) > 0 and os.path.exists(spoor) \
                    and open(spoor, encoding="utf-8").read() == bron:
                return doel, naam, None  # eerder opgehaald van dezelfde URL
            code, deny = curl_status(bron, doel, accept="*/*", volgen=False)
            if code == "200" and os.path.exists(doel) and os.path.getsize(doel) > 0:
                with open(spoor, "w", encoding="utf-8") as f:
                    f.write(bron)
                return doel, naam, None
            if os.path.exists(doel):
                os.remove(doel)
            if deny:
                return None, None, f"geblokkeerd door de omgeving: {bron}"
            if code.startswith("3"):
                return None, None, f"doorverwijzing (HTTP {code}) niet gevolgd: zet de eindbestemming als bron"
        else:
            if re.search(r"[\\/]|\.\.", naam):
                return None, None, "lijstnaam met pad-tekens"
            bron = sjabloon.format(lijst=naam)
            if not binnen(bron, projectmap):
                return None, None, f"lokaal pad buiten de projectmap geweigerd: {bron}"
            if os.path.isfile(bron):
                shutil.copyfile(bron, doel)
                return doel, naam, None
    return None, None, None


def main(inv_pad, project, doelmap):
    cfg = laad_keuzes(project)
    ex = (cfg["waarden"].get("extern") or {})
    sjabloon = ex.get("bron")
    if not sjabloon or "{lijst}" not in sjabloon:
        sys.exit("waarden.extern.bron ontbreekt of bevat geen {lijst}")
    ext = controleer_sjabloon(sjabloon)
    projectmap = os.path.dirname(os.path.abspath(project))
    if not sjabloon.startswith(("http://", "https://")) and not os.path.isabs(sjabloon):
        sjabloon = os.path.join(projectmap, sjabloon)
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
        pad, naam, melding = haal_lijst(sjabloon, c["name"], doelmap, ext, projectmap)
        if not pad:
            ontbreekt.append(c["name"] + (f" ({melding})" if melding else ""))
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
        c.setdefault("tags", {})["waarden_bron"] = sjabloon.format(lijst=naam)  # alleen ter informatie
        gevuld.append(c["name"])
        totaal += len(attrs)

    kolommen = next((c["kolommen"] for c in cod.values() if c.get("kolommen")), [])
    inv["waarden_extern"] = {"bron": ex.get("bron"), "lijsten": len(gevuld), "waarden": totaal,
                             "ontbreekt": ontbreekt, "kolommen": kolommen}
    json.dump(inv, open(inv_pad, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(gevuld)} waardelijsten gevuld met {totaal} waarden uit {ex.get('bron')}")
    if ontbreekt:
        print(f"LET OP: {len(ontbreekt)} waardelijsten zonder extern bestand (krijgen geen waarden; hun kolommen "
              "worden geen begrippen): "
              + ", ".join(ontbreekt[:20]) + (" ..." if len(ontbreekt) > 20 else ""))
    if zonder_def:
        print(f"LET OP: {len(zonder_def)} waarden zonder definitie (veld '{veld_def}'): "
              + ", ".join(zonder_def[:20]) + (" ..." if len(zonder_def) > 20 else ""))


if __name__ == "__main__":
    main(*sys.argv[1:4])
