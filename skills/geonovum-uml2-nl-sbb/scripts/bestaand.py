"""URI's van een al gepubliceerd begrippenkader overnemen. Deterministisch; genereer.py roept dit aan.

Per gepubliceerd begrip wordt een begrip in het nieuwe kader gezocht, in deze volgorde:
1. gelijke URI;
2. gelijke term (prefLabel, rdfs:label, altLabel, hiddenLabel of code, ook zonder kwalificatie tussen
   haakjes) en gelijke definitie;
3. gelijke term, als die term in beide kaders bij precies één begrip hoort (de definitie is dan veranderd).
Een begrip in het nieuwe kader krijgt hoogstens één gepubliceerde URI. Collecties worden gekoppeld op
URI of op naam (prefLabel, rdfs:label of code), het kader zelf als beide er één hebben.
"""
import collections
import html
import re

from rdflib import RDF, RDFS, Graph, Literal, URIRef
from rdflib.namespace import SKOS


def norm(s):
    return re.sub(r"[\W_]+", "", html.unescape(str(s)).lower())


def termen(g, c):
    uit = []
    for p in (SKOS.prefLabel, RDFS.label, SKOS.altLabel, SKOS.hiddenLabel, SKOS.notation):
        for lab in g.objects(c, p):
            lab = str(lab)
            uit.append(lab)
            m = re.fullmatch(r"\s*(.+?)\s*\((.+)\)\s*", lab)
            if m:  # '1 (Bovenbouwcode)', 'onverhard (wegdeel)'
                uit += [m.group(1), f"{m.group(2)} {m.group(1)}", f"{m.group(1)} {m.group(2)}"]
    return [norm(t) for t in uit if norm(t)]


def waarde_identiteit(pub: Graph):
    """{(waardelijst, waarde) genormaliseerd: gepubliceerde URI} uit de collecties van het gepubliceerde kader.
    Zo blijft een waarde die per lijst een eigen gepubliceerd begrip heeft, ook in het nieuwe kader apart."""
    uit = {}
    for col in pub.subjects(RDF.type, SKOS.Collection):
        for lijst in set(termen(pub, col)):
            for m in pub.objects(col, SKOS.member):
                for t in termen(pub, m):
                    uit.setdefault((lijst, t), m)
    return uit


def koppel(ons: Graph, pub: Graph, vooraf=None):
    """-> (mapping {onze URI: gepubliceerde URI}, regels voor uri-koppeling.tsv, telling).
    vooraf: koppelingen die al vaststaan (waarden via hun waardelijst)."""
    mapping, regels, tel = {}, [], collections.Counter()
    oc = set(ons.subjects(RDF.type, SKOS.Concept))
    pc = sorted(set(pub.subjects(RDF.type, SKOS.Concept)))
    idx = collections.defaultdict(set)
    for c in oc:
        for t in termen(ons, c):
            idx[t].add(c)
    pidx = collections.defaultdict(set)
    for c in pc:
        for t in termen(pub, c):
            pidx[t].add(c)
    odef = {c: norm(ons.value(c, SKOS.definition) or "") for c in oc}
    bezet = {}
    for o, p in (vooraf or {}).items():
        bezet[o] = p
        if o != p:
            mapping[o] = p
        regels.append((str(p), str(o), "waarde in gekoppelde waardelijst"))
        tel["waarde in lijst"] += 1

    def leg(p, o, hoe):
        if o in bezet:
            regels.append((str(p), str(o), f"niet gekoppeld: ons begrip al gekoppeld aan {bezet[o]}"))
            tel["dubbel"] += 1
            return
        bezet[o] = p
        if o != p:
            mapping[o] = p
        regels.append((str(p), str(o), hoe))
        tel[hoe] += 1

    rest = []
    voor = set(bezet.values())
    for p in pc:  # 1. gelijke URI
        if p in voor:
            continue
        (leg(p, p, "URI") if p in oc else rest.append(p))
    nog = []
    for p in rest:  # 2. term + definitie
        pdef = norm(pub.value(p, SKOS.definition) or "")
        kand = {o for t in termen(pub, p) for o in idx.get(t, ()) if o not in bezet}
        zelfde = {o for o in kand if pdef and odef[o] == pdef}
        if len(zelfde) == 1:
            leg(p, zelfde.pop(), "term+definitie")
        elif len(zelfde) > 1:
            regels.append((str(p), "; ".join(sorted(map(str, zelfde))), "niet gekoppeld: meer begrippen met die term en definitie"))
            tel["meerduidig"] += 1
        else:
            nog.append(p)
    for p in nog:  # 3. unieke term
        pt = termen(pub, p)
        kand = {o for t in pt for o in idx.get(t, ()) if o not in bezet}
        uniek_pub = all(len(pidx[t]) == 1 for t in pt if t in idx)
        if len(kand) == 1 and uniek_pub:
            leg(p, kand.pop(), "term (andere definitie)")
        else:
            regels.append((str(p), "; ".join(sorted(map(str, kand))) if kand else "",
                           "niet gekoppeld: " + ("term meerduidig" if kand else "geen begrip met die term")))
            tel["geen"] += 1

    # collecties op URI of naam
    ocol = set(ons.subjects(RDF.type, SKOS.Collection))
    pcol = set(pub.subjects(RDF.type, SKOS.Collection))
    onaam = collections.defaultdict(set)
    for c in ocol:
        for t in termen(ons, c):
            onaam[t].add(c)
    for p in sorted(pcol):
        if p in ocol:
            tel["collectie URI"] += 1
            continue
        kand = {o for t in termen(pub, p) for o in onaam.get(t, ())} - set(mapping)
        if len(kand) == 1:
            o = kand.pop()
            mapping[o] = p
            regels.append((str(p), str(o), "collectie op naam"))
            tel["collectie naam"] += 1
    # het kader zelf
    os_, ps = list(ons.subjects(RDF.type, SKOS.ConceptScheme)), list(pub.subjects(RDF.type, SKOS.ConceptScheme))
    if len(os_) == 1 and len(ps) == 1 and os_[0] != ps[0]:
        mapping[os_[0]] = ps[0]
        regels.append((str(ps[0]), str(os_[0]), "begrippenkader"))
    return mapping, regels, tel


def herschrijf(g: Graph, mapping: dict) -> Graph:
    """Een kopie van g met de URI's uit mapping vervangen (onderwerp, object; niet in literals)."""
    if not mapping:
        return g
    nieuw = Graph(namespace_manager=g.namespace_manager)
    def m(x):
        if isinstance(x, URIRef):
            return mapping.get(x, x)
        if isinstance(x, Literal) and x.datatype in mapping:  # code getypeerd met een (gekoppelde) collectie
            return Literal(str(x), datatype=mapping[x.datatype])
        return x
    for s, p, o in g:
        nieuw.add((m(s), p, m(o)))
    return nieuw
