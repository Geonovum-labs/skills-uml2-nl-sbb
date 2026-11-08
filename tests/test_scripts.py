"""Offline tests van de scripts van de skill, zonder AI-assistent.

Draaien vanuit de root van de repository, met een Python waarin de pakketten uit
skills/geonovum-uml2-nl-sbb/requirements.txt staan:

    python3 -m unittest discover -s tests -v

De SHACL-validatie haalt het NL-SBB-profiel uit het register en draait alleen met
BK_NETWERK=1.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "geonovum-uml2-nl-sbb")
BK = os.path.join(SKILL, "scripts", "bk.py")
FIXTURE = os.path.join(ROOT, "tests", "fixtures", "fietsparkeren.xmi")
sys.path.insert(0, os.path.join(SKILL, "scripts"))


def bk(werkmap, *args, invoer=None, ok=True):
    r = subprocess.run([sys.executable, BK, *args], cwd=werkmap, input=invoer, capture_output=True, text=True)
    if ok and r.returncode != 0:
        raise AssertionError(f"bk.py {' '.join(args)} gaf exitcode {r.returncode}:\n{r.stdout}\n{r.stderr}")
    return r


def termen(werkmap):
    with open(os.path.join(werkmap, "uit", "termen.tsv"), encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


class Keten(unittest.TestCase):
    """De hele keten van bk.py op het fictieve model Fietsparkeren."""

    @classmethod
    def setUpClass(cls):
        cls.w = tempfile.mkdtemp(prefix="bk-test-")
        bk(cls.w, "start", FIXTURE, "--package", "Fietsparkeren")
        bk(cls.w, "analyseer")
        bk(cls.w, "overnemen", "--alle")
        bk(cls.w, "analyseer")
        bk(cls.w, "genereer")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.w, ignore_errors=True)

    def test_inventaris_alleen_gekozen_package(self):
        inv = json.load(open(os.path.join(self.w, "werk", "inventaris.json")))
        namen = {c["name"] for c in inv["elementen"].values()}
        self.assertEqual(len(namen), 7)
        self.assertNotIn("GeoObject", namen)
        self.assertIn("GeoObject", inv["externe_klassen"].values())

    def test_geen_open_vragen_na_overnemen(self):
        punten = json.load(open(os.path.join(self.w, "werk", "beslispunten.json")))
        self.assertEqual([p["code"] for p in punten if p["soort"] == "VRAAG"], [])

    def test_aantallen_en_termen(self):
        t = {r["voorkeursterm"]: r for r in termen(self.w)}
        self.assertEqual(len(t), 21)
        # zelfde attribuutnaam, andere definitie -> objecttype-context
        self.assertIn("naam stalling", t)
        self.assertIn("naam fietsenrek", t)
        # zelfde waarde, andere definitie -> automatisch gesplitst
        self.assertIn("type rek overig", t)
        self.assertIn("type stalling overig", t)
        # zelfde waarde, alleen leestekens anders -> één begrip
        self.assertIn("onbekend", t)
        self.assertEqual(t["capaciteit fietsen"]["notatie"], "Stalling.capaciteitFietsen")

    def test_kader_is_geldige_turtle_met_collecties(self):
        import rdflib
        from rdflib.namespace import RDF, SKOS
        g = rdflib.Graph().parse(os.path.join(self.w, "uit", "kader.ttl"))
        self.assertEqual(len(set(g.subjects(RDF.type, SKOS.Concept))), 21)
        self.assertEqual(len(set(g.subjects(RDF.type, SKOS.Collection))), 3)
        self.assertEqual(len(set(g.subjects(RDF.type, SKOS.ConceptScheme))), 1)

    def test_ontbrekende_definitie_in_log(self):
        log = open(os.path.join(self.w, "uit", "beslissingen.md"), encoding="utf-8").read()
        self.assertIn("Geen definitie in het model: 'kluis code'", log)

    def test_review_in_delen_met_compleetheidscontrole(self):
        bk(self.w, "review", "--opnieuw")
        idx = json.load(open(os.path.join(self.w, "review", "index.json")))
        self.assertEqual(idx["aantal"], 21)
        # onvolledig: review klaar weigert
        self.assertNotEqual(bk(self.w, "review", "klaar", ok=False).returncode, 0)
        # alles ok, behalve begrippen met een signaal: die krijgen een opmerking
        delen = [os.path.join(self.w, "review", d["bestand"]) for d in idx["delen"]]
        regels = []
        for pad in delen:
            for blok in open(pad, encoding="utf-8").read().split("\n### ")[1:]:
                nr = blok.split(" |")[0]
                sig = re.search(r"^signalen: (.*)$", blok, re.M).group(1)
                regels.append(f"{nr} ok" + ("" if sig == "-" else " | signaal gezien, voor de test niet terecht"))
        bk(self.w, "oordeel", invoer="\n".join(regels))
        bk(self.w, "review", "klaar")
        self.assertTrue(os.path.exists(os.path.join(self.w, "reports", "review.md")))
        # een termcorrectie: oordelen van ongewijzigde begrippen blijven staan
        bk(self.w, "zet", "attributen.term_correcties[Fietskluis.kluisCode]", "kluiscode")
        bk(self.w, "genereer")
        uit = bk(self.w, "review", "--opnieuw").stdout
        self.assertIn("20 oordelen overgenomen", uit)

    def test_rapport_bevat_cijfers(self):
        bk(self.w, "rapport")
        r = open(os.path.join(self.w, "reports", "rapport.md"), encoding="utf-8").read()
        self.assertIn("begrippen: attribuut", r)
        self.assertIn("<!-- LLM:", r)


class ProjectControle(unittest.TestCase):
    def setUp(self):
        self.w = tempfile.mkdtemp(prefix="bk-test-")
        bk(self.w, "start", FIXTURE, "--package", "Fietsparkeren")

    def tearDown(self):
        shutil.rmtree(self.w, ignore_errors=True)

    def test_tikfout_in_sleutel(self):
        bk(self.w, "zet", "kader.uri", "http://example.org/fiets")
        uit = bk(self.w, "zet", "termen.camelcase_splitse", "false", ok=False).stdout
        self.assertIn("bedoel je 'camelcase_splitsen'", uit)
        self.assertNotEqual(bk(self.w, "controleer", ok=False).returncode, 0)

    def test_onbekende_klasse_in_gebruik(self):
        bk(self.w, "zet", "kader.uri", "http://example.org/fiets")
        bk(self.w, "zet", "relaties.gebruik.StatusStalling", "[Bestaatniet, null]", ok=False)
        uit = bk(self.w, "controleer", ok=False).stdout
        self.assertIn("klasse 'Bestaatniet' bestaat niet", uit)


class Termen(unittest.TestCase):
    def setUp(self):
        import kern
        self.T = kern.Termen(kern.laad_keuzes())
        self.Tc = kern.Termen(kern._merge(kern.laad_keuzes(), {"termen": {"cijfers_scheiden": True}}))

    def test_camelcase_en_afkortingen(self):
        self.assertEqual(self.T.humanize("aantalVerkeersgegevensWeg"), "aantal verkeersgegevens weg")
        self.assertEqual(self.T.humanize("BGTObject"), "BGT object")
        self.assertEqual(self.T.waarde("F4"), "F4")
        self.assertEqual(self.T.waarde("GT5"), "GT5")

    def test_cijfers_scheiden(self):
        self.assertEqual(self.Tc.humanize("golflengte12_5"), "golflengte 12,5")

    def test_local_name_houdt_cijfergroepen_apart(self):
        import kern
        self.assertNotEqual(kern.local_name("golflengte 12,5"), kern.local_name("golflengte 125"))

    def test_contextterm_bij_keuze(self):
        import genereer
        self.assertEqual(genereer.context_term("afstand", "afstand of geometrie van de overige contour"),
                         "afstand van de overige contour")
        self.assertEqual(genereer.context_term("stof", "stof of stofcategorie"), "stof bij keuze stof of stofcategorie")
        self.assertEqual(genereer.context_term("naam", "stalling"), "naam stalling")


class Package(unittest.TestCase):
    def test_voorstel_uit_bestandsnaam(self):
        sys.argv = ["bk.py", "help"]
        import bk as bkmod
        boom = ["Kies ...", "Geostandaarden", "  3610-MIM-Datatypen", "  NEN3610", "    Waardelijsten", "  IMGolf"]
        self.assertEqual(bkmod.package_voorstel(boom, "NEN3610-2022-template-20221116.xmi"), "NEN3610")


@unittest.skipUnless(os.environ.get("BK_NETWERK") == "1", "SHACL-validatie haalt het profiel uit het register (BK_NETWERK=1)")
class Validatie(unittest.TestCase):
    def test_shacl_telling(self):
        w = tempfile.mkdtemp(prefix="bk-test-")
        try:
            for stap in (["start", FIXTURE, "--package", "Fietsparkeren"], ["analyseer"], ["overnemen", "--alle"],
                         ["analyseer"], ["genereer"], ["valideer"]):
                bk(w, *stap)
            s = open(os.path.join(w, "reports", "shacl-samenvatting.txt")).read()
            tel = re.findall(r"Violation (\d+), Warning (\d+), Info (\d+)", s)[-1]
            # alleen 'kluis code' heeft geen definitie
            self.assertEqual(tel[0], "1")
        finally:
            shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
