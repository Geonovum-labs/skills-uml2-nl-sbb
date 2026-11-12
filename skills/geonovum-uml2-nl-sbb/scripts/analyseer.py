"""Stap 2 — inventaris.json + keuzes -> beslispunten.md/.json. Deterministisch.

Gebruik: python analyseer.py werk/inventaris.json [project.yaml] werk/

Somt op wat de standaardkeuzes automatisch afhandelen (INFO) en waar een beslissing van de
gebruiker nodig is (VRAAG). Voorstellen (VOORSTEL) zijn heuristisch en moeten bevestigd worden.
Pas na dit script legt de LLM de VRAAG-punten voor aan de gebruiker.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kern import Termen, _merge, bron_tag, clean_def, def_key, herkomst, indeling, laad_inventaris, laad_keuzes  # noqa: E402


MIM = {"objecttype", "gegevensgroeptype", "codelijst", "enumeratie", "referentielijst", "gestructureerd datatype",
       "primitief datatype", "keuze", "attribuutsoort"}


GETAL = re.compile(r"\d+(?:[.,]\d+)?")


def split_voorstel(anders):
    """Per conflict: kleinste onderlinge gelijkenis van de definities. Hoog -> zelfde begrip, anders splitsen."""
    from difflib import SequenceMatcher
    zelfde, rest = [], []
    for lab, lst in anders:
        defs = sorted({clean_def(d).lower() for _, d in lst})
        minimum = min((SequenceMatcher(None, a, b).ratio() for i, a in enumerate(defs) for b in defs[i + 1:]), default=1)
        # andere getallen = ander begrip, hoe gelijk de zin ook is (grof: 20-63 mm vs 630-2000 µm)
        getallen = {tuple(sorted(GETAL.findall(d))) for d in defs}
        (zelfde if minimum >= 0.8 and len(getallen) == 1 else rest).append(lab)
    v = {"waarden": {}}
    if zelfde:
        v["waarden"]["zelfde_begrip"] = zelfde
    if rest:
        v["waarden"]["automatisch_splitsen"] = "{waarde} ({lijst})"  # NL-SBB: onderscheidende term tussen haakjes
    return v


NAAMVELD = re.compile(r"^(waarde|code|naam|value|term)$", re.I)
DEFVELD = re.compile(r"^(omschrijving|definitie|description|definition|toelichting)$", re.I)


def kolomlijsten(cod):
    """Waardelijsten die kolommen bevatten in plaats van waarden: minstens 3 lijsten (en de helft) met
    precies dezelfde attribuutnamen, waaronder een naam- of definitieveld. Geeft (lijsten, kolommen)."""
    sets = Counter(frozenset(a["name"] for a in c["attrs"]) for c in cod.values() if c["attrs"])
    if not sets:
        return [], []
    kol, n = sets.most_common(1)[0]
    met = [c for c in cod.values() if c["attrs"]]
    if n < 3 or n * 2 < len(met) or not any(NAAMVELD.match(k) or DEFVELD.match(k) for k in kol):
        return [], []
    lijsten = sorted(c["name"] for c in met if frozenset(a["name"] for a in c["attrs"]) == kol)
    volgorde = next(c for c in met if c["name"] == lijsten[0])["attrs"]
    return lijsten, [a["name"] for a in volgorde]


def extern_voorstel(cod, lijsten, kolommen):
    """Voorstel voor waarden.extern: bron uit een URL-tag die de lijstnaam bevat (bv. Locatie), velden uit de kolommen."""
    bron = None
    for c in cod.values():
        if c["name"] not in lijsten:
            continue
        for v in (c.get("tags") or {}).values():
            v = (v or "").strip()
            if v.startswith(("http://", "https://")) and c["name"] in v:
                bron = v.replace(c["name"], "{lijst}")
                break
        if bron:
            break
    naam = next((k for k in kolommen if NAAMVELD.match(k)), kolommen[0])
    defi = next((k for k in kolommen if DEFVELD.match(k)), None)
    # De bron-URL komt uit het model (invoer van derden): nooit stil overnemen (bk.py overnemen --alle).
    # Hij staat in de details; de gebruiker bevestigt hem en zet hem met bk.py zet waarden.extern.bron.
    ex = {"bron": None, "naam": naam, "definitie": defi,
          # veldnamen in de bestanden hebben meestal geen leestekens (IMBRO/A -> IMBROA)
          "tags": [re.sub(r"[^0-9A-Za-z_]", "", k) for k in kolommen if k not in (naam, defi)]}
    if len(lijsten) < len(cod):
        ex["lijsten"] = lijsten
    return {"waarden": {"extern": ex}}, bron


def engels_score(s):
    """Grove taalscore van een naam: positief = eerder Engels, negatief = eerder Nederlands."""
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s).lower()
    nl = len(re.findall(r"ij|oe|aa|uu|ui|eu|sch|cht|heid|tie\b|isch|ige?\b|eer|oor|elijk|ng\b|en\b|eel", s))
    en = len(re.findall(r"th|tion|ea|w|y|ph|sh|qu|ck|ity\b|ed\b|al\b|ous|ing\b", s))
    return en - nl


def alias_engels(paren):
    """True als de aliassen in minstens twee derde van de paren (naam, alias) Engelser zijn dan de UML-naam."""
    paren = [(n, a) for n, a in paren if a and a.lower().replace(" ", "") != n.lower().replace(" ", "")]
    return bool(paren) and sum(engels_score(a) > engels_score(n) for n, a in paren) * 3 >= len(paren) * 2


GENERIEK = {"model", "informatiemodel", "conceptueel model", "conceptueelmodel", "logisch model", "uml", "classes",
            "package", "packages", "domein", "datamodel", "data model", "objecten", "objecttypen"}


def kader_voorstel(inv, obj):
    """Kader-URI en titel uit de modelnaam: een algemene packagenaam (Model) vervangen door de bovenliggende
    package; een afkorting tussen haakjes (BHR-GT) wordt de URI-naam."""
    paden = Counter(tuple(c.get("pkg_path") or []) for c in obj.values() if c.get("pkg_path"))
    pad = list(paden.most_common(1)[0][0]) if paden else []
    kand = [p for p in (inv.get("packages") or [])[:1]] + list(reversed(pad))
    naam = next((k.split("/")[-1] for k in kand if k and k.split("/")[-1].strip().lower() not in GENERIEK), None)
    naam = naam or os.path.splitext(os.path.basename(inv.get("bron", "model")))[0]
    m = re.search(r"\(([A-Za-z][\w-]*)\)", naam)
    slug = m.group(1).lower() if m else re.sub(r"[^0-9a-z]+", "", naam.lower())
    return {"uri": "http://definities.geostandaarden.nl/" + slug,
            "titel": f"Begrippenkader {naam}" if m or " " in naam else naam + "-begrippenkader",
            "omschrijving": f"Begrippen uit het informatiemodel {naam}, omgezet volgens NL-SBB."}


def bron_voorstel(onb):
    """Eén mappingregel per genormaliseerde tagwaarde; meest voorkomende schrijfwijze als titel."""
    groep = defaultdict(Counter)
    for t, n in onb.items():
        groep[t.strip().upper().replace(" ", "")][t.strip()] += n
    uit = []
    for pat, schrijf in sorted(groep.items(), key=lambda kv: -sum(kv[1].values())):
        t = schrijf.most_common(1)[0][0]
        titel = re.sub(r"\s+", " ", t).strip(" ;,.")
        uit.append({"patroon": re.escape(pat) + "$",
                    "sleutel": re.sub(r"[^0-9A-Za-z]+", "-", titel).strip("-")[:40] or "bron", "titel": titel})
    return uit


def main(inv_pad, project, uitdir):
    cfg = laad_keuzes(project)
    inv = laad_inventaris(inv_pad, cfg)
    T = Termen(cfg)
    obj, dat, cod, over = indeling(inv, cfg)
    klassen = {**obj, **dat}
    ext = inv.get("externe_klassen") or {}
    rel = cfg["relaties"]
    punten = []

    besloten = set(cfg.get("besloten") or [])

    def punt(soort, code, titel, details=None, voorstel=None):
        if soort == "VRAAG" and code in besloten:
            soort = "BESLOTEN"  # de gebruiker heeft dit punt bewust zo gelaten (project.yaml: besloten)
        punten.append(dict(soort=soort, code=code, titel=titel, details=details or [], voorstel=voorstel))

    # waardelijsten met kolommen i.p.v. waarden (extern beheerd): niet als waarden behandelen (punt G)
    ex = cfg["waarden"].get("extern") or {}
    gedaan = inv.get("waarden_extern")
    kl, kol = kolomlijsten(cod) if not gedaan else ([], [])

    # A. overzicht
    st = Counter((c["type"], c["stereo"]) for c in inv["elementen"].values())
    punt("INFO", "overzicht", f"{len(obj)} objecttypen, {len(dat)} datatypen, {len(cod)} waardelijsten, "
         f"{len(over)} overgeslagen; {sum(len(c['attrs']) for c in klassen.values())} attributen, "
         f"{sum(len(c['attrs']) for c in cod.values() if c['name'] not in kl)} waarden"
         + (f" (plus {len(kl)} lijsten met alleen kolommen, zie waarden-extern)" if kl else ""),
         [f"{t} «{s}»: {n}" for (t, s), n in sorted(st.items(), key=str)])

    # B. stereotypen die niet in de lijsten staan -> objecttype
    bekend = {s.lower() for s in cfg["stereotypen"]["waardelijst"] + cfg["stereotypen"]["datatype"]
              + (cfg["stereotypen"].get("overslaan") or [])}
    onbekend = Counter(c["stereo"] for c in obj.values() if c["stereo"] and c["stereo"].lower() not in bekend)
    if onbekend:
        punt("INFO", "stereotypen", "Stereotypen die als objecttype worden behandeld (controleer)",
             [f"«{s}»: {n}" for s, n in onbekend.items()])

    # C. hiërarchie
    by_name = {c["name"]: k for k, c in klassen.items()}
    zonder = []
    for k, c in klassen.items():
        if k in dat:
            continue
        intern = [g for g in c["gens"] if g in klassen and g != k]
        if intern:
            continue
        extn = [ext.get(g, g) for g in c["gens"] if g not in klassen]
        opnaam = [n for n in extn if n in by_name and by_name[n] != k]
        if opnaam and rel.get("externe_superklasse_op_naam", True):
            continue
        zonder.append((c["name"], extn))
    if zonder:
        cand = Counter(n for _, e in zonder for n in e)
        root_guess = next((c["name"] for c in klassen.values() if c["name"].lstrip("_") in
                           {n.lstrip("_") for n in cand}), None)
        soort = "INFO" if rel.get("wortel") else "VRAAG"
        punt(soort, "wortel",
             f"{len(zonder)} klassen zonder superklasse in het model"
             + (f" (komen onder wortel '{rel['wortel']}')" if rel.get("wortel") else
                ": allemaal topbegrip, of één wortelbegrip kiezen (relaties.wortel) en uitzonderingen (relaties.zelfstandig)?"),
             [f"{n}" + (f" (externe superklasse: {', '.join(e)})" if e else "") for n, e in zonder],
             voorstel={"relaties": {"wortel": root_guess}} if root_guess and not rel.get("wortel") else
             ({"relaties": {"wortel": None}} if not rel.get("wortel") else None))

    # D. ontbrekende definities
    leeg = [f"klasse {c['name']}" for c in klassen.values() if not clean_def(c["doc"])]
    leeg += [f"attribuut {c['name']}.{a['name']}" for c in klassen.values() for a in c["attrs"] if not clean_def(a["doc"])]
    leeg += [f"waarde {c['name']}.{a['name']}" for c in cod.values() for a in c["attrs"] if not clean_def(a["doc"])]
    if leeg:
        punt("INFO", "definities", f"{len(leeg)} elementen zonder definitie (komen zonder skos:definition in het kader -> SHACL-fout)", leeg)

    # E. attributen met dezelfde naam
    an = defaultdict(lambda: defaultdict(list))
    for c in klassen.values():
        for a in c["attrs"]:
            an[a["name"]][def_key(a["doc"])].append(c["name"])
    same = {n: d for n, d in an.items() if len(d) == 1 and len(next(iter(d.values()))) > 1}
    diff = {n: d for n, d in an.items() if len(d) > 1}
    if same:
        punt("INFO", "attributen-samen", f"{len(same)} attribuutnamen met gelijke definitie in meerdere klassen -> één begrip",
             [f"{n}: {', '.join(next(iter(d.values())))}" for n, d in same.items()])
    if diff:
        punt("INFO", "attributen-context", f"{len(diff)} attribuutnamen met verschillende definities -> termen krijgen objecttype-context",
             [f"{n}: {len(d)} definities" for n, d in diff.items()])
    pref = Counter(m.group(0) for c in klassen.values() for a in c["attrs"] if (m := re.match(r"^[a-z]+-", a["name"])))
    pref = {p: n for p, n in pref.items() if n > 1}
    if pref and not cfg["termen"].get("naam_prefixen_verwijderen"):
        punt("VRAAG", "prefixen", "Attribuutnamen met een prefix: verwijderen uit de term (termen.naam_prefixen_verwijderen) "
             "en eventueel als voorvoegsel behouden (attributen.prefix_term)?", [f"'{p}': {n}x" for p, n in pref.items()],
             voorstel={"termen": {"naam_prefixen_verwijderen": sorted(pref)}})

    # F. waarden in meerdere waardelijsten
    split = {k.lower() for k in (cfg["waarden"].get("splitsingen") or {})}
    hern = {k.lower(): v for k, v in (cfg["waarden"].get("hernoem") or {}).items()}
    vg = defaultdict(list)
    for c in cod.values():
        if c["name"] in kl:
            continue
        for a in c["attrs"]:
            nm = a["name"].strip()
            if f"{nm.lower()}|{c['name'].lower()}" in split:
                continue
            vg[hern.get(nm.lower()) or (a.get("term") or None) or T.waarde(nm)].append((c["name"], a["doc"]))
    zelfde = {z.lower() for z in cfg["waarden"].get("zelfde_begrip") or []}
    auto = cfg["waarden"].get("automatisch_splitsen")
    gelijk, lees, anders = [], [], []
    for lab, lst in sorted(vg.items()):
        if len(lst) < 2:
            continue
        keys = {def_key(d) for _, d in lst}
        variants = {clean_def(d) for _, d in lst}
        if len(keys) > 1 and lab.lower() in zelfde:
            lees.append(f"{lab}: {len(keys)} definitievarianten, samengevoegd via waarden.zelfde_begrip")
        elif len(keys) > 1:
            anders.append((lab, lst))
        elif len(variants) > 1:
            lees.append(f"{lab}: {', '.join(c for c, _ in lst)}")
        else:
            gelijk.append(f"{lab}: {len(lst)} lijsten ({', '.join(c for c, _ in lst)})")
    if gelijk:
        punt("INFO", "waarden-samen", f"{len(gelijk)} waarden met gelijke naam en definitie in meerdere lijsten -> één begrip "
             "(standaardkeuze), lid van meerdere collecties", gelijk)
    if lees:
        punt("INFO", "waarden-leestekens", f"{len(lees)} waarden waarvan de definities alleen in leestekens verschillen -> samengevoegd", lees)
    if anders and auto:
        punt("INFO", "waarden-splitsen", f"{len(anders)} waarden met gelijke naam en andere definitie worden automatisch "
             f"gesplitst volgens '{auto}' (waarden.automatisch_splitsen)", [lab for lab, _ in anders])
    elif anders:
        det = []
        for lab, lst in anders:
            det.append(f"'{lab}':")
            det += [f"    {c}: \"{clean_def(d)[:160]}\"" for c, d in lst]
        punt("VRAAG", "waarden-splitsen", f"{len(anders)} waarden met gelijke naam en inhoudelijk andere definitie: "
             "splitsen in aparte begrippen (waarden.splitsingen, sleutel 'waarde|Waardelijst') — genereer.py stopt anders. "
             "Voorstel: bijna gelijke definities (gelijkenis >= 0,8) als één begrip (waarden.zelfde_begrip), "
             "de rest automatisch splitsen met de term van de lijst ervoor", det,
             voorstel=split_voorstel(anders))

    # G. gebruik van waardelijsten
    gebruikt = {a.get("type") for c in klassen.values() for a in c["attrs"]}
    cfg_g = rel.get("gebruik") or {}
    leeg = [c["name"] for c in cod.values() if not c["attrs"]]
    if gedaan:
        punt("INFO", "waarden-extern", f"{gedaan['lijsten']} waardelijsten gevuld met {gedaan['waarden']} waarden uit "
             f"{gedaan['bron']} (bk.py waarden)", [f"geen extern bestand: {n}" for n in gedaan.get("ontbreekt") or []])
    elif kl and ex.get("bron"):
        punt("INFO", "waarden-extern", f"{len(kl)} waardelijsten bevatten kolommen ({', '.join(kol)}); de waarden "
             f"komen uit {ex['bron']}: draai bk.py waarden")
    elif kl:
        voorstel, kandidaat = extern_voorstel(cod, kl, kol)
        punt("VRAAG", "waarden-extern", f"{len(kl)} waardelijsten bevatten geen waarden maar kolommen ({', '.join(kol)}): "
             "de waarden worden extern beheerd. Waar staan ze (waarden.extern.bron, URL of pad met {lijst})? "
             "Zolang er geen bron is, worden de kolommen geen begrippen. "
             + (f"Kandidaat uit de tag met de lijstlocatie: {kandidaat} . Deze URL komt uit het model: leg hem aan "
                "de gebruiker voor (controleer host en versiemap) en zet hem pas na bevestiging met "
                "bk.py zet waarden.extern.bron '<url>'. Zonder gebruiker: niet invullen."
                if kandidaat else "Geen locatie gevonden in de tags: vraag de gebruiker om de URL."),
             kl, voorstel=voorstel)
    if leeg:
        punt("INFO", "waardelijsten-leeg", f"{len(leeg)} waardelijsten zonder waarden in het model (extern beheerd?): "
             "geen collectie; attributen die ze gebruiken worden wel begrip", leeg)
    los = [c for c in cod.values() if c["attrs"] and c["name"] not in gebruikt and c["name"] not in cfg_g]
    auto = [c["name"] for c in cod.values() if c["name"] in gebruikt and c["name"] not in cfg_g]
    if auto:
        punt("INFO", "gebruik-auto", f"{len(auto)} waardelijsten automatisch gekoppeld via attribuuttype", auto)
    if los:
        det, voorstel = [], {}
        cod_namen = {c["name"] for c in cod.values()}
        pfx_woorden = {m.group(1) for c in klassen.values() for a in c["attrs"] if (m := re.match(r"^([a-z]+)-", a["name"]))}
        labels = {c["name"]: [c["name"].lstrip("_"), c["alias"] or ""] for c in klassen.values()}
        for c in los:
            low = c["name"].lower()
            best = max(((len(x), n) for n, xs in labels.items() for x in xs if x and x.lower() in low), default=None)
            attr = None
            if best:
                cw = set(T.humanize(c["name"]).split())
                for a in klassen[by_name[best[1]]]["attrs"]:
                    m = re.match(r"^([a-z]+)-", a["name"])
                    q = m.group(1) if m else None
                    # prefix (bv. plus-) moet passen bij de lijst: TypeBakPlus -> plus-type, TypeBak niet
                    has = {p for p in pfx_woorden if p in low}
                    pas = (q in has) or (not has and (q is None or (c["name"] + q.capitalize()) not in cod_namen))
                    aw = set(T.humanize(re.sub(r"^[a-z]+-", "", a["name"])).split())
                    if pas and aw and aw <= cw | {"type"}:
                        attr = a["name"]
                voorstel[c["name"]] = [best[1], attr]
            else:
                voorstel[c["name"]] = None
            det.append(f"{c['name']} -> " + (f"[{best[1]}, {attr}]" if best else "geen voorstel"))
        punt("VRAAG", "gebruik", f"{len(los)} waardelijsten die door geen attribuut (type) worden gebruikt: aan welk "
             "attribuut of objecttype koppelen (relaties.gebruik; null = niet relateren -> verweesde waarden)?",
             det, voorstel={"relaties": {"gebruik": voorstel}})

    # H. herkomst
    tagnaam = cfg["bronnen"]["tag"]
    tags = Counter()
    for c in list(klassen.values()) + list(cod.values()):
        tags[bron_tag(c, cfg)] += 1
        for a in c["attrs"]:
            tags[bron_tag(a, cfg)] += 1
    url = {t for t in tags if t and re.fullmatch(r"https?://\S+", t.strip())}
    if url:
        punt("INFO", "bronnen-uri", f"{len(url)} herkomstwaarden zijn een URL: brondocument met foaf:page", sorted(url))
    onb = {t: n for t, n in tags.items() if t is not None and t not in url and herkomst(t, cfg) == "ONBEKEND"}
    bek = {t: herkomst(t, cfg) for t in tags if t is not None and herkomst(t, cfg) not in (None, "ONBEKEND")}
    if bek:
        punt("INFO", "bronnen", f"{len(set(bek.values()))} brondocumenten herkend uit tag '{tagnaam}'",
             [f"'{t}' -> {v[0]}" for t, v in sorted(bek.items())])
    if onb:
        punt("VRAAG", "bronnen-onbekend", f"{len(onb)} waarden van tag '{tagnaam}' zonder bronmapping (bronnen.mapping): "
             "welk brondocument (sleutel + titel)? Voorstel: één brondocument per tagwaarde (titel controleren)",
             [f"'{t}': {n}x" for t, n in sorted(onb.items(), key=lambda x: -x[1])],
             voorstel={"bronnen": {"mapping": bron_voorstel(onb)}})
    if not any(tags.keys() - {None}):
        alle = Counter(t for c in list(klassen.values()) + list(cod.values()) for a in [c] + c["attrs"] for t in a["tags"])
        punt("VRAAG", "bronnen-tag", f"Tag '{tagnaam}' komt niet voor; welke tagged value bevat de herkomst van definities?",
             [f"{t}: {n}x" for t, n in alle.most_common(25)],
             voorstel=next(({"bronnen": {"tag": [t]}} for t, _ in alle.most_common()
                            if re.search(r"herkomst|bron|source", t, re.I)), None))

    # I. aliassen
    al = Counter(c["stereo"] for c in klassen.values() if c["alias"] and c["alias"] != c["name"])
    engels = alias_engels([(c["name"], c["alias"]) for c in klassen.values() if c["alias"]])
    if al and engels and not cfg["termen"].get("alias_als_voorkeursterm"):
        punt("VRAAG", "alias", "Klassen met een alias, maar de aliassen lijken Engels en de UML-namen Nederlands: "
             "UML-naam als voorkeursterm houden (standaard; de alias komt dan niet in het kader)?",
             [f"«{s}»: {n}x, bv. " + ", ".join(f"{c['name']} = {c['alias']}" for c in klassen.values()
                                                if c["stereo"] == s and c["alias"])[:200] for s, n in al.items()],
             voorstel={"termen": {"alias_als_voorkeursterm": []}})
    elif al:
        punt("INFO" if cfg["termen"].get("alias_als_voorkeursterm") else "VRAAG", "alias",
             "Klassen met een alias: alias als voorkeursterm gebruiken (termen.alias_als_voorkeursterm), met "
             + ("de UML-naam als altLabel@" + cfg['termen']['alias_naam_als_altlabel'] if cfg['termen'].get('alias_naam_als_altlabel')
              else "de UML-naam alleen als notatie (geen altLabel)") + "?",
             [f"«{s}»: {n}x, bv. " + ", ".join(f"{c['name']} = {c['alias']}" for c in klassen.values()
                                                if c["stereo"] == s and c["alias"])[:200] for s, n in al.items()],
             voorstel=None if cfg["termen"].get("alias_als_voorkeursterm") else {"termen": {
                 "alias_als_voorkeursterm": ["*"],
                 # MIM-modellen hebben Nederlandse UML-namen: geen altLabel@en (UML-naam blijft notatie), zoals in voorbeelden/
                 "alias_naam_als_altlabel": None if any((c["stereo"] or "").lower() in MIM for c in klassen.values())
                 else cfg["termen"].get("alias_naam_als_altlabel")}})

    # I2. codes in namen: vastgeplakte getallen, normcodes, afkortingen in hoofdletters (BRO: RTKGPS0tot2cm)
    # Elke keuze wordt alleen voorgesteld als ze termen echt verandert; de details tonen het effect (naam -> term),
    # zodat een fout voorstel zichtbaar is voordat het wordt overgenomen.
    namen = [c["name"] for c in klassen.values()] + [a["name"] for c in klassen.values() for a in c["attrs"]]
    wnamen = [a["name"] for c in cod.values() for a in c["attrs"]]
    tc = cfg["termen"]

    def termen_met(extra):
        T2 = Termen(_merge(json.loads(json.dumps(cfg)), {"termen": extra}))
        return [T2.humanize(n) for n in namen] + [T2.waarde(n) for n in wnamen]
    nu = termen_met({})

    def effect(extra):
        return sorted({(n, t2) for n, t1, t2 in zip(namen + wnamen, nu, termen_met(extra)) if t1 != t2})
    # Afkortingen alleen met bewijs: de reeks hoofdletters staat ergens los (vóór een cijfer, leesteken of het einde),
    # zoals RTKGPS in RTKGPS0tot2cm of AHN in AHN3. Een reeks vóór een kleine letter is dubbelzinnig
    # (BAGObject = BAG + Object, PPgroot = PP + groot) en wordt zonder zo'n los voorkomen niet voorgesteld.
    los = {m.group(0) for n in namen + wnamen for m in re.finditer(r"(?<![A-Za-z])[A-Z]{2,}(?![A-Za-z])", n)}
    runs = Counter()
    for n in namen + wnamen:
        for m in re.finditer(r"(?<![A-Za-z])([A-Z]{2,})(?=[a-z]|\d)", n):
            r = m.group(1)
            kand = r if r in los else (r[:-1] if len(r) > 2 and r[:-1] in los else None)
            if kand:
                runs[kand] += 1
    gedekt = {k for k, _ in T.afkortingen} | set(T.behouden) | {"ISO", "NEN", "EN", "ASTM", "NPR"}
    afk = sorted(r for r in runs if r not in gedekt)
    voorstel, det = {}, []
    for sleutel, extra in (("getallen", {"getallen": True}), ("normcodes", {"normcodes": True}),
                           ("afkortingen", {"afkortingen": sorted(set(tc.get("afkortingen") or []) | set(afk))})):
        if (sleutel == "afkortingen" and not afk) or (sleutel != "afkortingen" and tc.get(sleutel)):
            continue
        eff = effect(extra)
        if eff:
            voorstel.update(extra)
            det += [f"{sleutel}: {n} -> {t}" for n, t in eff[:15]] + \
                ([f"{sleutel}: ... en nog {len(eff) - 15}"] if len(eff) > 15 else [])
    if voorstel:
        punt("VRAAG", "termen-codes", "Namen met codes: getallen aan woorden (termen.getallen), normcodes zoals "
             "iso17892d4v2016 (termen.normcodes) of afkortingen vóór een woord of getal (termen.afkortingen). "
             "De details tonen per keuze wat er met de termen gebeurt: controleer ze; een samenstelling schrijf je "
             "met '-' (RTK-GPS). Neem een keuze niet over als een voorbeeld fout uitpakt.",
             det, voorstel={"termen": voorstel})

    # J. parent-tag (staat standaard uit: modelspecifiek, en niet elke parent is een generieke relatie)
    pt = rel.get("waarde_parent_tag")
    np_ = sum(1 for c in cod.values() for a in c["attrs"] if (a["tags"].get(pt) or "").strip())
    if pt and np_:
        punt("INFO", "parent", f"{np_} waarden met tag '{pt}' -> skos:broader naar de bovenliggende waarde "
             "(relaties.waarde_parent_tag; controleer of elke parent echt een bovenliggend begrip is)")

    # J2. bestaand, al gepubliceerd kader: URI's gelijk houden
    if not cfg["uris"].get("bestaand"):
        punt("VRAAG", "bestaand-kader", "Is dit model al eerder als begrippenkader gepubliceerd? Geef dan de URL of het "
             "bestand (Turtle), zodat bestaande begrippen en collecties hun URI houden: bk.py bestaand <url|bestand>. "
             "Zo niet: bk.py overnemen bestaand-kader --standaard",
             ["Koppeling per gepubliceerd begrip: gelijke URI, anders gelijke term (ook altLabel of code) met gelijke "
              "definitie, anders gelijke term als die maar één keer voorkomt. Niet gekoppelde begrippen krijgen een nieuwe URI."])

    # K. kader
    if not cfg["kader"].get("uri"):
        punt("VRAAG", "kader", "Kader-URI, titel en omschrijving ontbreken (kader.uri / kader.titel / kader.omschrijving)",
             [f"modelnaam/package: {', '.join(sorted({c['pkg'] for c in obj.values() if c['pkg']}))}"],
             voorstel={"kader": kader_voorstel(inv, obj)})

    os.makedirs(uitdir, exist_ok=True)
    json.dump(punten, open(os.path.join(uitdir, "beslispunten.json"), "w"), ensure_ascii=False, indent=1)
    with open(os.path.join(uitdir, "beslispunten.md"), "w") as f:
        f.write(f"# Beslispunten — {os.path.basename(inv.get('bron', ''))}\n\n")
        for p in punten:
            f.write(f"## [{p['soort']}] {p['code']}: {p['titel']}\n\n")
            for d in p["details"]:
                f.write(f"- {d}\n" if not d.startswith("    ") else f"  - {d.strip()}\n")
            if p["voorstel"]:
                f.write(f"\nVoorstel (bevestigen):\n\n```yaml\n{json.dumps(p['voorstel'], ensure_ascii=False, indent=1)}\n```\n")
            f.write("\n")
    for p in punten:
        print(f"[{p['soort']}] {p['code']}: {p['titel']}")
    print(f"\n{sum(p['soort'] == 'VRAAG' for p in punten)} vragen; details in {os.path.join(uitdir, 'beslispunten.md')}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2:
        main(a[0], None, a[1])
    else:
        main(*a[:3])
