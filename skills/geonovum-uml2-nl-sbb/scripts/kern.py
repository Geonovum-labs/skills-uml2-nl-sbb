"""Gedeelde functies: keuzes laden, tekst opschonen, termen maken, model indelen."""
import html
import json
import os
import re

import yaml

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDAARD = os.path.join(SKILL_DIR, "standaardkeuzes.yaml")


def _merge(base, over):
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _merge(base[k], v)
        else:
            base[k] = v
    return base


def laad_keuzes(project=None):
    """Standaardkeuzes, overschreven door het projectbestand (diepe merge; lijsten worden vervangen)."""
    cfg = yaml.safe_load(open(STANDAARD, encoding="utf-8"))
    if project:
        _merge(cfg, yaml.safe_load(open(project, encoding="utf-8")) or {})
    return cfg


def laad_inventaris(pad, cfg=None):
    """Inventaris laden. Met cfg: definities uit secties halen (`definities`), toelichting en
    term uit tags; resultaat in el['doc'], el['toelichting'], el['term'] (zie standaardkeuzes)."""
    inv = json.load(open(pad, encoding="utf-8"))
    if cfg is not None:
        for c in inv["elementen"].values():
            for el in [c] + c["attrs"]:
                verrijk(el, cfg)
    return inv


SECTIEKOP = re.compile(r"^[ \t]*--+[ \t]*([^\n-][^\n]*?)[ \t]*--+[ \t]*$", re.M)


def secties(doc):
    """Notitie met koppen als '--Definitie--' -> {kop (kleine letters): tekst}. Zonder koppen: {}."""
    delen = SECTIEKOP.split(doc or "")
    if len(delen) < 3:
        return {}
    uit = {}
    if delen[0].strip():
        uit["_voor"] = delen[0].strip()
    for kop, tekst in zip(delen[1::2], delen[2::2]):
        k = kop.strip().lower()
        uit[k] = (uit[k] + "\n" + tekst.strip()) if k in uit else tekst.strip()
    return uit


def eerste_tag(tags, namen):
    """Waarde van de eerste niet-lege tag uit namen (string of lijst); <memo> telt als leeg."""
    for n in [namen] if isinstance(namen, str) else (namen or []):
        v = (tags.get(n) or "").strip()
        if v and v != "<memo>":
            return v
    return None


def verrijk(el, cfg):
    dc = cfg.get("definities") or {}
    sx = secties(el.get("doc"))
    el["secties_genegeerd"], el["bron_sectie"] = [], None
    if sx:
        defs = [sx[k] for k in dc.get("sectie_definitie") or [] if sx.get(k)]
        toel = [sx[k] for k in dc.get("sectie_toelichting") or [] if sx.get(k)]
        bekend = set(dc.get("sectie_definitie") or []) | set(dc.get("sectie_toelichting") or []) \
            | set(dc.get("sectie_negeren") or []) | set(dc.get("sectie_bron") or [])
        el["bron_sectie"] = next((re.sub(r"\s+", " ", sx[k]).strip() for k in dc.get("sectie_bron") or []
                                  if (sx.get(k) or "").strip()), None)
        el["secties_genegeerd"] = sorted(k for k in sx if k not in bekend and k != "_voor")
        el["doc"] = "\n".join(defs) if defs else (sx.get("_voor") or "")
    else:
        toel = []
    t = eerste_tag(el.get("tags") or {}, dc.get("toelichting_tag"))
    if t and any(re.fullmatch(p, clean_def(t)) for p in dc.get("toelichting_negeer") or []):
        t = None
    if t:
        toel.append(t)
    el["toelichting"] = "\n".join(dict.fromkeys(toel))
    el["term"] = eerste_tag(el.get("tags") or {}, (cfg.get("termen") or {}).get("term_tag"))


def bron_tag(el, cfg):
    """Herkomst: eerste niet-lege tag uit bronnen.tag, anders de bronsectie uit de notitie."""
    return eerste_tag(el.get("tags") or {}, cfg["bronnen"]["tag"]) or el.get("bron_sectie")


# ---------- tekst ----------

def clean_def(s):
    s = s or ""
    for _ in range(2):  # EA-export bevat soms dubbel geëscapete entiteiten (&amp;ndash;)
        s = html.unescape(s)
    s = s.replace("\xa0", " ")
    # Windows-1252-tekens die als C1-stuurteken zijn opgeslagen (bv. \x91 \x92 voor quotes)
    s = re.sub(r"[\x80-\x9f]", lambda m: bytes([ord(m.group())]).decode("cp1252", "ignore"), s)
    s = re.sub(r"<[^>]+>", " ", s) if re.search(r"</?(b|i|u|p|br|font|ul|ol|li|span|div|em|strong|a)\b", s, re.I) else s
    return re.sub(r"\s+", " ", s).strip()


def def_key(s):
    return re.sub(r"[\W_]+", "", clean_def(s).lower())


# afkortingen en codes blijven staan: BGT, OV-baan, maar ook F4, GT5, B3 (hoofdletter + cijfers)
ACRONIEM = re.compile(r"^([A-Z]{2,}|[A-Z]+\d+[A-Z]*)(-|$)")


class Termen:
    """UML-namen -> voorkeurstermen volgens de keuzes in `termen`."""

    def __init__(self, cfg):
        t = cfg["termen"]
        self.vast = {k.lower(): v for k, v in (t.get("vast") or {}).items()}
        self.prefixen = t.get("naam_prefixen_verwijderen") or []
        self.samenstellingen = t.get("samenstellingen") or {}
        self.camel = t.get("camelcase_splitsen", True)
        self.klein = t.get("kleine_letters", True)
        self.afk = t.get("afkortingen_behouden", True)
        self.cijfers = t.get("cijfers_scheiden", False)
        self.decimaal = t.get("decimaalteken", ",")
        # woorden die precies zo blijven staan (geen camelCase-splitsing, geen kleine letters), bv. IMGeo
        self.behouden = sorted(t.get("woorden_behouden") or [], key=len, reverse=True)
        # afkortingen die in codes aan een woord vastzitten (RTKGPS0tot2cm, PPgroot); "RTK-GPS" herkent ook RTKGPS
        self.afkortingen = sorted(((a.replace("-", ""), a) for a in t.get("afkortingen") or []),
                                  key=lambda x: len(x[0]), reverse=True)
        self.afk_klein = {k.lower(): a for k, a in self.afkortingen}
        self.getallen = t.get("getallen", False)
        self.normcodes = t.get("normcodes", False)

    def _woord(self, w):
        if w.lower() in self.afk_klein:
            return self.afk_klein[w.lower()]
        if self.afk and (ACRONIEM.match(w) or re.fullmatch(r"[A-Z]", w)):
            return w  # ook één hoofdletter blijft staan: klasseA -> klasse A
        if any(w == b or w.startswith(b + "-") for b in self.behouden):
            return w
        return w.lower() if self.klein else w

    def _bescherm(self, s, extra=()):
        """Vervangt woorden_behouden en afkortingen door merktekens, zodat de camelCase-regels ze niet splitsen.
        Een afkorting telt alleen als ze niet midden in een langere reeks hoofdletters staat."""
        bewaard = []
        paren = [(b, b) for b in self.behouden] + [
            (k, a) for k, a in self.afkortingen if re.search(rf"(?<![A-Z]){re.escape(k)}(?![A-Z])", s)] + list(extra)
        for zoek, uit in sorted(paren, key=lambda p: len(p[0]), reverse=True):
            if zoek in s:
                tok = f"{len(bewaard)}"
                bewaard.append((tok, uit))
                s = s.replace(zoek, tok)
        if bewaard:
            s = re.sub(r"(?<=[A-Za-z0-9])", " ", s)
            s = re.sub(r"(?=[A-Za-z]|\d+[A-Za-z])", " ", s)  # AHN3 blijft, GPS200tot... niet
            s = s.replace("", " ")  # twee normcodes of afkortingen achter elkaar
        return s, bewaard

    # organisatie + nummer [+ d deel] [+ v jaar]; een hoofdletter-organisatie mag aan een woord vastzitten (fijnNEN5104)
    NORM = re.compile(r"(?:(?<![A-Za-z])(ISO|iso|NEN|nen|EN|en|ASTM|astm|NPR|npr)|(?<=[a-z])(ISO|NEN|ASTM|NPR))"
                      r"_?([A-Za-z]?\d+)(?:d(\d+))?(?:v(\d{4}))?")

    def _normcodes(self, s):
        """iso17892d4v2016 -> ISO 17892-4:2016, ASTM_D4767v2011 -> ASTM D4767:2011 (d = deel, v = versie).
        Geeft de tekst met plaatshouders en de paren (plaatshouder, normcode) om te beschermen."""
        paren = []

        def f(m):
            org = (m.group(1) or m.group(2)).upper()
            if m.group(3)[0].isalpha() and org != "ASTM":
                return m.group(0)  # alleen ASTM heeft een letter voor het nummer (D4767); 'end9' is geen norm
            code = f"{org} {m.group(3).upper()}" + (f"-{m.group(4)}" if m.group(4) else "") \
                + (f":{m.group(5)}" if m.group(5) else "")
            ph = f"\ue002{len(paren)}\ue003"
            paren.append((ph, code))
            return ph
        return self.NORM.sub(f, s), paren

    def _getallen(self, s):
        """Getallen los van woorden: veel25tot50 -> veel 25 tot 50, 16tot31.5mm -> 16 tot 31,5 mm, um -> µm.
        Afkortingen met cijfers (WGS84, AHN3, QM1), normcodes (17892-4:2016) en versies (v6.0) blijven staan."""
        uit = []
        for w in s.split(" "):
            if not w or ACRONIEM.match(w) or re.fullmatch(r"[A-Z]+\d+[A-Za-z]?", w) or re.search(r"\d[-:]\d", w) \
                    or re.fullmatch(r"[vV]\d+(\.\d+)*", w) or "" in w:
                uit.append(w)
                continue
            w = re.sub(r"(?<=\d)\.(?=\d)", self.decimaal, w)
            w = re.sub(r"(?<=\d)([a-zµ]{1,2})tot(?=\d)", r"\1 tot ", w)  # 1400umtot2mm
            w = re.sub(r"(?<=\d)(tot|en|of)(?=\d)", r" \1 ", w)
            w = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", w)
            w = re.sub(r"(?<=\d)(?=[A-Za-zµ°])", " ", w)
            uit.append(w)
        s = " ".join(uit)
        s = re.sub(r"\bum\b", "µm", s)
        s = re.sub(r"\bk ?pa\b", "kPa", s, flags=re.I)
        return s

    def strip_prefix(self, name):
        for p in self.prefixen:
            if name.startswith(p):
                return name[len(p):]
        return name

    def humanize(self, name, prefix=True):
        """camelCase/PascalCase -> woorden; afkortingen in hoofdletters blijven."""
        if name.strip().lower() in self.vast:
            return self.vast[name.strip().lower()]
        s = name.strip().lstrip("_")
        s = self.strip_prefix(s) if prefix else s
        extra = []
        if self.normcodes:
            s, extra = self._normcodes(s)
        s, bewaard = self._bescherm(s, extra)
        if self.getallen:
            s = re.sub(r"_(?=[A-Za-z])", " ", s)  # klasseA_v2006 -> klasse A v2006
        if self.camel:
            s = re.sub(r"IJ(?=[a-z])", "\x01", s)  # IJ is één letter: obstakelIJzervloer -> obstakel ijzervloer
            s = re.sub(r"([a-z0-9])([A-Z\x01])", r"\1 \2", s)
            s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
            s = s.replace("\x01", "IJ")
        if self.cijfers:  # golflengte12_5 -> golflengte 12,5
            s = re.sub(r"(\d)_(\d)", r"\1" + self.decimaal + r"\2", s)
            s = re.sub(r"([A-Za-z])(\d)", r"\1 \2", s)
        s = re.sub(r"\s+", " ", " ".join(self._woord(w) for w in s.split())).strip()
        if self.getallen:
            s = re.sub(r"\s+", " ", self._getallen(s)).strip()
        for tok, b in bewaard:
            s = s.replace(tok, b)
        s = re.sub(r"\s+", " ", s).strip()
        for k, v in self.samenstellingen.items():
            s = s.replace(k, v)
        return s

    def waarde(self, name):
        """Waardenamen: camelCase splitsen, anders alleen kleine letters (afkortingen behouden)."""
        nm = name.strip()
        if nm.lower() in self.vast:
            return self.vast[nm.lower()]
        if re.search(r"[a-z][A-Z]", nm):
            return self.humanize(nm)
        if self.getallen or self.normcodes or any(k in nm for k, _ in self.afkortingen):
            return self.humanize(nm, prefix=False)  # codes met getallen, normcodes of afkortingen
        return " ".join(self._woord(w) for w in nm.split())


def local_name(label):
    # cijfergroepen gescheiden door een leesteken blijven gescheiden (12,5 -> 12_5, niet 125)
    label = re.sub(r"(\d)[^0-9A-Za-zÀ-ÿ\s]+(?=\d)", r"\1_", label)
    parts = re.split(r"[^0-9A-Za-zÀ-ÿ_]+", label)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


# ---------- model indelen ----------

def indeling(inv, cfg):
    """Splits de inventaris in objecttypen, datatypen, waardelijsten en overgeslagen elementen."""
    st = cfg["stereotypen"]
    sc = cfg["scope"]
    wl = {s.lower() for s in st["waardelijst"]}
    dt = {s.lower() for s in st["datatype"]}
    skip = {s.lower() for s in st.get("overslaan") or []}
    obj, dat, cod, over = {}, {}, {}, {}
    for k, c in inv["elementen"].items():
        s = (c["stereo"] or "").lower()
        if (s in skip or c["name"] in (sc.get("klassen_overslaan") or [])
                or c["pkg"] in (sc.get("packages_overslaan") or [])):
            over[k] = c
        elif c["type"] == "uml:Enumeration" or s in wl:
            (cod if sc.get("waardelijsten", True) else over)[k] = c
        elif c["type"] == "uml:DataType" or s in dt:
            (dat if sc.get("datatypen", True) else over)[k] = c
        elif c.get("abstract") and not sc.get("abstracte_klassen", True):
            over[k] = c
        else:
            obj[k] = c
    return obj, dat, cod, over


def herkomst(tag, cfg):
    """Tagwaarde -> (sleutel, titel) volgens bronnen.mapping, of None. 'ONBEKEND' als niets past."""
    b = cfg["bronnen"]
    tag = (tag or "").strip()
    if any(re.fullmatch(p, tag) for p in b.get("negeer") or []):
        return None
    t = tag.upper().replace(" ", "")
    for m in b.get("mapping") or []:
        mm = re.match(m["patroon"], t)
        if mm:
            gd = {k: (v or "") for k, v in mm.groupdict().items()}
            sleutel = m["sleutel"].format(**gd).strip("- ")
            titel = re.sub(r"\s+", " ", m["titel"].format(**gd)).strip()
            return sleutel, titel
    return "ONBEKEND"


def uri(cfg, soort, naam):
    return cfg["uris"][soort].format(kader=cfg["kader"]["uri"].rstrip("/"), naam=naam)


# ---------- downloaden (curl: systeemcertificaten, redirects) ----------

def curl_status(url, pad="/dev/null", accept="*/*", tries=6, timeout=90):
    """Haalt url op met curl -L. Geeft (status, deny) terug; status '429' wordt met backoff herhaald.
    deny = True bij een blokkade door de uitvoeromgeving (x-deny-reason / allowlist)."""
    import subprocess
    import tempfile
    import time
    for n in range(tries):
        with tempfile.NamedTemporaryFile() as hdr:
            r = subprocess.run(["curl", "-sL", "-m", str(timeout), "-H", f"Accept: {accept}",
                                "-A", "geonovum-uml2-nl-sbb", "-D", hdr.name, "-o", pad, "-w", "%{http_code}", url],
                               capture_output=True, text=True)
            headers = open(hdr.name, errors="ignore").read().lower()
        code = r.stdout.strip() or "000"
        if "x-deny-reason" in headers or "not in allowlist" in headers:
            return code, True
        if code == "429":
            time.sleep(4 * (n + 1))
            continue
        if code == "000" and n < 2:
            time.sleep(2)
            continue
        return code, False
    return code, False


def haal(url, pad, accept="text/turtle"):
    """Download naar pad (gecachet). True als gelukt (HTTP 200 en niet leeg)."""
    if os.path.exists(pad) and os.path.getsize(pad) > 0:
        return True
    code, deny = curl_status(url, pad, accept)
    ok = code == "200" and os.path.exists(pad) and os.path.getsize(pad) > 0
    if not ok:
        print(f"  {'GEBLOKKEERD door omgeving' if deny else 'HTTP ' + code}: {url}")
        if os.path.exists(pad):
            os.remove(pad)
    return ok
