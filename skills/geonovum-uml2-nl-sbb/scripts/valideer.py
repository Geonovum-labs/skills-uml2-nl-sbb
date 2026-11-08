"""Stap 4 — SHACL-validatie tegen NL-SBB (profiel + skill-extensie). Deterministisch.

Gebruik: python valideer.py uit/kader.ttl project.yaml reports/ [context.ttl ...]

Run A: alleen het kader. Run B (als er context is): kader + externe kaders, alleen
focusnodes binnen kader.uri geteld. Instellingen volgens de NL-SBB-skill: advanced=True,
inference=rdfs, geen allow-warnings; oordeel op telling per ernstniveau, niet op `conforms`.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyshacl  # noqa: E402
import rdflib  # noqa: E402
from rdflib.namespace import SKOS  # noqa: E402

from kern import SKILL_DIR, haal, laad_keuzes  # noqa: E402

SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")


def profiel(cfg, reports):
    pad = os.path.join(reports, "skos-ap-nl.ttl")
    if not os.path.exists(pad):
        for url in (cfg["validatie"]["profiel"], cfg["validatie"]["profiel_fallback"]):
            if haal(url, pad, accept="text/turtle,*/*"):
                print(f"profiel: {url}")
                break
        else:
            sys.exit("Geen SHACL-profiel beschikbaar")
    g = rdflib.Graph().parse(pad)
    versie = next(iter(g.objects(None, rdflib.OWL.versionInfo)), "?")
    g.parse(os.path.join(SKILL_DIR, "shacl", "skos-ap-nl-extensie.ttl"))
    return g, versie


def run(naam, data, shapes, alleen, reports, label_graph):
    conf, rg, txt = pyshacl.validate(data, shacl_graph=shapes, advanced=True, inference="rdfs")
    open(os.path.join(reports, f"shacl-{naam}.txt"), "w").write(txt)
    rows, tel = collections.defaultdict(list), collections.Counter()
    for r in rg.subjects(rdflib.RDF.type, SH.ValidationResult):
        foc = rg.value(r, SH.focusNode)
        if alleen and not str(foc).startswith(alleen):
            continue
        sev = str(rg.value(r, SH.resultSeverity)).split("#")[1]
        tel[sev] += 1
        shape = str(rg.value(r, SH.sourceShape)).split("#")[-1].split("/")[-1]
        # focus-URI's uit de melding halen, zodat gelijke bevindingen samen geteld worden
        msg = re.sub(r"<[^>]+>", "<…>", str(rg.value(r, SH.resultMessage)))[:110]
        rows[(sev, shape, msg)].append(str(label_graph.value(foc, SKOS.prefLabel) or foc))
    out = [f"=== {naam} ===", f"conforms-veld: {conf} (niet leidend) | telling: "
           f"Violation {tel['Violation']}, Warning {tel['Warning']}, Info {tel['Info']}"]
    volg = {"Violation": 0, "Warning": 1, "Info": 2}
    for (sev, sh, msg), l in sorted(rows.items(), key=lambda kv: (volg.get(kv[0][0], 3), -len(kv[1]), kv[0])):
        out.append(f"[{sev}] {sh} x{len(l)}: {msg}\n     bv. {sorted(set(l))[:8]}")
    s = "\n".join(out)
    print(s)
    return s


def main(kader, project, reports, *ctx):
    cfg = laad_keuzes(project)
    os.makedirs(reports, exist_ok=True)
    shapes, versie = profiel(cfg, reports)
    print(f"NL-SBB-profiel owl:versionInfo {versie}; pySHACL {pyshacl.__version__}; advanced=True, inference=rdfs\n")
    data = rdflib.Graph().parse(kader)
    delen = [run("A-kaal", data, shapes, None, reports, data)]
    if ctx:
        d2 = rdflib.Graph().parse(kader)
        for f in ctx:
            d2.parse(f)
        delen.append(run("B-context", d2, shapes, cfg["kader"]["uri"], reports, d2))
    open(os.path.join(reports, "shacl-samenvatting.txt"), "w").write(
        f"profiel {versie}, pySHACL {pyshacl.__version__}, advanced=True, inference=rdfs\n\n" + "\n\n".join(delen) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:])
